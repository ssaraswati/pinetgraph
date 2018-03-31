#!/usr/bin/python
import socket
import pyping
import time
import sys
from json import load
from urllib2 import urlopen
frames = 0
image_height, image_width = (250, 128)
hostname = socket.gethostname() 
print "hostname: " + hostname
print "Starting Pynet..."
if hostname == "raspberrypi":
    import Image
    import ImageDraw
    import ImageFont
    import epd2in13
    epd = epd2in13.EPD()
    epd.init(epd.lut_full_update)
    font_base = '/home/pi/pynet/'
else:
    from PIL import Image, ImageDraw, ImageFont
    font_base = './'


test_file = 'sample-out.jpg'
ping_host = '8.8.8.8'

ping_data = [5] * 50

font_big = ImageFont.truetype(font_base + 'FreeMonoBold.ttf', 12)
font_medium = ImageFont.truetype(font_base + 'runescape_uf.ttf', 16)
font_small = ImageFont.truetype(font_base + 'Super_Mario_World_Text_Box.ttf', 7)

print "Loaded Fonts"
def newBlankImage():
    image = Image.new('1', (image_width, image_height), 255) 
    image = image.rotate(90, expand=1)
    draw = ImageDraw.Draw(image)
    return image, draw

def draw_image(image_to_draw, frames):
    if hostname == "raspberrypi":
        epd.clear_frame_memory(0xFF)
        image_up = image.rotate(90, expand=1)
        epd.set_frame_memory(image_up, 0, 0)
        epd.display_frame()
        if frames == 0 or frames % 100 == 0:
            print frames + " have been drawing doing a full update of display"
            epd.init(epd.lut_full_update)
        else:
            epd.init(epd.lut_partial_update)
    else:
        image_to_draw.save(test_file)
    return frames + 1


def add_graph_to_image(parent_image, graph_data, x, y):
    image = Image.new('1', (150, 100), 255) 
    draw = ImageDraw.Draw(image)
    offset = 0
    for point in graph_data:
        height = int(point / 2)
        draw.rectangle([(offset, 100), (offset + 3, 100 - height)], 0)
        offset += 3
    parent_image.paste(image, (x, y))

def draw_spinner(drawobj, x, y, flag):
    drawobj.rectangle((0 + x, 0 + y, 10 + x, 10 + y), fill = 0 if flag else 255 , outline= 0)
    drawobj.rectangle((10 + x, 0 + y, 20 + x, 10 + y), fill = 255 if flag else 0, outline= 0)

    drawobj.rectangle((0 + x, 10 + y, 10 + x, 20 + y), fill = 255 if flag else 0, outline= 0)
    drawobj.rectangle((10 + x, 10 + y, 20 + x, 20 + y), fill = 0 if flag else 255, outline= 0)

def draw_top_bar(drawobj, ip_left, ip_right):
    ip_output = '{0:24s}<{1:5}>{2:>24s}'.format(ip_left, time.strftime('%H:%M'), ip_right)   
    draw.rectangle((1, 20, 249, 1), fill = 255, outline= 0)
    draw.text((5, 1), ip_output, font=font_medium, fill=0)

def make_startup_images():
    image, draw = newBlankImage()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    ip_output = '{0:10s}'.format(ip)
    draw.rectangle((5, 10, 128, 30), fill = 0)
    draw.rectangle((5, 30, 128, 50), fill = 255, outline= 0)
    draw.text((35, 14), 'Starting...', font = font_medium, fill = 255)
    draw.text((35, 36), ip_output, font = font_medium, fill = 0)
    return image 
###########



print "Trying to draw first frame"
frames = draw_image(make_startup_images(), frames)
print "First frame drawn successfully"


ip_public = load(urlopen('http://jsonip.com'))['ip']
print "Starting ping loop"
while True:
    image, draw = newBlankImage()
    

    ping_avg = -1
    try:
        r = pyping.ping(ping_host)
        ping_avg = float(r.avg_rtt)
    except Exception as ex:
        print ex.message

    ping_output = '{0:15.0f}ms'.format(ping_avg)

    draw.rectangle((0, 0, image_width, image_height), fill = 255)
    draw_top_bar(draw, ip_public, ping_host)

    draw.rectangle((150, 101, 250, 121), fill = 255, outline= 0)
    draw.text((150, 105), ping_output, font=font_medium, fill=0)
    draw_spinner(draw, 230, 101, frames % 2 == 0)

    ping_data.pop(0)
    ping_data.append(int(ping_avg))
    add_graph_to_image(image, ping_data, 0, 22)
    frames = draw_image(image, frames)    

