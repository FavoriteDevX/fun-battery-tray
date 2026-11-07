import math
import random
import threading
import time
import psutil
import pystray
from PIL import Image, ImageDraw

# Global state for animations
running = True
current_mode = "liquid"  # Options: "liquid", "leaking", "charging"
drops = []


def create_battery_frame(percent, is_charging, tick):
  width, height = 64, 64
  img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)

  # Battery outline coordinates
  bx1, by1, bx2, by2 = 14, 12, 50, 56
  # Battery positive terminal (top cap)
  draw.rectangle([26, 6, 38, 12], fill=(220, 220, 220, 255))
  # Battery body border
  draw.rectangle(
      [bx1, by1, bx2, by2], outline=(220, 220, 220, 255), width=3
  )

  # Choose color based on battery level
  if is_charging:
    fill_color = (0, 230, 118, 255)  # Neon Green
  elif percent <= 20:
    fill_color = (255, 61, 0, 255)  # Warning Red
  elif percent <= 50:
    fill_color = (255, 196, 0, 255)  # Yellow
  else:
    fill_color = (0, 176, 255, 255)  # Cyan Blue

  # Calculate liquid height inside battery
  inner_top = by1 + 3
  inner_bottom = by2 - 3
  max_liquid_height = inner_bottom - inner_top
  liquid_height = int((percent / 100.0) * max_liquid_height)
  surface_y = inner_bottom - liquid_height

  # Draw sloshing liquid wave
  if percent > 0:
    points = []
    for x in range(bx1 + 3, bx2 - 2):
      wave_offset = math.sin((x * 0.25) + (tick * 0.4)) * 2.5
      y = max(inner_top, min(inner_bottom, surface_y + wave_offset))
      points.append((x, y))

    points.append((bx2 - 3, inner_bottom))
    points.append((bx1 + 3, inner_bottom))
    draw.polygon(points, fill=fill_color)

  # Funny Animation 1: Leaking drops when battery is low (< 25%) and not charging
  if not is_charging and percent < 25 and percent > 0:
    if random.random() < 0.3:
      drops.append([random.randint(bx1 + 6, bx2 - 6), by2])
    for drop in drops[:]:
      drop[1] += 3  # Fall speed
      draw.ellipse(
          [drop[0] - 2, drop[1] - 2, drop[0] + 2, drop[1] + 2], fill=fill_color
      )
      if drop[1] > height:
        drops.remove(drop)

  # Funny Animation 2: Rising bubbles & lightning bolt when charging
  if is_charging:
    # Draw bubbles
    bubble_x = bx1 + 10 + int(math.sin(tick * 0.3) * 8)
    bubble_y = inner_bottom - ((tick * 4) % max(10, liquid_height))
    if bubble_y > surface_y:
      draw.ellipse(
          [bubble_x - 2, bubble_y - 2, bubble_x + 2, bubble_y + 2],
          fill=(255, 255, 255, 200),
      )

    # Draw simple lightning bolt in center
    bolt = [(34, 20), (26, 34), (32, 34), (28, 48), (38, 32), (32, 32)]
    draw.polygon(bolt, fill=(255, 255, 255, 240))

  return img


def update_icon(icon):
  tick = 0
  while running:
    battery = psutil.sensors_battery()
    if battery:
      percent = battery.percent
      is_charging = battery.power_plugged
      status_text = "Charging" if is_charging else "Discharging"
      icon.title = f"Battery: {percent}% ({status_text})"
    else:
      # Fallback simulation for desktop PCs without batteries
      percent = 18
      is_charging = False
      icon.title = "Simulated Battery: 18% (Leaking Mode)"

    icon.icon = create_battery_frame(percent, is_charging, tick)
    tick += 1
    time.sleep(0.15)


def on_quit(icon, item):
  global running
  running = False
  icon.stop()


def main():
  initial_image = create_battery_frame(50, False, 0)
  menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
  icon = pystray.Icon("FunBattery", initial_image, "Fun Battery", menu)

  thread = threading.Thread(target=update_icon, args=(icon,), daemon=True)
  thread.start()
  icon.run()


if __name__ == "__main__":
  main()
