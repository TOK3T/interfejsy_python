import threading

import connect


if __name__ == "__main__":
    connect.start_odbior()
    print("[BRIDGE] Most UDP działa. Naciśnij Ctrl+C, aby zakończyć.")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\n[BRIDGE] Zatrzymywanie mostu.")
