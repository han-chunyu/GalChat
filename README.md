# GalChat

<div align="center">

[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)](CONTRIBUTING.md)
[![Contributors](https://img.shields.io/github/contributors/anka-afk/GalChat?color=green)](https://github.com/anka-afk/GalChat/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/anka-afk/GalChat)](https://github.com/anka-afk/GalChat/commits/main)

[![Moe Counter](https://count.getloli.com/get/@GalChat?theme=moebooru)](https://github.com/anka-afk/GalChat)

</div>

## 目录

- [简介](#简介)
- [环境建议](#环境建议)
- [安装](#安装)
- [模型微调](#模型微调)
- [贡献](#贡献)
- [许可证](#许可证)

## 简介

本项目旨在使用 Galgame 数据微调大型语言模型，以实现角色扮演功能。项目包括数据预处理、模型微调等全套工具，使用 Swift 框架进行开发。

## 路线图

- [x] 数据预处理工具
- [ ] 模型微调
- [ ] 在线演示页面

## 环境建议

- Python 3.10.14

## 安装

1. **克隆项目**

   ```bash
   git clone https://github.com/anka-afk/GalChat
   cd GalChat
   ```

2. **安装 swift**

   - Windows：
     运行 `install_swift.bat` 脚本以安装所需的依赖项。

   - Linux/macOS：

   ```bash
   chmod +x install_swift.sh && ./install_swift.sh
   ```

3. **下载数据集(可选)**

   在 `data_prep` 目录下，运行 `download_dataset.py` 脚本以下载所需的数据集。

   ```bash
   python data_prep/download_dataset.py
   ```

### 模型微调

在完成数据预处理后，您可以使用微调工具对模型进行训练。请根据项目需求调整训练参数。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

![HuggingFace](https://img.shields.io/badge/HuggingFace-%23FFD21E.svg?logo=huggingface&logoColor=black)
