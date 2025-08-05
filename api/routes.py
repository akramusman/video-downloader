from flask import Blueprint, request, jsonify, send_file
from downloader.yt_dlp_handler import YTDLPHandler

api = Blueprint('api', __name__)
yt_dlp_handler = YTDLPHandler()

@api.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('url')
    format_id = data.get('format_id')

    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    if not format_id:
        # Analyze mode
        try:
            metadata = yt_dlp_handler.analyze_video(video_url)
            return jsonify(metadata), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        # Download mode
        try:
            file_path, file_name = yt_dlp_handler.download_video(video_url, format_id)
            import os, time

            # Wait up to 30 seconds for file to exist and be non-empty
            for _ in range(30):
                if os.path.exists(file_path) and os.path.getsize(file_path) > 1024:
                    break
                time.sleep(1)
            else:
                return jsonify({'error': 'File not ready or download failed'}), 500

            return send_file(file_path, as_attachment=True, download_name=file_name)
        except Exception as e:
            print("Download error:", e)
            return jsonify({'error': str(e)}), 500