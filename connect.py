# connect.py
import json
import socket
import threading
import time

UDP_IP = "0.0.0.0"
PORT_RPI = 5005          # Odczyty z Pico i nasłuch na telefonie
PORT_PICO = 5006         # Sterowanie odbierane przez Pico
PORT_TELEFON = 5005      # Port odbioru danych w aplikacji Flutter
PORT_STEROWANIA = 5006   # Port odbioru sterowania od aplikacji Flutter
MAX_PAKIET = 1024
ODSTEP_WYKRYWANIA = 2

_pico_ip = None
_telefon_addr = None
_oczekujace_sterowanie = None
_czy_nasluchuje = False
_blokada_stanu = threading.Lock()

_dane_z_pico = {
    "Day_State": 0,
    "Tryb": 0,
    "temperatura": 0.0,
    "wilgotnosc": 0.0,
    "wilgotnosc_gleby": 0,
    "poziom_swiatla": 0,
    "stan_wody": 0
}

_sock_odbior = None
_sock_sterowanie = None


def _odbieraj_odczyty():
    """Odbiera pomiary z Pico i przekazuje je do ostatniego telefonu."""
    global _pico_ip, _oczekujace_sterowanie
    print(f"[CONNECT] Nasłuchiwanie odczytów UDP na porcie {PORT_RPI}...")

    while True:
        try:
            data, addr = _sock_odbior.recvfrom(MAX_PAKIET)
        except OSError as error:
            print(f"[CONNECT] Błąd odbioru odczytów: {error}")
            return

        try:
            odebrane = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            print("[CONNECT] Błąd: Uszkodzony pakiet JSON z Pico")
            continue

        if not isinstance(odebrane, dict):
            print("[CONNECT] Błąd: Odczyty z Pico muszą być obiektem JSON")
            continue

        with _blokada_stanu:
            _pico_ip = addr[0]
            for klucz in _dane_z_pico:
                if klucz in odebrane:
                    _dane_z_pico[klucz] = odebrane[klucz]
            telefon_addr = _telefon_addr
            oczekujace_sterowanie = _oczekujace_sterowanie
            if oczekujace_sterowanie is not None:
                _oczekujace_sterowanie = None

        if oczekujace_sterowanie is not None:
            try:
                _sock_sterowanie.sendto(oczekujace_sterowanie, (addr[0], PORT_PICO))
                print(f"[CONNECT] Przekazano oczekujące sterowanie do Pico ({addr[0]}).")
            except OSError as error:
                print(f"[CONNECT] Błąd przekazywania oczekującego sterowania do Pico: {error}")

        if telefon_addr is not None:
            try:
                _sock_odbior.sendto(data, (telefon_addr[0], PORT_TELEFON))
            except OSError as error:
                print(f"[CONNECT] Błąd przekazywania odczytów do telefonu: {error}")


def _poprawny_pakiet_sterowania(pakiet):
    if not isinstance(pakiet, dict):
        return False

    zakresy = {
        "stan_1": (0, 1),
        "stan_2": (0, 1),
        "wartosc_1": (0, 255),
        "wartosc_2": (0, 255)
    }
    for klucz, (minimum, maksimum) in zakresy.items():
        wartosc = pakiet.get(klucz)
        if type(wartosc) is not int or not minimum <= wartosc <= maksimum:
            return False
    return True


def _odbieraj_sterowanie():
    """Odbiera polecenia telefonu i przekazuje je do Pico."""
    global _telefon_addr, _oczekujace_sterowanie
    print(f"[CONNECT] Nasłuchiwanie sterowania UDP na porcie {PORT_STEROWANIA}...")

    while True:
        try:
            data, addr = _sock_sterowanie.recvfrom(MAX_PAKIET)
        except OSError as error:
            print(f"[CONNECT] Błąd odbioru sterowania: {error}")
            return

        try:
            pakiet = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            print("[CONNECT] Błąd: Uszkodzony pakiet sterowania JSON")
            continue

        if pakiet == {"typ": "wykryj_pi"}:
            continue

        if not _poprawny_pakiet_sterowania(pakiet):
            print("[CONNECT] Błąd: Nieprawidłowy pakiet sterowania")
            continue

        with _blokada_stanu:
            _telefon_addr = addr
            pico_ip = _pico_ip
            if pico_ip is None:
                _oczekujace_sterowanie = data

        if pico_ip is None:
            print("[CONNECT] Polecenie odebrane; oczekiwanie na pierwszy pakiet z Pico.")
            continue

        try:
            _sock_sterowanie.sendto(data, (pico_ip, PORT_PICO))
            print(f"[CONNECT] Przekazano sterowanie z telefonu do Pico ({pico_ip}): {pakiet}")
        except OSError as error:
            print(f"[CONNECT] Błąd przekazywania sterowania do Pico: {error}")


def _wysylaj_wykrywanie_pi():
    """Rozgłasza adres Pi, aby Pico nie wymagało stałego IP Malinki."""
    wiadomosc = json.dumps({"typ": "wykryj_pi"}).encode("utf-8")
    while True:
        try:
            _sock_odbior.sendto(wiadomosc, ("255.255.255.255", PORT_PICO))
        except OSError as error:
            print(f"[CONNECT] Błąd rozgłaszania adresu Pi: {error}")
        time.sleep(ODSTEP_WYKRYWANIA)


def start_odbior():
    """Uruchamia nasłuch odczytów z Pico i sterowania z telefonu tylko raz."""
    global _czy_nasluchuje, _sock_odbior, _sock_sterowanie
    with _blokada_stanu:
        if _czy_nasluchuje:
            return

        sock_odbior = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_sterowanie = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock_odbior.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_odbior.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock_sterowanie.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_odbior.bind((UDP_IP, PORT_RPI))
            sock_sterowanie.bind((UDP_IP, PORT_STEROWANIA))
        except OSError:
            sock_odbior.close()
            sock_sterowanie.close()
            raise
        _sock_odbior = sock_odbior
        _sock_sterowanie = sock_sterowanie
        _czy_nasluchuje = True

    threading.Thread(target=_odbieraj_odczyty, daemon=True).start()
    threading.Thread(target=_odbieraj_sterowanie, daemon=True).start()
    threading.Thread(target=_wysylaj_wykrywanie_pi, daemon=True).start()


def pobierz_dane():
    """Zwraca kopię odczytów dla GUI."""
    with _blokada_stanu:
        return _dane_z_pico.copy()


def wyslij_do_pico(stan_1, stan_2, wartosc_1, wartosc_2):
    """Wysyła sterowanie z lokalnego GUI bezpośrednio do Pico."""
    with _blokada_stanu:
        pico_ip = _pico_ip

    if pico_ip is None:
        print("[CONNECT] Czekam na pierwszy pakiet z Pico, aby poznać jego IP.")
        return

    pakiet = {
        "stan_1": int(stan_1),
        "stan_2": int(stan_2),
        "wartosc_1": int(wartosc_1),
        "wartosc_2": int(wartosc_2)
    }
    if not _poprawny_pakiet_sterowania(pakiet):
        print("[CONNECT] Błąd: Wartości sterowania są poza dozwolonym zakresem.")
        return

    try:
        wiadomosc = json.dumps(pakiet).encode("utf-8")
        _sock_sterowanie.sendto(wiadomosc, (pico_ip, PORT_PICO))
        print(f"[CONNECT] Wysłano do Pico ({pico_ip}): {pakiet}")
    except OSError as error:
        print(f"[CONNECT] Błąd wysyłania do Pico: {error}")
