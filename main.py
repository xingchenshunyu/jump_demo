# _*_ coding:utf-8 _*_
import os
from PIL import Image
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
need_update = True

def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')#获取当前界面的截图
    os.system('adb pull /sdcard/screen.png')#下载截图到当前文件夹
    return numpy.array(Image.open('screen.png'))#获取截图到电脑


def jump_to_next(point1,point2):# 计算两点间距离
    x1, y1 = point1; x2, y2=point2
    distant = ((x2-x1)**2+(y2-y1)**2)**0.5
    os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distant*1.05)))

def on_calck(event, coor=[]):# [(x,y),(x2,y2)]/绑定的鼠标单击事件
    coor.append((event.xdata,event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())
    global need_update
    need_update = True

def update_screen(frame):# 更新图片
    global need_update
    if need_update:
        time.sleep(1)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,

figuer = plt.figure()#创建一个空白的图片对象/创建一张图片
axes_image = plt.imshow(get_screen_image(), animated=True) #获取的图片画在坐标轴上
figuer.canvas.mpl_connect('button_press_event', on_calck)
ant = FuncAnimation(figuer, update_screen, interval=50, blit=True)
plt.show()

