<a name="top-of-doc"></a>
# Train Times

This program will turn your Raspberry Pi into a display showing the estimated times of arrival for the next two westbound green-line trains coming to the Prospect Park station in Minneapolis, Minnesota. 

## Table of Contents

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Setup](#code-blocks)
- [Headings](#headings)
- [Formatting Text](#formatting-text)
- [Lists and Bullet Points](#lists-and-bullets)
	- [Ordered Lists](#ordered-lists)
	- [Bullet Points](#bullet-points)
	- [Mixed Lists and Sub-items](#mixed-lists)
- [Links and Anchors](#links)
- [Images](#images)
- [Footnotes](#footnotes)

<!-- TOC -->

[//]: # (In order for headings with spaces to link to an entry in the TOC, you need the HTML-ish line below. The name needs to match what is in the parentheses in the TOC. They are put on the line before the heading so that the heading shows up when the link is clicked.)

---

## Setup

This program was written for Python 3 and requires the following packages: `lxml`, `requests`, and `pygame`. If you have Python 3, you most likely have `pip3` installed which can be used to install these packages with the following commands:

```bash
$ sudo apt-get install python3-lxml
$ pip3 install requests
$ pip3 install pygame
```

---

## Useful references

Finding the resolution of the connected display in python:
https://stackoverflow.com/questions/46008890/getting-physical-screen-size-in-python

Setting a script to auto-run on startup
https://www.raspberrypi.org/forums/viewtopic.php?t=200174