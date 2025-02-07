# GalChat 贡献指南

欢迎来到 GalChat 社区！我们由衷感谢您对项目的关注与支持。在提交贡献前，请仔细阅读以下指南。

## 贡献流程

### 1. 准备工作

- 在 GitHub 上 Fork 本仓库
- 克隆你的 Fork 到本地：
  ```bash
  git clone https://github.com/anka-afk/GalChat.git
  cd GalChat
  ```

````

- 创建特性分支：
  ```bash
  git checkout -b feat/your-feature-name  # 功能开发
  git checkout -b fix/issue-number       # 问题修复
  ```

### 2. 开发环境配置

```bash
# 创建 Python 虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

## 代码贡献规范

### 问题报告

- 使用 [Issue 模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 包含以下信息：
  - 环境配置（Python/PyTorch/CUDA 版本）
  - 复现步骤（附带最小可复现代码）
  - 预期行为与实际行为
  - 相关日志/截图

### Pull Request

- 遵循 [PR 模板](.github/PULL_REQUEST_TEMPLATE.md)
- 必须包含：
  - 清晰的修改动机
  - 测试覆盖率证明
  - 相关文档更新
  - 代码性能基准测试（如适用）

### 代码风格

- Python 代码遵循 PEP8 规范
- 使用类型注解（Type Hints）
- 文档字符串遵循 Google 风格：

  ```python
  def preprocess_data(input_path: str) -> dict:
      """数据预处理函数

      Args:
          input_path (str): 原始数据路径

      Returns:
          dict: 处理后的数据集字典
      """
  ```

## 技术规范

### 数据预处理

- 新数据集必须放置在 `data_prep/raw_data/` 目录
- 预处理脚本输出到 `data_prep/processed_data/`
- 确保数据脱敏处理

### 模型训练

- 新增模型配置需存放在 `configs/models/`
- 训练日志保存至 `runs/experiment-name/`
- 必须包含验证集指标报告

### 测试要求

- 单元测试覆盖率 ≥ 80%
- 新增代码必须附带测试用例
- 运行测试套件：
  ```bash
  pytest tests/ --cov=galchat --cov-report=term-missing
  ```

## 文档标准

- 接口文档使用 [Sphinx](https://www.sphinx-doc.org/) 生成
- 更新文档后执行：
  ```bash
  cd docs && make clean && make html
  ```
- Markdown 文件遵循 [Google 文档风格](https://github.com/google/styleguide)

## 行为准则

请遵守 [贡献者公约](.github/CODE_OF_CONDUCT.md)，禁止：

- 发布攻击性/歧视性内容
- 传播恶意代码
- 提交未经授权的版权内容

## 许可证声明

所有贡献将默认遵循 [GPL-3.0 许可证](LICENSE)。提交代码即表示您确认拥有代码的版权，并同意以本协议授权使用。

---

感谢您为开源社区做出的贡献！🎉 有任何疑问请联系维护团队：1350989414@qq.com
````
