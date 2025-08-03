# Video Downloader Application

This project is a backend application for downloading videos and audio from various platforms using the `yt-dlp` library. It provides an API to analyze video links and download content in different formats.

## Project Structure

```
video-downloader-backend
├── src
│   ├── main.py                # Entry point of the application
│   ├── downloader
│   │   ├── __init__.py        # Package initialization
│   │   └── yt_dlp_handler.py   # Handles video analysis and downloading
│   ├── api
│   │   ├── __init__.py        # Package initialization
│   │   └── routes.py          # Defines API endpoints
│   └── utils
│       └── __init__.py        # Utility functions
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Files to ignore in Git
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd video-downloader-backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```
   python src/main.py
   ```

2. **API Endpoints:**
   - **Analyze Video:**
     - **Endpoint:** `/analyze`
     - **Method:** `POST`
     - **Body:** `{ "url": "<video_url>" }`
     - **Response:** Metadata of the video including title, duration, thumbnail, and available formats.
   
   - **Download Video:**
     - **Endpoint:** `/download`
     - **Method:** `POST`
     - **Body:** `{ "format_id": "<format_id>", "url": "<video_url>" }`
     - **Response:** Download link or status of the download.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.