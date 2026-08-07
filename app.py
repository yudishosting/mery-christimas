import http.server
import os
import socket
import socketserver
import webbrowser
import requests

AUDIO_FILE = "song.mp3"
AUDIO_URL = "https://files.catbox.moe/1odhi3.mp3"
BACKGROUND_URL = "https://raw.githubusercontent.com/Nex-Core/Uploader-Media/main/gambar-only/1786076602402_y9uydave.jpg"

LYRICS_DATA = [
    {"time": 0.0, "text": "You know it's true"},
    {"time": 4.17, "text": "Yeah, I miss you"},
    {"time": 9.09, "text": "You know it's true"},
    {"time": 13.18, "text": "So what if I call"},
    {"time": 17.89, "text": "And you pick up the phone"},
    {"time": 22.77, "text": "And I use this holiday to make my way to your ghost"},
    {"time": 31.68, "text": "Oh what if you're lonely"},
    {"time": 36.32, "text": "And you know I am too"},
    {"time": 41.09, "text": "And I get the chance to say"},
    {"time": 44.24, "text": "Merry Christmas, I miss you"},
    {"time": 50.11, "text": "I miss you"}
]

if not os.path.exists(AUDIO_FILE):
    print("[+] Mengunduh file lagu...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(AUDIO_URL, headers=headers, stream=True)
        res.raise_for_status()
        with open(AUDIO_FILE, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        print("[+] Download lagu selesai!")
    except Exception as e:
        print(f"[-] Gagal download otomatis: {e}")

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

PORT = get_free_port()
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Aesthetic Lyrics</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            /* Foto jernih 100% tanpa bayangan hitam */
            background: #000 url('{BACKGROUND_URL}') no-repeat center center fixed;
            background-size: cover;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 35px 20px;
            font-family: 'Inter', sans-serif;
            color: #fff;
        }}

        .top-info {{
            z-index: 5;
            text-align: center;
            margin-top: 10px;
            opacity: 0;
            transition: opacity 1s ease;
        }}
        .top-info.show {{
            opacity: 1;
        }}
        .top-info h2 {{
            font-size: 0.85rem;
            letter-spacing: 1px;
            font-weight: 600;
            opacity: 0.95;
            text-shadow: 0 2px 10px rgba(0,0,0,0.9);
        }}

        #lyric-container {{
            position: absolute;
            top: 36%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 85vw;
            text-align: center;
            pointer-events: none;
            z-index: 5;
        }}

        #lyric-text {{
            font-size: 1.55rem;
            font-weight: 700;
            color: #ffffff;
            text-shadow: 0 3px 15px rgba(0,0,0,0.95), 0 0 8px rgba(0,0,0,0.9);
            white-space: normal;
            word-wrap: break-word;
            line-height: 1.35;
            transition: all 0.3s ease;
            opacity: 0;
            transform: translateY(8px);
        }}

        #lyric-text.active {{
            opacity: 1;
            transform: translateY(0);
        }}

        /* Kotak kata-kata ultra transparan agar foto dibelakangnya keliatan 90%+ jernih */
        .quote-card {{
            position: absolute;
            bottom: 12%;
            left: 50%;
            transform: translateX(-50%);
            z-index: 5;
            width: 88vw;
            max-width: 390px;
            background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(2px);
            -webkit-backdrop-filter: blur(2px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            padding: 16px 20px;
            text-align: center;
            font-size: 0.78rem;
            line-height: 1.45;
            color: #ffffff;
            font-weight: 400;
            text-shadow: 0 2px 8px rgba(0,0,0,0.95);
            opacity: 0;
            transition: opacity 1s ease;
            pointer-events: none;
        }}

        .quote-card.show {{
            opacity: 1;
        }}

        #start-btn {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10;
            padding: 14px 28px;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            color: #fff;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 30px;
            cursor: pointer;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
            font-family: 'Inter', sans-serif;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{
                transform: translate(-50%, -50%) scale(1);
                box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4);
            }}
            50% {{
                transform: translate(-50%, -50%) scale(1.06);
                box-shadow: 0 0 20px 8px rgba(255, 255, 255, 0.15);
            }}
            100% {{
                transform: translate(-50%, -50%) scale(1);
                box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
            }}
        }}

        #start-btn:active {{
            animation: none;
            transform: translate(-50%, -50%) scale(0.95);
        }}
    </style>
</head>
<body>

    <div class="top-info" id="title-header">
        <h2>Merry Christmas, I Miss You</h2>
    </div>

    <button id="start-btn">Coba Pencet ✨</button>
    
    <div id="lyric-container">
        <div id="lyric-text"></div>
    </div>

    <div class="quote-card" id="quote">
        "Kalau ada lagu yang mampu menyaingi About You, mungkin itu cuma Merry Christmas, I Miss You. Sama-sama punya cara sederhana untuk mengingatkan kita pada seseorang yang pernah begitu berarti. Bukan karena ingin kembali, hanya rasa rindu yang sesekali muncul ketika mendengar lagu tertentu. Mungkin semuanya sudah berubah, tapi beberapa kenangan memang tetap punya tempatnya sendiri."
    </div>

    <audio id="audio" src="song.mp3"></audio>

    <script>
        const lyrics = {str(LYRICS_DATA)};
        const lyricText = document.getElementById('lyric-text');
        const quote = document.getElementById('quote');
        const titleHeader = document.getElementById('title-header');
        const audio = document.getElementById('audio');
        const startBtn = document.getElementById('start-btn');

        startBtn.addEventListener('click', () => {{
            startBtn.style.display = 'none';
            titleHeader.classList.add('show');
            quote.classList.add('show');
            audio.play();

            audio.ontimeupdate = () => {{
                const currentTime = audio.currentTime;

                const current = lyrics.filter(l => l.time <= currentTime).pop();
                if (current && current.text.trim() !== "") {{
                    if (lyricText.innerText !== current.text) {{
                        lyricText.classList.remove('active');
                        setTimeout(() => {{
                            lyricText.innerText = current.text;
                            lyricText.classList.add('active');
                        }}, 100);
                    }}
                }} else {{
                    lyricText.classList.remove('active');
                    lyricText.innerText = "";
                }}
            }};
        }});
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

class QuickHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

print(f"\n[+] Server Active: {URL}\n")

try:
    webbrowser.open(URL)
except Exception:
    pass

with socketserver.TCPServer(("", PORT), QuickHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Dihentikan.")
