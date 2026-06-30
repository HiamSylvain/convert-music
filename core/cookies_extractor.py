import json
import os
import time
import winreg
from pathlib import Path

import win32crypt
import undetected_chromedriver as uc

_APP_DIR = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'convert-music'
_APP_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_DIR = str(_APP_DIR / 'chrome_profile')
COOKIES_DAT = str(_APP_DIR / 'cookies.dat')
COOKIES_TMP = str(_APP_DIR / 'cookies_tmp.txt')
YOUTUBE_URL = 'https://www.youtube.com'


def _get_chrome_major_version() -> int | None:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        version, _ = winreg.QueryValueEx(key, 'version')
        winreg.CloseKey(key)
        return int(version.split('.')[0])
    except Exception:
        return None


def _build_driver(headless: bool = False) -> uc.Chrome:
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={PROFILE_DIR}')
    options.add_argument('--profile-directory=Default')
    return uc.Chrome(options=options, headless=headless, version_main=_get_chrome_major_version())


def _is_logged_in(driver: uc.Chrome) -> bool:
    driver.get(YOUTUBE_URL)
    time.sleep(3)
    names = {c['name'] for c in driver.get_cookies()}
    return 'SID' in names or 'HSID' in names or '__Secure-3PSID' in names


def _save_cookies(cookies: list):
    data = json.dumps(cookies).encode('utf-8')
    encrypted = win32crypt.CryptProtectData(data, None, None, None, None, 0)
    Path(COOKIES_DAT).write_bytes(encrypted)
    print(f'{len(cookies)} cookies chiffrés et sauvegardés.')


def get_cookiefile() -> str:
    encrypted = Path(COOKIES_DAT).read_bytes()
    _, data = win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)
    cookies = json.loads(data.decode('utf-8'))

    with open(COOKIES_TMP, 'w', encoding='utf-8') as f:
        f.write('# Netscape HTTP Cookie File\n')
        for c in cookies:
            domain = c.get('domain', '')
            flag = 'TRUE' if domain.startswith('.') else 'FALSE'
            path = c.get('path', '/')
            secure = 'TRUE' if c.get('secure') else 'FALSE'
            expiry = int(c.get('expiry', 0))
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{c['name']}\t{c['value']}\n")

    return COOKIES_TMP


def export_cookies():
    if Path(COOKIES_DAT).exists():
        return

    try:
        driver = _build_driver(headless=True)
        if _is_logged_in(driver):
            cookies = driver.get_cookies()
            driver.quit()
            _save_cookies(cookies)
            return
        driver.quit()
    except Exception:
        pass

    print('Connexion YouTube requise. Ouverture de Chrome...')
    driver = _build_driver(headless=False)
    driver.get('https://accounts.google.com/ServiceLogin?service=youtube')
    print('⚠ Ne fermez PAS la fenêtre Chrome.')
    input('Connectez-vous à YouTube, puis appuyez sur Entrée ici... ')
    try:
        cookies = driver.get_cookies()
        driver.quit()
    except Exception:
        raise RuntimeError('La fenêtre Chrome a été fermée avant la récupération des cookies. Relancez le script.')
    _save_cookies(cookies)


if __name__ == '__main__':
    export_cookies()