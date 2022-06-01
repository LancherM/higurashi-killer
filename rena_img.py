import random
import os


def get_random_pic(img_lists):
    img_name = random.choice(img_lists)
    if '.png' in img_name:
        return [img_name, img_name]
    else:
        new_list = os.listdir('img/' + img_name)
        final_img = random.choice(new_list)
        return [img_name, img_name + '/' + final_img]

