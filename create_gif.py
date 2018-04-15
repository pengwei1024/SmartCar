#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
https://blog.csdn.net/guduruyu/article/details/77540445
把outout下图片生成gif
'''

import imageio


def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
        # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.2)
    return


def main():
    image_list = []
    for num in range(1, 100):
        image_list.append("output/%s.jpg" % num)
        pass
    gif_name = 'detection_result.gif'
    create_gif(image_list, gif_name)


if __name__ == "__main__":
    main()
