import yt_dlp

from cookies_extractor import export_cookies, get_cookiefile
from downloader import get_playlist_info

PLAYLISTS_URL = 'https://www.youtube.com/feed/playlists'


def get_user_playlists() -> list[dict]:
    export_cookies()

    opts = {
        'quiet': True,
        'extract_flat': True,
        'cookiefile': get_cookiefile(),
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(PLAYLISTS_URL, download=False)

    playlists = []
    for entry in info.get('entries', []):
        url = f"https://youtube.com/playlist?list={entry.get('id')}"
        count = get_playlist_info(url).get('count', '?')
        playlists.append({
            'title': entry.get('title'),
            'url': url,
            'count': count,
        })

    return playlists


if __name__ == '__main__':
    for p in get_user_playlists():
        print(f"{p['title']} ({p['count']} vidéos) — {p['url']}")