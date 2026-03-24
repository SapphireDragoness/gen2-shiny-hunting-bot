from utils.utils import advance


def run(emulator: any) -> None:
    advance(emulator, 12)
    emulator.button("down")
    emulator.tick()
    advance(emulator, 12)
    emulator.button("right")
    emulator.tick()
    advance(emulator, 12)
    emulator.button("a")
    emulator.tick()
    advance(emulator, 12)
    emulator.button("a")
    emulator.tick()
    advance(emulator, 12)
    emulator.button("a")
    emulator.tick()
