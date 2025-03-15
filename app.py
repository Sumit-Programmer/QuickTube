from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import yt_dlp
import os
import time
import logging
import threading

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url, quality, download_type):
    try:
        if download_type == "audio":
            format_string = "bestaudio"
            extension = "mp3"
        elif quality == "auto":
            format_string = "bestvideo+bestaudio/best"
            extension = "mp4"
        else:
            format_string = f"bv*[height={quality}]+ba/b[height={quality}]/b"
            extension = "mp4"

        # yt-dlp options
        ydl_opts = {
            "format": format_string,
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            "merge_output_format": extension,
            "ffmpeg_location": "/usr/bin/ffmpeg",  
            "cookiefile": "cookies.txt",  # ✅ Add this line to use cookies
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            file_name = os.path.basename(file_path)

        return file_name
    except Exception as e:
        return str(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    quality = data.get("quality", "auto")
    download_type = data.get("type", "video")

    file_name = download_video(url, quality, download_type)

    if not file_name:
        return jsonify({"error": "Download failed. Try a different video."})

    return jsonify({"file": file_name})


@app.route("/download-file")
def download_file():
    file_name = request.args.get("file")
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

    if not os.path.exists(file_path):
        return "File not found!", 404

    def delete_file_later():
        try:
            time.sleep(30)  # Give time for the file to be fully downloaded
            os.remove(file_path)
            logging.info(f"Deleted: {file_path}")
        except Exception as e:
            logging.error(f"Error deleting file: {e}")

    threading.Thread(target=delete_file_later).start()

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
