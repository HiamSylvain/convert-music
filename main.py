from fastapi import FastAPI
import subprocess
import shlex
import os
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

app=FastAPI()

link_site='http://147.79.101.206/#'

app.add_middleware(
    CORSMiddleware,
    allow_origins=[link_site], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def download_zip():
    output_dir = "output_dir"
    zip_filename = "output.zip"

    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    shutil.make_archive("output", "zip", output_dir)

    return FileResponse(
        path=zip_filename,
        media_type="application/zip",
        filename="output_mp3.zip"
    )


@app.get('/convert')
def convert_playlist_to_mp3(link_playlist :str):

    output_dir='output_dir'
    print('création fichier...')
    os.makedirs(output_dir, exist_ok=True)

    cmd = (
        'yt-dlp '
        '--cookies cookies.txt '
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

    print("conversion en zip...")
    res=download_zip()
    print("conversion terminée...")

    return res

if __name__ == "__main__":

    url='https://youtube.com/playlist?list=PL_DW1oF5je4ybgpmpck2DRds_l9w5OyQv&si=WkR_-e8JETiEZKjP'
    convert_playlist_to_mp3(url)
    # print('hello world')

