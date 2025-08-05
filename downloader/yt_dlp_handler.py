import yt_dlp
import tempfile
import os

class YTDLPHandler:
    def analyze_video(self, url):
        self.last_url = url
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info['formats']:
                if not f.get('filesize'):
                    continue
                size_mb = round(f['filesize'] / (1024 * 1024), 2)
                formats.append({
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('resolution') or f.get('height'),
                    'filesize_mb': size_mb,
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                })
            return {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats,
            }

    def is_video_only(self, format_id):
        # Check if the format_id is video-only (vcodec not 'none', acodec is 'none')
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.last_url, download=False)
            for f in info['formats']:
                if f['format_id'] == str(format_id):
                    return f.get('vcodec') != 'none' and f.get('acodec') == 'none'
        return False

    def download_video(self, url, format_id):
        import re
        temp_dir = tempfile.mkdtemp()
        merge_output = None
        if '+' in str(format_id) or re.search(r'bestaudio', str(format_id)):
            merge_output = 'mp4'
        ydl_opts = {
            'format': str(format_id),
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
        }
        # If format_id is video-only, merge with bestaudio
        if self.is_video_only(format_id):
            format_id = f"{format_id}+bestaudio/best"
        if merge_output:
            ydl_opts['merge_output_format'] = merge_output
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            for key in ['title']:
                if key in info and not isinstance(info[key], str):
                    info[key] = str(info[key])
            filename = ydl.prepare_filename(info)
            if merge_output:
                filename = os.path.splitext(filename)[0] + '.mp4'
        # --- Robust file check ---
        if not os.path.exists(filename) or os.path.getsize(filename) < 1024 * 1024:
            raise Exception("Download failed or file is too small/corrupted.")
        return filename, os.path.basename(filename)