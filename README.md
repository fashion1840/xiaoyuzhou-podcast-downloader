# Xiaoyuzhou Podcast Downloader Skill

OpenCode skill for downloading audio from Xiaoyuzhou (小宇宙FM) podcast platform.

## Features

- Download single podcast episodes (MP3/M4A)
- Download entire podcast series/albums
- Extract episode metadata (title, description, duration, cover)
- Batch download multiple episodes
- Progress tracking

## Installation

### Using Skills CLI (Recommended)

```bash
npx skills add fashion1840/xiaoyuzhou-podcast-downloader
```

### Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/fashion1840/xiaoyuzhou-podcast-downloader.git
```

2. Copy to your skills directory:
```bash
cp -r xiaoyuzhou-podcast-downloader ~/.agents/skills/xiaoyuzhou-downloader
```

## Usage

### Trigger Phrases

This skill activates when you use these phrases:
- "下载小宇宙"
- "小宇宙音频下载"
- "download xiaoyuzhou"
- "小宇宙播客下载"

### Examples

```python
# Download single episode
from scripts import xiaoyuzhou_downloader

xiaoyuzhou_downloader.download_episode(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3",
    output_dir="./downloads"
)

# Download entire podcast
xiaoyuzhou_downloader.download_podcast(
    podcast_url="https://www.xiaoyuzhoufm.com/podcast/1234567890",
    output_dir="./downloads"
)

# Get metadata
metadata = xiaoyuzhou_downloader.get_episode_metadata(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## License

MIT License
