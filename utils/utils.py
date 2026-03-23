ATK_VALUES = [2, 3, 6, 7, 10, 11, 14, 15]


def check_shiny(attack, speed, defense, special) -> bool:
    if attack in ATK_VALUES and speed == 10 and defense == 10 and special == 10:
        return True
    return False
