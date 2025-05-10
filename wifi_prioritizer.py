import time
from rede_wifi import RedeWifi
from wifi_manager import WifiManager

class WifiPrioritizer:
    def __init__(self, rede_a: RedeWifi, rede_b: RedeWifi, wifi_manager: WifiManager):
        self.rede_a = rede_a
        self.rede_b = rede_b
        self.wifi = wifi_manager
        self.sinal_a_anterior = None
        self.sinal_b_anterior = None


    def prioridade(self):
        redes_disponiveis = self.wifi.escanear_redes()
        ssid_atual = self.wifi.get_rede_conectada()

        sinal_a = self.wifi.get_nivel_sinal(self.rede_a.ssid, redes_disponiveis)
        sinal_b = self.wifi.get_nivel_sinal(self.rede_b.ssid, redes_disponiveis)

        print(f"[{time.strftime('%H:%M:%S')}] Sinal de {self.rede_a.ssid}: {sinal_a or 'não encontrada'}")
        print(f"[{time.strftime('%H:%M:%S')}] Sinal de {self.rede_b.ssid}: {sinal_b or 'não encontrada'}")

        if sinal_a is not None and sinal_a >= 4:
            if ssid_atual != self.rede_a.ssid:
                print(f"🔄 Reconectando à {self.rede_a.ssid}")
                self.wifi.conectar(self.rede_a)
            else:
                print(f"✅ Já conectado à {self.rede_a.ssid}")
        elif sinal_b is not None and sinal_b >= 4 and (sinal_a is None or sinal_a < 4):
            if ssid_atual != self.rede_b.ssid:
                print(f"🔄 Reconectando à {self.rede_b.ssid}")
                self.wifi.conectar(self.rede_b)
            else:
                print(f"✅ Já conectado à {self.rede_b.ssid}")
        else:
            print("Nenhuma rede atende aos critérios.")