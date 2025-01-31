import time
import random
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
from adafruit_display_text import label

displayio.release_displays()

DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32
FRAME_DELAY = 0.03
FLAME_COLORS = [0x000000, 0x201000, 0x402000, 0x800000, 0xFF4000, 0xFFFF00, 0xFFFFFF]
WOOD_HEIGHT = 4

matrix = rgbmatrix.RGBMatrix(
    width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)



display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, len(FLAME_COLORS))
palette = displayio.Palette(len(FLAME_COLORS))
for i, color in enumerate(FLAME_COLORS):
    palette[i] = color

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(scale=1)
group.append(tile_grid)

text_group = displayio.Group(scale=1)
text = label.Label(terminalio.FONT, text="Lock in!", color=0xFFFF00)
text.y = 2
text_group.append(text)
group.append(text_group)

display.root_group = group

flame_data = [[0] * DISPLAY_WIDTH for _ in range(DISPLAY_HEIGHT)]

for y in range(DISPLAY_HEIGHT - WOOD_HEIGHT, DISPLAY_HEIGHT):
    for x in range(DISPLAY_WIDTH):
        bitmap[x, y] = 2

text_x_position = DISPLAY_WIDTH
text_speed = 1

while True:
    for y in range(DISPLAY_HEIGHT - WOOD_HEIGHT):
        for x in range(DISPLAY_WIDTH):
            bitmap[x, y] = 0

    for x in range(DISPLAY_WIDTH):
        flame_data[DISPLAY_HEIGHT - WOOD_HEIGHT - 1][x] = random.randint(3, len(FLAME_COLORS) - 1) if random.random() < 0.5 else max(0, flame_data[DISPLAY_HEIGHT - WOOD_HEIGHT - 1][x] - 1)

    for y in range(DISPLAY_HEIGHT - WOOD_HEIGHT - 2, -1, -1):
        for x in range(DISPLAY_WIDTH):
            below_intensity = flame_data[y + 1][x]
            flicker = random.choice([-1, 0, 1]) if random.random() < 0.9 else 0
            spread_effect = int(below_intensity * 0.9)
            flame_data[y][x] = max(0, min(len(FLAME_COLORS) - 1, spread_effect - 1 + flicker))

    for y in range(DISPLAY_HEIGHT - WOOD_HEIGHT):
        for x in range(DISPLAY_WIDTH):
            bitmap[x, y] = flame_data[y][x]

    text.x = text_x_position
    text_x_position -= text_speed
    if text_x_position < -len("keep hacking") * 6:
        text_x_position = DISPLAY_WIDTH

    display.auto_refresh = True
    display.refresh()
    time.sleep(FRAME_DELAY)
