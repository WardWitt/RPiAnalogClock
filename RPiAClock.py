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

ipTxtColor = tuple(map(int, config['Color']['IP_Address_Color'].split(',')))
NTP_GoodColor = tuple(map(int, config['Color']['NTP_Good_Color'].split(',')))
NTP_BadColor = tuple(map(int, config['Color']['NTP_Bad_Color'].split(',')))

# Scaling to the right size for the clock display
digiclocksize  = int(bg.get_height()/4.5)
digiclockspace = int(bg.get_height()/10.5)
dotsize = int(bg.get_height()/90)
hradius = bg.get_height()/2.5
secradius = hradius - (bg.get_height()/26)

# Coordinates of items on display
# xclockpos = int(bg.get_width()*0.2875)
xclockpos = int(bg.get_width()/2.5)
ycenter = int(bg.get_height()/2)
xcenter = int(bg.get_width()/2)

# # Set relative indicator box 'x' location


txthmy = int(ycenter)

# Fonts  
clockfont = pygame.font.Font(None,digiclocksize)
ipFont = pygame.font.Font(None, 30)
    
def paraeqsmx(smx):
    return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
    return ycenter-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
    return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
    return ycenter-(int(hradius*(math.sin(math.radians((shy)+90)))))

ipTxt = ipFont.render(ipAddress, True, ipTxtColor)

# Logo position
imageXY = image.get_rect(centerx = xclockpos, centery = ycenter + int(secradius / 2))

######################### Main program loop. ####################################

while True :
    pygame.display.update()

    bg.fill(bgcolor)

    # Retrieve seconds and turn them into integers
    # int_seconds = int(time.strftime("%S",time.localtime(time.time())))

    # To get the dots in sync with the seconds
    

    current_time = datetime.datetime.now()
    float_seconds = float(current_time.strftime('%S.%f'))
    int_seconds = int(current_time.strftime('%S'))
    retrievehm = (current_time.strftime('%I:%M:%S'))
    secdeg  = (int_seconds + 1) * 6
  

    # Draw second markers
    smx=smy=0
    while smx < secdeg:
        # pygame.draw.circle(bg, clockcolor, (paraeqsmx(smx),paraeqsmy(smy)),dotsize)
        pygame.gfxdraw.aacircle(bg, paraeqsmx(smx), paraeqsmy(smy), dotsize, clockcolor)
        pygame.gfxdraw.filled_circle(bg, paraeqsmx(smx), paraeqsmy(smy), dotsize, clockcolor)
        smy += 6  # 6 Degrees per second
        smx += 6

    # Draw hour markers
    shx=shy=0
    while shx < 360:
        # pygame.draw.circle(bg, hourcolor, (paraeqshx(shx),paraeqshy(shy)),dotsize)
        pygame.gfxdraw.aacircle(bg, paraeqshx(shx), paraeqshy(shy), dotsize, hourcolor)
        pygame.gfxdraw.filled_circle(bg, paraeqshx(shx), paraeqshy(shy), dotsize, hourcolor)
        shy += 30  # 30 Degrees per hour
        shx += 30

    # Retrieve time for digital clock
    # retrievehm    = time.strftime("%I:%M:%S",time.localtime(time.time()))
    digiclockhm   = clockfont.render(retrievehm,True,hourcolor)
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

    smx = smy = float_seconds * 6
    pygame.gfxdraw.aapolygon(bg, [(paraeqsmx(smx), paraeqsmy(smy)), (xclockpos, ycenter), (xclockpos, ycenter)], clockcolor)

    pygame.gfxdraw.aatrigon(bg, xclockpos - 510, ycenter, xclockpos - 500, ycenter + int_seconds, xclockpos - 490, ycenter, clockcolor)

    # time.sleep(0.04)
    pygame.time.Clock().tick(60)

    for event in pygame.event.get() :
         if event.type == QUIT:
             pygame.quit()
             sys.exit()
         # Pressing q+t to exit
         elif event.type == KEYDOWN:
             if event.key == K_q and K_t:
                 pygame.quit()
       #          GPIO.cleanup()
                 sys.exit()
