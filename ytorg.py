import tkinter as tk
from tkinter import ttk
from pytube import Playlist
import json
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

class YouTubePlaylistViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Viewer")

        self.data_file = "playlists.json"
        self.playlist_urls = []
        self.watched_statuses = {}

        # Load saved data
        self.load_data()

        # Entry for playlist URL
        self.playlist_url_label = tk.Label(root, text="Playlist URL:")
        self.playlist_url_label.pack(pady=5)
        self.playlist_url_entry = tk.Entry(root, width=50)
        self.playlist_url_entry.pack(pady=5)

        # Entry for start and end range
        self.range_label = tk.Label(root, text="Enter video range (e.g., 50-60):")
        self.range_label.pack(pady=5)
        self.range_entry = tk.Entry(root, width=20)
        self.range_entry.pack(pady=5)

        # Button to add playlist
        self.add_button = tk.Button(root, text="Add Playlist", command=self.add_playlist)
        self.add_button.pack(pady=10)

        # Button to view playlist history
        self.view_button = tk.Button(root, text="View Playlist History", command=self.view_playlists)
        self.view_button.pack(pady=10)

        # Frame to hold the video titles and checkboxes
        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable canvas within the frame
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Display loaded playlists
        for playlist_url in self.playlist_urls:
            self.fetch_and_display_playlist(playlist_url, self.scrollable_frame)

    def add_playlist(self):
        playlist_url = self.playlist_url_entry.get()
        if playlist_url:
            self.playlist_urls.append(playlist_url)
            self.fetch_and_display_playlist(playlist_url, self.scrollable_frame)
            self.save_data()

    def fetch_and_display_playlist(self, playlist_url, frame):
        try:
            # Validate range input
            range_text = self.range_entry.get()
            if '-' not in range_text or not range_text.replace('-', '').isdigit():
                raise ValueError("Invalid range input. Please enter a range like '50-60'.")

            start, end = map(int, range_text.split('-'))
            playlist = Playlist(playlist_url)
            videos = list(playlist.videos)[start-1:end]

            for widget in frame.winfo_children():
                widget.destroy()

            for i, video in enumerate(videos, start=start):
                vid_frame = ttk.Frame(frame)
                vid_frame.grid(row=i-start, column=0, sticky="w", padx=5, pady=5)

                thumbnail_url = video.thumbnail_url
                response = requests.get(thumbnail_url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((120, 90), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)

                img_label = tk.Label(vid_frame, image=img)
                img_label.image = img  # Keep a reference to avoid garbage collection
                img_label.pack(side="left", padx=5)

                video_label = tk.Label(vid_frame, text=video.title, wraplength=400, justify="left")
                video_label.pack(side="left", padx=5)

                var = tk.BooleanVar(value=self.watched_statuses.get(video.watch_url, False))
                checkbox = tk.Checkbutton(vid_frame, variable=var, command=lambda url=video.watch_url, v=var: self.update_watched_status(url, v))
                checkbox.pack(side="right", padx=5)

                play_button = tk.Button(vid_frame, text="Play", command=lambda url=video.watch_url: self.play_video(url))
                play_button.pack(side="right", padx=5)
        except Exception as e:
            print(f"Error fetching playlist: {e}")

    def update_watched_status(self, video_url, var):
        self.watched_statuses[video_url] = var.get()
        self.save_data()

    def play_video(self, video_url):
        webbrowser.open(video_url)

    def save_data(self):
        data = {
            "playlists": self.playlist_urls,
            "watched_statuses": self.watched_statuses
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.playlist_urls = data.get("playlists", [])
                self.watched_statuses = data.get("watched_statuses", {})

    def view_playlists(self):
        top = tk.Toplevel(self.root)
        top.title("Playlist History")

        history_frame = ttk.Frame(top)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(history_frame)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for playlist_url in self.playlist_urls:
            self.fetch_and_display_playlist(playlist_url, scrollable_frame)

        for i, url in enumerate(self.playlist_urls):
            frame = ttk.Frame(scrollable_frame)
            frame.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            label = tk.Label(frame, text=url, wraplength=400, justify="left")
            label.pack(side="left", padx=5)

            delete_button = tk.Button(frame, text="Delete", command=lambda u=url: self.delete_playlist(u, top))
            delete_button.pack(side="right", padx=5)

    def delete_playlist(self, url, top):
        if url in self.playlist_urls:
            self.playlist_urls.remove(url)
            self.save_data()
            top.destroy()
            self.view_playlists()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubePlaylistViewer(root)
    root.mainloop()
