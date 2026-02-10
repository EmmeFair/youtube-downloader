from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <body style="font-family:sans-serif; text-align:center; padding-top:50px; background-color:#f4f4f4;">
            <div style="background:white; display:inline-block; padding:30px; border-radius:15px; shadow: 0px 4px 10px rgba(0,0,0,0.1);">
                <h1>YouTube to MP3</h1>
                <p>Inserisci il link per scaricare l'audio</p>
                <form action="/download" method="post">
                    <input type="text" name="url" placeholder="Incolla link YouTube" style="width:300px; padding:10px; border:1px solid #ccc; border-radius:5px;">
                    <br><br>
                    <button type="submit" style="padding:10px 20px; background-color:#ff0000; color:white; border:none; border-radius:5px; cursor:pointer;">Scarica MP3</button>
                </form>
            </div>
        </body>
    '''

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    # Cartella temporanea obbligatoria per Render
    output_tmpl = '/tmp/%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Prende la migliore qualità audio disponibile
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_tmpl,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Estraiamo le info e scarichiamo
            info = ydl.extract_info(video_url, download=True)
            # yt-dlp cambia l'estensione in .mp3 dopo il post-processing
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"<div style='color:red;'>Errore durante la conversione: {str(e)}</div><br><a href='/'>Torna indietro</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
