#include <WiFi.h>
#include <WiFiUdp.h>
#include <string.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include <ArduinoJson.h>

// --- KONFIGURACJA SIECI ---
const char* WIFI_SSID  = "Patryq21_Network";
const char* WIFI_HASLO = "fa721c2e649569c36ee2d6d1e6";
IPAddress IP_MALINKI;
bool malinka_wykryta = false;

const uint16_t PORT_PICO = 5006;       // Port nasłuchu na Pico WH
const uint16_t PORT_RPI  = 5005;       // Port odbiorczy na PC / Malince

WiFiUDP udp;
Adafruit_AHTX0 aht;

// --- DEFINICJE PINÓW ---
const int PIN_LED_1 = 2; // GP2 - Wyjście 1 (0/1)
const int PIN_LED_2 = 3; // GP3 - Wyjście 2 (0/1)
const int PIN_PWM_1 = 4; // GP4 - Suwak 1 (0-255)
const int PIN_PWM_2 = 5; // GP5 - Suwak 2 (0-255)

// --- ZMIENNE STAŁE I POMIAROWE ---
int Day_State        = 1;
int Tryb             = 1;
int wilgotnosc_gleby = 45;
int poziom_swiatla   = 750;
int stan_wody        = 1;

unsigned long ostatniPomiar = 0;

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n--- START PICO WH (Arduino IDE) ---");

    // Konfiguracja pinów cyfrowych i PWM
    pinMode(PIN_LED_1, OUTPUT);
    pinMode(PIN_LED_2, OUTPUT);
    pinMode(PIN_PWM_1, OUTPUT);
    pinMode(PIN_PWM_2, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    digitalWrite(PIN_LED_1, LOW);
    digitalWrite(PIN_LED_2, LOW);
    analogWrite(PIN_PWM_1, 0);
    analogWrite(PIN_PWM_2, 0);

    // Inicjalizacja I2C0 na pinach GP0 (SDA) i GP1 (SCL)
    Wire.setSDA(0);
    Wire.setSCL(1);
    Wire.begin();

    if (!aht.begin(&Wire)) {
        Serial.println("[I2C] BŁĄD: Nie znaleziono czujnika AHT20 na GP0/GP1!");
    } else {
        Serial.println("[I2C] Czujnik AHT20 gotowy.");
    }

    // Łączenie z Wi-Fi
    Serial.print("[WIFI] Łączenie z siecią ");
    Serial.println(WIFI_SSID);
    
    WiFi.begin(WIFI_SSID, WIFI_HASLO);
    
    int proby = 0;
    while (WiFi.status() != WL_CONNECTED) {
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN)); // Mruganie diody podczas łączenia
        delay(500);
        Serial.print(".");
        proby++;
        if (proby > 40) { // Po 20 sekundach przestaje mrugać, żeby nie blokować w nieskończoność
            Serial.println("\n[WIFI] Błąd połączenia! Sprawdź nazwę/hasło (wymagane pasmo 2.4 GHz).");
            break;
        }
    }

    digitalWrite(LED_BUILTIN, HIGH); // Świeci ciągle = Połączono z Wi-Fi
    Serial.println("\n[WIFI] Połączono pomyślnie!");
    Serial.print("[WIFI] IP Pico WH: ");
    Serial.println(WiFi.localIP());

    // Uruchomienie nasłuchu UDP
    udp.begin(PORT_PICO);
    Serial.println("[UDP] Nasłuch na porcie 5006 aktywny.");
}

void loop() {
    // 1. ODBIERANIE ROZKAZÓW Z PI I ODKRYWANIE ADRESU PI (UDP port 5006)
    int rozmiarPakietu = udp.parsePacket();
    if (rozmiarPakietu > 0) {
        JsonDocument docRx;
        DeserializationError blad = deserializeJson(docRx, udp);
        
        if (!blad) {
            const char* typ = docRx["typ"] | "";
            if (strcmp(typ, "wykryj_pi") == 0) {
                IP_MALINKI = udp.remoteIP();
                malinka_wykryta = true;
                Serial.print("[UDP] Wykryto Raspberry Pi: ");
                Serial.println(IP_MALINKI);
            } else {
                int s1 = docRx["stan_1"] | -1;
                int s2 = docRx["stan_2"] | -1;
                int w1 = docRx["wartosc_1"] | -1;
                int w2 = docRx["wartosc_2"] | -1;

                if (s1 != -1) digitalWrite(PIN_LED_1, s1 > 0 ? HIGH : LOW);
                if (s2 != -1) digitalWrite(PIN_LED_2, s2 > 0 ? HIGH : LOW);
                if (w1 != -1) analogWrite(PIN_PWM_1, constrain(w1, 0, 255));
                if (w2 != -1) analogWrite(PIN_PWM_2, constrain(w2, 0, 255));

                Serial.printf("[PI -> PICO] Odebrano -> S1:%d, S2:%d, W1:%d, W2:%d\n", s1, s2, w1, w2);
            }
        } else {
            Serial.println("[UDP] Błąd parsowania JSON od GUI");
        }
    }

    // 2. WYSYŁANIE POMIARÓW DO PI (co 1 sekundę)
    if (millis() - ostatniPomiar >= 1000) {
        ostatniPomiar = millis();

        // Odczyt z czujnika AHT20
        sensors_event_t wilg, temp;
        aht.getEvent(&wilg, &temp);

        float temperatura = isnan(temp.temperature) ? 0.0 : round(temp.temperature * 10) / 10.0;
        float wilgotnosc  = isnan(wilg.relative_humidity) ? 0.0 : round(wilg.relative_humidity * 10) / 10.0;

        // Tworzenie pakietu JSON
        JsonDocument docTx;
        docTx["Day_State"]        = Day_State;
        docTx["Tryb"]             = Tryb;
        docTx["temperatura"]      = temperatura;
        docTx["wilgotnosc"]       = wilgotnosc;
        docTx["wilgotnosc_gleby"] = wilgotnosc_gleby;
        docTx["poziom_swiatla"]   = poziom_swiatla;
        docTx["stan_wody"]        = stan_wody;

        if (malinka_wykryta) {
            udp.beginPacket(IP_MALINKI, PORT_RPI);
            serializeJson(docTx, udp);
            udp.endPacket();

            Serial.printf("[PICO -> PI] Wysłano -> Temp: %.1f°C, Wilg: %.1f%%\n", temperatura, wilgotnosc);
        }
    }
}