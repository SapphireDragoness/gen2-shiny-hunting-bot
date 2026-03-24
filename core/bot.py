from pyboy import PyBoy
from pyboy.utils import WindowEvent
from loguru import logger

from utils.utils import read_stats, check_shiny, read_battle_info


def bot():
    # TODO: accept all Gen 2 ROMs
    emu = PyBoy(
        "roms/crystal.gbc",
    )

    while not emu.send_input(WindowEvent.QUIT):
        # run normally in overworld
        emu.tick()

        # in a wild battle
        # TODO: works, but could be better
        if hex(emu.memory[0xD22D]) == "0x1":
            info = read_battle_info(
                species=emu.memory[0xD206],
                level=emu.memory[0xD213],
                location=emu.memory[0xDCB6],
            )

            stats = read_stats(emu.memory[0xD20C], emu.memory[0xD20D])

            logger.debug(f"Species: {info["species"]}")
            logger.debug(f"Level: {info["level"]}")
            logger.debug(f"Attack DV: {stats["attack"]}")
            logger.debug(f"Defense DV: {stats["defense"]}")
            logger.debug(f"Speed DV: {stats["speed"]}")
            logger.debug(f"Special DV: {stats["special"]}")

            for _ in range(300):
                emu.tick(1, True)

            if check_shiny(stats):
                # shiny found: log and save
                logger.success(f"Shiny {info["species"]} found!")
                with open(
                    f"save_states/{info["species"]}_{info["location"]}.state", "wb"
                ) as f:
                    emu.save_state(f)
            else:
                # run from battle
                for _ in range(12):
                    emu.tick(1, True)
                emu.button("down")
                emu.tick()
                for _ in range(12):
                    emu.tick(1, True)
                emu.button("right")
                emu.tick()
                for _ in range(12):
                    emu.tick(1, True)
                emu.button("a")
                emu.tick()
                for _ in range(12):
                    emu.tick(1, True)
                emu.button("a")
                emu.tick()
                for _ in range(12):
                    emu.tick(1, True)
                emu.button("a")
                emu.tick()
