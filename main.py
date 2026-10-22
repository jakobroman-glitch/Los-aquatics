import random
import turtle
import math
import time
from _engine import t, USE_SVG

# Enable RGB color tuples (0-255) on the turtle's drawing screen.
t.getscreen().colormode(255)

# --- BASELINE EXAMPLES ---
def draw_bubble(x, y, radius):
    """
    Draws a single circular bubble using turtle commands.
    
    Args:
        x (int): The x-coordinate for the center of the bubble.
        y (int): The y-coordinate for the center of the bubble.
        radius (int): The size of the bubble.
        
    Returns:
        None
    """
    t.penup()
    t.goto(x, y - radius)
    t.color("white")
    t.pensize(2)
    t.pendown()
    t.circle(radius)
    t.penup()


def draw_seaweed(x, y, segments, color_name, phase=0.0):
    """
    Draws a wavy stalk of seaweed.
    
    Args:
        x (int): The starting x-coordinate for the seaweed.
        y (int): The starting y-coordinate (usually the tank floor).
        segments (int): How tall the seaweed should grow.
        color_name (str): The color of the seaweed.
        phase (float): The animation phase used to sway the stalk.
        
    Returns:
        None
    """
    stem_color = (25, 125, 48) if color_name == "darkgreen" else (35, 175, 55)
    highlight_color = (115, 230, 75)
    leaf_colors = ((54, 195, 66), (85, 215, 55), (38, 165, 58))

    t.color(stem_color)
    t.pensize(6)
    leaf_bases = []
    stem_points = [(x, y)]

    for segment in range(segments):
        mid_y = y + segment * 30 + 15
        end_y = y + (segment + 1) * 30
        base_x = x + segment * 3.9
        mid_sway = 5 * math.sin(phase + (segment + 0.5) * 0.48)
        end_sway = 5 * math.sin(phase + (segment + 1) * 0.48)
        leaf_bases.append((base_x + mid_sway, mid_y))
        stem_points.extend((
            (base_x + mid_sway, mid_y),
            (x + (segment + 1) * 3.9 + end_sway, end_y),
        ))

    t.penup()
    t.goto(*stem_points[0])
    t.pendown()
    for point in stem_points[1:]:
        t.goto(*point)
    t.penup()
    t.color(highlight_color)
    t.pensize(2)
    t.goto(stem_points[0][0] - 1, stem_points[0][1])
    t.pendown()
    for point_x, point_y in stem_points[1:]:
        t.goto(point_x - 1, point_y)
    t.penup()

    for index, (base_x, base_y) in enumerate(leaf_bases):
        side = -1 if index % 2 else 1
        length = 11 + (index % 3) * 2
        tip_x = base_x + side * length
        tip_y = base_y + 4 + (index % 2) * 2
        width = 4
        t.color((22, 125, 44), leaf_colors[index % len(leaf_colors)])
        t.pensize(1)
        t.penup()
        t.goto(base_x, base_y)
        t.pendown()
        t.begin_fill()
        t.goto(base_x + side * width, base_y + 5)
        t.goto(tip_x, tip_y)
        t.goto(base_x + side * width, base_y - 2)
        t.goto(base_x, base_y)
        t.end_fill()
        t.penup()


# --- STUDENT FUNCTIONS ---
def draw_tank(build_left, build_bottom, build_right, build_top):
    """
    Draws the 4 walls of the rectangular fish tank using the turtle.
    
    Args:
        build_left (bool): If True, draws the left wall.
        build_bottom (bool): If True, draws the floor of the tank.
        build_right (bool): If True, draws the right wall.
        build_top (bool): If True, draws the lid of the tank.
        
    Returns:
        None
    """
    t.color("blue")
    t.pensize(3)    
    t.fillcolor("lightblue")
    t.begin_fill()
    
    t.penup()
    t.goto(-380, 280)
    t.setheading(270) 

    walls = [build_left, build_bottom, build_right, build_top]
    
    for i in range(4):
        if walls[i]:
            t.pendown()
        else:
            t.penup()

        if i % 2 == 0:
            t.forward(560) # Vertical walls
        else:
            t.forward(760) # Horizontal walls
        t.left(90)

    t.end_fill()


def draw_sand():
    """
    Draws a cream-colored strip of sand along the bottom of the aquarium.

    Args:
        None

    Returns:
        None
    """
    def surface_height(x):
        return -251 + 2.8 * math.sin(x * 0.035) + 1.5 * math.sin(x * 0.11)

    surface = [(x, surface_height(x)) for x in range(-378, 379, 12)]
    t.penup()
    t.goto(-378, -278)
    t.color("tan", "wheat")
    t.pendown()
    t.begin_fill()
    t.goto(378, -278)
    for point in reversed(surface):
        t.goto(*point)
    t.goto(-378, -278)
    t.end_fill()

    grain_colors = ("tan", "#c7ad7e", "#d5bf96", "#b99b6d")
    for row, y in enumerate(range(-273, -238, 7)):
        offset = 0 if row % 2 == 0 else 8
        for column, x in enumerate(range(-369 + offset, 370, 16)):
            if y < surface_height(x):
                grain = (row * 7 + column * 3) % len(grain_colors)
                size = 2 if (row + column) % 4 else 3
                t.penup()
                t.goto(x, y)
                t.dot(size, grain_colors[grain])

    t.penup()


def draw_fish(x, y, size, is_facing_left):
    """
    Draws a rounded fish with a tail, fin, gill, and eye.
    
    Args:
        x (int): The x-coordinate for the fish center.
        y (int): The y-coordinate for the fish center.
        size (int): The scale of the fish.
        is_facing_left (bool): If True, draws the fish facing left. 
                               If False, draws it facing right.
        
    Returns:
        None
    """
    direction = -1 if is_facing_left else 1

    def move_to(local_x, local_y):
        t.goto(x + direction * local_x, y + local_y)

    def draw_triangle(points, outline, fill):
        t.color(outline, fill)
        t.penup()
        move_to(*points[0])
        t.pendown()
        t.begin_fill()
        for point in points[1:]:
            move_to(*point)
        t.goto(x + direction * points[0][0], y + points[0][1])
        t.end_fill()

    # Tail, behind the body
    draw_triangle(
        [(-size * 0.8, 0), (-size * 1.6, size * 0.65),
         (-size * 1.6, -size * 0.65)],
        "darkorange",
        "orange",
    )

    # Rounded body made from two smooth curves
    upper = []
    lower = []
    for step in range(21):
        progress = step / 20
        inverse = 1 - progress
        upper.append((
            -size + 2 * size * progress,
            3 * size * 0.8 * inverse * inverse * progress
            + 3 * size * 0.8 * inverse * progress * progress,
        ))
        lower.append((
            size - 2 * size * progress,
            -(3 * size * 0.8 * inverse * inverse * progress
              + 3 * size * 0.8 * inverse * progress * progress),
        ))

    t.color("darkorange", "gold")
    t.penup()
    move_to(*upper[0])
    t.pendown()
    t.begin_fill()
    for point in upper[1:] + lower:
        move_to(*point)
    t.goto(x - direction * size, y)
    t.end_fill()

    # Lower fin
    draw_triangle(
    [(-size * 0.15, -size * 0.48), (size * 0.35, -size * 0.48),
     (size * 0.05, -size * 0.9)],
    "darkorange",
    "orange",
    )

    # Gill and eye
    t.color("darkorange")
    t.pensize(max(1, size // 12))
    t.penup()
    move_to(size * 0.35, size * 0.42)
    t.pendown()
    move_to(size * 0.48, 0)
    move_to(size * 0.35, -size * 0.42)

    t.penup()
    move_to(size * 0.62, size * 0.22)
    t.dot(max(4, size * 0.28), "white")
    t.dot(max(2, size * 0.14), "black")

def draw_crab(x, y, size, is_facing_left):
    """
    Draws a crab with an oval shell, legs, pincers, and eyes.

    Args:
        x (int): The x-coordinate for the crab center.
        y (int): The y-coordinate for the crab center.
        size (int): The scale of the crab.
        is_facing_left (bool): If True, the crab faces left.

    Returns:
        None
    """
    direction = -1 if is_facing_left else 1

    def move_to(local_x, local_y):
        t.goto(x + direction * local_x, y + local_y)

    def draw_line(points, color, width):
        t.color(color)
        t.pensize(max(1, int(size * width)))
        t.penup()
        move_to(*points[0])
        t.pendown()
        for point in points[1:]:
            move_to(*point)
        t.penup()

    def draw_polygon(points, outline, fill):
        t.color(outline, fill)
        t.penup()
        move_to(*points[0])
        t.pendown()
        t.begin_fill()
        for point in points[1:]:
            move_to(*point)
        move_to(*points[0])
        t.end_fill()
        t.penup()

    # Legs behind the shell
    for leg_x in (-0.75, -0.25, 0.25, 0.75):
        draw_line(
            [(leg_x * size, -size * 0.35),
             ((leg_x - 0.25) * size, -size * 0.75),
             ((leg_x - 0.4) * size, -size * 0.9)],
            "darkred",
            0.09,
        )

    # Arms and pincers
    draw_line(
        [(size * 0.55, size * 0.2), (size * 0.9, size * 0.55),
         (size * 1.15, size * 0.65)],
        "darkred",
        0.12,
    )
    draw_line(
        [(size * 0.45, -size * 0.15), (size * 0.85, -size * 0.45),
         (size * 1.1, -size * 0.5)],
        "darkred",
        0.12,
    )
    draw_polygon(
        [(size * 1.05, size * 0.55), (size * 1.42, size * 0.85),
         (size * 1.35, size * 0.55), (size * 1.48, size * 0.3),
         (size * 1.12, size * 0.4)],
        "darkred",
        "tomato",
    )
    draw_polygon(
        [(size * 1.0, -size * 0.5), (size * 1.38, -size * 0.25),
         (size * 1.3, -size * 0.5), (size * 1.42, -size * 0.75),
         (size * 1.08, -size * 0.68)],
        "darkred",
        "tomato",
    )

    # Rounded shell
    shell_points = [
        (1.15 * size * math.cos(math.radians(angle)),
         0.72 * size * math.sin(math.radians(angle)))
        for angle in range(0, 360, 10)
    ]
    draw_polygon(shell_points, "#8b1a1a", "#dc143c")

    # Shell detail and eye stalks
    draw_line(
        [(-size * 0.65, size * 0.1), (0, size * 0.42),
         (size * 0.65, size * 0.1)],
        "salmon",
        0.06,
    )
    for eye_x in (size * 0.35, size * 0.75):
        draw_line(
            [(eye_x, size * 0.48), (eye_x + size * 0.08, size * 0.78)],
            "darkred",
            0.08,
        )
        t.penup()
        move_to(eye_x + size * 0.08, size * 0.82)
        t.dot(max(5, int(size * 0.38)), "white")
        t.dot(max(3, int(size * 0.19)), "black")


def draw_shark(x, y, size, is_facing_left, mouth_open=0.0):
    """
    Draws an original, cinematic great white shark with detailed features.

    Args:
        x (int): The x-coordinate for the shark center.
        y (int): The y-coordinate for the shark center.
        size (int): The scale of the shark.
        is_facing_left (bool): If True, the shark faces left.
        mouth_open (float): How far the shark opens its jaw, from 0 to 1.

    Returns:
        None
    """
    direction = -1 if is_facing_left else 1

    def move_to(local_x, local_y):
        t.goto(x + direction * local_x * size * 1.25, y + local_y * size)

    def draw_polygon(points, outline, fill):
        t.color(outline, fill)
        t.penup()
        move_to(*points[0])
        t.pendown()
        t.begin_fill()
        for point in points[1:]:
            move_to(*point)
        move_to(*points[0])
        t.end_fill()
        t.penup()

    def draw_line(points, color, width):
        t.color(color)
        t.pensize(max(1, int(size * width)))
        t.penup()
        move_to(*points[0])
        t.pendown()
        for point in points[1:]:
            move_to(*point)
        t.penup()

    def curve(start, control1, control2, end, steps=12):
        points = []
        for step in range(steps + 1):
            progress = step / steps
            inverse = 1 - progress
            points.append((
                inverse ** 3 * start[0]
                + 3 * inverse ** 2 * progress * control1[0]
                + 3 * inverse * progress ** 2 * control2[0]
                + progress ** 3 * end[0],
                inverse ** 3 * start[1]
                + 3 * inverse ** 2 * progress * control1[1]
                + 3 * inverse * progress ** 2 * control2[1]
                + progress ** 3 * end[1],
            ))
        return points

    outline = "#253944"
    body_color = "#527386"

    # The tail overlaps the body, with straighter lobes in the same skin color.
    draw_polygon(
        [(-1.1, 0.16), (-1.78, 0.9), (-1.55, 0.1),
         (-1.77, -0.62), (-1.1, -0.2)],
        outline, body_color,
    )
    draw_polygon(
        curve((-0.84, 0.31), (-0.8, 0.47), (-0.68, 0.56), (-0.59, 0.51))
        + curve((-0.59, 0.51), (-0.5, 0.46), (-0.43, 0.37), (-0.34, 0.34))[1:]
        + curve((-0.34, 0.34), (-0.51, 0.39), (-0.7, 0.36), (-0.84, 0.31))[1:],
        outline, "#607e8e",
    )
    draw_polygon(
        curve((-0.72, -0.28), (-0.69, -0.4), (-0.62, -0.49), (-0.55, -0.45))
        + curve((-0.55, -0.45), (-0.47, -0.4), (-0.4, -0.34), (-0.34, -0.3))[1:]
        + curve((-0.34, -0.3), (-0.48, -0.32), (-0.6, -0.3), (-0.72, -0.28))[1:],
        outline, "#607e8e",
    )

    # Compact, curved dorsal and pectoral fins are tucked under the body.
    draw_polygon(
        curve((-0.4, 0.52), (-0.43, 0.74), (-0.52, 1.04), (-0.35, 1.1))
        + curve((-0.35, 1.1), (-0.16, 1.08), (0.16, 0.72), (0.48, 0.48))[1:]
        + curve((0.48, 0.48), (0.13, 0.57), (-0.18, 0.59), (-0.4, 0.52))[1:],
        outline, "#58788a",
    )
    draw_polygon(
        curve((0.57, -0.15), (0.28, -0.23), (-0.11, -0.48), (-0.46, -0.73))
        + curve((-0.46, -0.73), (-0.36, -0.48), (-0.19, -0.27), (0.08, -0.17))[1:]
        + curve((0.08, -0.17), (0.25, -0.13), (0.43, -0.13), (0.57, -0.15))[1:],
        outline, "#617f8e",
    )

    # The rear body stays full before smoothly tapering into the tail root.
    top = curve((-1.42, 0.12), (-1.19, 0.29), (-0.92, 0.58), (-0.24, 0.7))
    top.append((0.48, 0.7))
    belly_tip = (1.98, 0.12)
    top += curve((0.48, 0.7), (0.92, 0.66), (1.52, 0.3), belly_tip)[1:]
    bottom = curve(belly_tip, (1.79, 0.03), (1.57, 0.02), (1.42, -0.06))
    bottom += curve((1.42, -0.06), (1.2, -0.14), (1.02, -0.26), (0.82, -0.32))[1:]
    bottom += curve((0.82, -0.32), (0.27, -0.53), (-0.7, -0.42), (-1.02, -0.28))[1:]
    bottom += curve((-1.02, -0.28), (-1.23, -0.2), (-1.34, -0.07), (-1.42, 0.12))[1:]
    draw_polygon(top + bottom[1:], outline, body_color)

    # A darker blue-gray saddle follows the back and fades into the flanks.
    back = curve((-0.93, 0.22), (-0.76, 0.52), (-0.2, 0.69), (0.38, 0.55))
    back += curve((0.38, 0.55), (0.82, 0.46), (1.22, 0.27), (1.58, 0.2))[1:]
    back += curve((1.58, 0.2), (1.12, 0.25), (0.71, 0.37), (0.3, 0.4))[1:]
    back += curve((0.3, 0.4), (-0.23, 0.45), (-0.65, 0.34), (-0.93, 0.22))[1:]
    draw_polygon(back, "#527386", "#496879")
    draw_line(
        [(-0.73, 0.22), (-0.35, 0.38), (0.08, 0.4), (0.48, 0.31)],
        "#829aa4",
        0.014,
    )

    # Bright underside with a curved, rising boundary.
    belly = curve((-1.42, 0.12), (-1.22, -0.02), (-1.02, -0.14), (-0.84, -0.12))
    belly += curve((-0.84, -0.12), (-0.47, -0.24), (-0.18, -0.19), (0.08, -0.25))[1:]
    belly += curve((0.08, -0.25), (0.35, -0.33), (0.49, -0.13), (0.75, -0.16))[1:]
    belly += curve((0.75, -0.16), (1.12, -0.17), (1.62, 0.18), belly_tip)[1:]
    belly += curve(belly_tip, (1.56, -0.02), (1.3, -0.27), (1.12, -0.36))[1:]
    belly += curve((1.12, -0.36), (0.76, -0.46), (0.38, -0.48), (0.04, -0.45))[1:]
    belly += curve((0.04, -0.45), (-0.42, -0.48), (-1.08, -0.27), (-1.42, 0.12))[1:]
    draw_polygon(belly, body_color, "#ffffff")

    mouth_corner = (1.78, 0.07)
    jaw_drop = 0.24 * max(0.0, min(1.0, mouth_open))
    lower_corner = (mouth_corner[0], mouth_corner[1] - jaw_drop)
    mouth = curve(mouth_corner, (1.59, 0.04), (1.38, 0.0), (1.16, -0.035))
    mouth += curve(
        (1.16, -0.035),
        (1.37, -0.25 - jaw_drop * 0.8),
        (1.62, -0.22 - jaw_drop * 0.9),
        lower_corner,
    )[1:]
    draw_polygon(mouth, outline, "#35454d")
    upper_teeth = (
        [(1.2, -0.03), (1.34, -0.01), (1.29, -0.075)],
        [(1.38, 0.0), (1.53, 0.025), (1.48, -0.055)],
        [(1.57, 0.03), (1.72, 0.06), (1.67, -0.025)],
    )
    lower_teeth = (
        [(1.22, -0.075), (1.36, -0.105), (1.33, -0.025)],
        [(1.4, -0.16), (1.55, -0.18), (1.52, -0.02)],
        [(1.59, -0.15), (1.73, -0.115), (1.69, 0.02)],
    )
    for tooth_points in upper_teeth:
        draw_polygon(tooth_points, "#dce4e5", "#ffffff")
    for tooth_points in lower_teeth:
        lowered_teeth = [
            (tooth_x, tooth_y - jaw_drop * 0.85)
            for tooth_x, tooth_y in tooth_points
        ]
        draw_polygon(lowered_teeth, "#dce4e5", "#ffffff")

    # Fins overlap the body at their roots, leaving only their curved tips exposed.
    draw_line([(-0.35, 1.0), (0.08, 0.66)], "#8ba2ae", 0.018)
    draw_line([(-0.2, 0.98), (0.21, 0.64)], "#758f9d", 0.014)
    draw_line([(0.3, -0.34), (-0.31, -0.63)], "#8ba2ae", 0.018)
    draw_line([(0.18, -0.32), (-0.25, -0.56)], "#7b94a1", 0.014)
    draw_line([(-1.49, 0.48), (-1.2, 0.1)], "#879eaa", 0.018)
    draw_line([(-1.51, 0.24), (-1.25, 0.04)], "#7b94a1", 0.014)
    draw_line([(-1.48, -0.3), (-1.23, -0.12)], "#7b94a1", 0.014)
    draw_line([(-1.65, 0.57), (-1.57, 0.3), (-1.48, 0.12)],
              "#8299a4", 0.012)
    draw_line([(-1.66, -0.42), (-1.56, -0.2), (-1.47, -0.08)],
              "#8299a4", 0.012)
    draw_line([(-0.36, 0.98), (-0.27, 0.77), (-0.08, 0.59)],
              "#91a7b1", 0.012)
    draw_line([(-0.28, 0.94), (-0.12, 0.77), (0.13, 0.6)],
              "#78929f", 0.01)
    draw_line([(0.42, -0.2), (0.16, -0.35), (-0.12, -0.51)],
              "#8ba2ae", 0.012)

    # A restrained lateral line and a few mottled markings add texture.
    draw_line([(-0.82, 0.08), (-0.4, 0.17), (0.02, 0.16), (0.42, 0.1)],
              "#3d5b6b", 0.018)
    draw_line([(-0.78, 0.015), (-0.38, 0.075), (0.02, 0.07)],
              "#718b98", 0.012)
    draw_line([(-0.7, -0.04), (-0.32, 0.015), (0.06, 0.005),
               (0.43, -0.045)], "#8299a4", 0.009)
    for spot_x, spot_y, spot_scale in (
        (-0.78, 0.17, 0.022), (-0.67, 0.27, 0.028),
        (-0.56, 0.19, 0.018), (-0.43, 0.38, 0.025),
        (-0.31, 0.25, 0.018), (-0.18, 0.43, 0.026),
        (-0.06, 0.28, 0.02), (0.08, 0.37, 0.024),
        (0.2, 0.24, 0.018), (0.3, 0.28, 0.023),
        (0.4, 0.18, 0.017), (0.51, 0.2, 0.02),
        (-0.62, 0.02, 0.014), (-0.46, -0.07, 0.016),
        (-0.22, 0.08, 0.014), (0.02, -0.04, 0.014),
        (0.82, 0.15, 0.016), (0.96, 0.08, 0.014),
    ):
        t.penup()
        move_to(spot_x, spot_y)
        t.dot(max(2, int(size * spot_scale)), "#405d6d")

    # Five gills with a soft edge and highlight make them read as folds.
    for gill_x in (0.23, 0.36, 0.49, 0.62, 0.75):
        draw_line(
            [(gill_x, 0.39), (gill_x - 0.02, 0.24),
             (gill_x - 0.035, 0.08), (gill_x - 0.04, -0.06)],
            "#344b58", 0.026,
        )
        draw_line(
            [(gill_x + 0.025, 0.34), (gill_x + 0.005, 0.22),
             (gill_x - 0.005, 0.1)],
            "#7f96a0", 0.012,
        )

    # Small nostril and socket frame the subdued, dark eye.
    t.penup()
    move_to(1.56, 0.14)
    t.dot(max(2, int(size * 0.035)), "#263d49")
    move_to(1.04, 0.24)
    t.dot(max(9, int(size * 0.14)), "#91a4aa")
    move_to(1.04, 0.24)
    t.dot(max(7, int(size * 0.105)), "#293b45")
    move_to(1.055, 0.265)
    t.dot(max(2, int(size * 0.035)), "#e8f0f0")

    t.penup()


def draw_creature(creature_type, x, y, size, is_facing_left, mouth_open=0.0):
    """
    Dispatcher function to draw different creatures based on parameters.

    Args:
        creature_type (str): The type of creature to draw (e.g., "fish").
        x (int): The x-coordinate for the creature.
        y (int): The y-coordinate for the creature.
        size (int): The scale or radius of the creature.
        is_facing_left (bool): If True, draws the creature facing left.
                               If False, draws it facing right.
        mouth_open (float): Shark jaw opening amount, from 0 to 1.

    Returns:
        None
    """
    if creature_type == "fish" and is_facing_left:
        draw_fish(x, y, size, True)
    elif creature_type == "fish" and not is_facing_left:
        draw_fish(x, y, size, False)
    elif creature_type == "crab" and is_facing_left:
        draw_crab(x, y, size, True)
    elif creature_type == "crab" and not is_facing_left:
        draw_crab(x, y, size, False)
    elif creature_type == "shark" and is_facing_left:
        draw_shark(x, y, size, True, mouth_open)
    elif creature_type == "shark" and not is_facing_left:
        draw_shark(x, y, size, False, mouth_open)

def draw_environment(elapsed=0.0):
    """
    Draws the background elements of the tank, including bubbles and seaweed.
    
    Args:
        None
        
    Returns:
        None
    """
    bubble_rng = random.Random(1729)
    for index in range(9):
        bubble_radius = 7 + index % 3 * 2
        bubble_x = bubble_rng.randint(-370 + bubble_radius, 370 - bubble_radius)
        bubble_y = -245 + (elapsed * 24 + index * 61) % 480
        draw_bubble(bubble_x, bubble_y, bubble_radius)

    for i, x in enumerate(range(-300, 301, 100)):
        if i % 2 == 0:
            draw_seaweed(x, -280, 6, "green", elapsed * 1.4 + i)
        else:
            draw_seaweed(x, -280, 4, "darkgreen", elapsed * 1.4 + i)


def draw_scene(elapsed=0.0):
    """Draws one aquarium frame at the given animation time."""
    draw_tank(True, True, True, True)
    draw_sand()
    draw_environment(elapsed)

    for i in range(6):
        for row, (base_x, base_y, size, speed) in enumerate((
            (-220 + i * 80, 80 - (i % 3) * 30, 20, 1),
            (-180 + i * 70, -40 + (i % 2) * 25, 18, -1),
        )):
            x = -350 + (base_x + 350 + speed * elapsed * 32) % 700
            y = base_y + math.sin(elapsed * 2.2 + i + row) * 5
            draw_creature("fish", x, y, size, speed < 0)

    for index, (base_x, base_y, size) in enumerate(((0, -120, 16), (180, -90, 18))):
        crab_phase = elapsed * 0.8 + index * math.pi
        crab_x = base_x + math.sin(crab_phase) * 18
        crab_y = base_y + math.sin(crab_phase * 1.5) * 2
        draw_creature("crab", crab_x, crab_y, size, math.cos(crab_phase) < 0)

    shark_phase = (elapsed * 16) % 640
    if shark_phase <= 320:
        shark_x = -160 + shark_phase
        shark_faces_left = False
    else:
        shark_x = 160 - (shark_phase - 320)
        shark_faces_left = True
    shark_y = 155 + math.sin(elapsed * 1.3) * 4
    jaw_open = (1 + math.sin(elapsed * 2.4)) / 2
    draw_creature("shark", shark_x, shark_y, 75, shark_faces_left, jaw_open)

def main():
    """
    Main execution function to assemble the fish tank.
    
    Args:
        None
        
    Returns:
        None
    """
    draw_scene()


def animate_aquarium():
    screen = turtle.Screen()
    screen.tracer(0, 0)
    start_time = time.perf_counter()

    def animate_frame():
        elapsed = time.perf_counter() - start_time
        t.clear()
        draw_scene(elapsed)
        screen.update()
        screen.ontimer(animate_frame, 50)

    animate_frame()


if __name__ == "__main__":
    if USE_SVG:
        main()
        t.save_as('my_fishtank.svg')
        print("Successfully saved my_fishtank.svg")
    else:
        animate_aquarium()
        turtle.done()