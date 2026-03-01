---
name: xiaoyuzhou-downloader
description: |
  Download audio from Xiaoyuzhou (小宇宙FM) podcast platform. Supports single episode download, entire podcast series download, metadata extraction, and batch download.
  Trigger phrases: "下载小宇宙", "小宇宙音频下载", "download xiaoyuzhou", "小宇宙播客下载"
---

# Xiaoyuzhou Audio Downloader

Download audio from Xiaoyuzhou (小宇宙FM) podcast platform.

## Quick Start

### Single Episode Download

```python
from scripts import xiaoyuzhou_downloader

# Download single episode
xiaoyuzhou_downloader.download_episode(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3",
    output_dir="./downloads"
)
```

### Podcast Series Download

```python
# Download entire podcast series
xiaoyuzhou_downloader.download_podcast(
    podcast_id="1234567890",
    output_dir="./downloads"
)
```

### Get Metadata

```python
# Get episode metadata
metadata = xiaoyuzhou_downloader.get_episode_metadata(
    episode_url="https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"Duration: {metadata['duration']}")
```

## Supported Features

- Single episode download (MP3/M4A)
- Podcast series/album download
- Episode metadata extraction (title, description, duration, cover)
- Batch download multiple episodes
- Progress tracking and resume support
- Output format customization

## Usage Patterns

### Method 1: Using xyz-dl CLI Tool

The skill includes integration with the xyz-dl open source tool:

```bash
# Install xyz-dl
pip install xyz-dl

# Download single episode
xyz-dl https://www.xiaoyuzhoufm.com/episode/xxxxx

# Download entire podcast
xyz-dl --podcast https://www.xiaoyuzhoufm.com/podcast/xxxxx
```

### Method 2: Using Online API

Use the built-in downloader that calls xyzdownloader.xyz API:

```python
from scripts import xiaoyuzhou_downloader

# Parse episode
result = xiaoyuzhou_downloader.parse_episode(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)

# Download audio
xiaoyuzhou_downloader.download_audio(
    url=result['audio_url'],
    filename=f"{result['title']}.mp3",
    output_dir="./downloads"
)
```

### Method 3: Using Browser Extension

Install the Xiaoyuzhou FM Audio Downloader browser extension from Greasy Fork.

## API Reference

See [references/api.md](references/api.md) for complete API documentation.

## Examples

See [references/examples.md](references/examples.md) for more usage examples.
