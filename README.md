# GalChat

## 简介

本项目旨在使用 Galgame 数据微调大型语言模型，以实现角色扮演功能。项目包括数据预处理、模型微调等全套工具，使用 Swift 框架进行开发。

## 环境建议

- Python 3.10.14

## 安装

1. **克隆项目**

   ```bash
   git clone https://github.com/anka-afk/GalChat
   cd <GalChat>
   ```

2. **安装 swift**

   运行 `install_swift.bat` 脚本以安装所需的依赖项。

3. **(可选)下载数据集**

   在 `data_prep` 目录下，运行 `download_dataset.py` 脚本以下载所需的数据集。

   ```bash
   python data_prep/download_dataset.py
   ```

### 模型微调

在完成数据预处理后，您可以使用微调工具对模型进行训练。请根据项目需求调整训练参数。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
