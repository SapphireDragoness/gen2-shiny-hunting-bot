import threading
import tkinter as tk
from pyboy import PyBoy
from loguru import logger

from utils.utils import read_stats, check_shiny, read_battle_info, advance, send_message
from core.battle import run


class HuntingBotUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gen 2 Shiny Hunting Bot")
        self.root.geometry("200x150")

        self.is_hunting = False
        self.start_btn = tk.Button(
            self.root, text="Start", command=self.start_hunting, bg="green", fg="white"
        )
        self.start_btn.pack(pady=10, fill=tk.X)

        self.stop_btn = tk.Button(
            self.root, text="Stop", command=self.stop_hunting, bg="red", fg="white"
        )
        self.stop_btn.pack(pady=10, fill=tk.X)

        self.status_label = tk.Label(self.root, text="Idle...")
        self.status_label.pack(pady=5)

        self.bot_thread = threading.Thread(target=self.emu_loop, daemon=True)
        self.bot_thread.start()

        self.root.mainloop()

    def start_hunting(self):
        self.is_hunting = True
        self.status_label.config(text="On it!")

    def stop_hunting(self):
        self.is_hunting = False
        self.status_label.config(text="Idle...")

    def emu_loop(self):
        self.emu = PyBoy("roms/crystal.gbc", window="SDL2")
        while self.emu.tick():
            if self.is_hunting:
                self.emu.button("right")
                self.emu.tick()
                self.emu.button("left")
                self.emu.tick()
                # in a wild battle
                if hex(self.emu.memory[0xD22D]) == "0x1":
                    self.battle_handler()

        self.emu.stop()

    def battle_handler(self):
        info = read_battle_info(
            species=self.emu.memory[0xD206],
            level=self.emu.memory[0xD213],
            location=self.emu.memory[0xDCB6],
        )

        stats = read_stats(self.emu.memory[0xD20C], self.emu.memory[0xD20D])

        logger.debug(f"Species: {info["species"]}")
        logger.debug(f"Level: {info["level"]}")
        logger.debug(f"Attack DV: {stats["attack"]}")
        logger.debug(f"Defense DV: {stats["defense"]}")
        logger.debug(f"Speed DV: {stats["speed"]}")
        logger.debug(f"Special DV: {stats["special"]}")

        # advance 300 frames, wait for animation to end
        advance(self.emu, 300)

        if check_shiny(stats):
            # shiny found: log and save
            logger.success(f"Shiny {info["species"]} found!")
            with open(
                f"save_states/{info["species"]}_{info["location"]}.state",
                "wb",
            ) as f:
                self.emu.save_state(f)
                send_message(info["species"])
        else:
            # run from battle
            run(self.emu)
