from flask import Flask, request, jsonify, render_template_string, Response, redirect
import json
import requests
from datetime import datetime

app = Flask(__name__)

AUDIO_URL = "https://files.catbox.moe/1odhi3.mp3"
BACKGROUND_URL = "https://raw.githubusercontent.com/Nex-Core/Uploader-Media/main/gambar-only/1786076602402_y9uydave.jpg"

ADMIN_USER = "admin"
ADMIN_PASS = "admin123#"

secret_messages = []

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

HTML_MAIN = f"""<!DOCTYPE html>
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

        .toast-notification {{
            position: fixed;
            top: -70px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.35);
            padding: 12px 22px;
            border-radius: 30px;
            font-size: 0.78rem;
            font-weight: 500;
            color: #ffffff;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 30;
            transition: top 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            display: flex;
            align-items: center;
            gap: 8px;
            pointer-events: none;
            text-shadow: 0 1px 4px rgba(0,0,0,0.8);
        }}
        .toast-notification.show {{ top: 25px; }}

        .top-info {{
            z-index: 5;
            text-align: center;
            margin-top: 10px;
            opacity: 0;
            transition: opacity 1s ease;
        }}
        .top-info.show {{ opacity: 1; }}
        .top-info h2 {{
            font-size: 0.85rem;
            letter-spacing: 1px;
            font-weight: 600;
            opacity: 0.95;
            text-shadow: 0 2px 10px rgba(0,0,0,0.9);
        }}

        #lyric-container {{
            position: absolute;
            top: 34%;
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
        #lyric-text.active {{ opacity: 1; transform: translateY(0); }}

        .bottom-container {{
            position: absolute;
            bottom: 8%;
            left: 50%;
            transform: translateX(-50%);
            z-index: 5;
            width: 88vw;
            max-width: 390px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            align-items: center;
            opacity: 0;
            transition: opacity 1s ease;
        }}
        .bottom-container.show {{ opacity: 1; }}

        .quote-card {{
            width: 100%;
            background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(2px);
            -webkit-backdrop-filter: blur(2px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            padding: 14px 18px;
            text-align: center;
            font-size: 0.76rem;
            line-height: 1.45;
            color: #ffffff;
            font-weight: 400;
            text-shadow: 0 2px 8px rgba(0,0,0,0.95);
        }}

        .msg-btn {{
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: #fff;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.72rem;
            cursor: pointer;
            backdrop-filter: blur(6px);
            transition: all 0.2s;
        }}

        .modal-overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7);
            z-index: 20;
            display: none;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(6px);
        }}
        .modal-box {{
            background: rgba(20, 20, 20, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 20px;
            width: 85vw;
            max-width: 340px;
            text-align: left;
        }}
        .modal-box h3 {{ font-size: 0.9rem; margin-bottom: 4px; font-weight: 600; text-align: center; }}
        .modal-box p {{ font-size: 0.7rem; opacity: 0.7; margin-bottom: 12px; text-align: center; }}
        
        .form-group {{ margin-bottom: 10px; }}
        .form-group label {{ display: block; font-size: 0.68rem; opacity: 0.8; margin-bottom: 4px; }}
        .form-group input, .form-group textarea {{
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 8px 10px;
            color: #fff;
            font-size: 0.78rem;
            outline: none;
            font-family: inherit;
        }}
        .form-group textarea {{ height: 70px; resize: none; }}

        .modal-actions {{ display: flex; gap: 10px; margin-top: 10px; }}
        .modal-actions button {{
            flex: 1; padding: 8px; border-radius: 8px; border: none; font-size: 0.75rem; font-weight: 600; cursor: pointer;
        }}
        .btn-cancel {{ background: rgba(255,255,255,0.15); color: #fff; }}
        .btn-send {{ background: #fff; color: #000; }}

        #start-btn {{
            position: absolute;
            top: 50%; left: 50%;
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
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }}
            50% {{ transform: translate(-50%, -50%) scale(1.06); box-shadow: 0 0 20px 8px rgba(255, 255, 255, 0.15); }}
            100% {{ transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }}
        }}
    </style>
</head>
<body>

    <div class="toast-notification" id="toast">
        ✨ Pesan rahasiamu berhasil terkirim.
    </div>

    <div class="top-info" id="title-header">
        <h2>Merry Christmas, I Miss You</h2>
    </div>

    <button id="start-btn">Coba Pencet ✨</button>
    
    <div id="lyric-container">
        <div id="lyric-text"></div>
    </div>

    <div class="bottom-container" id="bottom-box">
        <div class="quote-card">
            "Kalau ada lagu yang mampu menyaingi About You, mungkin itu cuma Merry Christmas, I Miss You. Sama-sama punya cara sederhana untuk mengingatkan kita pada seseorang yang pernah begitu berarti. Bukan karena ingin kembali, hanya rasa rindu yang sesekali muncul ketika mendengar lagu tertentu. Mungkin semuanya sudah berubah, tapi beberapa kenangan memang tetap punya tempatnya sendiri."
        </div>
        <button class="msg-btn" id="open-modal-btn">💬 Ada pesan yang mau disampaikan?</button>
    </div>

    <div class="modal-overlay" id="modal">
        <div class="modal-box">
            <h3>Kirim Pesan</h3>
            <p>Sampaikan hal yang ingin kamu katakan.</p>
            <div class="form-group">
                <label>Nama (Opsional)</label>
                <input type="text" id="name-input" placeholder="Anonim (Opsional)">
            </div>
            <div class="form-group">
                <label>Isi Pesan</label>
                <textarea id="msg-input" placeholder="Tulis pesan kamu di sini..."></textarea>
            </div>
            <div class="modal-actions">
                <button class="btn-cancel" id="close-modal-btn">Batal</button>
                <button class="btn-send" id="send-msg-btn">Kirim Pesan</button>
            </div>
        </div>
    </div>

    <audio id="audio" src="/song.mp3"></audio>

    <script>
        const lyrics = {json.dumps(LYRICS_DATA)};
        const lyricText = document.getElementById('lyric-text');
        const bottomBox = document.getElementById('bottom-box');
        const titleHeader = document.getElementById('title-header');
        const toast = document.getElementById('toast');
        const audio = document.getElementById('audio');
        const startBtn = document.getElementById('start-btn');

        const modal = document.getElementById('modal');
        const openModalBtn = document.getElementById('open-modal-btn');
        const closeModalBtn = document.getElementById('close-modal-btn');
        const sendMsgBtn = document.getElementById('send-msg-btn');
        const nameInput = document.getElementById('name-input');
        const msgInput = document.getElementById('msg-input');

        startBtn.addEventListener('click', () => {{
            startBtn.style.display = 'none';
            titleHeader.classList.add('show');
            bottomBox.classList.add('show');
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

        openModalBtn.addEventListener('click', () => modal.style.display = 'flex');
        closeModalBtn.addEventListener('click', () => modal.style.display = 'none');

        function showToast() {{
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
        }}

        sendMsgBtn.addEventListener('click', async () => {{
            const msg = msgInput.value.trim();
            const senderName = nameInput.value.trim() || 'Anonim';
            if(!msg) return;

            await fetch('/api/send-message', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ name: senderName, message: msg }})
            }});

            msgInput.value = '';
            nameInput.value = '';
            modal.style.display = 'none';
            showToast();
        }});
    </script>
</body>
</html>
"""

HTML_LOGIN = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #090d16; color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
            height: 100vh; display: flex; justify-content: center; align-items: center;
        }
        .login-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            padding: 35px 30px; border-radius: 20px;
            width: 90%; max-width: 380px; border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        }
        h2 { text-align: center; margin-bottom: 8px; font-size: 1.35rem; font-weight: 700; }
        p.sub { text-align: center; font-size: 0.75rem; color: #94a3b8; margin-bottom: 25px; }
        .input-group { margin-bottom: 18px; }
        label { display: block; font-size: 0.78rem; color: #cbd5e1; margin-bottom: 6px; font-weight: 500; }
        input {
            width: 100%; padding: 12px 14px; border-radius: 10px;
            border: 1px solid #334155; background: #0f172a; color: #fff; outline: none;
            font-family: inherit; font-size: 0.85rem; transition: all 0.2s;
        }
        input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2); }
        button {
            width: 100%; padding: 12px; background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white; border: none; border-radius: 10px; font-weight: 600; font-size: 0.88rem;
            cursor: pointer; margin-top: 10px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-1px); }
        .error { color: #f87171; font-size: 0.8rem; text-align: center; margin-top: 12px; font-weight: 500; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>🔒 Admin Portal</h2>
        <p class="sub">Masukan akses untuk melihat pesan masuk</p>
        <form method="POST" action="/admin">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="username" required autocomplete="off" placeholder="Username">
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" required placeholder="••••••••">
            </div>
            <button type="submit">Masuk Dashboard</button>
            {{ERROR_MSG}}
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_MAIN)

@app.route("/song.mp3")
def song():
    res = requests.get(AUDIO_URL, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
    return Response(res.content, mimetype="audio/mpeg")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USER and password == ADMIN_PASS:
            msg_rows = ""
            for msg in reversed(secret_messages):
                badge_style = "background: rgba(96, 165, 250, 0.15); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3);"
                if msg['sender'].lower() == 'anonim':
                    badge_style = "background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3);"
                
                msg_rows += f"""<tr>
                    <td style='white-space: nowrap; color: #94a3b8;'>{msg['time']}</td>
                    <td><span style='padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-block; {badge_style}'>{msg['sender']}</span></td>
                    <td style='line-height: 1.5; color: #f1f5f9; font-weight: 500;'>{msg['text']}</td>
                </tr>"""

            if not msg_rows:
                msg_rows = "<tr><td colspan='3' style='text-align:center; padding: 30px; color: #64748b;'>Belum ada pesan masuk saat ini.</td></tr>"

            admin_dashboard = f"""<!DOCTYPE html>
            <html lang="id">
            <head>
                <meta charset="UTF-8">
                <title>Admin Dashboard</title>
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{
                        background: #090d16; color: #f8fafc;
                        font-family: 'Plus Jakarta Sans', sans-serif;
                        padding: 30px 20px; min-height: 100vh;
                    }}
                    .container {{ max-width: 900px; margin: 0 auto; }}
                    .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }}
                    .header h1 {{ font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
                    
                    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }}
                    .stat-card {{
                        background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08);
                        padding: 18px; border-radius: 14px; backdrop-filter: blur(10px);
                    }}
                    .stat-card p {{ font-size: 0.75rem; color: #94a3b8; font-weight: 500; }}
                    .stat-card h3 {{ font-size: 1.4rem; font-weight: 700; margin-top: 4px; color: #38bdf8; }}

                    .table-card {{
                        background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 16px; overflow: hidden; backdrop-filter: blur(10px);
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th {{ background: rgba(15, 23, 42, 0.8); color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; padding: 14px 18px; text-align: left; font-weight: 600; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }}
                    td {{ padding: 16px 18px; font-size: 0.82rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
                    tr:hover {{ background: rgba(255, 255, 255, 0.02); }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⚙️ Inbox Messages</h1>
                    </div>

                    <div class="stats">
                        <div class="stat-card">
                            <p>Total Pesan Masuk</p>
                            <h3>{len(secret_messages)} Pesan</h3>
                        </div>
                    </div>

                    <div class="table-card">
                        <table>
                            <thead>
                                <tr>
                                    <th style="width: 170px;">Waktu Kirim</th>
                                    <th style="width: 140px;">Pengirim</th>
                                    <th>Isi Pesan</th>
                                </tr>
                            </thead>
                            <tbody>{msg_rows}</tbody>
                        </table>
                    </div>
                </div>
            </body>
            </html>"""
            return render_template_string(admin_dashboard)
        else:
            err = "<div class='error'>Username atau Password salah!</div>"
            return render_template_string(HTML_LOGIN.replace("{{ERROR_MSG}}", err))

    return render_template_string(HTML_LOGIN.replace("{{ERROR_MSG}}", ""))

@app.route("/api/send-message", methods=["POST"])
def send_message():
    data = request.get_json(silent=True) or {}
    secret_messages.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": data.get("name", "Anonim"),
        "text": data.get("message", "")
    })
    return jsonify({"status": "success"})

app = app
