# API Reference

## XiaoyuzhouDownloader Class

### Constructor

```python
downloader = XiaoyuzhouDownloader(output_dir="./downloads")
```

**Parameters:**
- `output_dir` (str): Directory to save downloaded files. Default: "./downloads"

### Methods

#### get_episode_metadata(episode_url: str) -> Dict

Get metadata for a single episode.

```python
metadata = downloader.get_episode_metadata(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
```

**Returns:**
```python
{
    'id': '671657a30d2f24f289c293c3',
    'title': 'Episode Title',
    'description': 'Episode description...',
    'duration': 840,  # seconds
    'audio_url': 'https://example.com/audio.mp3',
    'cover_url': 'https://example.com/cover.jpg',
    'podcast_title': 'Podcast Name',
    'publish_date': '2024-01-01'
}
```

#### download_episode(episode_url: str, output_dir: str = None) -> str

Download a single episode.

```python
filepath = downloader.download_episode(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3",
    output_dir="./my_podcasts"
)
```

**Parameters:**
- `episode_url` (str): Xiaoyuzhou episode URL
- `output_dir` (str, optional): Output directory

**Returns:**
- str: Path to downloaded file

#### download_podcast(podcast_url: str, output_dir: str = None) -> List[str]

Download entire podcast series.

```python
files = downloader.download_podcast(
    "https://www.xiaoyuzhoufm.com/podcast/1234567890",
    output_dir="./podcasts"
)
```

**Parameters:**
- `podcast_url` (str): Xiaoyuzhou podcast URL
- `output_dir` (str, optional): Output directory

**Returns:**
- List[str]: List of downloaded file paths

#### extract_episode_id(url: str) -> str

Extract episode ID from URL.

```python
episode_id = downloader.extract_episode_id(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
# Returns: '671657a30d2f24f289c293c3'
```

## Convenience Functions

### download_episode(episode_url: str, output_dir: str = "./downloads") -> str

Simple function to download single episode.

### download_podcast(podcast_url: str, output_dir: str = "./downloads") -> List[str]

Simple function to download entire podcast.

### get_episode_metadata(episode_url: str) -> Dict

Simple function to get episode metadata.

## URL Formats Supported

- Single episode: `https://www.xiaoyuzhoufm.com/episode/{episode_id}`
- Podcast series: `https://www.xiaoyuzhoufm.com/podcast/{podcast_id}`

## Error Handling

```python
try:
    metadata = get_episode_metadata(url)
    print(f"Title: {metadata['title']}")
except ValueError as e:
    print(f"Invalid URL: {e}")
except Exception as e:
    print(f"Download failed: {e}")
```

## Notes

- Audio format is typically MP3 or M4A
- Duration is returned in seconds
- Cover images are in JPEG/PNG format
- Metadata JSON file is saved alongside audio file
