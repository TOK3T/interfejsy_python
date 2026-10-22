import connect
import leds
from PySide6.QtCore import QObject, Property, Signal, Slot


class Backend(QObject):
    odczytyZmienione = Signal()
    sterowanieZmienione = Signal()

    def __init__(self):
        super().__init__()
        self._odczyty = connect.pobierz_dane()
        self._stan_1 = 0
        self._stan_2 = 0
        self._wartosc_1 = 0
        self._wartosc_2 = 0

    def pobierz_temperature(self):
        return float(self._odczyty["temperatura"])

    def pobierz_wilgotnosc(self):
        return float(self._odczyty["wilgotnosc"])

    def pobierz_wilgotnosc_gleby(self):
        return int(self._odczyty["wilgotnosc_gleby"])

    def pobierz_poziom_swiatla(self):
        return int(self._odczyty["poziom_swiatla"])

    def pobierz_stan_wody(self):
        return int(self._odczyty["stan_wody"])

    def pobierz_stan_dnia(self):
        return int(self._odczyty["Day_State"])

    def pobierz_tryb(self):
        return int(self._odczyty["Tryb"])

    def pobierz_stan_1(self):
        return self._stan_1

    def pobierz_stan_2(self):
        return self._stan_2

    def pobierz_wartosc_1(self):
        return self._wartosc_1

    def pobierz_wartosc_2(self):
        return self._wartosc_2

    temperatura = Property(float, pobierz_temperature, notify=odczytyZmienione)
    wilgotnosc = Property(float, pobierz_wilgotnosc, notify=odczytyZmienione)
    wilgotnoscGleby = Property(int, pobierz_wilgotnosc_gleby, notify=odczytyZmienione)
    poziomSwiatla = Property(int, pobierz_poziom_swiatla, notify=odczytyZmienione)
    stanWody = Property(int, pobierz_stan_wody, notify=odczytyZmienione)
    stanDnia = Property(int, pobierz_stan_dnia, notify=odczytyZmienione)
    tryb = Property(int, pobierz_tryb, notify=odczytyZmienione)

    stan1 = Property(int, pobierz_stan_1, notify=sterowanieZmienione)
    stan2 = Property(int, pobierz_stan_2, notify=sterowanieZmienione)
    wartosc1 = Property(int, pobierz_wartosc_1, notify=sterowanieZmienione)
    wartosc2 = Property(int, pobierz_wartosc_2, notify=sterowanieZmienione)

    def _wyslij_sterowanie(self):
        connect.wyslij_do_pico(
            self._stan_1,
            self._stan_2,
            self._wartosc_1,
            self._wartosc_2,
        )

    @Slot()
    def odswiezDane(self):
        nowe_odczyty = connect.pobierz_dane()
        if nowe_odczyty != self._odczyty:
            self._odczyty = nowe_odczyty
            self.odczytyZmienione.emit()

        leds.aktualizuj_led(self._odczyty["Day_State"], self._odczyty["Tryb"])

    @Slot()
    def przelaczWyjscie1(self):
        self._stan_1 = 1 - self._stan_1
        self.sterowanieZmienione.emit()
        self._wyslij_sterowanie()

    @Slot()
    def przelaczWyjscie2(self):
        self._stan_2 = 1 - self._stan_2
        self.sterowanieZmienione.emit()
        self._wyslij_sterowanie()

    @Slot(int)
    def ustawWartosc1(self, wartosc):
        wartosc = max(0, min(255, wartosc))
        if wartosc == self._wartosc_1:
            return
        self._wartosc_1 = wartosc
        self.sterowanieZmienione.emit()
        self._wyslij_sterowanie()

    @Slot(int)
    def ustawWartosc2(self, wartosc):
        wartosc = max(0, min(255, wartosc))
        if wartosc == self._wartosc_2:
            return
        self._wartosc_2 = wartosc
        self.sterowanieZmienione.emit()
        self._wyslij_sterowanie()
