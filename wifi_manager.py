import time
import pywifi
from pywifi import const
from rede_wifi import RedeWifi
import subprocess


class WifiManager:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]

    def escanear_redes(self):
        self.iface.scan()
        time.sleep(3)
        return self.iface.scan_results()
    
    def get_rede_conectada(self):
        try:
            resultado = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8')
            for i in resultado.splitlines():
                if "SSID" in i and "BSSID" not in i:
                    return i.split(":", 1)[1].strip()
        except Exception as e:
            print(f"Erro ao obter rede conectada: {e}")
        return None

    def get_nivel_sinal(self, ssid: str, redes):
        for rede in redes:
            if rede.ssid == ssid:
                return self.rssi_para_nivel(rede.signal)
        return None

    def rssi_para_nivel(self, rssi: int):
        if rssi >= -50: return 5
        elif rssi >= -60: return 4
        elif rssi >= -70: return 3
        elif rssi >= -80: return 2
        elif rssi >= -90: return 1
        else: return 0

    def conectar(self, rede: RedeWifi):
        print(f"Tentando conectar à {rede.ssid}...")

        profile = pywifi.Profile()
        profile.ssid = rede.ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = rede.senha

        self.iface.remove_all_network_profiles()
        tmp_profile = self.iface.add_network_profile(profile)

        self.iface.disconnect()
        time.sleep(1)
        self.iface.connect(tmp_profile)
        time.sleep(5)

        if self.iface.status() == const.IFACE_CONNECTED:
            print(f"✅ Conectado à {rede.ssid}")
        else:
            print(f"❌ Falha ao conectar à {rede.ssid}")