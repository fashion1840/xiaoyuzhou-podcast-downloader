"""
Xiaoyuzhou (小宇宙FM) Audio Downloader
Download audio from Xiaoyuzhou podcast platform
"""

import os
import re
import sys
import json
import requests
import html as html_module
from typing import Dict, Optional, List
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup


class XiaoyuzhouDownloader:
    """Download audio from Xiaoyuzhou FM"""

    def __init__(self, output_dir: str = "./downloads"):
        self.output_dir = output_dir
        self.base_url = "https://www.xiaoyuzhoufm.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        os.makedirs(output_dir, exist_ok=True)

    def extract_episode_id(self, url: str) -> str:
        """Extract episode ID from URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")

        if len(path_parts) >= 2 and path_parts[0] == "episode":
            return path_parts[1]

        query = parse_qs(parsed.query)
        if "id" in query:
            return query["id"][0]

        raise ValueError(f"Invalid Xiaoyuzhou episode URL: {url}")

    def extract_podcast_id(self, url: str) -> str:
        """Extract podcast ID from URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")

        if "podcast" in path_parts:
            return path_parts[path_parts.index("podcast") + 1]

        raise ValueError(f"Invalid Xiaoyuzhou podcast URL: {url}")

    def is_episode_url(self, url: str) -> bool:
        """Check if URL is an episode URL"""
        return "episode" in url

    def is_podcast_url(self, url: str) -> bool:
        """Check if URL is a podcast URL"""
        return "podcast" in url

    def get_episode_metadata(self, episode_url: str) -> Dict:
        """Get episode metadata from URL"""

        # Method 1: Parse from webpage
        try:
            metadata = self._parse_from_webpage(episode_url)
            if metadata and metadata.get("audio_url"):
                return metadata
        except Exception as e:
            print(f"  [INFO] Webpage parse failed: {e}")

        # Method 2: Use online parser
        try:
            metadata = self._parse_online(episode_url)
            if metadata and metadata.get("audio_url"):
                return metadata
        except Exception as e:
            print(f"  [INFO] Online parser failed: {e}")

        raise Exception("Failed to get episode metadata - please check the URL")

    def _parse_from_webpage(self, episode_url: str) -> Dict:
        """Parse episode info directly from webpage"""
        response = requests.get(episode_url, headers=self.headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("meta", property="og:title")
        title = title_tag["content"] if title_tag else "Unknown"

        audio_tag = soup.find("meta", property="og:audio")
        audio_url = audio_tag["content"] if audio_tag else ""

        desc_tag = soup.find("meta", property="og:description")
        description = desc_tag["content"] if desc_tag else ""

        image_tag = soup.find("meta", property="og:image")
        cover_url = image_tag["content"] if image_tag else ""

        duration = 0
        duration_match = re.search(r'"duration":\s*(\d+)', response.text)
        if duration_match:
            duration = int(duration_match.group(1))

        # Extract shownotes - look for episode notes/description in page
        shownotes = self._extract_shownotes(soup, response.text)

        return {
            "id": self.extract_episode_id(episode_url),
            "title": title,
            "description": description,
            "shownotes": shownotes,
            "duration": duration,
            "duration_formatted": self._format_duration(duration),
            "audio_url": audio_url,
            "cover_url": cover_url,
            "podcast_title": "",
            "publish_date": "",
        }

    def _extract_shownotes(self, soup: BeautifulSoup, html: str) -> str:
        """Extract shownotes from webpage"""
        shownotes = ""

        # Method 1: Parse from __NEXT_DATA__ JSON (most reliable)
        try:
            import json as json_module

            next_data_pattern = r'<script[^>]*id="__NEXT_DATA__"[^>]*>([^<]+)</script>'
            match = re.search(next_data_pattern, html)
            if match:
                next_data = json_module.loads(match.group(1))
                props = next_data.get("props", {})
                page_props = props.get("pageProps", {})
                episode = page_props.get("episode", {})

                # Try different fields for shownotes
                shownotes = (
                    episode.get("shownotes", "")
                    or episode.get("detailContent", "")
                    or episode.get("content", "")
                    or ""
                )

                if shownotes:
                    # Decode HTML entities
                    shownotes = html_module.unescape(shownotes)
                    # Clean up HTML tags
                    if "<" in shownotes and ">" in shownotes:
                        clean_soup = BeautifulSoup(shownotes, "html.parser")
                        shownotes = clean_soup.get_text(separator="\n", strip=True)
                    return shownotes
        except Exception as e:
            pass

        # Method 2: Look for episode content/notes section in HTML
        selectors = [
            "div.episode-notes",
            "div.shownotes",
            "div.content",
            "div.episode-content",
            "div.description",
            "section.notes",
            "div.notes-content",
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                shownotes = element.get_text(strip=True)
                if shownotes and len(shownotes) > 50:
                    # Decode HTML entities properly
                    shownotes = html_module.unescape(shownotes)
                    return shownotes

        # Method 3: Use description as fallback
        return shownotes

        # Method 2: Look for JSON data in page - extract raw content
        try:
            import json as json_module

            # Try to find JSON data in script tags
            script_patterns = [
                r"window\.__INITIAL_STATE__\s*=\s*({.*?});",
                r"window\.initialState\s*=\s*({.*?});",
                r'"content":\s*"([^"]*(?:\\.[^"]*)*)"',
                r'"shownotes":\s*"([^"]*(?:\\.[^"]*)*)"',
                r'"detailContent":\s*"([^"]*(?:\\.[^"]*)*)"',
            ]

            for script_pattern in script_patterns:
                script_match = re.search(script_pattern, html, re.DOTALL)
                if script_match:
                    try:
                        # Try direct JSON extraction
                        json_str = (
                            script_match.group(1)
                            if script_match.lastindex
                            else script_match.group(0)
                        )

                        # Clean up escaped characters
                        json_str = (
                            json_str.replace("\\n", "\n")
                            .replace("\\t", "\t")
                            .replace('\\"', '"')
                            .replace("\\\\", "\\")
                        )

                        # Try to parse as JSON to extract content
                        data = json_module.loads(json_str)
                        if isinstance(data, dict):
                            # Navigate through nested structure
                            content = (
                                data.get("episode", {}).get("detailContent", "")
                                or data.get("episode", {}).get("content", "")
                                or data.get("shownotes", "")
                                or data.get("content", "")
                            )
                            if content:
                                return html_module.unescape(content)
                    except (json_module.JSONDecodeError, AttributeError):
                        continue
        except Exception as e:
            pass

        # Method 3: Try to find and decode escaped Unicode in raw HTML
        try:
            # Look for escaped Unicode patterns like \u4e2d\u6587
            unicode_pattern = (
                r'"(?:shownotes|detailContent|content)":\s*"((?:[^"\\]|\\.)*)"'
            )
            match = re.search(unicode_pattern, html)
            if match:
                raw_str = match.group(1)
                # Handle various escape sequences
                decoded = raw_str.encode("utf-8").decode("unicode_escape")
                # Clean up
                decoded = (
                    decoded.replace("\\n", "\n")
                    .replace("\\t", "\t")
                    .replace('\\"', '"')
                    .replace("\\\\", "\\")
                )
                # Decode HTML entities
                decoded = html_module.unescape(decoded)
                if decoded and len(decoded) > 20:
                    return decoded
        except Exception as e:
            pass

        # Method 4: Use description as fallback
        return shownotes

    def _format_duration(self, seconds: int) -> str:
        """Format duration in human readable format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def _parse_online(self, episode_url: str) -> Dict:
        """Use online parser to get episode info"""
        try:
            parser_url = "https://xyzdownloader.xyz/api/parse"
            response = requests.post(parser_url, json={"url": episode_url}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return {
                    "id": self.extract_episode_id(episode_url),
                    "title": data.get("title", "Unknown"),
                    "description": data.get("description", ""),
                    "duration": data.get("duration", 0),
                    "audio_url": data.get("audio_url", ""),
                    "cover_url": data.get("cover_url", ""),
                    "podcast_title": data.get("podcast_title", ""),
                    "publish_date": data.get("publish_date", ""),
                }
        except Exception as e:
            pass

        raise Exception("Online parser unavailable")

    def download_episode(
        self,
        episode_url: str,
        output_dir: Optional[str] = None,
        show_progress: bool = True,
    ) -> str:
        """Download single episode"""
        output_dir = output_dir or self.output_dir

        # Get metadata
        metadata = self.get_episode_metadata(episode_url)

        # Download audio
        audio_url = metadata["audio_url"]
        if not audio_url:
            raise Exception(
                "No audio URL found - the episode may be premium or unavailable"
            )

        # Determine filename
        safe_title = self._sanitize_filename(metadata["title"])
        filename = f"{safe_title}.mp3"
        filepath = os.path.join(output_dir, filename)

        # Download with progress
        self._download_file(audio_url, filepath, show_progress)

        # Save metadata
        metadata_file = filepath + ".json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # Save shownotes to separate file
        shownotes = metadata.get("shownotes", "")
        if shownotes:
            shownotes_file = filepath.replace(".mp3", ".txt")
            with open(shownotes_file, "w", encoding="utf-8") as f:
                f.write(f"Title: {metadata.get('title', '')}\n")
                f.write(f"Duration: {metadata.get('duration_formatted', '')}\n")
                f.write(f"Description: {metadata.get('description', '')}\n")
                f.write("\n" + "=" * 50 + "\n\n")
                f.write("Shownotes:\n")
                f.write(shownotes)

        return filepath

    def download_podcast(
        self, podcast_url: str, output_dir: Optional[str] = None
    ) -> Dict:
        """Download entire podcast series"""
        output_dir = output_dir or self.output_dir

        podcast_id = self.extract_podcast_id(podcast_url)
        podcast_title = ""

        # Get podcast info and episodes
        try:
            podcast_info = self._get_podcast_info(podcast_url)
            episodes = podcast_info.get("episodes", [])
            podcast_title = podcast_info.get("title", "Unknown Podcast")
        except Exception as e:
            print(f"  [WARN] Failed to get podcast episodes: {e}")
            print(f"  [INFO] Trying to fetch episodes from webpage...")
            episodes = self._get_podcast_episodes_from_page(podcast_url)

        if not episodes:
            raise Exception("No episodes found - please check the podcast URL")

        print(f"\n[Podcast] {podcast_title}")
        print(f"[Total] Found {len(episodes)} episodes\n")

        # Create podcast folder
        safe_podcast_title = self._sanitize_filename(podcast_title)
        podcast_folder = os.path.join(output_dir, safe_podcast_title)
        os.makedirs(podcast_folder, exist_ok=True)

        # Download each episode
        downloaded = []
        failed = []
        total = len(episodes)

        for i, episode in enumerate(episodes, 1):
            episode_id = episode.get("id")
            episode_title = episode.get("title", f"Episode {i}")

            try:
                episode_url = f"{self.base_url}/episode/{episode_id}"
                print(f"[{i}/{total}] Downloading: {episode_title[:50]}...")

                filepath = self.download_episode(
                    episode_url, podcast_folder, show_progress=False
                )
                downloaded.append(filepath)
                print(f"  [OK] Saved: {os.path.basename(filepath)}\n")
            except Exception as e:
                failed.append({"title": episode_title, "error": str(e)})
                print(f"  [FAIL] {episode_title[:40]}... - {str(e)[:50]}\n")

        # Summary
        print("=" * 50)
        print(f"[Summary] Downloaded: {len(downloaded)}/{total}")
        if failed:
            print(f"[Failed] {len(failed)} episodes:")
            for f in failed[:5]:
                print(f"  - {f['title'][:40]}...")
            if len(failed) > 5:
                print(f"  ... and {len(failed) - 5} more")
        print("=" * 50)

        return {
            "podcast_title": podcast_title,
            "total": total,
            "downloaded": len(downloaded),
            "failed": len(failed),
            "files": downloaded,
        }

    def _get_podcast_info(self, podcast_url: str) -> Dict:
        """Get podcast info from online parser"""
        try:
            parser_url = "https://xyzdownloader.xyz/api/podcast"
            response = requests.post(parser_url, json={"url": podcast_url}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return {
                    "title": data.get("title", "Unknown"),
                    "episodes": data.get("episodes", []),
                }
        except Exception as e:
            raise Exception(f"Online parser failed: {e}")

        raise Exception("Failed to get podcast info")

    def _get_podcast_episodes_from_page(self, podcast_url: str) -> List[Dict]:
        """Get podcast episodes from webpage"""
        try:
            response = requests.get(podcast_url, headers=self.headers, timeout=15)
            response.raise_for_status()

            # Find all episode links
            soup = BeautifulSoup(response.text, "html.parser")
            episodes = []

            # Look for episode links
            links = soup.find_all("a", href=lambda x: x and "/episode/" in x)
            for link in links:
                href = link.get("href", "")
                if "/episode/" in href:
                    episode_id = href.split("/episode/")[-1].split("?")[0]
                    title = link.get_text(strip=True)
                    if episode_id and title:
                        episodes.append({"id": episode_id, "title": title})

            # Remove duplicates
            seen = set()
            unique_episodes = []
            for ep in episodes:
                if ep["id"] not in seen:
                    seen.add(ep["id"])
                    unique_episodes.append(ep)

            return unique_episodes
        except Exception as e:
            print(f"  [ERROR] Failed to parse podcast page: {e}")
            return []

    def download_batch(self, urls: List[str], output_dir: Optional[str] = None) -> Dict:
        """Download multiple episodes/podcasts"""
        output_dir = output_dir or self.output_dir

        print(f"\n[Batch] Starting batch download of {len(urls)} items\n")

        episodes = []
        podcasts = []

        # Classify URLs
        for url in urls:
            if self.is_episode_url(url):
                episodes.append(url)
            elif self.is_podcast_url(url):
                podcasts.append(url)
            else:
                print(f"  [WARN] Unknown URL format: {url}")

        results = {
            "episodes_downloaded": 0,
            "podcasts_processed": 0,
            "total_files": 0,
            "failed": 0,
        }

        # Download single episodes
        if episodes:
            print(f"[Episodes] Downloading {len(episodes)} single episodes...\n")

            for i, url in enumerate(episodes, 1):
                try:
                    print(f"[{i}/{len(episodes)}] {url}")
                    filepath = self.download_episode(
                        url, output_dir, show_progress=False
                    )
                    results["episodes_downloaded"] += 1
                    results["total_files"] += 1
                    print(f"  [OK]\n")
                except Exception as e:
                    results["failed"] += 1
                    print(f"  [FAIL] {str(e)[:60]}\n")

        # Download podcasts
        if podcasts:
            print(f"\n[Podcasts] Processing {len(podcasts)} podcasts...\n")

            for i, url in enumerate(podcasts, 1):
                try:
                    print(f"[{i}/{len(podcasts)}] {url}")
                    result = self.download_podcast(url, output_dir)
                    results["podcasts_processed"] += 1
                    results["total_files"] += result["downloaded"]
                    results["failed"] += result["failed"]
                except Exception as e:
                    results["failed"] += 1
                    print(f"  [FAIL] {str(e)[:60]}\n")

        # Summary
        print("=" * 50)
        print(f"[Summary]")
        print(f"  Episodes: {results['episodes_downloaded']}")
        print(f"  Podcasts: {results['podcasts_processed']}")
        print(f"  Total files: {results['total_files']}")
        print(f"  Failed: {results['failed']}")
        print("=" * 50)

        return results

    def _download_file(self, url: str, filepath: str, show_progress: bool = True):
        """Download file with progress"""
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if show_progress and total_size:
                        progress = int((downloaded / total_size) * 100)
                        if progress != getattr(self, "_last_progress", -1):
                            self._last_progress = progress
                            bar_len = 60
                            filled = int(bar_len * progress / 100)
                            bar = "#" * filled + "-" * (bar_len - filled)
                            sys.stdout.write(f"\r下载进度 [{bar}] {progress}%")
                            sys.stdout.flush()

        if show_progress:
            print()

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return filename[:200]


# Convenience functions
def download_episode(episode_url: str, output_dir: str = "./downloads") -> str:
    """Download single episode"""
    downloader = XiaoyuzhouDownloader(output_dir)
    return downloader.download_episode(episode_url, output_dir)


def download_podcast(podcast_url: str, output_dir: str = "./downloads") -> Dict:
    """Download entire podcast"""
    downloader = XiaoyuzhouDownloader(output_dir)
    return downloader.download_podcast(podcast_url, output_dir)


def download_batch(urls: List[str], output_dir: str = "./downloads") -> Dict:
    """Download multiple episodes/podcasts"""
    downloader = XiaoyuzhouDownloader(output_dir)
    return downloader.download_batch(urls, output_dir)


def get_episode_metadata(episode_url: str) -> Dict:
    """Get episode metadata"""
    downloader = XiaoyuzhouDownloader()
    return downloader.get_episode_metadata(episode_url)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Xiaoyuzhou (小宇宙FM) Audio Downloader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download single episode
  python xiaoyuzhou_downloader.py "https://www.xiaoyuzhoufm.com/episode/xxx"

  # Download to custom directory
  python xiaoyuzhou_downloader.py "https://www.xiaoyuzhoufm.com/episode/xxx" -o ./my_music

  # Download entire podcast
  python xiaoyuzhou_downloader.py "https://www.xiaoyuzhoufm.com/podcast/xxx" --podcast

  # Batch download (multiple URLs from file)
  python xiaoyuzhou_downloader.py --batch urls.txt

  # Batch download (multiple URLs from command line)
  python xiaoyuzhou_downloader.py --batch "url1" "url2" "url3"
        """,
    )

    parser.add_argument("url", nargs="?", help="Episode or podcast URL")
    parser.add_argument(
        "-o", "--output", default="./downloads", help="Output directory"
    )
    parser.add_argument(
        "-p", "--podcast", action="store_true", help="Download entire podcast"
    )
    parser.add_argument("-b", "--batch", nargs="+", help="Batch download multiple URLs")
    parser.add_argument("-f", "--file", help="Read URLs from file (one per line)")

    args = parser.parse_args()

    downloader = XiaoyuzhouDownloader(args.output)

    try:
        # Batch mode
        if args.batch or args.file:
            urls = []

            if args.batch:
                urls.extend(args.batch)

            if args.file:
                with open(args.file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            urls.append(line)

            if not urls:
                print("[ERROR] No URLs provided for batch download")
                sys.exit(1)

            results = downloader.download_batch(urls, args.output)
            sys.exit(0 if results["failed"] == 0 else 1)

        # Single URL
        if not args.url:
            parser.print_help()
            sys.exit(1)

        # Podcast mode
        if args.podcast or downloader.is_podcast_url(args.url):
            print(f"[Podcast] {args.url}\n")
            result = downloader.download_podcast(args.url, args.output)
            sys.exit(0 if result["failed"] == 0 else 1)

        # Episode mode
        print(f"Downloading: {args.url}\n")
        filepath = downloader.download_episode(args.url, args.output)
        print(f"\n[OK] Downloaded to: {filepath}")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Network connection failed - please check your internet")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\n[ERROR] Request timeout - please try again")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERROR] Invalid URL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)
