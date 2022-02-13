#
#Telegrambot.py
#
#Autor: Alex Merz
#


#Libraries
import telebot
import datetime
import requests
import time
import threading
from threading import *
from bs4 import BeautifulSoup
import Clock
from telebot import types
import os


#API of bot
bot = telebot.TeleBot("Your Telegram API")


#User id's
Alex_Id = "Your Id, so only you have access to it"


#Url of websites
urlPiHole = 'Ip/Adress pf your Pihole'
urlCloud = 'Ip/Adress of your cloud'
urlSwissfotoclan = 'Adress of your webside'
urlSmartHome = 'Ip/Adress of your smarthome page'


#Local variable
attackCounter = 0
shutdownCounter = 0
runBot = True
ClockGreen = 0
ClockRed = 0
ClockBlue = 50
ClockBrightness = 100
ClockStatus = True


#Local const
attackNbrWarning = 20
attackNbrLastWarning = 40
attackNbrMax = 50
resetAttackCounterTimeHour = 23
resetAttackCounterTimeMinute = 1

dailyMessageTimeHour = 12
dailyMessageTimeMinute = 10

ClockSleepStartHour = 23
ClockSleepStartMinute = 59
ClockSleepEndHour = 5
ClockSleepEndMinute = 30
ClockSleepSet = False


####################Function: Command /help
@bot.message_handler(commands=['help'])
def command_Help(message):
	Tmp_text = 'Hallo '
	Tmp_text = Tmp_text + str(message.from_user.first_name)
	Tmp_text = Tmp_text + '. Ich bin der AXBot\n\nMeine Befehlliste:\n'
	Tmp_text = Tmp_text + '/getid -> Erhalte deine eigene Id\n'
	Tmp_text = Tmp_text + '/server -> Erhalte den Server Status\n'
	Tmp_text = Tmp_text + '/shutdownbot -> Schalte den Bot aus\n'
	Tmp_text = Tmp_text + '/setclockcolor -> Wanduhr Farbe umstellen\n'
	Tmp_text = Tmp_text + '/setclockbrightness -> Wanduhr Helligkeit umstellen\n'
	bot.send_message(message.chat.id, Tmp_text)


####################Function: Command /setclockbrightness
@bot.message_handler(commands=['setclockbrightness'])
def command_SetClockBrightness(message):
	if message.chat.id == Alex_Id:
		keyboard = telebot.types.InlineKeyboardMarkup()

		button_1 = telebot.types.InlineKeyboardButton(text="0", callback_data="0")
		button_2 = telebot.types.InlineKeyboardButton(text="+10", callback_data="+10")
		button_3 = telebot.types.InlineKeyboardButton(text="+100", callback_data="+100")
		button_4 = telebot.types.InlineKeyboardButton(text="-100", callback_data="-100")
		button_5 = telebot.types.InlineKeyboardButton(text="-10", callback_data="-10")
		button_6 = telebot.types.InlineKeyboardButton(text="255", callback_data="255")

		keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
		keyboard.one_time_keyboard = True
		bot.send_message(message.chat.id, "Waehle die Helligkeit der Uhr:", reply_markup=keyboard)
	else: #Unknown user
		botFirewall(message.chat.id)
		bot.send_message(Alex_Id, "Bot wurde angegriffen von User " + str(message.chat.id))
		bot.send_message(message.chat.id, "Du hast die Freigabe nicht um den Server Status einzusehen")
		print('User ' + str(message.chat.id) + ' wollte Server Status einsehen')
		return


####################Function: Command /setclockcolor
@bot.message_handler(commands=['setclockcolor'])
def command_SetClockColor(message):
	if message.chat.id == Alex_Id:
		keyboard = telebot.types.InlineKeyboardMarkup()

		button_1 = telebot.types.InlineKeyboardButton(text="G=0", callback_data="G=0")
		button_2 = telebot.types.InlineKeyboardButton(text="G+10", callback_data="G+10")
		button_3 = telebot.types.InlineKeyboardButton(text="G+100", callback_data="G+100")
		button_4 = telebot.types.InlineKeyboardButton(text="G-100", callback_data="G-100")
		button_5 = telebot.types.InlineKeyboardButton(text="G-10", callback_data="G-10")
		button_6 = telebot.types.InlineKeyboardButton(text="G=255", callback_data="G=255")

		button_7 = telebot.types.InlineKeyboardButton(text="R=0", callback_data="R=0")
		button_8 = telebot.types.InlineKeyboardButton(text="R+10", callback_data="R+10")
		button_9 = telebot.types.InlineKeyboardButton(text="R+100", callback_data="R+100")
		button_10 = telebot.types.InlineKeyboardButton(text="R-100", callback_data="R-100")
		button_11 = telebot.types.InlineKeyboardButton(text="R-10", callback_data="R-10")
		button_12 = telebot.types.InlineKeyboardButton(text="R=255", callback_data="R=255")

		button_13 = telebot.types.InlineKeyboardButton(text="B=0", callback_data="B=0")
		button_14 = telebot.types.InlineKeyboardButton(text="B+10", callback_data="B+10")
		button_15 = telebot.types.InlineKeyboardButton(text="B+100", callback_data="B+100")
		button_16 = telebot.types.InlineKeyboardButton(text="B-100", callback_data="B-100")
		button_17 = telebot.types.InlineKeyboardButton(text="B-10", callback_data="B-10")
		button_18 = telebot.types.InlineKeyboardButton(text="B=255", callback_data="B=255")

		button_19 = telebot.types.InlineKeyboardButton(text="Ein", callback_data="Ein")
		button_20 = telebot.types.InlineKeyboardButton(text="Aus", callback_data="Aus")

		keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6,
					button_7, button_8, button_9, button_10, button_11, button_12,
					button_13, button_14, button_15, button_16, button_17, button_18,
					button_19, button_20)
		keyboard.one_time_keyboard = True
		bot.send_message(message.chat.id, "Setze die Uhr Farbe:", reply_markup=keyboard)
	else: #Unknown user
		botFirewall(message.chat.id)
		bot.send_message(Alex_Id, "Bot wurde angegriffen von User " + str(message.chat.id))
		bot.send_message(message.chat.id, "Du hast die Freigabe nicht um den Server Status einzusehen")
		print('User ' + str(message.chat.id) + ' wollte Server Status einsehen')
		return


####################Function: callback after setclockcolor command
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		global ClockGreen
		global ClockRed
		global ClockBlue
		global ClockBrightness
		global ClockStatus
		global ClockRainbow

		if call.data == "G=0":
			ClockGreen = 0
		if call.data == "G=255":
			ClockGreen = 255
		if call.data == "G+10":
			ClockGreen = ClockGreen + 10
		if call.data == "G+100":
			ClockGreen = ClockGreen + 100
		if call.data == "G-10":
			ClockGreen = ClockGreen - 10
		if call.data == "G-100":
			ClockGreen = ClockGreen - 100
		if ClockGreen < 0:
			ClockGreen = 0
		if ClockGreen > 255:
			ClockGreen = 255

		if call.data == "R=0":
			ClockRed = 0
		if call.data == "R=255":
			ClockRed = 255
		if call.data == "R+10":
			ClockRed = ClockRed + 10
		if call.data == "R+100":
			ClockRed = ClockRed + 100
		if call.data == "R-10":
			ClockRed = ClockRed - 10
		if call.data == "R-100":
			ClockRed = ClockRed - 100
		if ClockRed < 0:
			ClockRed = 0
		if ClockRed > 255:
			ClockRed = 255

		if call.data == "B=0":
			ClockBlue = 0
		if call.data == "B=255":
			ClockBlue = 255
		if call.data == "B+10":
			ClockBlue = ClockBlue + 10
		if call.data == "B+100":
			ClockBlue = ClockBlue + 100
		if call.data == "B-10":
			ClockBlue = ClockBlue - 10
		if call.data == "B-100":
			ClockBlue = ClockBlue - 100
		if ClockBlue < 0:
			ClockBlue = 0
		if ClockBlue > 255:
			ClockBlue = 255

		if call.data == "Ein":
			ClockStatus = True
		if call.data == "Aus":
			ClockStatus = False

		if call.data == "0":
			ClockBrightness = 0
		if call.data == "255":
			ClockBrightness = 255
		if call.data == "+10":
			ClockBrightness = ClockBrightness + 10
		if call.data == "+100":
			ClockBrightness = ClockBrightness + 100
		if call.data == "-10":
			ClockBrightness = ClockBrightness - 10
		if call.data == "-100":
			ClockBrightness = ClockBrightness - 100
		if ClockBrightness < 0:
			ClockBrightness = 0
		if ClockBrightness > 255:
			ClockBrightness = 255


####################Function: Command /getid
@bot.message_handler(commands=['getid'])
def command_GetId(message):
	Tmp_text = 'Deine Id ist: '
	Tmp_text = Tmp_text + str(message.chat.id)
	bot.send_message(message.chat.id, Tmp_text)


####################Function: Command /server (Get server status)
@bot.message_handler(commands=['server'])
def command_GetServerStatus(message):
	if message.chat.id == Alex_Id:
		#####PiHole Server
		Tmp_text = 'Pi-Hole Server Status:\n'

		#Check connection
		connection = False #Default
		try:
			Server_PiHole = requests.get(urlPiHole, timeout=5)
			connection = True
		except:
			connection = False
			Tmp_text = Tmp_text + '     -Offline -> ERROR!!!\n\n'
			print('Server PiHole Error (Keine Verbindung)')

		#Check server
		if connection:
			if Server_PiHole.ok: #Check if server works
				Tmp_text = Tmp_text + '     -Online\n\n'
			else: #Server error
				Tmp_text = Tmp_text + '     -Fehler -> ERROR!!!\n\n'
				print('Server PiHole Error (Status_code=' + str(Server_PiHole.status_code) + ')')


		#####Cloud Server
		Tmp_text = Tmp_text + 'NextCloud Server Status:\n'

		#Check connection
		connection = False #Default
		try:
			Server_Cloud = requests.get(urlCloud, timeout=5)
			connection = True
		except:
			connection = False
			Tmp_text = Tmp_text + '     -Offline -> ERROR!!!\n'
			print('Server NextCloud Error (Keine Verbindung)')

		#Check server
		if connection:
			if Server_Cloud.ok: #Check if server works
				Tmp_text = Tmp_text + '     -Online\n\n'
			else: #Server error
				Tmp_text = Tmp_text + '     -Fehler -> ERROR!!!\n\n'
				print('Server NextCloud Error (Status_code=' + str(Server_Cloud.status_code) + ')')

		#####Smart Home
		Tmp_text = Tmp_text + 'Smart Home Status:\n'

		#Check connection
		connection = False #Default
		try:
			Server_SmartHome = requests.get(urlSmartHome, timeout=5)
			connection = True
		except:
			connection = False
			Tmp_text = Tmp_text + '     -Offline -> ERROR!!!\n'
			print('Smart Home Error (Keine Verbindung)')

		#Check server
		if connection:
			if Server_SmartHome.ok: #Check if server works
				Tmp_text = Tmp_text + '     -Online\n\n'
			else: #Server error
				Tmp_text = Tmp_text + '     -Fehler -> ERROR!!!\n\n'
				print('Smart Home Error (Status_code=' + str(Server_SmartHome.status_code) + ')')

		bot.send_message(message.chat.id, Tmp_text)
		return
	else: #Unknown user
		botFirewall(message.chat.id)
		bot.send_message(Alex_Id, "Bot wurde angegriffen von User " + str(message.chat.id))
		bot.send_message(message.chat.id, "Du hast die Freigabe nicht um den Server Status einzusehen")
		print('User ' + str(message.chat.id) + ' wollte Server Status einsehen')
		return


####################Function: Get daily server status
def getDailyServerStatus():
	#####PiHole Server
	Tmp_text = 'Pi-Hole Server Status:\n'

	#Check connection
	connection = False #Default
	try:
		Server_PiHole = requests.get(urlPiHole, timeout=5)
		connection = True
	except:
		connection = False
		Tmp_text = Tmp_text + '     -Offline -> ERROR!!!\n\n'
		print('Server PiHole Error (Keine Verbindung)')

	#Check server
	if connection:
		if Server_PiHole.ok: #Check if server works
			Tmp_text = Tmp_text + '     -Online\n\n'
		else: #Server error
			Tmp_text = Tmp_text + '     -Fehler -> ERROR!!!\n\n'
			print('Server PiHole Error (Status_code=' + str(Server_PiHole.status_code) + ')')


	#####Cloud Server
	Tmp_text = Tmp_text + 'NextCloud Server Status:\n'

	#Check connection
	connection = False #Default
	try:
		Server_Cloud = requests.get(urlCloud, timeout=5)
		connection = True
	except:
		connection = False
		Tmp_text = Tmp_text + '     -Offline -> ERROR!!!\n'
		print('Server NextCloud Error (Keine Verbindung)')

	#Check server
	if connection:
		if Server_Cloud.ok: #Check if server works
			Tmp_text = Tmp_text + '     -Online\n\n'
		else: #Server error
			Tmp_text = Tmp_text + '     -Fehler -> ERROR!!!\n\n'
			print('Server NextCloud Error (Status_code=' + str(Server_Cloud.status_code) + ')')


	#####Smart Home
		Tmp_text = Tmp_text + 'Smart Home Status:\n'

		#Check connection
		connection = False #Default
		try:
			Server_SmartHome = requests.get(urlSmartHome, timeout=5)
			connection = True
		except:
			connection = False
			Tmp_text = Tmp_text + '     -Offline -> ERROR!!!\n'
			print('Smart Home Error (Keine Verbindung)')

		#Check server
		if connection:
			if Server_SmartHome.ok: #Check if server works
				Tmp_text = Tmp_text + '     -Online\n\n'
			else: #Server error
				Tmp_text = Tmp_text + '     -Fehler -> ERROR!!!\n\n'
				print('Smart Home Error (Status_code=' + str(Server_SmartHome.status_code) + ')')

	bot.send_message(Alex_Id, Tmp_text)


####################Function: Command /shutdownbot
@bot.message_handler(commands=['shutdownbot'])
def command_ShutdownBot(message):
	if message.chat.id == Alex_Id:
		global shutdownCounter
		
		if shutdownCounter == 0:
			bot.send_message(Alex_Id, 'Bot abschalten -> Sind Sie sicher?')
			shutdownCounter = shutdownCounter + 1
		elif shutdownCounter == 1:
			bot.send_message(Alex_Id, 'ABSOLUT SICHER???')
			shutdownCounter = shutdownCounter + 1
		elif shutdownCounter >= 2:
			bot.send_message(Alex_Id, 'Bot schaltet sich aus -> Bye bye')
			global runBot
			runBot = False
	else:
		bot.send_message(message.chat.id, 'Du hast keine Berechtigung dafuer')


####################Function: Return in case of wrong command
@bot.message_handler(func=lambda m: True)
def command_Unknown(message):

	bot.send_message(message.chat.id, "Dieses Kommando kenne ich nicht -> Tipp /help")
	botFirewall(message.chat.id)
	print('Ungueltiges Kommando von User ' + str(message.chat.id))


####################Function: Bot firewall
def botFirewall(HackerId):
	global attackCounter
	attackCounter = attackCounter + 1

	#Check attackCounter
	if attackCounter == attackNbrWarning:
		bot.send_message(Alex_Id, "WARNUNG!!! Bot wurde " + str(attackNbrWarning) + ' mal angegriffen')
	elif attackCounter == attackNbrLastWarning:
		bot.send_message(Alex_Id, "WARNUNG!!! Bot wurde " + str(attackNbrLastWarning) + ' mal angegriffen. Bot schaltet sich demnaechst automatisch aus.')
	elif attackCounter >= attackNbrMax:
		bot.send_message(HackerId, "YOU SHALL NOT PASS!!!")
		bot.send_message(Alex_Id, 'Letzte Nachricht von Bot -> Bot schaltet sich zum Schutz fuer Netzwerk ab.')
		print('Bot wurde ' + str(attackNbrMax) + ' mal angegriffen. Automatischer Shutdown.')
		global runBot
		runBot = False


####################Function: Reboot
def reboot():
	os.system('sudo reboot')


####################Thread: Telegrambot
class botThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		bot.polling()


####################Thread: Daily message from Telegrambot
class dailyThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			#Get actual time
			actualDateTime = datetime.datetime.now()
			actualTime = actualDateTime.time()

			#Check if message has to be send
			if ((actualTime.hour == dailyMessageTimeHour) and (actualTime.minute == dailyMessageTimeMinute)):
				getDailyServerStatus()
				time.sleep(60)
			elif ((actualTime.hour == resetAttackCounterTimeHour) and (actualTime.minute == resetAttackCounterTimeMinute)):
				global attackCounter
				attackCounter = 0
				global shutdownCounter
				shutdownCounter = 0

			time.sleep(30)


####################Thread: Check heardbeat of bot
class checkBotThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			#Check connection
			connection = False #Default
			try:
				Swissfotoclan = requests.get(urlSwissfotoclan, timeout=5)
				connection = True
			except:
				connection = False
				print('Keine Verbindung zum Internet')

			#Check Bot
			if (not Swissfotoclan.ok) or (not connection): #Check if server doesn't works
				print('Raspberry Pi wird automatisch neugestartet')
				reboot()

			time.sleep(3600) #Sleep for 1 hour


####################Thread: Clock
class clockThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global ClockGreen
		global ClockRed
		global ClockBlue
		global ClockBrightness
		global ClockStatus
		global ClockSleepStartHour
		global ClockSleepStartMinute
		global ClockSleepEndHour
		global ClockSleepEndMinute
		global ClockSleepSet
		global ClockStatus

		Clock.Startup()

		while True:
			#Get actual time
			actualDateTime = datetime.datetime.now()
			actualTime = actualDateTime.time()

			#Check if clock has to sleep
			if ((ClockSleepSet == False) and (actualTime.hour == ClockSleepStartHour) and (actualTime.minute == ClockSleepStartMinute)):
				ClockSleepSet = True
				ClockStatus = False #Turn light off
			elif ((ClockSleepSet == True) and (actualTime.hour == ClockSleepEndHour) and (actualTime.minute == ClockSleepEndMinute)):
				ClockSleepSet = False
				ClockStatus = True #Turn light on
				reboot() #Reboot after 24h, because after Telegram update a reboot is necessary

			Clock.ClockControl(ClockGreen, ClockRed, ClockBlue, ClockBrightness, ClockStatus)


####################Multithreading handling
thread1 = botThread()
thread2 = dailyThread()
thread3 = clockThread()
thread4 = checkBotThread()

thread1.daemon = True #If main dies the child thread dies too
thread2.daemon = True #If main dies the child thread dies too
thread3.daemon = True #If main dies the child thread dies too
thread4.daemon = True #If main dies the child thread dies too

thread1.start()
thread2.start()
thread3.start()
thread4.start()


####################Main
bot.send_message(Alex_Id, 'Bot ist online')
print('Bot ist online')
while (runBot):
	pass
print('Bot ist offline')

