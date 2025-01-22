"""
务必先下载数据集
如果下载过慢, 请先设置环境变量, 使用镜像源:
在终端执行:
linux: export HF_ENDPOINT="https://hf-mirror.com"
windows: set HF_ENDPOINT="https://hf-mirror.com"

你也可以直接使用命令下载:
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Limour/b-corpus', repo_type='dataset', local_dir=r'./data')"
"""

from huggingface_hub import snapshot_download

local_dir = r"./data"
snapshot_download(repo_id="Limour/b-corpus", repo_type="dataset", local_dir=local_dir)
