import numpy as np
import mss
import keyboard
import time

# !!!!!!!!! Y COORDS GO FROM TOP TO BOTTOM !!!!!!!!!
#ALL HARDCODED FOR 1440p screens
min_y = 960 #BOTTOM
min_x = 330
med_y = 900
med_x = 370
max_y = 790 #TOP
max_x = 550

y_dif = 1
x_dif = 40

#     700
# 490     720
#     900

# All commented values are for simpler visualization, but could change (no hardcoding here)
high_y = 0  # 700 - 700
high_x_start = max_x - min_x - x_dif  # 100
high_x_end = high_x_start + x_dif # 140

med_y = min_y - med_y  # 20
med_x_start = med_x - min_x  # 30
med_x_end = med_x_start + x_dif # 70

low_y = min_y - max_y - 1  # 99
low_x_start = 0
low_x_end = x_dif

BOX = {'top': max_y,
       'left': min_x,
       'width': max_x - min_x,
       'height': min_y - max_y}

sct = mss.mss()

def is_obstacle() -> tuple:
    # img_sample = sct.grab(BOX) #Here for debugging purpose
    # full_screen_sample = sct.grab((0,0,2560,1440))
    bot_fov = np.array(sct.grab(BOX))[:, :, :3]

    slice_high = bot_fov[high_y, high_x_start:high_x_end, :]
    slice_med = bot_fov[med_y, med_x_start:med_x_end, :]
    slice_low = bot_fov[low_y, low_x_start:low_x_end, :]

    bg_color = np.array(sct.grab({
        'top': 800,
        'left': 10,
        'width': 1,
        'height': 1,
    }))[:, :, :3][0,0]

    for label, sl in [('high', slice_high), ('med', slice_med), ('low', slice_low)]:
        if np.any(np.abs(sl - bg_color).sum(axis=1) > 30):

            # img = Image.frombytes('RGB', img_sample.size, img_sample.rgb)
            # screen = Image.frombytes('RGB', full_screen_sample.size, full_screen_sample.rgb)
            # img.save("debug_capture.png")
            # screen.save("debug_screen.png") #Same here for debugging

            return True, label
    return False, ''

# Makes the dyno jump low
def short_jump():
    keyboard.press('space')
    time.sleep(.01)
    keyboard.release('space')

# Makes the dyno jump high
def long_jump():
    keyboard.press('space')
    time.sleep(.1)
    keyboard.release('space')

# MAIN LOOP
def main():
    n = 0
    print('Starting...')
    time.sleep(3)
    while True:
        # start = time.time()
        if keyboard.is_pressed('q'):
            break

        check_result = is_obstacle()

        if check_result[0] and check_result[1] == 'low':
            short_jump()
            n+=1
            print('jump low', n)
            # break
        elif check_result[0] and check_result[1] in ['med', 'high']:
            long_jump()
            n+=1
            print(f'jump {check_result[1]}', n)
            # break
        # print(f"Frame time: {1000 * (time.time() - start):.2f} ms") #Yes debugging again and optimization

if __name__ == '__main__':
    main()