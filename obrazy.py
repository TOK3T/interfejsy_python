# obrazy.py

# Kolory
Ground_day = (112, 173, 71)
Ground_night = (56, 87, 35)
Back_day = (0, 176, 240)
Back_night = (32, 56, 100)
Sun = (255, 255, 0)
Moon_1 = (216, 216, 216)
Moon_2 = (191, 191, 191)
Moon_3 = (165, 165, 165)
Moon_4 = (127, 127, 127)
Cloud_day = (216, 216, 216)
Cloud_night = (127, 127, 127)
Dry_day = (197, 90, 17)
Dry_night = (131, 60, 11)
Stem_day = (168, 208, 142)
Stem_night = (84, 128, 53)
Petal_day = (255, 0, 0)
Petal_night = (192, 0, 0)
Middle_day = (255, 217, 101)
Middle_night = (190, 143, 0)

# Tablice Obrazów
Day_Empty = [
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Petal_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Petal_day, Middle_day, Petal_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Petal_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Stem_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day
]

Day_Sun = [
    Back_day, Back_day, Back_day, Back_day, Back_day, Sun, Sun, Sun,
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Sun, Sun,
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Sun,
    Back_day, Back_day, Petal_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Petal_day, Middle_day, Petal_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Petal_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Stem_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day
]

Day_Clouds = [
    Cloud_day, Cloud_day, Back_day, Back_day, Back_day, Back_day, Cloud_day, Cloud_day,
    Cloud_day, Cloud_day, Cloud_day, Cloud_day, Back_day, Cloud_day, Cloud_day, Cloud_day,
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Petal_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Petal_day, Middle_day, Petal_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Petal_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Stem_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day
]

Day_Dry = [
    Cloud_day, Cloud_day, Back_day, Back_day, Back_day, Back_day, Cloud_day, Cloud_day,
    Cloud_day, Cloud_day, Cloud_day, Cloud_day, Back_day, Cloud_day, Cloud_day, Cloud_day,
    Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Dry_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Dry_day, Dry_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Dry_day, Dry_day, Back_day, Back_day, Back_day, Back_day,
    Back_day, Back_day, Dry_day, Back_day, Back_day, Back_day, Back_day, Back_day,
    Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day, Ground_day
]

Night_Empty = [
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Petal_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Petal_night, Middle_night, Petal_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Petal_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Stem_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night
]

Night_Moon = [
    Back_night, Back_night, Back_night, Back_night, Back_night, Moon_2, Moon_1, Moon_4,
    Back_night, Back_night, Back_night, Back_night, Back_night, Moon_2, Moon_1, Moon_2,
    Back_night, Back_night, Back_night, Back_night, Back_night, Moon_4, Moon_1, Moon_3,
    Back_night, Back_night, Petal_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Petal_night, Middle_night, Petal_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Petal_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Stem_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night
]

Night_Clouds = [
    Cloud_night, Cloud_night, Back_night, Back_night, Back_night, Back_night, Cloud_night, Cloud_night,
    Cloud_night, Cloud_night, Cloud_night, Cloud_night, Back_night, Cloud_night, Cloud_night, Cloud_night,
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Petal_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Petal_night, Middle_night, Petal_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Petal_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Stem_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night
]

Night_Dry = [
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Dry_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Dry_night, Dry_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Dry_night, Dry_night, Back_night, Back_night, Back_night, Back_night,
    Back_night, Back_night, Dry_night, Back_night, Back_night, Back_night, Back_night, Back_night,
    Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night, Ground_night
]