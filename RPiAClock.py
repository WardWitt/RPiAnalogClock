import pygame, sys, time, os, math, socket, configparser, logging, datetime

import pygame.gfxdraw

logging.basicConfig(level=logging.WARNING, filename='RPiclock.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s - %(asctime)s')

# get our base path
base_dir = os.path.dirname(os.path.realpath(__file__))

# Load configuration
config = configparser.ConfigParser()
config.read(base_dir + '/RPiclock.ini')

# NTP status
timeStatus = False

counter = 0

# Initialize the pygame class
logging.info('Start RPiclock')
pygame.display.init()
pygame.font.init()

# Figure out our IP Address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connect() for UDP doesn't send packets
s.connect(('8.8.8.8', 0))
ipAddress = s.getsockname()[0]

bg = pygame.display.set_mode(tuple(map(int, config['Display']['Resolution'].split(','))))
pygame.mouse.set_visible(False)

image = pygame.image.load(config['Logo']['Logo_Image'])

# Change color to preference (R,G,B) 255 max value
bgcolor = tuple(map(int, config['Color']['Background_Color'].split(',')))
clockcolor = tuple(map(int, config['Color']['Second_Color'].split(',')))
hourcolor = tuple(map(int, config['Color']['Hour_Color'].split(',')))
white = (255, 255 ,255, 255)

ipTxtColor = tuple(map(int, config['Color']['IP_Address_Color'].split(',')))
NTP_GoodColor = tuple(map(int, config['Color']['NTP_Good_Color'].split(',')))
NTP_BadColor = tuple(map(int, config['Color']['NTP_Bad_Color'].split(',')))

# Scaling to the right size for the clock display
digiclocksize  = int(bg.get_height()/4.5)
digiclockspace = int(bg.get_height()/10.5)
dotsize = int(bg.get_height()/90)
hour_radius = bg.get_height()/2.5
seconds_radius = hour_radius - (bg.get_height()/26)

# Coordinates of items on display
# xclockpos = int(bg.get_width()*0.2875)
xclockpos = int(bg.get_width()/2)
ycenter = int(bg.get_height()/2)
xcenter = int(bg.get_width()/2)

# Set relative indicator box 'x' location

txthmy = int(ycenter)

# Fonts  
clockfont = pygame.font.Font(None,digiclocksize)
ipFont = pygame.font.Font(None, 30)
    
def polar_to_X_seconds(angle):
    return xclockpos-(int(seconds_radius*(math.cos(math.radians((angle)+90)))))

def polar_to_Y_seconds(angle):
    return ycenter-(int(seconds_radius*(math.sin(math.radians((angle)+90)))))

# Equations for hour markers
def polar_to_X_hours(angle):
    return xclockpos-(int(hour_radius*(math.cos(math.radians((angle)+90)))))

def polar_to_Y_hours(angle):
    return ycenter-(int(hour_radius*(math.sin(math.radians((angle)+90)))))

def rotate(origin, points, angle):
    ox, oy = origin
    rotatedPoints = []
    for point in points:
        px, py = point

        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
        rotatedPoints.append((qx, qy))

    return rotatedPoints

ipTxt = ipFont.render(ipAddress, True, ipTxtColor)

# Logo position
imageXY = image.get_rect(centerx = xclockpos, centery = ycenter + int(seconds_radius / 2))


secondHand = [(xclockpos + 10, ycenter + 30), (xclockpos - 10, ycenter + 30), (xclockpos, ycenter - seconds_radius + 20)]
minuteHand = [(xclockpos + 10, ycenter), (xclockpos - 10, ycenter), (xclockpos, ycenter - seconds_radius + 50)]
hourHand = [(xclockpos + 10, ycenter), (xclockpos - 10, ycenter), (xclockpos, ycenter - seconds_radius + 100)]

######################### Main program loop. ####################################

while True :
    pygame.display.update()

    bg.fill(bgcolor)

    current_time = datetime.datetime.now()
    float_seconds = float(current_time.strftime('%S.%f'))
    int_seconds = int(current_time.strftime('%S'))
    int_minutes = int(current_time.strftime('%M'))
    int_hours = int(current_time.strftime('%I'))
    retrievehm = (current_time.strftime('%I:%M:%S'))
    secdeg  = (int_seconds + 1) * 6
    secondAngle = float_seconds * 6
    minuteAngle = int_minutes * 6 + int_seconds / 10
    hourAngle = int_hours * 30 + int_minutes / 5

    rotatedSecondHand = rotate((xclockpos, ycenter), secondHand, secondAngle)
    rotatedMinuteHand = rotate((xclockpos, ycenter), minuteHand, minuteAngle)
    rotatedHourHand = rotate((xclockpos, ycenter), hourHand, hourAngle)

    pygame.gfxdraw.filled_polygon(bg, rotatedMinuteHand, hourcolor)
    pygame.gfxdraw.aapolygon(bg, rotatedMinuteHand, hourcolor)
    pygame.gfxdraw.filled_polygon(bg, rotatedHourHand, hourcolor)
    pygame.gfxdraw.aapolygon(bg, rotatedHourHand, hourcolor)
    pygame.gfxdraw.filled_polygon(bg, rotatedSecondHand, clockcolor)
    pygame.gfxdraw.aapolygon(bg, rotatedSecondHand, clockcolor)

    # Draw second markers
    angle = 0
    while angle < secdeg:
        # pygame.draw.circle(bg, clockcolor, (polar_to_X_seconds(smx),polar_to_Y_seconds(smy)),dotsize)
        pygame.gfxdraw.filled_circle(bg, polar_to_X_seconds(angle), polar_to_Y_seconds(angle), dotsize, clockcolor)
        pygame.gfxdraw.aacircle(bg, polar_to_X_seconds(angle), polar_to_Y_seconds(angle), dotsize, clockcolor)
        angle += 6  # 6 Degrees per second

    # Draw hour markers
    angle = 0
    while angle < 360:
        # pygame.draw.circle(bg, hourcolor, (polar_to_X_hours(shx),polar_to_Y_hours(shy)),dotsize)
        pygame.gfxdraw.filled_circle(bg, polar_to_X_hours(angle), polar_to_Y_hours(angle), dotsize, hourcolor)
        pygame.gfxdraw.aacircle(bg, polar_to_X_hours(angle), polar_to_Y_hours(angle), dotsize, hourcolor)
        angle += 30  # 30 Degrees per hour

    # Retrieve time for digital clock
    # retrievehm    = time.strftime("%I:%M:%S",time.localtime(time.time()))
    digiclockhm   = clockfont.render(retrievehm,True,white)
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)

    # NTP warning flag
    counter += 1
    if counter == 3600:
        chronyc = os.popen('chronyc -c tracking').read().split(',')
        lastTimeUpdate = time.time() - float(chronyc[3])
        if lastTimeUpdate < 3600:
            timeStatus = True
            logging.info('Last valad time update %f seconds ago', lastTimeUpdate)
        else:
            timeStatus = False
            logging.warning('!!! - Last valad time update %f seconds ago - !!!', lastTimeUpdate)
        counter = 0

    if timeStatus:
        pygame.gfxdraw.aacircle(bg, dotsize + 5, bg.get_height()- dotsize - 5, dotsize, NTP_GoodColor)
        pygame.gfxdraw.filled_circle(bg, dotsize + 5, bg.get_height()- dotsize - 5, dotsize, NTP_GoodColor)
    else:
        pygame.gfxdraw.aacircle(bg, dotsize + 5, bg.get_height()- dotsize - 5, dotsize, NTP_BadColor)
        pygame.gfxdraw.filled_circle(bg, dotsize + 5, bg.get_height()- dotsize - 5, dotsize, NTP_BadColor)

    # Render the normal screen
    bg.blit(digiclockhm, txtposhm)
    bg.blit(image, imageXY)

    # Display IP address
    bg.blit(ipTxt, ipTxt.get_rect())

    

    # secondhandend = (polar_to_X_seconds(angle), polar_to_Y_seconds(angle))
    # pygame.gfxdraw.filled_polygon(bg, [secondhandend, (xclockpos, ycenter + 10), (xclockpos, ycenter - 10)], clockcolor)
    # pygame.gfxdraw.aapolygon(bg, [secondhandend, (xclockpos, ycenter + 10), (xclockpos, ycenter - 10)], clockcolor)

    # triangleOrigin = secondhandend
    # trianglePoints = [(xclockpos - 50, ycenter), (xclockpos, ycenter + 50), (xclockpos + 50, ycenter)]
    # triangle[0] = rotate(triangleOrigin, trianglePoints[0], float_seconds * 6)
    # triangle[1] = rotate(triangleOrigin, trianglePoints[1], float_seconds * 6)
    # triangle[2] = rotate(triangleOrigin, trianglePoints[2], float_seconds * 6)
    # pygame.gfxdraw.aapolygon(bg, triangle, clockcolor)

    pygame.time.Clock().tick(60)

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
