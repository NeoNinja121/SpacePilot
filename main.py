# main.py – Updated Game Logic with Ship Flicker Intro

import time
import random
from PIL import Image, ImageDraw, ImageFont
import os
import displayhatmini as dhm
import sys


from game.constants import WIDTH, HEIGHT, COLOR_BLACK, COLOR_GREEN, COLOR_RED
from game.events import get_random_event
from game.ui import StatusBar, ButtonBar, EventDisplay

# === Load explosion frames ===
EXPLOSION_FRAMES = [
    Image.open(os.path.join("sprites", f"exp{i}.png")).convert("RGBA")
    for i in range(1, 7)
]

# === Load engine flame animation frames ===
ENGINE_FLAME_FRAMES = [
    Image.open(os.path.join("sprites", f"flame{i}.png")).convert("RGBA")
    for i in range(1, 5)
]
ENGINE_FLAME_BIG_FRAMES = [
    Image.open(os.path.join("sprites", f"flamebig{i}.png")).convert("RGBA")
    for i in range(1, 5)
]



# === Load Random Sprite Function ===
def load_random_sprite(prefix, max_index):
    index = random.randint(1, max_index)
    path = os.path.join("sprites", f"{prefix}{index}.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    return Image.open(path).convert("RGBA")

# === Ship Builder ===
def build_ship_image():
    MODULE_WIDTH = 33
    MODULE_HEIGHT = 30
    ship = Image.new("RGBA", (MODULE_WIDTH * 3, MODULE_HEIGHT * 2))

    base = load_random_sprite("base", 8)
    ship.paste(base, (0, 0), base)

    engine_top = load_random_sprite("engine", 9)
    storage_top = load_random_sprite("storagetop", 9)
    cabin = load_random_sprite("cabin", 21)
    engine_bottom = load_random_sprite("engine", 10)
    storage_bottom = load_random_sprite("storagebottom", 10)
    gun = load_random_sprite("gun", 10)

    ship.paste(engine_top, (0, 0), engine_top)
    ship.paste(storage_top, (33, 0), storage_top)
    ship.paste(cabin, (66, 0), cabin)
    ship.paste(engine_bottom, (0, 30), engine_bottom)
    ship.paste(storage_bottom, (33, 30), storage_bottom)
    ship.paste(gun, (66, 30), gun)

    # Optional overlays
    logo = load_random_sprite("logo", 14)
    wires = load_random_sprite("wires", 7)
    pipes = load_random_sprite("pipes", 10)

    ship.paste(logo, (0, 0), logo)
    ship.paste(wires, (0, 0), wires)
    ship.paste(pipes, (0, 0), pipes)

    return ship

# === Display Setup ===
buffer = Image.new("RGBA", (WIDTH, HEIGHT))
displayhat = dhm.DisplayHATMini(buffer.convert("RGB"))

# === Show Intro Logo ===
logo_path = os.path.join("sprites", "SpaceSim_logo_5.png")
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path).convert("RGB").resize((WIDTH, HEIGHT))
    displayhat.buffer = logo_image
    displayhat.display()
    time.sleep(2)

# === Ship Flicker Intro ===
# === Progressive Ship Builder with Flickering ===

# Load background
building_bg_path = os.path.join("sprites", "buildingship.png")
building_bg = Image.open(building_bg_path).convert("RGBA").resize((WIDTH, HEIGHT))

# Load HUD overlay
hud_overlay_path = os.path.join("sprites", "hud.png")
hud_overlay = Image.open(hud_overlay_path).convert("RGBA").resize((WIDTH, HEIGHT))


# Create placeholders
parts = {
    "base": None,
    "engine_top": None,
    "engine_bottom": None,
    "storage_top": None,
    "storage_bottom": None,
    "gun": None,
    "cabin": None,
    "logo": None,
    "pipes": None,
    "wires": None,
}

# Renders the current ship-in-progress
def render_build_state(message=None):
    buffer.paste(building_bg, (0, 0), building_bg)
    ship = Image.new("RGBA", (99, 60))
    if parts["base"]: ship.paste(parts["base"], (0, 0), parts["base"])
    if parts["engine_top"]: ship.paste(parts["engine_top"], (0, 0), parts["engine_top"])
    if parts["engine_bottom"]: ship.paste(parts["engine_bottom"], (0, 30), parts["engine_bottom"])
    if parts["storage_top"]: ship.paste(parts["storage_top"], (33, 0), parts["storage_top"])
    if parts["storage_bottom"]: ship.paste(parts["storage_bottom"], (33, 30), parts["storage_bottom"])
    if parts["cabin"]: ship.paste(parts["cabin"], (66, 0), parts["cabin"])
    if parts["gun"]: ship.paste(parts["gun"], (66, 30), parts["gun"])
    if parts["logo"]: ship.paste(parts["logo"], (0, 0), parts["logo"])
    if parts["pipes"]: ship.paste(parts["pipes"], (0, 0), parts["pipes"])
    if parts["wires"]: ship.paste(parts["wires"], (0, 0), parts["wires"])
    x = (WIDTH - ship.width) // 2
    y = (HEIGHT - ship.height) // 2
    buffer.paste(ship, (x, y), ship)

    if message:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)  # Larger font
        draw = ImageDraw.Draw(buffer)
        text_width = draw.textlength(message, font=font)
        draw.text(((WIDTH - text_width) // 2, HEIGHT - 25), message, font=font, fill=(255, 255, 255))


    displayhat.buffer = buffer.convert("RGB")
    displayhat.display()


# Flicker logic for each part
def flicker_part(key, duration, loader_fn, message):
    start = time.time()
    while time.time() - start < duration:
        parts[key] = loader_fn()
        render_build_state(message)
        time.sleep(0.05)


# Build ship step-by-step
build_steps = [
    ("base", 1.0, lambda: load_random_sprite("base", 8), "BUILDING STRUCTURE"),
    ("engine_top", 1.0, lambda: load_random_sprite("engine", 9), "TUNING TOP ENGINE"),
    ("engine_bottom", 1.0, lambda: load_random_sprite("engine", 10), "SPOOLING BOTTOM ENGINE"),
    ("storage_top", 1.0, lambda: load_random_sprite("storagetop", 9), "BOLTING ON TOP STORAGE"),
    ("storage_bottom", 1.0, lambda: load_random_sprite("storagebottom", 10), "GLUEING ON BOTTOM STORAGE"),
    ("cabin", 1.0, lambda: load_random_sprite("cabin", 21), "PUTTING SEATS IN"),
    ("gun", 1.0, lambda: load_random_sprite("gun", 10), "LOADING GUNS"),
    ("logo", 1.0, lambda: load_random_sprite("logo", 14), "CUSTOMISATION"),
    ("wires", 1.0, lambda: load_random_sprite("wires", 7), "WIRING ENGINE"),
    ("pipes", 1.0, lambda: load_random_sprite("pipes", 10), "FINAL COOLING SYSTEMS"),
]

for key, duration, loader_fn, message in build_steps:
    flicker_part(key, duration, loader_fn, message)

# Final launch message
render_build_state("LAUNCHING")
time.sleep(1.0)


# === Assemble final ship with proper coordinates
final_ship = Image.new("RGBA", (99, 60))
if parts["base"]: final_ship.paste(parts["base"], (0, 0), parts["base"])
if parts["engine_top"]: final_ship.paste(parts["engine_top"], (0, 0), parts["engine_top"])
if parts["engine_bottom"]: final_ship.paste(parts["engine_bottom"], (0, 30), parts["engine_bottom"])
if parts["storage_top"]: final_ship.paste(parts["storage_top"], (33, 0), parts["storage_top"])
if parts["storage_bottom"]: final_ship.paste(parts["storage_bottom"], (33, 30), parts["storage_bottom"])
if parts["cabin"]: final_ship.paste(parts["cabin"], (66, 0), parts["cabin"])
if parts["gun"]: final_ship.paste(parts["gun"], (66, 30), parts["gun"])
if parts["logo"]: final_ship.paste(parts["logo"], (0, 0), parts["logo"])
if parts["pipes"]: final_ship.paste(parts["pipes"], (0, 0), parts["pipes"])
if parts["wires"]: final_ship.paste(parts["wires"], (0, 0), parts["wires"])

spaceship_image = final_ship.copy()

# === Engine Flame Offsets: behind top and bottom engines ===
engine_flames = [
    {'x_offset': -10, 'y_offset': 15},    # Behind top engine
    {'x_offset': -10, 'y_offset': 45},   # Behind bottom engine
]



# === Setup final ship image ===
spaceship_image = final_ship.copy()

def flash_and_explode():
    global spaceship_image

    # Create a white version of the ship for flashing
    white_ship = spaceship_image.copy()
    r, g, b, a = white_ship.split()
    white_overlay = Image.new("RGBA", white_ship.size, (255, 255, 255, 255))
    white_ship = Image.composite(white_overlay, spaceship_image, a)

    for _ in range(10):
        # Flash white
        buffer.paste((0, 0, 0), [0, 0, WIDTH, HEIGHT])
        for s in stars:
            draw.ellipse((s["x"], s["y"], s["x"] + 2, s["y"] + 2), fill=(255, 255, 255))
        buffer.paste(white_ship, (WIDTH // 2 - white_ship.width // 2, HEIGHT // 2 - white_ship.height // 2), white_ship)
        displayhat.buffer = buffer.convert("RGB")
        displayhat.display()
        time.sleep(0.05)

        # Back to normal ship
        buffer.paste((0, 0, 0), [0, 0, WIDTH, HEIGHT])
        for s in stars:
            draw.ellipse((s["x"], s["y"], s["x"] + 2, s["y"] + 2), fill=(255, 255, 255))
        buffer.paste(spaceship_image, (WIDTH // 2 - spaceship_image.width // 2, HEIGHT // 2 - spaceship_image.height // 2), spaceship_image)
        displayhat.buffer = buffer.convert("RGB")
        displayhat.display()
        time.sleep(0.05)

    # Play explosion frames
    for frame in EXPLOSION_FRAMES:
        buffer.paste((0, 0, 0), [0, 0, WIDTH, HEIGHT])
        for s in stars:
            draw.ellipse((s["x"], s["y"], s["x"] + 2, s["y"] + 2), fill=(255, 255, 255))
        x = WIDTH // 2 - frame.width // 2
        y = HEIGHT // 2 - frame.height // 2
        buffer.paste(frame, (x, y), frame)
        displayhat.buffer = buffer.convert("RGB")
        displayhat.display()
        time.sleep(0.08)

    # Remove ship after explosion
    spaceship_image = Image.new("RGBA", spaceship_image.size, (0, 0, 0, 0))

    # Load and show game over image
    game_over_path = os.path.join("sprites", "gameover.png")
    if os.path.exists(game_over_path):
        game_over = Image.open(game_over_path).convert("RGBA").resize((WIDTH, HEIGHT))
        displayhat.buffer = game_over.convert("RGB")
        displayhat.display()

    # Load optional overlay image to show when A is pressed
    game_over2_path = os.path.join("sprites", "gameover2.png")
    game_over2 = None
    if os.path.exists(game_over2_path):
        game_over2 = Image.open(game_over2_path).convert("RGBA").resize((WIDTH, HEIGHT))

    # Wait for A to restart, show visual feedback if pressed
    while True:
        if displayhat.read_button(displayhat.BUTTON_A):
            # Show overlay
            if game_over2:
                combined = game_over.copy()
                combined.paste(game_over2, (0, 0), game_over2)
                displayhat.buffer = combined.convert("RGB")
                displayhat.display()
            # Debounce and restart
            while displayhat.read_button(displayhat.BUTTON_A):
                time.sleep(0.05)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        time.sleep(0.1)





# === Convert static image to draw-friendly format ===
def get_ship_image():
    return spaceship_image

# === Game Setup ===
from game.display_config import detect_display
from game.sprites import Spaceship

config = detect_display()
spaceship = Spaceship(x=WIDTH // 2, y=HEIGHT // 2, ship_data={"speed": 1})
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(50)]

# === Fixed ambient lights: 2 green (front), 2 red (back) ===
ambient_lights = [
    {'x': WIDTH // 2 - 40, 'y': HEIGHT // 2 - 10, 'type': 'red', 'shape': 'circle'},
    {'x': WIDTH // 2 - 20, 'y': HEIGHT // 2 - 5, 'type': 'red', 'shape': 'circle'},
    {'x': WIDTH // 2 + 20, 'y': HEIGHT // 2 + 5, 'type': 'green', 'shape': 'circle'},
    {'x': WIDTH // 2 + 35, 'y': HEIGHT // 2 + 10, 'type': 'green', 'shape': 'circle'},
]
light_flash_state = True
light_flash_timer = 0


engine_flame_index = 0
last_flame_index = -1  # Used to track the previous flame frame

boost_active = False
boost_points = 10
boost_end_time = 0
distance_covered = 0
repair_points = 2
damaged_systems = []
current_event = None
font = ImageFont.load_default()

status_bar = StatusBar(config, 1, boost_active, boost_points, repair_points, damaged_systems, distance_covered)
button_bar = ButtonBar(config, boost_points, boost_active, repair_points, len(damaged_systems), False)
event_display = None

# === Button Input ===
def on_button(index):
    global boost_active, boost_points, repair_points, damaged_systems, current_event, boost_end_time
    if current_event and current_event.options:
        choice = current_event.options[index] if index < len(current_event.options) else None
        if choice:
            if random.randint(1, 100) <= choice.get("success_rate", 100):
                boost_points += 1
        current_event = None
        return
    if index == 0 and boost_points > 0 and not boost_active:
        boost_active = True
        boost_end_time = time.time() + boost_points
        boost_points = 0
    elif index == 1 and repair_points > 0 and damaged_systems:
        repair_points -= 1
        damaged_systems = []

# === Main Game Loop ===
try:
    last_time = time.time()
    while True:
        now = time.time()
        # Flash toggle logic (e.g. every 0.5s at 6fps = 3 frames)
        light_flash_timer += 1
        if light_flash_timer >= 3:
            light_flash_state = not light_flash_state
            light_flash_timer = 0

        dt = now - last_time
        last_time = now

        speed = 4 if boost_active else 1
        distance_covered += speed
        if boost_active and now >= boost_end_time:
            boost_active = False

        for s in stars:
            s["x"] -= speed
            if s["x"] < 0:
                s["x"] = WIDTH
                s["y"] = random.randint(0, HEIGHT)

        if not boost_active and current_event is None and random.random() < 0.0002:
            current_event = get_random_event()
            event_display = EventDisplay(config, current_event)

        draw = ImageDraw.Draw(buffer)
        draw.rectangle((0, 0, WIDTH, HEIGHT), fill=COLOR_BLACK)
        for s in stars:
            draw.ellipse((s["x"], s["y"], s["x"] + 2, s["y"] + 2), fill=(255, 255, 255))

        # Draw static ship
        buffer.paste(spaceship_image, (WIDTH // 2 - spaceship_image.width // 2, HEIGHT // 2 - spaceship_image.height // 2), spaceship_image)
        
        # === Ambient Ship Lights Flicker ===
        ambient_draw = ImageDraw.Draw(buffer)

        for light in ambient_lights:
            x, y = light['x'], light['y']
            flicker_type = light['type']
            shape = light['shape']

            # Flicker between ON and OFF shades
            if flicker_type == 'red':
                color = (255, 50, 50) if light_flash_state else (100, 0, 0)
            elif flicker_type == 'green':
                color = (50, 255, 50) if light_flash_state else (0, 100, 0)
            if shape == 'circle':
                ambient_draw.ellipse((x, y, x+2, y+2), fill=color)
            else:
                ambient_draw.line((x, y, x + 3, y), fill=color, width=1)



        # === Draw engine flame frame behind ship (normal vs boost) ===
        current_frames = ENGINE_FLAME_BIG_FRAMES if boost_active else ENGINE_FLAME_FRAMES

        while True:
            flame_index = random.randint(0, len(current_frames) - 1)
            if flame_index != last_flame_index:
                break
        last_flame_index = flame_index

        flame_image = current_frames[flame_index]
        fx = WIDTH // 2 - spaceship_image.width // 2 - 99
        fy = HEIGHT // 2 - spaceship_image.height // 2
        buffer.paste(flame_image, (fx, fy), flame_image)






        # Overlay the HUD (before text)     
        buffer.paste(hud_overlay, (0, 0), hud_overlay)


        draw.text((25, 10), f"Boost: {'ACTIVE' if boost_active else boost_points}", font=font, fill=COLOR_GREEN)
        repair_text = f"{repair_points} :Repair"
        text_width = draw.textlength(repair_text, font=font)
        draw.text((WIDTH - text_width - 25, 10), repair_text, font=font, fill=COLOR_RED)

        if current_event and event_display:
            draw.rectangle((0, 0, WIDTH, HEIGHT), fill=COLOR_BLACK)
            event_display.draw(draw)

        status_bar.update(1, boost_active, boost_points, repair_points, damaged_systems, distance_covered)
        button_bar.update(boost_points, boost_active, repair_points, len(damaged_systems), current_event is not None)
        status_bar.draw(draw)
        button_bar.draw(draw)

        if displayhat.read_button(displayhat.BUTTON_A):
            on_button(0)
            while displayhat.read_button(displayhat.BUTTON_A): time.sleep(0.05)
        if displayhat.read_button(displayhat.BUTTON_X):
            on_button(1)
            while displayhat.read_button(displayhat.BUTTON_X): time.sleep(0.05)            
        if displayhat.read_button(displayhat.BUTTON_Y):
            flash_and_explode()
            while displayhat.read_button(displayhat.BUTTON_Y): time.sleep(0.05)

        displayhat.buffer = buffer.convert("RGB")
        displayhat.display()
        time.sleep(0.03)

except KeyboardInterrupt:
    print("Exiting cleanly.")
