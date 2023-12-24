import tls_client
import uuid
import ctypes
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from datetime import datetime
from threading import Lock
from traceback import print_exc
from random import choice
import schedule
import time

lock = Lock()
genned = 0

class Logger:
    @staticmethod
    def Sprint(tag: str, content: str, color):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        with lock:
            print(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)

    @staticmethod
    def Ask(tag: str, content: str, color):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        return input(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)

def update_title():
    ctypes.windll.kernel32.SetConsoleTitleW(f" PGEN | STATUS : {genned}")

class O:
    def __init__(self, proxy) -> None:
        self.session = tls_client.Session(client_identifier="chrome112")
        self.proxy = proxy
        self.gen()

    def p(self, *args, **kwargs):
        while True:
            try:
                return self.session.post(*args, **kwargs)
            except Exception as e:
                # print_exc()
                continue

    def gen(self):
        global genned
        for _ in range(99999999999999999999999999999999999999999999999999999999999999999999999999999):  # Code limit
            try:
                response = self.p('https://api.discord.gx.games/v1/direct-fulfillment', json={
                    'partnerUserId': str(uuid.uuid4()),
                }, proxy=self.proxy)
                if response.status_code == 429:
                    Logger.Sprint("RATELIMIT", "You are being rate limited!", Fore.RED)
                    return
                ptoken = response.json()['token']
                link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{ptoken}"
                Logger.Sprint(">", f"Successfully Generated : {link}", Fore.LIGHTBLUE_EX)
               # Logger.Sprint("+", f"Successfully Generated : {link}", Fore.GREEN) -- previous
                genned += 1
                with lock:
                    open("codes.txt", 'a').write(f"{link}\n")
                    update_title()
            except:
                print_exc()

def gnr():
    try:
        proxy = "http://" + choice(open("proxies.txt").read().splitlines())
    except:
        proxy = None
    while True:
        try:
            O(proxy)
        except:
            print_exc()

def job():
    art = """
 ____  _______     _______ ____  ___ _______   ______    ____  ____   ___  __  __  ___   ____ _____ _   _  
/ ___|| ____\ \   / / ____|  _ \|_ _|_   _\ \ / / ___|  |  _ \|  _ \ / _ \|  \/  |/ _ \ / ___| ____| \ | | 
\___ \|  _|  \ \ / /|  _| | |_) || |  | |  \ V /\___ \  | |_) | |_) | | | | |\/| | | | | |  _|  _| |  \| | 
 ___) | |___  \ V / | |___|  _ < | |  | |   | |  ___) | |  __/|  _ <| |_| | |  | | |_| | |_| | |___| |\  | 
|____/|_____|  \_/  |_____|_| \_\___| |_|   |_| |____/  |_|   |_| \_\\___/|_|  |_|\___/ \____|_____|_| \_| 
    """
    developer_info = "GITHUB : https://github.com/S3verity/Discord-Promo-Generator"

    print(Fore.LIGHTBLUE_EX + art + Fore.LIGHTBLUE_EX)
    print(developer_info, Fore.LIGHTBLUE_EX)

    t = int(Logger.Ask(">", "Thread Count : ", Fore.LIGHTBLUE_EX))
    with ThreadPoolExecutor(max_workers=t + 1) as exc:
        for i in range(t):
            exc.submit(gnr)
            
if __name__ == "__main__":
    init()
    schedule.every(0).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(0)
