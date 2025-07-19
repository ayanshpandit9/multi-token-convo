import requests
import time
import os
import platform
import urllib.request
import uuid
from getmac import get_mac_address  # For device-specific key
import json

# Colors
BOLD    = '\033[1m'
CYAN    = '\033[96m'
GREEN   = '\033[92m'
RED     = '\033[91m'
YELLOW  = '\033[93m'
BLUE    = '\033[94m'
MAGENTA = '\033[95m'
RESET   = '\033[0m'

# Banner (unchanged)
logo = f"""{CYAN}
      ___           ___           ___           ___           ___           ___     
     /\\  \\         |\\__\\         /\\  \\         /\\__\\         /\\  \\         /\\__\\    
    /::\\  \\        |:|  |       /::\\  \\       /::|  |       /::\\  \\       /:/  /    
   /:/\\:\\  \\       |:|  |      /:/\\:\\  \\     /:|:|  |      /:/\\ \\  \\     /:/__/     
  /::\\~\\:\\  \\      |:|__|__   /::\\~\\:\\  \\   /:/|:|  |__   _\\:\\~\\ \\  \\   /::\\  \\ ___ 
 /:/\\:\\ \\:\\__\\     /::::\\__\\ /:/\\:\\ \\:\\__\\ /:/ |:| /\\__\\ /\\ \\:\\ \\ \\__\\ /:/\\:\\  /\\__\\
 \\/__\\:\\/:/  /    /:/~~/~    \\/__\\:\\/:/  / \\/__|:|/:/  / \\:\\ \\:\\ \\/__/ \\/__\\:\\/:/  /
      \\::/  /    /:/  /           \\::/  /      |:/:/  /   \\:\\ \\:\\__\\        \\::/  / 
      /:/  /     \\/__/            /:/  /       |::/  /     \\:\\/:/  /        /:/  /  
     /:/  /                      /:/  /        /:/  /       \\::/  /        /:/  /   
     \\/__/                       \\/__/         \\/__/         \\/__/         \\/__/    

{MAGENTA}╔═════════════════════ Messenger Tool ═════════════════════╗
║             V9MPIR3 OWN3R 9Y9NSH H3R3 🩵              ║
╚════════════════════════════════════════════════════════╝

\033[1;92m.Author     :  𝐀𝐘𝟗𝐍𝐒𝐇 𝐇𝟑𝐑𝟃
\033[1;31m.Brother    : 𝐀𝐋𝐎𝐍𝐄 𝐒𝐓𝟗𝐍𝐃 𝐀𝐘𝟗𝐍𝐒𝐇
\033[1;32m.Facebook   : 𝐀𝐘𝟗𝐍𝐒𝐇
\033[1;34m.Tool Name  : 𝐌𝟑𝐒𝐒𝟗𝐍𝐆𝟑𝐑 𝐓𝐎𝐎𝐋
\033[1;36m.Type type  : 𝐅𝐑𝟑𝟑 𝐁𝐘 𝐀𝐘𝟗𝐍𝐒𝐇 𝐓𝐎𝐎𝐋
────────────────────────────────────────────────────────────
𖣘︎𖣘︎𖣘︎𖣘︎𖣘︎︻╦デ╤━╼【★ 𝐀𝐘𝟗𝐍𝐒𝐇 𝐓𝐎𝐎𝐋 𝐎𝐖𝐍𝐀𝐑 ★】╾━╤デ╦︻𖣘︎𖣘︎𖣘︎𖣘︎𖣘︎
────────────────────────────────────────────────────────────
\033[1;32m【𝐅𝟃𝟃𝐋 𝐓𝐇𝟃 𝐏𝟎𝐖𝟃𝐑 𝐎𝐅 𝐕𝟗𝐌𝐏𝐈𝐑𝟃 𝐑𝐔𝐋𝟃𝐗 𝐎𝐖𝐍𝟃𝐑 𝐀𝐘𝟗𝐍𝐒𝐇】
\033[1;36m       𖣘︎𖣘︎𖣘︎【 𝐀𝐘𝟗𝐍𝐒𝐇 𝐈𝐍𝐒𝐈𝐃𝐄 】𖣘︎𖣘︎𖣘︎
{RESET}
"""

def cls():
    os.system('clear' if platform.system() != 'Windows' else 'cls')

def generate_device_key():
    # Generate a device-specific key using MAC address and hostname
    mac = get_mac_address() or "unknown_mac"
    hostname = platform.node() or "unknown_host"
    unique_string = f"{mac}:{hostname}"
    key = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_string))  # Deterministic UUID
    return key

def save_device_key(key):
    # Save key to a local file
    with open("device_key.txt", "w") as f:
        f.write(key)

def load_device_key():
    # Load key from file if exists, else generate and save
    if os.path.exists("device_key.txt"):
        with open("device_key.txt", "r") as f:
            return f.read().strip()
    else:
        key = generate_device_key()
        save_device_key(key)
        return key

def check_approval(key):
    # Check if key is in approved_keys.txt
    try:
        with open("approved_keys.txt", "r") as f:
            approved_keys = [line.strip() for line in f.readlines()]
        return key in approved_keys
    except FileNotFoundError:
        return False

def get_access_tokens(token_file):
    with open(token_file, 'r') as file:
        return [token.strip() for token in file.readlines() if token.strip()]

def is_connected():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False

def send_messages(convo_id, tokens, messages, custom_name, speed):
    headers = {
        'Content-type': 'application/json',
    }
    message_count = 0  # Initialize message counter
    symbols = ['|', '/', '-', '\\']  # Symbols for animation

    while True:
        if is_connected():
            try:
                for i, message in enumerate(messages):
                    token = tokens[i % len(tokens)]
                    full_message = f"{custom_name} {message.strip()}"
                    url = f"https://graph.facebook.com/v17.0/t_{convo_id}"
                    response = requests.post(url, json={"access_token": token, "message": full_message}, headers=headers)

                    current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                    message_count += 1  # Increment counter

                    if response.ok:
                        # Dynamic width calculation
                        max_width = max(len(f"{custom_name}: {message.strip()}"), len(f"Time: {current_time}")) + 10
                        border = "─" * max_width
                        
                        # Animation effect
                        for j in range(4):
                            print(f"{GREEN}┌───[⚡TERMINAL:AY9NSH#MSG{message_count}{symbols[j]}]───╴")
                            print(f"│ > {custom_name}: {message.strip().ljust(max_width-6)} > │")
                            print(f"│ > Time: {current_time.ljust(max_width-6)} > │")
                            print(f"└{border}┘{RESET}")
                            time.sleep(0.1)
                            print("\033[4A\033[K", end="")  # Move cursor up and clear lines
                        
                        # Final static box
                        print(f"{GREEN}┌───[⚡TERMINAL:AY9NSH#MSG{message_count}]───╴")
                        print(f"│ > {custom_name}: {message.strip().ljust(max_width-6)} > │")
                        print(f"│ > Time: {current_time.ljust(max_width-6)} > │")
                        print(f"└{border}┘{RESET}")
                    else:
                        print(f"{RED}[FAILED] TOKEN SAHI DAAL LE BHAYA | Time: {current_time}{RESET}")
                    time.sleep(speed)

                print(f"{YELLOW}[+] Loop #{message_count//len(messages)} completed. Restarting...{RESET}")
            except Exception as e:
                print(f"{RED}[!] Exception: {e}{RESET}")
        else:
            print(f"{BLUE}[!] INTERNET BAND KAR DIYA TUNE...{RESET}")
            while not is_connected():
                time.sleep(5)
            print(f"{GREEN}[+] OKAY CONNECT HOGYA NOW CHECK...{RESET}")

def main():
    cls()
    print(logo)

    # Generate or load device key
    device_key = load_device_key()
    print(f"{YELLOW}[!] Your Device Key: {device_key}{RESET}")
    print(f"{RED}[!] Send this key to AY9NSH for approval!{RESET}")

    # Check if key is approved
    if not check_approval(device_key):
        print(f"{RED}[!] Key not approved. Contact AY9NSH with your key: {device_key}{RESET}")
        return  # Exit if not approved

    print(f"{GREEN}[+] Key approved! Starting Messenger Tool...{RESET}")

    token_file = input(BOLD + CYAN + "FATAFAT TOKEN DALO => " + RESET).strip()
    convo_id = input(BOLD + CYAN + "THREAD ID YA GC ID DAL=> " + RESET).strip()
    messages_file = input(BOLD + CYAN + "MESSAGE DAAL JO JO SEND KAREGA => " + RESET).strip()
    custom_name = input(BOLD + CYAN + "HATER NAME => " + RESET).strip()
    speed = int(input(BOLD + CYAN + "SPEED (sec) => " + RESET).strip())

    tokens = get_access_tokens(token_file)
    with open(messages_file, 'r') as f:
        messages = f.readlines()

    send_messages(convo_id, tokens, messages, custom_name, speed)

if __name__ == "__main__":
    main()
