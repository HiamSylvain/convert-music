import os

import imageio_ffmpeg
import yt_dlp

from cookies_extractor import export_cookies, get_cookiefile

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()


def get_playlist_info(url: str) -> dict:
    opts = {
        'quiet': True,
        'extract_flat': True,
        'cookiefile': get_cookiefile(),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        'title': info.get('title', 'Playlist'),
        'count': len(info.get('entries') or []),
    }


def download_playlist(url: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '0'},
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
        ],
        'ffmpeg_location': FFMPEG_PATH,
        'outtmpl': os.path.join(output_dir, '%(playlist_index)s - %(title)s.%(ext)s'),
        'ignoreerrors': True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    export_cookies()  # no-op si cookies.dat existe déjà

    TEST_URL = 'https://youtube.com/playlist?list=PL_DW1oF5je4ybgpmpck2DRds_l9w5OyQv'

    info = get_playlist_info(TEST_URL)
    print(f"Playlist : {info['title']} ({info['count']} vidéos)")

    download_playlist(TEST_URL, 'output_dir2')
    print('Terminé.')