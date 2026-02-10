from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <body style="font-family:sans-serif; text-align:center; background:#121212; color:white; padding-top:50px;">
            <div style="display:inline-block; background:#1e1e1e; padding:40px; border-radius:20px; border: 1px solid #333;">
                <h1 style="color:#ff0000;">YT MP3 Downloader</h1>
                <p>Inserisci il link del video</p>
                <form action="/download" method="post">
                    <input type="text" name="url" placeholder="Incolla link qui..." 
                           style="width:80%; padding:15px; border-radius:10px; border:none; margin-bottom:20px;">
                    <br>
                    <button type="submit" style="padding:15px 30px; background:#ff0000; color:white; border:none; border-radius:10px; font-weight:bold;">SCARICA ORA</button>
                </form>
            </div>
        </body>
    '''

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    output_tmpl = '/tmp/%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_tmpl,
        # TRUCCO: Ci fingiamo un iPhone reale per bypassare il blocco bot
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'referer': 'https://www.youtube.com/',
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Errore di sistema: YouTube ha bloccato la connessione. Prova con un altro video o riprova tra poco. <br> Dettaglio: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
