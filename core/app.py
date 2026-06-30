import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cookies_extractor import export_cookies
from downloader import download_playlist
from youtube_auth import get_user_playlists


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Convert Music')
        self.geometry('500x420')
        self.resizable(False, False)

        self._playlists = []
        self._output_dir = os.path.expanduser('~/Downloads')

        self._build_ui()
        self._load_playlists()

    def _build_ui(self):
        tk.Label(self, text='Mes Playlists YouTube', font=('Arial', 14, 'bold')).pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(fill='both', expand=True, padx=20)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')

        self._listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=('Arial', 11))
        self._listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self._listbox.yview)

        folder_frame = tk.Frame(self)
        folder_frame.pack(fill='x', padx=20, pady=8)
        tk.Label(folder_frame, text='Dossier :').pack(side='left')
        self._folder_label = tk.Label(folder_frame, text=self._output_dir, fg='gray')
        self._folder_label.pack(side='left', padx=5)
        tk.Button(folder_frame, text='Choisir', command=self._choose_folder).pack(side='right')

        self._download_btn = tk.Button(
            self, text='Télécharger en MP3', command=self._on_download,
            bg='#FF0000', fg='white', font=('Arial', 12, 'bold'), pady=8,
        )
        self._download_btn.pack(fill='x', padx=20, pady=4)

        self._status = tk.Label(self, text='', fg='gray')
        self._status.pack(pady=4)

    def _load_playlists(self):
        self._status.config(text='Chargement des playlists...')
        threading.Thread(target=self._fetch_playlists, daemon=True).start()


    def _fetch_playlists(self):
        try:
            export_cookies()
            self._playlists = get_user_playlists()
            self.after(0, self._populate_listbox)

        except Exception as e:
            self.after(0, lambda: self._status.config(text=f'Erreur : {e}'))

    def _populate_listbox(self):
        self._listbox.delete(0, 'end')
        for p in self._playlists:
            tag = '[Privée] ' if p.get('private') else ''
            self._listbox.insert('end', f"{tag}{p['title']} ({p.get('count', '?')} vidéos)")
        self._status.config(text=f'{len(self._playlists)} playlist(s) trouvée(s).')

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self._output_dir)
        if folder:
            self._output_dir = folder
            self._folder_label.config(text=folder)

    def _on_download(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showwarning('Attention', 'Sélectionnez une playlist.')
            return

        playlist = self._playlists[selection[0]]
        self._download_btn.config(state='disabled')
        self._status.config(text=f'Téléchargement de "{playlist["title"]}"...')

        def _run_download():
            download_playlist(playlist['url'], self._output_dir)
            self.after(0, lambda: self._download_btn.config(state='normal'))
            self.after(0, lambda: self._status.config(text='Terminé !'))
        threading.Thread(target=_run_download, daemon=True).start()


if __name__ == '__main__':
    App().mainloop()
