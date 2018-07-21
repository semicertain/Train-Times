<a name="top-of-doc"></a>
# Train Times
> A document from [semicertain.com](semicertain.com)
>
> Find the full repository [here](http://github.com/semicertain/Train-Times).

This program will turn your Raspberry Pi into a display showing the estimated times of arrival for the next two westbound green-line trains coming to the Prospect Park station in Minneapolis, Minnesota. 

## Table of Contents

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Overview](#overview)
- [Setup](#setup)
	- [Packages](#packages)
	- [Auto-Run on Startup](#auto-run)
- [Adapting the Code](#adapting)
- [The Reality of the Situation](#reality)
	- [Metro Transit Hedges Their Bets](#hedges-bets)
	- [Reaction Time](#reaction-time)
	- [Refresh Rate](#refresh-rate)
	- [Manual Restarts](#restarts)
- [Useful References](#references)

<!-- TOC -->

[//]: # (In order for headings with spaces to link to an entry in the TOC, you need the HTML-ish line below. The name needs to match what is in the parentheses in the TOC. They are put on the line before the heading so that the heading shows up when the link is clicked.)

---

<a name="overview"></a>
## Overview

In Minneapolis, all of the light rail stations have displays showing the estimates for when the next two trains will show up. This program brings this vital information to the comfort of your own home so you don't need to wait out in the cold. All you need is a Raspberry Pi, mouse, monitor, WiFi connection, and patience. 

This program is meant to run continuously so the train times are always readily available. It has two main loops. The first is when the monitor is off and the program waits for input. A click of the mouse sends it to the second loop where it scrapes the train times from [Metro Transit](www.metrotransit.org) every second until a count threshold is reached. At that point, it turns the monitor off and goes back to the first loop. 

This means that, on your way out, you can click the mouse, see the train times, and walk away confident that your monitor will turn off automatically in a few minutes. If you ever need to stop the program, hitting any button on your keyboard will end the script.

---

<a name="setup"></a>
## Setup

Download the file `TrainTimes_v2.py` and place it in a directory on your Raspberry Pi. The rest of this document assumes it is placed on the desktop, but you can put it anywhere that makes sense to you and modify the paths accordingly. 

<a name="packages"></a>
### Packages

This program was written for Python 3 and requires the following packages: `lxml`, `requests`, and `pygame`. If you have Python 3, you most likely have `pip3` installed which can be used to install these packages with the following commands:

```bash
$ sudo apt-get install python3-lxml
$ pip3 install requests
$ pip3 install pygame
```

<a name="auto-run"></a>
### Auto-Run on Startup

In the case of a power outage, this auto-run setup will ensure the program will start again after power is restored.

Create a file named `IMS.service` in the directory `/etc/systemd/system/`. Copy the contents of [`IMS.service`](http://github.com/semicertain/Train-Times/blob/master/IMS.service) in this repository into the new file. Root permissions are required to do this.

```bash
$ sudo vi IMS.service
```

After the file is created and saved, enable it using the following command:

```bash
$ sudo systemctl enable IMS.service
```

If you need to check the status of this procedure, use this command:

```bash
$ systemctl status IMS.service
```

---

<a name="adapting"></a>
## Adapting the Code

This program has some limits. If you have taken a good look through the code for this program, you may get the impression that it was cobbled together. You would be right. I am not a professional programmer and many of the code blocks were heavily adapted from posts on Stack Exchange. 

With that disclaimer out of the way, let's say you wanted to adapt this code to give times for a different stop or direction. That would happen in the `Scraping the train times` section. In there, you will find this definition of the `page` variable:

```python
page = requests.get("https://www.metrotransit.org/NexTripBadge.aspx?route=902&direction=3&stop=PSPK")
```

The information on route, direction, and stop are all contained at the end of the URL. Route `902` is the green line, `3` means the direction is westbound, and `PSPK` is short for the Prospect Park Station. All of these values are arbitrary and set by Metro Transit, so consult the NexTrip page for a specific stop to	find out how the values need to be changed. 

I have not tried adapting this code for a different stop. It very well might be that the `xpath` for the first and second trains may also be different.

---

<a name="reality"></a>
## The Reality of the Situation

This program isn't perfect. Neither is your Raspberry Pi's hardware or Metro Transit's website. All three of these have limits, and after using this program daily for several months, there are a few things I have noticed. 

<a name="hedges-bets"></a>
### Metro Transit Hedges Their Bets

The times displayed are generally longer than it will actually take for the train to arrive. This is true on the platform displays as well, but is less noticeable. When you're waiting on the platform and the display says `5 min`, but the train comes in 4 minutes, usually you don't mind. But if you know you need 5 minutes to walk to the station, you should probably leave when your home train time display says `6 min` or even `7 min` to be safe.

<a name="reaction-time"></a>
### Reaction Time

The program generally takes its sweet time responding to inputs. After a mouse click, the screen would turn on after 1 or 2 seconds. After a key press, the program would take 5 to 10 seconds to close.

<a name="refresh-rate"></a>
### Refresh Rate

The way the code is written, each go through the program loop should take one second. It usually takes longer. This is likely because of internet connection limitations. I made the clock in the top right blink the colon (`:`) on and off every time though the loop so you can monitor the refresh rate without closing the program. 

<a name="restarts"></a>
### Manual Restarts

I'm not sure what causes it, but once about every two weeks or so, the program will just fail. This often causes a blank screen, with or without a mouse cursor, or a view of the desktop. This is the main reason I built in the auto-run on startup. I would unplug and plug my Raspberry Pi back in. It usually took about 5 minutes for the program to actually be running again, but whatever the problem was seemed to go away. 

---

<a name="references"></a>
## Useful References

[Finding the resolution of the connected display in python]
(https://stackoverflow.com/questions/46008890/getting-physical-screen-size-in-python)

[Setting a script to auto-run on startup]
(https://www.raspberrypi.org/forums/viewtopic.php?t=200174`)