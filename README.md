

# YouTube Playlist Viewer

A Tkinter-based GUI application to view and manage YouTube playlists. This application allows users to add playlists, view video titles and thumbnails, mark videos as watched, and maintain a history of playlists.

## Features

- Add YouTube playlists via URL
- Specify a range of videos to display from the playlist
- Display video thumbnails and titles
- Mark videos as watched
- Save and load playlist data, including watched status
- View and delete playlist history
- Play videos directly from the application

## Installation

### Prerequisites

- Python 3.6+
- Tkinter (usually included with Python)
- Required Python packages: `pytube`, `Pillow`, `requests`

### Clone the repository

```sh
git clone https://github.com/adityajhakumar/youtube-playlist-viewer.git
cd youtube-playlist-viewer
```

### Install dependencies

```sh
pip install pytube pillow requests
```

## Usage

Run the application using the following command:

```sh
python youtube_playlist_viewer.py
```

### Adding a Playlist

1. Enter the URL of the YouTube playlist in the "Playlist URL" field.
2. Enter the range of videos you want to display (e.g., `1-10`) in the "Enter video range" field.
3. Click the "Add Playlist" button.

### Viewing and Managing Playlists

- Click the "View Playlist History" button to view a list of added playlists.
- In the history window, you can delete a playlist by clicking the "Delete" button next to it.
- To play a video, click the "Play" button next to the video title.
- Mark videos as watched by checking the checkbox next to the video title.

## Data Persistence

The application saves the playlist URLs and watched statuses to a JSON file (`playlists.json`). The data is automatically loaded when the application starts and saved whenever a playlist is added, a video is marked as watched, or a playlist is deleted.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request.

## Author

- [Aditya Jha Kumar](https://github.com/adityajhakumar)

## Acknowledgments

- The [pytube](https://pytube.io/en/latest/) library for handling YouTube video data.
- The [Pillow](https://python-pillow.org/) library for image processing.
- The [requests](https://docs.python-requests.org/en/latest/) library for handling HTTP requests.


