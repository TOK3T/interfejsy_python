from obrazy import (
    Day_Empty, Day_Sun, Day_Clouds, Day_Dry,
    Night_Empty, Night_Moon, Night_Clouds, Night_Dry
)

try:
    from sense_hat import SenseHat
    sense = SenseHat()
    print("Sense HAT detected. Using real Sense HAT.")
except (ImportError, OSError):
     sense = None
     print("Sense HAT not detected. Using mock Sense HAT.")

last_state = (None, None)

def aktualizuj_led(day_state, tryb):
    global last_state

    if (sense is None):
        return

    if (day_state, tryb) == last_state:
        return
    last_state = (day_state, tryb)

    if day_state == 1:
            if tryb == 0:
                sense.set_pixels(Day_Empty)
            elif tryb == 1:
                sense.set_pixels(Day_Sun)
            elif tryb == 2:
                sense.set_pixels(Day_Clouds)
            else:
                sense.set_pixels(Day_Dry)
    else:
           if tryb == 0:
               sense.set_pixels(Night_Empty)
           elif tryb == 1:
                sense.set_pixels(Night_Moon)
           elif tryb == 2:
                sense.set_pixels(Night_Clouds)
           else:
                sense.set_pixels(Night_Dry)

