# Usage Examples

## Basic Usage

### Download Single Episode

```python
from scripts.xiaoyuzhou_downloader import download_episode

# Download episode to default directory
filepath = download_episode(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)
print(f"Downloaded to: {filepath}")
```

### Download to Custom Directory

```python
from scripts.xiaoyuzhou_downloader import download_episode

# Download to specific directory
filepath = download_episode(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3",
    output_dir="C:/Users/gfanny/Downloads/Podcasts"
)
```

### Get Metadata Only

```python
from scripts.xiaoyuzhou_downloader import get_episode_metadata

metadata = get_episode_metadata(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)

print(f"Title: {metadata['title']}")
print(f"Podcast: {metadata['podcast_title']}")
print(f"Duration: {metadata['duration'] // 60} minutes")
print(f"Description: {metadata['description'][:200]}...")
```

## Advanced Usage

### Using XiaoyuzhouDownloader Class

```python
from scripts.xiaoyuzhou_downloader import XiaoyuzhouDownloader

# Initialize with custom output directory
downloader = XiaoyuzhouDownloader(output_dir="./my_podcasts")

# Download episode
filepath = downloader.download_episode(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)

# Download to different directory
filepath2 = downloader.download_episode(
    "https://www.xiaoyuzhoufm.com/episode/1234567890",
    output_dir="./other_podcasts"
)
```

### Batch Download Multiple Episodes

```python
from scripts.xiaoyuzhou_downloader import XiaoyuzhouDownloader

downloader = XiaoyuzhouDownloader(output_dir="./downloads")

episodes = [
    "https://www.xiaoyuzhoufm.com/episode/episode1_id",
    "https://www.xiaoyuzhoufm.com/episode/episode2_id",
    "https://www.xiaoyuzhoufm.com/episode/episode3_id",
]

for episode_url in episodes:
    try:
        filepath = downloader.download_episode(episode_url)
        print(f"Success: {filepath}")
    except Exception as e:
        print(f"Failed: {episode_url} - {e}")
```

### Download Entire Podcast Series

```python
from scripts.xiaoyuzhou_downloader import download_podcast

# Download entire podcast
files = download_podcast(
    "https://www.xiaoyuzhoufm.com/podcast/1234567890",
    output_dir="./podcast_series"
)

print(f"Downloaded {len(files)} episodes:")
for f in files:
    print(f"  - {f}")
```

### Process Downloaded Files

```python
import os
import json
from scripts.xiaoyuzhou_downloader import XiaoyuzhouDownloader

downloader = XiaoyuzhouDownloader(output_dir="./downloads")

# Download and process
episode_url = "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
audio_path = downloader.download_episode(episode_url)

# Read metadata
metadata_path = audio_path + '.json'
with open(metadata_path, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Rename file with better name
new_name = f"{metadata['podcast_title']} - {metadata['title']}.mp3"
new_path = os.path.join(downloader.output_dir, new_name)
os.rename(audio_path, new_path)
print(f"Renamed to: {new_path}")
```

## Command Line Usage

### Using the Script Directly

```bash
python xiaoyuzhou_downloader.py "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
```

### Using xyz-dl Tool

```bash
# Install xyz-dl
pip install xyz-dl

# Download single episode
xyz-dl https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3

# Download with custom filename
xyz-dl https://www.xiaoyuzhoufm.com/episode/xxx -o my_episode.mp3

# Download entire podcast
xyz-dl --podcast https://www.xiaoyuzhoufm.com/podcast/1234567890

# List episodes without downloading
xyz-dl https://www.xiaoyuzhoufm.com/podcast/1234567890 --list
```

## Integration Examples

### With transcription service

```python
from scripts.xiaoyuzhou_downloader import download_episode
from some_transcription_service import transcribe

# Download episode
audio_path = download_episode(
    "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
)

# Transcribe
transcript = transcribe(audio_path)
print(transcript)
```

### With file organizer

```python
from scripts.xiaoyuzhou_downloader import XiaoyuzhouDownloader
import os
import shutil

downloader = XiaoyuzhouDownloader(output_dir="./downloads")

# Download episode
episode_url = "https://www.xiaoyuzhoufm.com/episode/671657a30d2f24f289c293c3"
audio_path = downloader.download_episode(episode_url)

# Get metadata and organize
metadata = downloader.get_episode_metadata(episode_url)
podcast_dir = os.path.join(downloader.output_dir, metadata['podcast_title'])
os.makedirs(podcast_dir, exist_ok=True)

# Move to podcast folder
new_path = os.path.join(podcast_dir, os.path.basename(audio_path))
shutil.move(audio_path, new_path)
print(f"Organized to: {new_path}")
```

## Error Handling Examples

```python
from scripts.xiaoyuzhou_downloader import XiaoyuzhouDownloader, ValueError

downloader = XiaoyuzhouDownloader()

# Handle invalid URLs
try:
    downloader.download_episode("invalid-url")
except ValueError as e:
    print(f"Invalid URL: {e}")

# Handle network errors
try:
    downloader.download_episode("https://www.xiaoyuzhoufm.com/episode/xxx")
except requests.exceptions.ConnectionError:
    print("Network error - check your connection")
except requests.exceptions.Timeout:
    print("Request timed out - try again")
except Exception as e:
    print(f"Error: {e}")
```
