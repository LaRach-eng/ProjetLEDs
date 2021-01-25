import time

LED_COUNT = 300

x = 12  # Number of LEDs in a unit distance
a = list(range(5 * x))
b_0 = list(range(a[-1] + 1, a[-1] + 1 + 4 * x))
b_1 = list(range(b_0[-1] + 1, b_0[-1] + 1 + 4 * x))
c_0 = list(range(b_1[-1] + 1, b_1[-1] + 1 + 3 * x))
c_1 = list(range(c_0[-1] + 1, c_0[-1] + 1 + 3 * x))
d_0 = list(range(c_1[-1] + 1, c_1[-1] + 1 + 2 * x))
d_1 = list(range(d_0[-1] + 1, d_0[-1] + 1 + 2 * x))
e_0 = list(range(d_1[-1] + 1, d_1[-1] + 1 + x))
e_1 = list(range(e_0[-1] + 1, e_0[-1] + 1 + x))

all_segments = [a, b_0, b_1, c_0, c_1, d_0, d_1, e_0, e_1]

vertical_indices = a + b_1 + c_1 + d_1 + e_1
horizontal_indices = b_0 + c_0 + d_0 + e_0
all_indices = list(range(LED_COUNT))


def Color(r, g, b):
    return [r, g, b]


RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

# ====================================== FUNCTIONS 👇🏼 ====================================== #


def rgb_basic(strip, wait_ms=0):
    strip.set_color_list(vertical_indices, RED)
    strip.set_color_list(horizontal_indices, BLUE)
    strip.show()
    time.sleep(wait_ms / 1000.0)
    strip.set_color_list(all_indices, GREEN)
    strip.show()
    time.sleep(wait_ms / 1000.0)


def rainbow_wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rotate_colors(strip, wait_ms=0):
    colors = [RED, GREEN, BLUE]
    for _ in range(1000):
        print(_)
        for i in range(3):
            strip.set_color_list(vertical_indices, colors[i])
            strip.set_color_list(horizontal_indices, colors[(i + 1) % 3])
            strip.show()
            time.sleep(wait_ms / 1000.0)


def balaye_segs(strip, segs, color_segs, total_time):
    # Cette fonction balaye les segments de segs avec les nouvelles couleurs colors segs et ce en en temps time
    segs_step_dict = {}
    for i in range(len(segs)):
        segs_step_dict[i] = total_time / len(segs[i])

    # on crée le calendrier des events
    events = {}
    for i in range(len(segs)):
        time_step = segs_step_dict[i]
        color_ = color_segs[i]
        for j in range(len(segs[i])):
            date = time_step * j
            if date not in events.keys():
                events[date] = []

            events[date].append((segs[i][j], color_))
    # Maintenant nous devons lire le calendrier des events
    sorted_dates = list(events.keys())
    sorted_dates.sort()

    # Initialisation à la date 0
    for event in events[0]:
        index_, color_ = event
        strip.setPixelColor(index_, color_)

    previous_date = 0
    for i in range(1, len(sorted_dates)):
        new_date = sorted_dates[i]
        delay = new_date - previous_date
        # time.sleep(delay)
        if i % 2 == 0:
            strip.show()

        for event in events[new_date]:
            index_, color_ = event
            strip.setPixelColor(index_, color_)
        previous_date = new_date


def spirale_balaye(strip, segs, possible_color, total_time):
    # initialisation
    segs_color_index = []
    segs_color = []
    for i in range(len(segs)):
        color_index = i % len(possible_color)
        segs_color_index.append(color_index)
        segs_color.append(possible_color[color_index])

    while True:
        balaye_segs(strip, segs, segs_color, total_time)
        segs_color_index = [
            (index_ - 1) % len(possible_color) for index_ in segs_color_index
        ]
        segs_color = [possible_color[color_index] for color_index in segs_color_index]


def spirale_balaye_rainbow_wheel(strip, segs, intial_color_pos, total_time):
    # initialisation
    segs_color_index = []
    segs_color = []
    for i in range(len(segs)):
        color_index = i % len(intial_color_pos)
        segs_color_index.append(color_index)
        segs_color.append(rainbow_wheel(intial_color_pos[color_index]))

    while True:
        balaye_segs(strip, segs, segs_color, total_time)
        segs_color_index = [
            (index_ - 1) % len(intial_color_pos) for index_ in segs_color_index
        ]
        segs_color = [
            rainbow_wheel(intial_color_pos[color_index])
            for color_index in segs_color_index
        ]

        # On shift les couleurs de 1:

        for i in range(len(intial_color_pos)):
            intial_color_pos[i] = (intial_color_pos[i] + 10) % 255


# def three_dimensions(strip, wait_ms=0):
#     pairs_c_1 = [c_1[i] for i in range(len(c_1)) if i % 2 == 0]
#     pairs_c_1_ext = [pairs_c_1[i] for i in range(len(pairs_c_1)) if i < len(pairs_c_1)/2]
#     pairs_c_1_int = [pairs_c_1[i] for i in range(len(pairs_c_1)) if i >= len(pairs_c_1)/2]
#     a_int = [a[i] for i in]


def spirale(strip, colors, wait_ms=10):
    # Initialisation
    strips_color_index = [i % len(colors) for i in range(len(all_segments))]

    while True:
        for i in range(len(strips_color_index)):
            strips_color_index[i] = (strips_color_index[i] + 1) % len(colors)
            strip.set_color_list(all_segments[i], colors[strips_color_index[i]])

        strip.show()
        time.sleep(wait_ms / 1000.0)