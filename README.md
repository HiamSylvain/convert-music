# Convert Music

Outil desktop pour télécharger ses playlists YouTube en MP3.

## Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) — `pip install uv`
- Google Chrome installé

## Installation

```bash
git clone https://github.com/HiamSylvain/convert-music.git
cd convert-music
uv sync
```

## Lancement

```bash
uv run python core/app.py
```

Au premier lancement, une fenêtre Chrome s'ouvre pour se connecter à YouTube. Les lancements suivants sont silencieux.

## Notes

- Les playlists doivent être **publiques** sur YouTube pour pouvoir être téléchargées.
- Les MP3 sont sauvegardés dans le dossier `Téléchargements` par défaut.