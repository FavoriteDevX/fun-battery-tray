import ctypes
import math
import random
import tkinter as tk
import psutil


class GradualWaterBattery:

  def __init__(self):
    self.root = tk.Tk()
    self.transparent_color = "#010101"
    self.root.overrideredirect(True)
    self.root.attributes("-topmost", True)
    self.root.attributes("-transparentcolor", self.transparent_color)
    self.root.config(bg=self.transparent_color)

    self.width = self.root.winfo_screenwidth()
    self.height = 140
    screen_h = self.root.winfo_screenheight()

    self.root.geometry(
        f"{self.width}x{self.height}+0+{screen_h - self.height}"
    )

    self.canvas = tk.Canvas(
        self.root,
        width=self.width,
        height=self.height,
        bg=self.transparent_color,
        highlightthickness=0,
    )
    self.canvas.pack()

    self.hwnd = None
    self.setup_window_styles()

    self.tick = 0
    self.charge = 96.0
    self.drops = []
    self.water_height = 0.0
    self.water_spread = 0.0
    self.demo_mode = True  # Set False to trigger only when plugged in

    self.animate()
    self.root.mainloop()

  def setup_window_styles(self):
    try:
      self.root.update_idletasks()
      self.hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
      style = ctypes.windll.user32.GetWindowLongW(self.hwnd, -20)
      ctypes.windll.user32.SetWindowLongW(
          self.hwnd, -20, style | 0x80000 | 0x20 | 0x80
      )
    except Exception:
      pass

  def keep_on_top(self):
    try:
      if self.hwnd:
        ctypes.windll.user32.SetWindowPos(
            self.hwnd, -1, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0010
        )
    except Exception:
      pass

  def animate(self):
    if self.tick % 25 == 0:
      self.keep_on_top()

    self.canvas.delete("all")

    battery = psutil.sensors_battery()
    real_percent = float(battery.percent) if battery else 96.0
    is_charging = battery.power_plugged if battery else True

    base_x = self.width - 142
    base_y = self.height - 31

    if is_charging or self.demo_mode:
      self.charge += 0.35
      display_pct = int(self.charge)
      overflow = max(0.0, self.charge - 100.0)

      shake = 1 if overflow > 15 else 0
      sx = random.randint(-shake, shake) if shake else 0
      sy = random.randint(-shake, shake) if shake else 0

      bx, by = base_x + sx, base_y + sy
      bw, bh = 22, 12

      # Battery frame
      self.canvas.create_rectangle(
          bx, by, bx + bw, by + bh, fill="#181818", outline="white", width=1
      )
      self.canvas.create_rectangle(
          bx + bw, by + 3, bx + bw + 2, by + bh - 3, fill="white", outline=""
      )

      # Liquid bar bulging slightly out
      normal_fill = min(1.0, self.charge / 100.0) * (bw - 2)
      bulge = min(18.0, overflow * 0.15)
      total_bar_w = int(normal_fill + bulge)

      water_main = "#00E575"
      water_highlight = "#80FFEA"

      self.canvas.create_rectangle(
          bx + bw - 2 - total_bar_w,
          by + 2,
          bx + bw - 2,
          by + bh - 2,
          fill=water_main,
          outline="",
      )

      if overflow > 0:
        self.canvas.create_text(
            bx + bw - total_bar_w - 24,
            by + 6,
            text=f"{display_pct}%",
            fill=water_highlight,
            font=("Segoe UI", 9, "bold"),
        )

      # Gradual dripping once past 100%
      if overflow > 1.0:
        drip_chance = min(0.90, 0.15 + (overflow * 0.01))
        if random.random() < drip_chance:
          leak_x = bx + bw - 2 - total_bar_w + random.uniform(-2, 4)
          self.drops.append({
              "x": leak_x,
              "y": float(by + bh - 2),
              "vx": random.uniform(-1.8, 0.4),
              "vy": random.uniform(0.3, 1.3),
              "sz": random.uniform(1.8, 2.8),
          })

        target_height = min(14.0, overflow * 0.08)
        if self.water_height < target_height:
          self.water_height += 0.05

        if self.water_height > 1.2 and self.water_spread < self.width:
          self.water_spread += min(4.0, 0.8 + (overflow * 0.025))
    else:
      self.charge = real_percent
      self.water_height = max(0.0, self.water_height - 0.1)
      self.water_spread = max(0.0, self.water_spread - 4.0)

    # Update falling droplets safely using dictionary keys
    active_drops = []
    for drop in self.drops:
      drop["x"] += drop["vx"]
      drop["y"] += drop["vy"]
      drop["vy"] += 0.35

      x = drop["x"]
      y = drop["y"]
      sz = drop["sz"]

      self.canvas.create_oval(
          x - sz, y - sz * 1.3, x + sz, y + sz * 1.3, fill="#00E575", outline=""
      )

      if y < self.height - self.water_height:
        active_drops.append(drop)
    self.drops = active_drops

    # Draw smooth flowing water along the bottom edge
    if self.water_height > 0.3:
      start_x = max(0, int(self.width - self.water_spread))
      wave_pts = [start_x, self.height]
      highlight_pts = []

      for x in range(start_x, self.width + 10, 8):
        dist_from_tip = x - start_x
        taper = min(1.0, dist_from_tip / 90.0)
        ripple = math.sin((x * 0.06) + (self.tick * 0.25)) * 1.5 * taper
        y = self.height - (self.water_height * taper) + ripple

        wave_pts.extend([x, y])
        highlight_pts.extend([x, y + 1])

      wave_pts.extend([self.width, self.height])
      self.canvas.create_polygon(wave_pts, fill="#00E575", outline="")

      if len(highlight_pts) >= 4:
        self.canvas.create_line(
            highlight_pts, fill="#80FFEA", width=1, smooth=True
        )

    self.tick += 1
    self.root.after(40, self.animate)


if __name__ == "__main__":
  GradualWaterBattery()
