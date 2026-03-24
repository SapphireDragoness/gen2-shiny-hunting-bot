from pyboy import PyBoy
from pyboy.utils import WindowEvent
from loguru import logger

from utils.utils import read_stats, check_shiny, read_battle_info

emu = PyBoy(
    "roms/crystal.gbc",
)

FLAG = False

while not emu.send_input(WindowEvent.QUIT):
    emu.tick()

    # in a wild battle
    if hex(emu.memory[0xD22D]) == "0x1":
        # show pokemon info only once per battle
        if not FLAG:
            FLAG = True
            info = read_battle_info(
                species=emu.memory[0xD206],
                level=emu.memory[0xD213],
                location=emu.memory[0xDCB6],
            )

            stats = read_stats(emu.memory[0xD20C], emu.memory[0xD20D])

            logger.debug(f"Attack DV: {stats["attack"]}")
            logger.debug(f"Defense DV: {stats["defense"]}")
            logger.debug(f"Speed DV: {stats["speed"]}")
            logger.debug(f"Special DV: {stats["special"]}")

            if check_shiny(stats):
                logger.success("Shiny found!")
                with open(
                    f"save_states/{info["species"]}_{info["location"]}.state", "wb"
                ) as f:
                    emu.save_state()
    else:
        logger.debug("Not in a battle.")
        FLAG = False
