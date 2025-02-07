# GalChat 🎮💬

<div align="center">

[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Version](https://img.shields.io/badge/Python-3.10.14%2B-blue)
![PyTorch Version](https://img.shields.io/badge/PyTorch-2.5.1%2B-red)
![SWIFT Version](https://img.shields.io/badge/SWIFT-3.0.3%2B-orange)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)](CONTRIBUTING.md)
[![Contributors](https://img.shields.io/github/contributors/anka-afk/GalChat?color=green)](https://github.com/anka-afk/GalChat/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/anka-afk/GalChat)](https://github.com/anka-afk/GalChat/commits/main)

</div>

<div align="center">

[![Moe Counter](https://count.getloli.com/get/@GalChat?theme=moebooru)](https://github.com/anka-afk/GalChat)

</div>

## 目录

- [简介](#简介-)
- [核心特性](#核心特性-)
- [路线图](#路线图-)
- [环境要求](#环境要求-)
- [快速开始](#快速开始-)
  - [克隆项目](#1-克隆项目)
  - [配置环境](#2-配置环境)
  - [准备数据](#3-准备数据可选)
  - [微调模型](#4-微调模型)
- [进阶指南](#进阶指南-)
  - [自定义数据集](#自定义数据集)
  - [微调参数调优](#微调参数调优)
- [贡献指南](#贡献指南-)
- [致谢](#致谢-)
- [许可证](#许可证-)

## 简介 🌟

GalChat 是一个基于大规模语言模型的角色扮演对话系统，专为 Galgame 爱好者设计。通过精细处理的多轮对话数据集，我们提供从数据清洗、模型微调到交互式部署的全流程解决方案。项目基于 Modelscope 的 [SWIFT](https://github.com/modelscope/swift) 框架构建，支持高效参数微调和分布式训练。

## 核心特性 🧩

- 🧩 支持 LLaMA、ChatGLM、Deepseek 等主流大模型
- 📊 包含自动化数据清洗流水线
- ⚡ 基于 QLoRA 的高效微调技术
- 🎭 多角色情感一致性控制
- 🚀 开箱即用的 Gradio 交互界面

## 路线图 🗺️

- [x] 数据预处理工具（v0.1）
- [x] 基础微调框架集成（v0.2）
- [ ] 交互式演示页面（v0.3）
- [ ] 多模态扩展（v1.0 Roadmap）

## 环境要求 ⚙️

- Python 3.10.14
- CUDA 11.7+ (推荐 NVIDIA GPU 显存 ≥ 16GB)
- PyTorch 2.0+

## 快速开始 🚀

### 1. **克隆项目**

```bash
git clone https://github.com/anka-afk/GalChat
cd GalChat
```

### 2. **配置环境**

```
# 创建并激活虚拟环境
python -m venv galchat-env
source galchat-env/bin/activate  # Linux/macOS
galchat-env\Scripts\activate.bat  # Windows

# 安装核心依赖
pip install -r requirements.txt
```

安装 SWIFT 框架:

- Windows：
  运行 `install_swift.bat` 脚本以安装所需的依赖项。

- Linux/macOS：

```bash
chmod +x install_swift.sh && ./install_swift.sh
```

### 3. **准备数据(可选)(约 2GB)**

在 `data_prep` 目录下，运行 `download_dataset.py` 脚本以下载所需的数据集。

```bash
python data_prep/download_dataset.py
```

### 4. 微调模型

在完成数据预处理后，您可以使用微调工具对模型进行训练。请根据项目需求调整训练参数。

在 `finetune` 目录下，运行 `finetune.py` 脚本进行微调。

```
python finetune/finetune.py
```

### 启动交互界面

标记为未完成

## 进阶指南 📚

### 自定义数据集

1. 将原始文本放入 `raw_data/` 目录
2. 确保数据格式为：

```json
{
  "conversation": [
    { "role": "user", "content": "你好..." },
    { "role": "character", "content": "晚上好..." }
  ]
}
```

3. 运行预处理脚本生成训练数据

### 微调参数调优

参考 `configs/tuning/` 下的示例配置文件，支持以下训练策略：

- 全参数微调
- LoRA/QLoRA
- P-Tuning v2
- 多任务学习

## 贡献指南 🤝

我们欢迎各种形式的贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解：

- 问题报告规范
- Pull Request 流程
- 代码风格要求
- 社区行为准则

## 致谢 🙏

- [ModelScope](https://modelscope.cn/) 提供的基础设施支持
- [SWIFT](https://github.com/modelscope/swift) 高效微调框架
- 所有数据集贡献者

## 许可证 📜

本项目采用 GPL-3.0 许可证，详见 [LICENSE](https://github.com/anka-afk/GalChat/blob/main/LICENSE) 文件。
