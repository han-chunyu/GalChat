import os
import re
import json
import asyncio
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from docx import Document
from tqdm import tqdm
from openai import AsyncOpenAI, APIConnectionError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging

# ======================
# 日志
# ======================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================
# 配置类
# ======================
@dataclass
class Config:
    # API配置
    api_key: str = "sk-"  # 替换为你的API密钥
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: str = "qwen-max-latest"

    # 路径配置
    input_dir: Path = Path("atri_raw_data")
    output_dir: Path = Path("processed_data")
    error_dir: Path = Path("failed_chunks")

    # 网络参数
    request_timeout: int = 60
    max_retries: int = 8
    concurrency_limit: int = 5

    # 处理参数
    chunk_size: int = 600
    temperature: float = 0.3


# ======================
# 系统Prompt
# ======================
ROLE_PLAY_PROMPT = """
你是一位专业的视觉小说剧本处理专家，请根据《ATRI-my dear moments》的剧本特点，严格按照以下规则转换对话：

# 角色定义
1. 用户(user)：仅限主角「夏生」的对话
2. 助手(assistant)：仅限机器人少女「ATRI」的对话
3. 系统(system)：
   - 其他角色的对话（格式：【角色名】内容）
   - 环境描述（时间、地点、天气等）
   - 动作描写（非对话内容）
4. 用户心理(user_thought)：夏生的内心活动（无角色标注且包含心理动词）

# 转换规则
1. 行类型判断：
   - 有角色标注 → 对话（按角色分类）
   - 无角色标注 → 心理活动或环境描述

2. 复合内容处理：
   - 对话+动作 → 分离为content和action字段
   示例：ATRI（微笑）：这样吗？ → 
   {"role":"assistant","content":"这样吗？","action":"微笑"}

3. 性格标签：
   - 从固定列表选择1-2个标签
   - 必须使用双引号包裹
   - 示例："traits": ["傲娇", "关心"]

4. 心理活动识别：
   - 包含第一人称代词（我、我们）或心理动词（想、觉得）
   - 示例：该不会出问题吧？ → user_thought

5. 特殊标记：
   - 环境音效 → 【音效】海浪声
   - 时间地点 → 【场景】黄昏的海边

# 输出要求
- 使用严格JSON数组格式
- 保留原始文本的所有细节
- 为assistant对话添加性格特征标签：
  "traits": ["傲娇", "关心"] （从预定义列表选择）

请严格按照以下JSON格式输出：
{
  "dialogues": [
    {"role": "assistant", "content": "对话内容", "action": "动作描述", "traits": ["性格标签"]},
    {"role": "user", "content": "对话内容"},
    {"role": "system", "content": "系统描述"}
  ]
}
1. 禁止出现数字类型值(指性格标签)
2. 保留原始文本的所有细节

请转换以下内容：
${chat_piece}

预定义性格标签：[温柔, 傲娇, 关心, 疑惑, 开心, 低落, 惊讶, 严肃]
"""


# ======================
# 重试
# ======================
retry_condition = retry_if_exception_type((APIConnectionError, asyncio.TimeoutError))
retry_decorator = retry(
    stop=stop_after_attempt(Config.max_retries),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_condition,
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)


# ======================
# 核心
# ======================
class RobustDialogueProcessor:
    def __init__(self, config: Config):
        self.cfg = config
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.request_timeout,
        )
        self._prepare_directories()

    def _prepare_directories(self):
        """创建必要目录"""
        self.cfg.output_dir.mkdir(exist_ok=True)
        self.cfg.error_dir.mkdir(exist_ok=True)

    async def process_document(self, doc_path: Path):
        """处理文档"""
        try:
            doc = Document(doc_path)
            full_text = self._extract_text(doc)
            chunks = self._chunk_text(full_text)

            output_dir = self.cfg.output_dir / doc_path.stem
            output_dir.mkdir(exist_ok=True)

            semaphore = asyncio.Semaphore(self.cfg.concurrency_limit)
            pbar = tqdm(total=len(chunks), desc=f"处理 {doc_path.name}")

            tasks = [
                self._process_chunk(
                    chunk=chunk,
                    chunk_id=idx,
                    output_dir=output_dir,
                    semaphore=semaphore,
                    pbar=pbar,
                )
                for idx, chunk in enumerate(chunks)
            ]

            await asyncio.gather(*tasks)
            pbar.close()

        except Exception as e:
            logger.error(f"文档处理失败 {doc_path.name}: {str(e)}")
            raise

    def _extract_text(self, doc: Document) -> str:
        """提取并清理文本"""
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

    def _chunk_text(self, text: str) -> List[str]:
        """文本分块"""
        paragraphs = text.split("\n")
        chunks = []
        current_chunk = []
        current_length = 0

        for para in paragraphs:
            para_length = len(para)
            if current_length + para_length > self.cfg.chunk_size:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(para)
            current_length += para_length

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    @retry_decorator
    async def _process_chunk(
        self,
        chunk: str,
        chunk_id: int,
        output_dir: Path,
        semaphore: asyncio.Semaphore,
        pbar: tqdm,
    ):
        """处理单个文本块"""
        async with semaphore:
            try:
                result = await self._api_call(chunk)
                if result:
                    self._save_result(result, output_dir / f"chunk_{chunk_id:04d}.json")
            except Exception as e:
                self._save_error(chunk, chunk_id, e)
            finally:
                pbar.update(1)

    async def _api_call(self, chunk: str) -> Optional[Dict]:
        """API调用"""
        messages = [
            {
                "role": "system",
                "content": "你是一个严格遵循JSON格式输出的剧本数据处理系统",
            },
            {
                "role": "user",
                "content": ROLE_PLAY_PROMPT.replace("${chat_piece}", chunk),
            },
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.cfg.model_name,
                messages=messages,
                temperature=self.cfg.temperature,
                response_format={"type": "json_object"},
            )
            return self._validate_response(response)
        except Exception as e:
            logger.error(f"API请求异常: {str(e)}")
            return None

    def _validate_response(self, response) -> Dict:
        """响应验证"""
        try:
            data = json.loads(response.choices[0].message.content)
            assert isinstance(data.get("dialogues", []), list)
            return data
        except Exception as e:
            logger.error(f"响应验证失败: {str(e)}")
            raise

    def _save_result(self, data: Dict, path: Path):
        """保存成功结果"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_error(self, chunk: str, chunk_id: int, error: Exception):
        """保存失败块"""
        error_file = self.cfg.error_dir / f"error_{chunk_id}.txt"
        with open(error_file, "w", encoding="utf-8") as f:
            f.write(f"Error: {str(error)}\n\nOriginal Text:\n{chunk}")


# ======================
# 测试
# ======================
class ConnectionAwareTester(RobustDialogueProcessor):
    async def test_connection(self):
        """连接测试"""
        test_prompt = "测试连接"
        try:
            await self.client.chat.completions.create(
                model=self.cfg.model_name,
                messages=[{"role": "user", "content": test_prompt}],
                max_tokens=1,
            )
            logger.info("API连接测试成功")
            return True
        except Exception as e:
            logger.error(f"连接测试失败: {str(e)}")
            return False

    async def test_from_file(self, file_path: str):
        """从文件读取测试内容"""
        with open(file_path, "r", encoding="utf-8") as f:
            test_text = f.read()

        print(f"\n测试内容：\n{test_text}")
        result = await self._safe_api_call(test_text)

        if result:
            print("\n转换结果：")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("转换失败")


# ======================
# 主程序
# ======================
async def main():
    config = Config()
    processor = ConnectionAwareTester(config)

    # 运行连接测试
    if not await processor.test_connection():
        return

    # # 处理文档
    # for doc_file in config.input_dir.glob("*.docx"):
    #     await processor.process_document(doc_file)

    # 测试
    await processor.test_from_file("test_input.txt")


if __name__ == "__main__":
    asyncio.run(main())
