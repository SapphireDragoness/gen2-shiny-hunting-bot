from pyboy import PyBoy
from pyboy.utils import WindowEvent
from loguru import logger

emu = PyBoy(
    "roms/crystal.gbc",
)

while not emu.send_input(WindowEvent.QUIT):
    emu.tick()

    # in a wild battle
    if hex(emu.memory[0xD22D]) == "0x1":
        attack = hex(emu.memory[0xD20C])[2]
        defense = hex(emu.memory[0xD20C])[3]
        speed = hex(emu.memory[0xD20D])[2]
        special = hex(emu.memory[0xD20D])[3]

        logger.debug(f"Attack DV: {str(int(attack, 16))}")
        logger.debug(f"Defense DV: {str(int(defense, 16))}")
        logger.debug(f"Speed DV: {str(int(speed, 16))}")
        logger.debug(f"Special DV: {str(int(special, 16))}")
    else:
        logger.debug("Not in a battle.")
