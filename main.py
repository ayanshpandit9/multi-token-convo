from flask import Flask
import threading
import time
from instagrapi import Client

app = Flask(__name__)

def insta_bot():
    cl = Client()

    username = "hyp319_2027899"
    password = "pandit@ak90"
    target_username = "pandit_292"

    messages = [
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "khushi_gawar_h3re"
        "#H9R_H9R_M9H9D3V_#V9MPIR3_RUL3X_H3R3: O:) _____________ <3 Kitna Wakif Thi Woh meri Kamjori Se,          Wo Ro Deti Thi Aur Main Har Jata Tha.     =) )   ___________ <3    ~{{ 3:) (^^^) O:) #khushi_gawar_h3re 3:)  (y)   <3 }}~ <3",
        "yy"
    ]

    delay_seconds = 6  # Delay between messages

    try:
        cl.login(username, password)
        print(f"✅ Logged in as @{username}")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return

    try:
        target_user_id = cl.user_id_from_username(target_username)
        print(f"🎯 Target user ID found for @{target_username}")
    except Exception as e:
        print(f"❌ Could not get target user ID: {e}")
        return

    last_sent_time = 0
    message_index = 0

    while True:
        now = time.time()
        if now - last_sent_time >= delay_seconds:
            try:
                msg = messages[message_index]
                cl.direct_send(msg, [target_user_id])
                print(f"✅ Sent message {message_index+1} to @{target_username}")
                message_index = (message_index + 1) % len(messages)
                last_sent_time = now
            except Exception as e:
                print(f"❌ Error sending message: {e}")
        time.sleep(5)

@app.route('/')
def index():
    return "✅ Instagram Bot with 2 Messages Running on Zeabur!"

if __name__ == '__main__':
    threading.Thread(target=insta_bot).start()
    app.run(host="0.0.0.0", port=8080)
