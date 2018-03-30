#!/usr/bin/python
import socket
import pyping
import time
EPD_WIDTH       = 128
EPD_HEIGHT      = 250
image_height, image_width = (250, 128)
hostname = socket.gethostname() 
if hostname == "raspberrypi":
    import Image
    import ImageDraw
    import ImageFont
    import epd2in13
    epd = epd2in13.EPD()
    epd.init(epd.lut_full_update)
else:
    from PIL import Image, ImageDraw, ImageFont


from json import load
from urllib2 import urlopen

test_file = 'sample-out.jpg'
ping_host = 'google.com.au'

graph_width = (image_width - 100) / 3
ping_data = [1] * 50

font_big = ImageFont.truetype('./FreeMonoBold.ttf', 12)
font_medium = ImageFont.truetype('./runescape_uf.ttf', 16)
font_small = ImageFont.truetype('./Super_Mario_World_Text_Box.ttf', 7)


def newBlankImage():
    image = Image.new('1', (image_width, image_height), 255) 
    image = image.rotate(90, expand=1)
    draw = ImageDraw.Draw(image)
    return image, draw

def draw_image(image_to_draw):
    if hostname == "raspberrypi":
        epd.clear_frame_memory(0xFF)
        image_up = image.rotate(90, expand=1)
        epd.set_frame_memory(image_up, 0, 0)
        epd.display_frame()
    else:
        image_to_draw.save(test_file)


def draw_graph(graph_data):
    image = Image.new('1', (150, 100), 255) 
    draw = ImageDraw.Draw(image)
    offset = 0
    for point in graph_data:
        height = int(point / 2)
        draw.rectangle([(offset, 100), (offset + 3, 100 - height)], 0)
        offset += 3
    return image


    

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
ip_output = '{0:10s}'.format(ip)

font = ImageFont.truetype('./FreeMonoBold.ttf', 12)
# Draw device Ip
image, draw = newBlankImage()

draw.rectangle((5, 10, 128, 30), fill = 0)
draw.rectangle((5, 30, 128, 50), fill = 255, outline= 0)
draw.text((35, 14), 'Starting...', font = font_medium, fill = 255)
draw.text((35, 36), ip_output, font = font_medium, fill = 0)


draw_image(image)

# for partial update
if hostname == "raspberrypi":
    frames = 0
    epd.init(epd.lut_partial_update)
###########
ip_public = load(urlopen('http://jsonip.com'))['ip']

while True:
    image, draw = newBlankImage()
    

    ip_output = '{0:20s}<{1:5}>{2:>20s}'.format(ip_public, time.strftime('%H:%M'), ping_host)   

    r = pyping.ping(ping_host)
    print r.avg_rtt
    ping_avg = float(r.avg_rtt)
    ping_output = '         {0:15.0f}ms'.format(ping_avg)

    draw.rectangle((0, 0, image_width, image_height), fill = 255)
    draw.rectangle((1, 20, 249, 1), fill = 255, outline= 0)
    draw.text((5, 1), ip_output, font=font_medium, fill=0)
    draw.rectangle((150, 80, 250, 121), fill = 255, outline= 0)
    draw.text((150, 105), ping_output, font=font_medium, fill=0)
    ping_data.pop(0)
    ping_data.append(int(ping_avg))
    graph = draw_graph(ping_data)
    image.paste(graph, (0,22)) 
    draw_image(image)
    if hostname == "raspberrypi":
        frames += 1
        if frames % 10 == 0:
            epd.init(epd.lut_full_update)
        else:
            epd.init(epd.lut_partial_update)



