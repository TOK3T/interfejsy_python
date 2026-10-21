# gui.py
import tkinter as tk
import connect
import leds

# Zmienne przechowujące aktualny stan przycisków (0 lub 1)
stan_przycisku_1 = 0
stan_przycisku_2 = 0

def uruchom_gui():
    """Tworzy i uruchamia główne okno programu."""
    okno = tk.Tk()
    okno.title("Panel Czujników i Sterowania")
    okno.geometry("320x420")

    # --- FUNKCJE WEWNĘTRZNE DO OBSŁUGI PRZYCISKÓW I SUWAKÓW ---
    def wyslij_aktualne_nastawy():
        w1 = suwak_1.get()
        w2 = suwak_2.get()
        connect.wyslij_do_pico(stan_przycisku_1, stan_przycisku_2, w1, w2)

    def przelacz_1():
        global stan_przycisku_1
        stan_przycisku_1 = 1 if stan_przycisku_1 == 0 else 0
        btn_1.config(text=f"Wyjście 1: {stan_przycisku_1}")
        wyslij_aktualne_nastawy()

    def przelacz_2():
        global stan_przycisku_2
        stan_przycisku_2 = 1 if stan_przycisku_2 == 0 else 0
        btn_2.config(text=f"Wyjście 2: {stan_przycisku_2}")
        wyslij_aktualne_nastawy()

    def zmiana_suwaka(_):
        wyslij_aktualne_nastawy()

    # --- ELEMENTY OKNA: ODCZYTY Z PICO ---
    tk.Label(okno, text="--- ODCZYTY Z PICO WH ---", font=("Arial", 11, "bold")).pack(pady=8)

    lbl_temp = tk.Label(okno, text="Temperatura: --- °C", font=("Arial", 10))
    lbl_temp.pack(anchor="w", padx=20)

    lbl_wilg = tk.Label(okno, text="Wilgotność: --- %", font=("Arial", 10))
    lbl_wilg.pack(anchor="w", padx=20)

    lbl_gleba = tk.Label(okno, text="Wilgotność gleby: --- %", font=("Arial", 10))
    lbl_gleba.pack(anchor="w", padx=20)

    lbl_swiatlo = tk.Label(okno, text="Poziom światła: ---", font=("Arial", 10))
    lbl_swiatlo.pack(anchor="w", padx=20)

    lbl_woda = tk.Label(okno, text="Stan wody: ---", font=("Arial", 10))
    lbl_woda.pack(anchor="w", padx=20)

    lbl_led = tk.Label(okno, text="Stan dnia: --- | Tryb LED: ---", font=("Arial", 10))
    lbl_led.pack(anchor="w", padx=20, pady=5)

    # --- ELEMENTY OKNA: STEROWANIE PICO ---
    tk.Label(okno, text="--- STEROWANIE PICO ---", font=("Arial", 11, "bold")).pack(pady=10)

    btn_1 = tk.Button(okno, text="Wyjście 1: 0", width=20, command=przelacz_1)
    btn_1.pack(pady=4)

    btn_2 = tk.Button(okno, text="Wyjście 2: 0", width=20, command=przelacz_2)
    btn_2.pack(pady=4)

    tk.Label(okno, text="Suwak 1 (0-255):").pack(pady=(8, 0))
    suwak_1 = tk.Scale(okno, from_=0, to=255, orient="horizontal", length=220, command=zmiana_suwaka)
    suwak_1.pack()

    tk.Label(okno, text="Suwak 2 (0-255):").pack(pady=(8, 0))
    suwak_2 = tk.Scale(okno, from_=0, to=255, orient="horizontal", length=220, command=zmiana_suwaka)
    suwak_2.pack()

    # --- PĘTLA ODŚWIEŻANIA DANYCH (CO 500 ms) ---
    def odswiez_program():
        dane = connect.pobierz_dane()

        # Aktualizacja matrycy Sense HAT
        leds.aktualizuj_led(dane["Day_State"], dane["Tryb"])

        # Aktualizacja napisów w oknie
        lbl_temp.config(text=f"Temperatura: {dane['temperatura']} °C")
        lbl_wilg.config(text=f"Wilgotność: {dane['wilgotnosc']} %")
        lbl_gleba.config(text=f"Wilgotność gleby: {dane['wilgotnosc_gleby']} %")
        lbl_swiatlo.config(text=f"Poziom światła: {dane['poziom_swiatla']}")
        lbl_woda.config(text=f"Stan wody: {dane['stan_wody']}")
        lbl_led.config(text=f"Stan dnia: {dane['Day_State']} | Tryb LED: {dane['Tryb']}")

        okno.after(500, odswiez_program)

    # Start cyklicznego odświeżania i głównej pętli okna
    odswiez_program()
    okno.mainloop()