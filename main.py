import os
import sys
import threading
import time
from dotenv import load_dotenv
from PIL import Image
import pystray
from rede_wifi import RedeWifi
from wifi_manager import WifiManager
from wifi_prioritizer import WifiPrioritizer

load_dotenv()

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def verificar_redes_continuamente(prioritizer: WifiPrioritizer, intervalo=30):
    while True:
        prioritizer.prioridade()
        time.sleep(intervalo)

def main():
    rede_a = RedeWifi(os.getenv("REDE_A_SSID"), os.getenv("REDE_A_SENHA"))
    rede_b = RedeWifi(os.getenv("REDE_B_SSID"), os.getenv("REDE_B_SENHA"))

    wifi_manager = WifiManager()
    prioritizer = WifiPrioritizer(rede_a, rede_b, wifi_manager)

    t = threading.Thread(target=verificar_redes_continuamente, args=(prioritizer,), daemon=True)
    t.start()

    icon_path = get_resource_path("icon/icon.png")
    icon_image = Image.open(icon_path)
    icon = pystray.Icon("WifiPrioritizer")

    def sair(icon, item):
        icon.stop()

    icon.menu = pystray.Menu(pystray.MenuItem("Sair", sair))
    icon.title = "WiFi Prioritizer"
    icon.icon = icon_image
    icon.run()

if __name__ == "__main__":
    main()
