import pyping
import time
from PIL import Image, ImageDraw, ImageFont
import socket
from json import load
from urllib2 import urlopen
hostname = socket.gethostname() 
test_file = 'sample-out.jpg'

if hostname == "raspberrypi":
    import epd2in13
    epd = epd2in13.EPD()
    epd.init(epd.lut_full_update)
    

# ip_public = load(urlopen('http://jsonip.com'))['ip']
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# For simplicity, the arguments are explicit numerical coordinates
image = Image.new('1', (128, 250), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('./FreeMonoBold.ttf', 10)
image_width, image_height = (96, 32)
while True:
    print 'Ping...Pong?'
    r = pyping.ping('google.com')
    output = "IP: " + ip + "Public IP: " + "sdf" + "ms:" + r.avg_rtt

    draw.rectangle((0, 0, image_width, image_height), fill = 255)
    draw.text((30, 14), output, font=font, fill=0)
    if hostname == "pynet":
        epd.display_frame()
    else:
        print test_file
    image.save(test_file)

    time.sleep(5)