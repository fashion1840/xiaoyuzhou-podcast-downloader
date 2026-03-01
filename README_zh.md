# 🎧 小宇宙播客下载器

[English](./README.md) | [中文](./README_zh.md)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square)

<img src="assets/icon.svg" width="128" height="128" alt="小宇宙下载器">

用于从小宇宙FM播客平台下载音频的 OpenCode 技能。

</div>

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 🎵 单集下载 | 下载单个播客 episode (MP3/M4A) |
| 📚 专辑下载 | 下载整个播客系列/专辑 |
| 📋 元数据 | 获取节目信息（标题、描述、时长、封面） |
| 🔄 批量下载 | 批量下载多个 episode |
| 📊 进度跟踪 | 实时下载进度显示 |

## 📦 安装方法

### 方法一：使用 Skills CLI（推荐）

```bash
npx skills add fashion1840/xiaoyuzhou-podcast-downloader
```

### 方法二：手动安装

```bash
# 克隆仓库
git clone https://github.com/fashion1840/xiaoyuzhou-podcast-downloader.git

# 复制到 skills 目录
cp -r xiaoyuzhou-podcast-downloader ~/.agents/skills/xiaoyuzhou-downloader
```

## 🚀 使用方法

### 触发关键词

使用以下关键词会自动激活此技能：

- 下载小宇宙
- 小宇宙音频下载
- 小宇宙播客下载
- download xiaoyuzhou

### 代码示例

```python
# 导入下载器
from scripts import xiaoyuzhou_downloader

# 下载单个 episode
xiaoyuzhou_downloader.download_episode(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3",
    output_dir="./downloads"
)

# 下载整个播客专辑
xiaoyuzhou_downloader.download_podcast(
    podcast_url="https://www.xiaoyuzhoufm.com/podcast/1234567890",
    output_dir="./downloads"
)

# 获取 episode 元数据
metadata = xiaoyuzhou_downloader.get_episode_metadata(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
print(f"标题: {metadata['title']}")
print(f"时长: {metadata['duration']} 秒")
```

### 使用 xyz-dl 命令行工具

```bash
# 安装 xyz-dl
pip install xyz-dl

# 下载单个 episode
xyz-dl https://www.xiaoyuzhoufm.com/episode/xxxxx

# 下载整个播客
xyz-dl --podcast https://www.xiaoyuzhoufm.com/podcast/xxxxx
```

## 📋 环境要求

- Python 3.7+
- [requests](https://pypi.org/project/requests/) >= 2.25.0
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) >= 4.9.0

安装依赖：
```bash
pip install requests beautifulsoup4
```

## 📁 项目结构

```
xiaoyuzhou-podcast-downloader/
├── SKILL.md                   # 技能元信息
├── README.md                  # 英文文档
├── README_zh.md               # 中文文档
├── .gitignore
├── assets/
│   └── icon.svg              # 技能图标
├── references/
│   ├── api.md                # API 文档
│   └── examples.md           # 使用示例
└── scripts/
    ├── __init__.py
    └── xiaoyuzhou_downloader.py
```

## 🤝 贡献代码

欢迎提交 Pull Request！请访问 [Pull Requests](https://github.com/fashion1840/xiaoyuzhou-podcast-downloader/pulls)。

## 📄 开源许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解更多详情。

## 🙏 致谢

- [xyz-dl](https://github.com/xyz-dl) - 小宇宙下载命令行工具
- [小宇宙 FM](https://www.xiaoyuzhoufm.com) - 播客平台

---

<div align="center">

由 [fashion1840](https://github.com/fashion1840) ❤️ 开发

</div>
