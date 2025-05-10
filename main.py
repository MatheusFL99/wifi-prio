import os
from dotenv import load_dotenv
from rede_wifi import RedeWifi
from wifi_manager import WifiManager
from wifi_prioritizer import WifiPrioritizer

load_dotenv()

def main():
    rede_a = RedeWifi(os.getenv("REDE_A_SSID"), os.getenv("REDE_A_SENHA"))
    rede_b = RedeWifi(os.getenv("REDE_B_SSID"), os.getenv("REDE_B_SENHA"))

    wifi_manager = WifiManager()
    prioritizer = WifiPrioritizer(rede_a, rede_b, wifi_manager)

    prioritizer.prioridade()

if __name__ == "__main__":
    main()