import pyping
import time
from PIL import Image, ImageDraw, ImageFont
import socket
from json import load
from urllib2 import urlopen
hostname = socket.gethostname() 
test_file = 'sample-out.jpg'
image_width, image_height = (250, 122)

font_big = ImageFont.truetype('./enhanced_dot_digital-7.ttf', 20)
font_medium = ImageFont.truetype('./runescape_uf.ttf', 16)
font_small = ImageFont.truetype('./Super_Mario_World_Text_Box.ttf', 7)


def newBlankImage():
    image = Image.new('1', (image_width, image_height), 255) 
    draw = ImageDraw.Draw(image)
    return image, draw

def draw_image(image_to_draw):
    if hostname == "raspberrypi":
        print "Drawing Frame"
        epd.set_frame_memory(image_to_draw.rotate(90), 0, 0)
        epd.display_frame()
    else:
        print test_file
        image_to_draw.save(test_file)

if hostname == "raspberrypi":
    import epd2in13
    epd = epd2in13.EPD()
    epd.init(epd.lut_partial_update)
    

ip_public = load(urlopen('http://jsonip.com'))['ip']
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# Draw device Ip
image, draw = newBlankImage()
ip_output = '{0:10s} ...Starting'.format(ip)
draw.text((5, 14), ip_output, font=font_big, fill=0)
draw_image(image)
time.sleep(2)
############

while True:
    image, draw = newBlankImage()
    

    ip_output = '{0:10s}'.format(ip_public)   

    r = pyping.ping('google.com')

    ping_output = '       {0:10.0f}ms'.format(float(r.avg_rtt))

    draw.rectangle((0, 0, image_width, image_height), fill = 255)
    draw.text((5, 14), ip_output, font=font_medium, fill=0)
    draw.text((5, 90), ping_output, font=font_big, fill=0)


    draw_image(image)


