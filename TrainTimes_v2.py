#!/usr/bin/python
# for making executable

#########################################################################
###############   Raspberry Pi Train Time Display   #####################
#########################################################################

# Originally from https://github.com/semicertain/Train-Times
# Questions? Email: me [at] semicertain.com

# This code will turn your Raspberry Pi into a display showing the times 
#   for the next two westbound greenline trains coming to the Prospect  
#   Park station in Minneapolis. 

# The graphics work was done relying heavily on this resource:
# http://programarcadegames.com/index.php?chapter=introduction_to_graphics

# Make sure to install 'lxml', 'requests', and 'pygame'
# $ sudo apt-get install python3-lxml
# $ pip3 install requests
# $ pip3 install pygame

# To boot this script on startup:
#   Create a file named 'IMS.service' in /etc/systemd/system/
#   The contents of this file can be found at the end of the script or at:
#   https://github.com/semicertain/Train-Times/blob/master/IMS.service
#   Note: root privileges required
#   Enable
#   $ sudo systemctl enable IMS.service
#   Check status
#   $ systemctl status IMS.service

# For crontab startup procedure
# os.chdir("Desktop")

#########################################################################
# Setup
import datetime         # for getting the date and time
import requests         # for getting data from webpages
import subprocess       # for terminal commands (turing screen off)
from lxml import html
# Import a library of functions called 'pygame'
import pygame
# Initialize the game engine
pygame.init()

# Find screen resolution
screenInfo = pygame.display.Info()
WIDTH  = screenInfo.current_w
HEIGHT = screenInfo.current_h

# Set fullscreen size
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Train Times")

# Define constants for the graphics
#   There are 7 lines of text and 9 spacers between them
#   Text is twice as high as a spacer, so need 7*2 + 9 = 23 units
SPACER = int(HEIGHT / 23) # needs to be an integer
TEXT_H = SPACER * 2

# Define lines upon which text will appear
LINE1 = SPACER                  # Current date and current time
LINE2 = LINE1 + TEXT_H + SPACER # This line intentionally left blark
LINE3 = LINE2 + TEXT_H + SPACER # Station
LINE4 = LINE3 + TEXT_H + SPACER # Connection error
LINE5 = LINE4 + TEXT_H + SPACER # Track
LINE6 = LINE5 + TEXT_H + SPACER # NextTrain and Arrival Time
LINE7 = LINE6 + TEXT_H + SPACER # NextNextTrain and Arrival Time

# Define colors
BLACK = (0, 0, 0)
YELLOW = (204, 184, 55)
WHITE = (255, 255, 255)

##########################################################################
# Program

# Originally from https://github.com/semicertain/Train-Times
# Questions? Email: me [at] semicertain.com

# Define initial conditions
done = False
refresh = True
count = 0
clock = pygame.time.Clock()

# Enter main loop
while not done:
    
    while refresh == False and done == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                refresh = True
                subprocess.call('vcgencmd display_power 1', shell=True)
            # press any key to quit
            elif event.type == pygame.KEYDOWN:
                done = True
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # press any key to quit
        elif event.type == pygame.KEYDOWN:
            done = True

    
    # Check for internet connection
    connection = False
    try:
        response = requests.get("https://www.metrotransit.org")
        connection = True
    
####### Scraping the train times
        # Go to Metro Transit's NexTrip page with parameters to specify route, direction, and stop
        page = requests.get("https://www.metrotransit.org/NexTripBadge.aspx?route=902&direction=3&stop=PSPK")
        # Scrap the html contents from that page
        data = html.fromstring(page.content)
        # Use inspector to find element's class name then
        #   follow the guide on this webpage to construct the xpath:
        #   http://python-guide-pt-br.readthedocs.io/en/latest/scenarios/scrape/
        firstTrain = data.xpath('//*[@id="NexTripControl1_NexTripResults1_departures"]/div[1]/span[3]/text()')
        secondTrain = data.xpath('//*[@id="NexTripControl1_NexTripResults1_departures"]/div[2]/span[3]/text()')
        
    except requests.ConnectionError:
        connection = False
        firstTrain = "N/A"
        secondTrain = "N/A"

    # Fill screen background
    screen.fill(BLACK)

    # Select the (font to use, size, bold, italics)
    font = pygame.font.SysFont('monospace', TEXT_H, True, False)
 
    # Render the text. "True" means anti-aliased text.
    #   Black is the color. The variable BLACK was defined
    #   above as a list of [0, 0, 0]
    #   Note: This line creates an image of the letters,
    #   but does not put it on the screen yet.
    station = font.render("PROSPECT  PARK  STATION", True, YELLOW)
    track1 = font.render("TRACK  1", True, YELLOW)
    connectionLost = font.render("CONNECTION LOST", True, WHITE)
 
    # Put the image of the text on the screen at 250x250
    screen.blit(station, [SPACER, LINE3])
    screen.blit(track1, [SPACER, LINE5])
    if connection == False:
        screen.blit(connectionLost, [SPACER, LINE4])

    # Counter
    #   For turning off the screen after a period of time
    count = count + 1
    #   counter = font.render(str(count), True, WHITE)
    #   screen.blit(counter, [0, 300])

    # Blinking time
    #   The ':' in the middle of the time will blink every other refresh
    #   This works best with a monospaced font
    if count%2==0:
        timeFormat = "%I %M %p" # I-12 hour, H-24 hour
    else:
        timeFormat = "%I:%M %p" # I-12 hour, H-24 hour

    # Current time
    currentTime = datetime.datetime.now().strftime(timeFormat) 
    currentTime = font.render(currentTime, True, YELLOW)
    time_rect = currentTime.get_rect() # for right align
    time_rect.right = WIDTH-SPACER
    time_rect.top = LINE1
    screen.blit(currentTime, time_rect)

    # Current date
    currentDate = datetime.datetime.now().strftime("%a, %d %b %Y")
    currentDate = font.render(currentDate.upper(), True, YELLOW)
    screen.blit(currentDate, [SPACER, LINE1])
    
    # Next trains
    nextTrain = font.render("GREEN     MINNEAPOLIS", True, YELLOW)
    screen.blit(nextTrain, [SPACER, LINE6])
    nextNextTrain = font.render("GREEN     MINNEAPOLIS", True, YELLOW)
    screen.blit(nextNextTrain, [SPACER, LINE7])

    # Arrival times
    nextTime = font.render(firstTrain[0].upper(), True, YELLOW)
    text_rect1 = nextTime.get_rect()
    text_rect1.right = WIDTH-SPACER
    text_rect1.top = LINE6
    screen.blit(nextTime, text_rect1)
    
    nextNextTime = font.render(secondTrain[0].upper(), True, YELLOW)
    text_rect2 = nextNextTime.get_rect()
    text_rect2.right = WIDTH-SPACER
    text_rect2.top = LINE7
    screen.blit(nextNextTime, text_rect2)

    # Update screen
    pygame.display.flip() 

    # Limit rate of update to (X) times a second
    clock.tick(1) 

    # Auto turn off display
    if count == 200: # roughly the number of seconds before auto-off
        refresh = False
        count = 0
        subprocess.call('vcgencmd display_power 0', shell=True)

# Originally from https://github.com/semicertain/Train-Times
# Questions? Email: me [at] semicertain.com

# If main loop is exited, quit program
pygame.quit()


# Start up script
#   Delete hashes and paste into 'IMS.service'
#   Note: root privileges required

#[Unit]
#Description=Get IMS service running at boot
#After=mosquitto.service mysql.service
#
#[Service]
#ExecStart=/home/pi/Desktop/Train-Times/TrainTimes_v2.py
#Restart=always
#StandardOutput=syslog
#StandardError=syslog
#SyslogIdentifier=IMS
#User=pi
#Group=pi
#
#[Install]
#WantedBy=multi-user.target
