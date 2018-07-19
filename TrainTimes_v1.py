#!/usr/bin/python
# for making executable

# http://programarcadegames.com/index.php?chapter=introduction_to_graphics

# Make sure to install 'lxml', 'requests', and 'pygame'
# $ sudo apt-get install python3-lxml
# $ pip3 install requests
# $ pip3 install pygame

# For crontab startup procedure
# os.chdir("Desktop")

import datetime
import requests
import subprocess       # for terminal commands (turing screen off)
from lxml import html
import pygame
# Import a library of functions called 'pygame'
pygame.init()
# Initialize the game engine

WIDTH = 1360
HEIGHT = 768
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Train Times")

#pygame.display.set_mode(size, pygame.FULLSCREEN)

# colors
BLACK = (0, 0, 0)
YELLOW = (204, 184, 55)
WHITE = (255, 255, 255)

# lines of text
LINE1 = 10 # Current date and current time
LINE2 = 200 # Station
LINE3 = 400 # Track
LINE4 = 530 # NextTrain and Arrival Time
LINE5 = 660 # NextNextTrain and Arrival Time

# program 
done = False
refresh = True
count = 0
clock = pygame.time.Clock()
while not done:
    
    while refresh == False and done == False:
        #subprocess.call('xset dpms force off', shell=True)
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
    
        # Scraping the train times
        page = requests.get("https://www.metrotransit.org/NexTripBadge.aspx?route=902&direction=3&stop=PSPK")
        # go to Metro Transit's NexTrip page with parameters to specify route, direction, and stop
        data = html.fromstring(page.content)
        # scrap the html contents from that page
        firstTrain = data.xpath('//*[@id="NexTripControl1_NexTripResults1_departures"]/div[1]/span[3]/text()')
        secondTrain = data.xpath('//*[@id="NexTripControl1_NexTripResults1_departures"]/div[2]/span[3]/text()')
        # Use inspector to find element's class name then
        # follow the guide on this webpage to construct the xpath:
        # http://python-guide-pt-br.readthedocs.io/en/latest/scenarios/scrape/
    except requests.ConnectionError:
        connection = False
        firstTrain = "N/A"
        secondTrain = "N/A"

    screen.fill(BLACK)

    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('roboto', 75, True, False)
 
    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    station = font.render("PROSPECT  PARK  STATION", True, YELLOW)
    track1 = font.render("TRACK  1", True, YELLOW)
    connectionLost = font.render("CONNECTION LOST", True, WHITE)
 
    # Put the image of the text on the screen at 250x250
    screen.blit(station, [0, LINE2])
    screen.blit(track1, [0, LINE3])
    if connection == False:
        screen.blit(connectionLost, [0, LINE2+130])

    # counter
    count = count + 1
    counter = font.render(str(count), True, WHITE)
    #screen.blit(counter, [0, 300])

    # current time
    currentTime = datetime.datetime.now().strftime("%I:%M %p") # I-12 hour, H-24 hour
    currentTime = font.render(currentTime, True, YELLOW)
    time_rect = currentTime.get_rect() # for right align
    time_rect.right = WIDTH-90
    time_rect.top = LINE1
    screen.blit(currentTime, time_rect)

    # blinking time
    # the ':' in the middle of the time will blink every other refresh
    if count%2==0:
        pygame.draw.rect(screen, BLACK, (1035, LINE1+25, 15, 60))
        # if on 24 hour time, change to (1165, LINE1+25, 15, 60)

    # current date
    currentDate = datetime.datetime.now().strftime("%a, %d %b %Y")
    currentDate = font.render(currentDate.upper(), True, YELLOW)
    screen.blit(currentDate, [0, LINE1])
    
    # next trains
    nextTrain = font.render("GREEN     MINNEAPOLIS", True, YELLOW)
    screen.blit(nextTrain, [0, LINE4])
    nextNextTrain = font.render("GREEN     MINNEAPOLIS", True, YELLOW)
    screen.blit(nextNextTrain, [0, LINE5])

    # arrival times
    nextTime = font.render(firstTrain[0].upper(), True, YELLOW)
    text_rect1 = nextTime.get_rect()
    text_rect1.right = WIDTH-90
    text_rect1.top = LINE4
    screen.blit(nextTime, text_rect1)
    
    nextNextTime = font.render(secondTrain[0].upper(), True, YELLOW)
    text_rect2 = nextNextTime.get_rect()
    text_rect2.right = WIDTH-90
    text_rect2.top = LINE5
    screen.blit(nextNextTime, text_rect2)


    pygame.display.flip() # update screen

    clock.tick(1) # limit to (X) fps

    # auto turn off display
    if count == 200: # (300) roughly the number of seconds before auto-off
        refresh = False
        count = 0
        subprocess.call('vcgencmd display_power 0', shell=True)

pygame.quit()
