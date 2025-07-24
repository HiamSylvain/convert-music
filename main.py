from fastapi import FastAPI
import subprocess
import shlex
import os
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

#si je rentre

app=FastAPI()

link_site=''

app.add_middleware(
    CORSMiddleware,
    allow_origins=[link_site], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/hello')
def root():
    return {"Hello": "Worlddddd"}



@app.get("/api/download")
def download_zip():
    output_dir = "output"
    zip_filename = "output.zip"

    # Supprimer le zip s'il existe déjà
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    # Créer un fichier zip depuis le dossier output/
    shutil.make_archive("output", "zip", output_dir)

    # Envoyer le zip comme fichier à télécharger
    return FileResponse(
        path=zip_filename,
        media_type="application/zip",
        filename="mes_mp3.zip"
    )




def convert_playlist_to_mp3(link_playlist):

    print('création fichier...')
    output_dir='output_dir'
    os.makedirs(output_dir, exist_ok=True)

    cmd = (
        'yt-dlp '
        '--cookies cookies_yt.txt '
        '-i ' 
        '-f bestaudio/best '
        '-x --audio-format mp3 --audio-quality 0 ' 
        '--add-metadata '
        '--embed-thumbnail '
        f'-o "{output_dir}/%(playlist_index)s - %(title)s.%(ext)s" '
        f'"{link_playlist}"'
        
    )

    print("Exécution :", cmd)
    subprocess.run(shlex.split(cmd), check=False)

    print('convertion terminé !')

if __name__ == "__main__":

    url='https://youtube.com/playlist?list=PL_DW1oF5je4ybgpmpck2DRds_l9w5OyQv&si=WkR_-e8JETiEZKjP'
    convert_playlist_to_mp3(url)


