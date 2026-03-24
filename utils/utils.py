from utils.dicts import POKES


def check_shiny(stats: dict) -> bool:
    # from https://bulbapedia.bulbagarden.net/wiki/Shiny_Pok%C3%A9mon#Generation_II
    ATK_VALUES = ["2", "3", "6", "7", "10", "11", "14", "15"]
    if (
        stats["attack"] in ATK_VALUES
        and stats["speed"] == "10"
        and stats["defense"] == "10"
        and stats["special"] == "10"
    ):
        return True
    return False


def int_to_zeroed_hex(value: int) -> str:
    val = str(hex(value))
    # already 0xXX
    if len(val) == 4:
        return val
    # 0xX -> 0x0X
    return val[:2] + "0" + val[2:]


def read_stats(d20c: int, d20d: int) -> dict:
    return {
        "attack": str(int(int_to_zeroed_hex(d20c)[2], 16)),
        "defense": str(int(int_to_zeroed_hex(d20c)[3], 16)),
        "speed": str(int(int_to_zeroed_hex(d20d)[2], 16)),
        "special": str(int(int_to_zeroed_hex(d20d)[3], 16)),
    }


def read_battle_info(species: int, level: int, location: int) -> dict:
    return {
        "species": POKES[int_to_zeroed_hex(species)[2:].upper()],
        "level": str(level),
        "location": str(
            location
        ),  # TODO: find out where the location is stored in RAM and map it in dicts.py
    }
