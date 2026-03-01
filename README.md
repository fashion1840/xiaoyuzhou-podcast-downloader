# 🎧 Xiaoyuzhou Podcast Downloader

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square)

<img src="assets/icon.svg" width="128" height="128" alt="Xiaoyuzhou Downloader">

An OpenCode skill for downloading audio from Xiaoyuzhou (小宇宙FM) podcast platform.

</div>

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎵 Single Episode | Download individual podcast episodes (MP3/M4A) |
| 📚 Podcast Series | Download entire podcast albums/series |
| 📋 Metadata | Extract episode info (title, description, duration, cover) |
| 🔄 Batch Download | Download multiple episodes at once |
| 📊 Progress | Real-time progress tracking |

## 📦 Installation

### Method 1: Using Skills CLI (Recommended)

```bash
npx skills add fashion1840/xiaoyuzhou-podcast-downloader
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/fashion1840/xiaoyuzhou-podcast-downloader.git

# Copy to skills directory
cp -r xiaoyuzhou-podcast-downloader ~/.agents/skills/xiaoyuzhou-downloader
```

## 🚀 Usage

### Trigger Phrases

This skill automatically activates when you use these keywords:

| Chinese | English |
|---------|---------|
| 下载小宇宙 | download xiaoyuzhou |
| 小宇宙音频下载 | - |
| 小宇宙播客下载 | - |

### Code Examples

```python
# Import the downloader
from scripts import xiaoyuzhou_downloader

# Download single episode
xiaoyuzhou_downloader.download_episode(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3",
    output_dir="./downloads"
)

# Download entire podcast series
xiaoyuzhou_downloader.download_podcast(
    podcast_url="https://www.xiaoyuzhoufm.com/podcast/1234567890",
    output_dir="./downloads"
)

# Get episode metadata
metadata = xiaoyuzhou_downloader.get_episode_metadata(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
print(f"Title: {metadata['title']}")
print(f"Duration: {metadata['duration']} seconds")
```

### Using xyz-dl CLI

```bash
# Install xyz-dl
pip install xyz-dl

# Download single episode
xyz-dl https://www.xiaoyuzhoufm.com/episode/xxxxx

# Download entire podcast
xyz-dl --podcast https://www.xiaoyuzhoufm.com/podcast/xxxxx
```

## 📋 Requirements

- Python 3.7+
- [requests](https://pypi.org/project/requests/) >= 2.25.0
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) >= 4.9.0

Install dependencies:
```bash
pip install requests beautifulsoup4
```

## 📁 Project Structure

```
xiaoyuzhou-podcast-downloader/
├── SKILL.md                   # Skill metadata
├── README.md                  # English documentation
├── README_zh.md               # Chinese documentation
├── .gitignore
├── assets/
│   └── icon.svg              # Skill icon
├── references/
│   ├── api.md                # API documentation
│   └── examples.md           # Usage examples
└── scripts/
    ├── __init__.py
    └── xiaoyuzhou_downloader.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a [Pull Request](https://github.com/fashion1840/xiaoyuzhou-podcast-downloader/pulls).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [xyz-dl](https://github.com/xyz-dl) - CLI tool for Xiaoyuzhou downloads
- [Xiaoyuzhou FM](https://www.xiaoyuzhoufm.com) - Podcast platform

---

<div align="center">

Made with ❤️ by [fashion1840](https://github.com/fashion1840)

</div>
