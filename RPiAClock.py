import pygame
import sys
import time
import os
import math
import socket
import configparser
import logging
import datetime
import pygame.gfxdraw

logging.basicConfig(
    level = logging.WARNING,
    filename="RPiclock.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s - %(asctime)s",
)

# get our base path
base_dir = os.path.dirname(os.path.realpath(__file__))

# Load configuration
config = configparser.ConfigParser()
config.read(base_dir + "/RPiclock.ini")

# NTP status
timeStatus = False

counter = 0

# Initialize the pygame class
logging.info("Start RPiclock")
pygame.display.init()
pygame.font.init()

# Figure out our IP Address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connect() for UDP doesn't send packets
s.connect(("8.8.8.8", 0))
ipAddress = s.getsockname()[0]

bg = pygame.display.set_mode(
    tuple(map(int, config["Display"]["Resolution"].split(",")))
)
pygame.mouse.set_visible(False)

image = pygame.image.load(config["Logo"]["Logo_Image"])

# Change color to preference (R,G,B) 255 max value
bgcolor = tuple(map(int, config["Color"]["Background_Color"].split(",")))
clockcolor = tuple(map(int, config["Color"]["Second_Color"].split(",")))
hourcolor = tuple(map(int, config["Color"]["Hour_Color"].split(",")))
secondHandColor = tuple(map(int, config["Color"]["Second_Hand_Color"].split(",")))
minuteHandColor = tuple(map(int, config["Color"]["Minute_Hand_Color"].split(",")))
hourHandColor = tuple(map(int, config["Color"]["Hour_Hand_Color"].split(",")))
white = (255, 255, 255, 255)
black = (0, 0, 0, 255)

ipTxtColor = tuple(map(int, config["Color"]["IP_Address_Color"].split(",")))
NTP_GoodColor = tuple(map(int, config["Color"]["NTP_Good_Color"].split(",")))
NTP_BadColor = tuple(map(int, config["Color"]["NTP_Bad_Color"].split(",")))

# Scaling to the right size for the clock display
displayHeight = bg.get_height()
displayWidth = bg.get_width()
digiclocksize = int(displayHeight / 4.5)
digiclockspace = int(displayHeight / 10.5)
dotsize = int(displayHeight / 90)
hour_radius = displayHeight / 2.5
seconds_radius = hour_radius - (displayHeight / 26)
handWidth = (displayHeight * 0.02)

# Coordinates of items on display
# xclockpos = int(bg.get_width()*0.2875)
xclockpos = int(displayWidth / 2)
ycenter = int(displayHeight / 2)
xcenter = int(displayWidth / 2)

# Set relative indicator box 'x' location

txthmy = int(ycenter)

# Fonts
clockfont = pygame.font.Font(None, digiclocksize)
ipFont = pygame.font.Font(None, 30)

def polar_to_X_seconds(angle):
    return xclockpos - (int(seconds_radius * (math.cos(math.radians((angle) + 90)))))

def polar_to_Y_seconds(angle):
    return ycenter - (int(seconds_radius * (math.sin(math.radians((angle) + 90)))))

# Equations for hour markers

def polar_to_X_hours(angle):
    return xclockpos - (int(hour_radius * (math.cos(math.radians((angle) + 90)))))

def polar_to_Y_hours(angle):
    return ycenter - (int(hour_radius * (math.sin(math.radians((angle) + 90)))))

def rotate(origin, points, angle):
    ox, oy = origin
    rotatedPoints = []
    for point in points:
        px, py = point

        qx = (
            ox
            + math.cos(math.radians(angle)) * (px - ox)
            - math.sin(math.radians(angle)) * (py - oy)
        )
        qy = (
            oy
            + math.sin(math.radians(angle)) * (px - ox)
            + math.cos(math.radians(angle)) * (py - oy)
        )
        rotatedPoints.append((qx, qy))

    return rotatedPoints

ipTxt = ipFont.render(ipAddress, True, ipTxtColor)

# Logo position
imageXY = image.get_rect(
    centerx=xclockpos, centery=ycenter + int(seconds_radius / 2))

secondHand = [
    (xclockpos + handWidth / 2, ycenter - handWidth * 1.5),
    (xclockpos - handWidth / 2, ycenter - handWidth * 1.5),
    (xclockpos, ycenter + seconds_radius * 0.95)
]
minuteHand = [
    (xclockpos + handWidth / 2, ycenter),
    (xclockpos - handWidth / 2, ycenter),
    (xclockpos - handWidth / 4, ycenter + seconds_radius * 0.8),
    (xclockpos, ycenter + seconds_radius * 0.85),
    (xclockpos + handWidth / 4, ycenter + seconds_radius * 0.8)
]
hourHand = [
    (xclockpos + handWidth / 2, ycenter),
    (xclockpos - handWidth / 2, ycenter),
    (xclockpos - handWidth / 4, ycenter + seconds_radius * 0.6),
    (xclockpos, ycenter + seconds_radius * 0.65),
    (xclockpos + handWidth / 4, ycenter + seconds_radius * 0.6)
]

######################### Main program loop. ####################################

while True:
    pygame.display.update()

    bg.fill(bgcolor)

    # Display the logo
    bg.blit(image, imageXY)

    current_time = datetime.datetime.now()
    float_seconds = float(current_time.strftime("%S.%f"))
    int_seconds = int(current_time.strftime("%S"))
    int_minutes = int(current_time.strftime("%M"))
    int_hours = int(current_time.strftime("%I"))
    string_time = current_time.strftime("%I:%M:%S")
    secdeg = (int_seconds + 1) * 6
    secondAngle = float_seconds * 6
    minuteAngle = int_minutes * 6 + int_seconds / 10
    hourAngle = int_hours * 30 + int_minutes / 2

    rotatedSecondHand = rotate((xclockpos, ycenter), secondHand, secondAngle + 180)
    rotatedMinuteHand = rotate((xclockpos, ycenter), minuteHand, minuteAngle + 180)
    rotatedHourHand = rotate((xclockpos, ycenter), hourHand, hourAngle + 180)

    pygame.gfxdraw.filled_polygon(bg, rotatedHourHand, hourHandColor)
    pygame.gfxdraw.aapolygon(bg, rotatedHourHand, hourHandColor)

    pygame.gfxdraw.filled_polygon(bg, rotatedMinuteHand, minuteHandColor)
    pygame.gfxdraw.aapolygon(bg, rotatedMinuteHand, minuteHandColor)

    pygame.gfxdraw.filled_polygon(bg, rotatedSecondHand, secondHandColor)
    pygame.gfxdraw.aapolygon(bg, rotatedSecondHand, secondHandColor)

    # Draw second markers
    angle = 0
    while angle < secdeg:
        pygame.gfxdraw.filled_circle(
            bg,
            polar_to_X_seconds(angle),
            polar_to_Y_seconds(angle),
            dotsize,
            clockcolor,
        )
        pygame.gfxdraw.aacircle(
            bg,
            polar_to_X_seconds(angle),
            polar_to_Y_seconds(angle),
            dotsize,
            clockcolor,
        )
        angle += 6  # 6 Degrees per second

    # Draw hour markers
    angle = 0
    while angle < 360:
        pygame.gfxdraw.filled_circle(
            bg, polar_to_X_hours(angle), polar_to_Y_hours(
                angle), dotsize, hourcolor
        )
        pygame.gfxdraw.aacircle(
            bg, polar_to_X_hours(angle), polar_to_Y_hours(
                angle), dotsize, hourcolor
        )
        angle += 30  # 30 Degrees per hour

    # NTP warning flag
    counter += 1
    if counter == 1800:
        chronyc = os.popen("chronyc -c tracking").read().split(",")
        lastTimeUpdate = time.time() - float(chronyc[3])
        if lastTimeUpdate < 3600:
            timeStatus = True
            logging.info("Last valad time update %f seconds ago",
                         lastTimeUpdate)
        else:
            timeStatus = False
            logging.warning(
                "!!! - Last valad time update %f seconds ago - !!!", lastTimeUpdate
            )
        counter = 0

    if timeStatus:
        pygame.gfxdraw.aacircle(
            bg, dotsize + 5, displayHeight - dotsize - 5, dotsize, NTP_GoodColor
        )
        pygame.gfxdraw.filled_circle(
            bg, dotsize + 5, displayHeight - dotsize - 5, dotsize, NTP_GoodColor
        )
    else:
        pygame.gfxdraw.aacircle(
            bg, dotsize + 5, displayHeight - dotsize - 5, dotsize, NTP_BadColor
        )
        pygame.gfxdraw.filled_circle(
            bg, dotsize + 5, displayHeight - dotsize - 5, dotsize, NTP_BadColor
        )

    # Render our digital clock
    digital_clock = clockfont.render(string_time, True, white)
    # Digital clock with a drop shadow
    digital_clock_ds = clockfont.render(string_time, True, black)
    txtposhm = digital_clock.get_rect(centerx=xclockpos, centery=txthmy)

    # Display the normal screen
    # Insert our drop shadow first
    bg.blit(digital_clock_ds, txtposhm.move(+2, +2))
    bg.blit(digital_clock, txtposhm)  # Now add the digital clock

    # Display IP address
    bg.blit(ipTxt, ipTxt.get_rect())

    # This sets the frame rate
    pygame.time.Clock().tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Pressing q+t to exit
        elif event.type == KEYDOWN:
            if event.key == K_q and K_t:
                pygame.quit()
                #          GPIO.cleanup()
                sys.exit()
