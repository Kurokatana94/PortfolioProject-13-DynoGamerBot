from PIL import Image
import numpy as np
import mss
import keyboard
import time

min_y = 700
min_x = 290
med_y = 750
med_x = 400
max_y = 800
max_x = 720

y_dif = 1
x_dif = 40

#     700
# 490     720
#     900

# All commented values are for simpler visualization, but could change (no hardcoding here)
high_y = 0  # 700 - 700
high_x_start = 480 - min_x  # 100
high_x_end = high_x_start + x_dif # 140

med_y = med_y - min_y  # 20
med_x_start = med_x - min_x  # 30
med_x_end = med_x_start + x_dif # 70

low_y = max_y - min_y - 1  # 99
low_x_start = 0
low_x_end = x_dif

BOX = {'top': max_y,
       'left': min_x,
       'width': max_x - min_x,
       'height': max_y - min_y}

def is_obstacle() -> tuple:
    sct = mss.mss()
    # img_sample = sct.grab(BOX)
    # full_screen_sample = sct.grab((0,0,2560,1440))
    bot_fov = np.array(sct.grab(BOX))[:, :, :3]

    slice_high = bot_fov[high_y, high_x_start:high_x_end, :]
    slice_med = bot_fov[med_y, med_x_start:med_x_end, :]
    slice_low = bot_fov[low_y, low_x_start:low_x_end, :]

    color = np.array(sct.grab({
        'top': 800,
        'left': 10,
        'width': 1,
        'height': 1,
    }))[:, :, :3][0,0]

    for label, sl in [('high', slice_high), ('med', slice_med), ('low', slice_low)]:
        if (sl != color).all(axis=1).any():

            # img = Image.frombytes('RGB', img_sample.size, img_sample.rgb)
            # screen = Image.frombytes('RGB', full_screen_sample.size, full_screen_sample.rgb)
            # img.save("debug_capture.png")
            # screen.save("debug_screen.png")

            return True, label
    return False, ''

# Makes the dyno jump low
def short_jump():
    keyboard.press('space')
    time.sleep(.02)
    keyboard.release('space')

# Makes the dyno jump high
def long_jump():
    keyboard.press('space')
    time.sleep(.2)
    keyboard.release('space')

def main():
    n = 0
    print('Starting...')
    time.sleep(3)
    while True:
        start = time.time()
        if keyboard.is_pressed('q'):
            break

        check_result = is_obstacle()

        if check_result[0] and check_result[1] == 'low':
            short_jump()
            n+=1
            print('jump low', n)
            # break
        elif check_result[0]:
            long_jump()
            n+=1
            print(f'jump {check_result[1]}', n)
            # break
        print(f"Frame time: {1000 * (time.time() - start):.2f} ms")

if __name__ == '__main__':
    main()