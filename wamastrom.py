"""
WAMASTROMBOT v2.0 by @Schmuel

Wamastrombot gives daily updates about the 🅆🄰ter level of the Elbe at the 🄼🄰gdeburg 🅂🅃🅁🄾🄼brücke.
This bot is a Christmas present for the author's big brother Sascha. Version 1.0 was tested and released in December 2019.

Version 2.0 is a performance update. Whats new?
🚀 Complete refactored Code
📎 Complete commentary
🔋 Better performance
🖳 Compatible with ARMv7 Processor
♺ This bot can run on Postmarket OS (tested on Nokia N900)

Wamastrombot v2.0 is powered by telebot from pyTelegramBotAPI.
https://pypi.org/project/pyTelegramBotAPI/

Wamastrombot v1.0 used the outdated version of Telepot:
https://github.com/nickoala/telepot

[SEWPER]
You may download use and modify this code. You are pleased to always copy the Licensing text (everything in this comment section from the [SEWPER] Tag and below) into your modified version.
WAMASTROMBOT by Schmuel
Release: 27.07.2021
Web: schmuel.net
Mail: pybots@schmuel.net
Telegram: @schmuel
Okuna: @schmuel
"""

"""
Imports:
Telebot 			-> API to receive and send messages
thread				-> Allow multithreads (better performance)
Time.sleep 			-> To reduce CPU usage
datetime.datetime && .time 	-> to check if its time to send the current water level
requests 			-> Access data information from the web
codecs				-> to be able to read UTF-8 files from the web
"""
import telebot
import _thread
from time import sleep
from datetime import datetime, time
import requests
import codecs

"""
init function: get user
This function creates a List with all user IDs from users.txt
The list will be used to send everyone the message with the current water level.
"""

def get_users():													#
	user_list = []													# Create empty List
	try:														#
		with open("users.txt", 'r') as users_file:								# open users.txt in read mode
			for line in users_file.readlines():								# Read every line in file
				user_list.append(int(line))								# Add ID to list
	except FileNotFoundError:											# This file might not exist
		pass													# Pass the error
	return user_list												#


"""
Globals:
bot 	-> Access the Telegram API
users 	-> Create a list of all users of this bot
"""
bot = telebot.TeleBot("[[API-KEY]]")
users = get_users()


"""
THREAD-function: check_time
This function will be called in a new Thread. It checks the time and sends the water level message to all
entities of the user_list
"""

def check_time():													#
	while True:													# infinite repeat
		if time(13, 15) < datetime.now().time() < time(13, 16):							# defined Time to send message: at 13:15 (01:15pm)
			level=getWaterLevel()										# get water level once to avoid multiple requests
			for user in users:										#
				bot.send_message(user, level)								# send message to all users
		sleep(60)												# sleep for one minute (must be improved)


"""
Function: write User
This function opens the file users.txt to add all the users from the user_list
"""
def write_users(user_list):												#
	with open("users.txt", 'w') as users_file:									# open users.txt in write mode
		users_file.write("\n".join([str(uid) for uid in user_list]))						# insert every item of users_list. Seperate by \n

		
"""
Function: append user
This function checks if the ID is already in user_list.
If not, it will add the ID to the list and update the users.txt file
"""
def append_user(id):													#
	if id not in users:												# Check if id not in users
		users.append(id)											# Append to list
		write_users(users)											# update file


"""
Function: get water level
This is a core function.
It opens the Data file and searches for 
"""

def getWaterLevel():
	url = 'https://www.elwis.de/DE/dynamisch/gewaesserkunde/wasserstaende/index.php?target=2&pegelId=ccccb57f-a2f9-4183-ae88-5710d3afaefd'
	with requests.Session() as s:											# Open a new Session called s
		try:													#
			r = s.post(url)											# load data from url as r
			content=r.text											# save the full string as content
			r.close()											# close the connection to the server
			content=content.split('<td valign="top" align="right" nowrap="nowrap"><b>', 1);			# cut the string at the defined HTML markerpoint 1
			content=content[1].split("</b></td>", 1);							# cut the string at the defined HTML markerpoint 2
			content=content[0]										# Get the string between both markerpoints. This should be the level in cm
			print(content)											# DEBUG: Print water level to console
		except:													# The requests.Session might fail
			pass												# pass the error
	return "Wasserstand: "+content+"cm"										# return a complete String (e.g. "197 cm")


"""
Start-Handler:
This function checks for an incomming /start command. It fetches the message.chat.id and sends it to append_user() in order to store it in a file called users.txt
The Data is used to send the daily water level information to all users of this bot. It can only be removed by the Bots owner or by the user by sending /stop (see also: Stop Handler)
"""
@bot.message_handler(commands=['start'])										# Init Handler
def handle_start(message):												# Function to call
	print(message.chat.id)												# DEBUG: Print ID to terminal (to be removed in release)
	append_user(message.chat.id)											# Add ID to User_list
	bot.send_message(message.chat.id, getWaterLevel())								# Send init Waterlevel on start


"""
Bot management
The commands below controll the different threads
bot.polling	-> Listen for handler events (as defined above)
thread.*	-> Start Threads
"""
_thread.start_new_thread(check_time, ())										# Start the time listener
print("Bot started")	
bot.polling()														# Start the bot listener											#
