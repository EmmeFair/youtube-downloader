from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Il mio Downloader</h1>
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="Incolla link YouTube" style="width:300px">
            <button type="submit">Scarica Video</button>
        </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    # Cartella temporanea per Render
    out_dir = '/tmp/'
    ydl_opts = {
        'format': 'best',
        'outtmpl': out_dir + '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        path = ydl.prepare_filename(info)

    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run()
