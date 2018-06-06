# Import Statements:
import re
import socket
from time import sleep

# Setup Variables:
HOST = "irc.twitch.tv"	# Twitch's IRC Server Address.
PORT = 6667		# Port for the Twitch IRC Server.
CHAN = "#kaoatlantis"	# Channel to connect to.
NICK = "BotAtlantis"	# Bot username.
PASS = "oauth:"		# Bot's AUTH Key.

#####################
# IRC Send Functions
#####################
def send_pong(msg):
	con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
	con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
	con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
	con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
	con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
	con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


########################
# IRC Recieve Functions
########################
def get_sender(msg):
	result = ""
	for char in msg:
		if char == "!":
			break
		if char != ":":
			result += char
	return result

def get_message(msg):
	result = ""
	i = 3
	length = len(msg)
	while i < length:
		result += msg[i] + " "
		i += 1
	result = result.lstrip(':')
	return result

########################
# IRC Recieve Functions
########################
def parse_message(msg):
	if len(msg) >= 1:
		fmsg = msg
		msg  = msg.split(' ')
		options = {'!social': command_social,
				}
		if msg[0] in options:
			options[msg[0]]()
		elif msg[0] == '!caster':
			command_caster(msg[1])

####################
# Command Functions
####################
def command_social(): # Need to come up with a way to rate limit the bot.
	send_message(CHAN, '.me Follow me on Twitter: https://twitter.com/kaoatlantis -and- Instagram: https://instagram.com/kaoatlantis')
	
def command_caster(caster):
	send_message(CHAN, 'Follow ' + caster + " because they are awesome! :D " + "http://twitch.tv/" + caster)
	
####################################
# Create Socekts and Connect to IRC
####################################
con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

# While loop to process recieved data:
while True:
	try:
		data = data+con.recv(1024).decode('UTF-8')
		data_split = re.split(r"[~\r\n]+", data)
		data = data_split.pop()

		for line in data_split:
			line = str.rstrip(line)
			line = str.split(line)

			if len(line) >= 1:
				if line[0] == 'PING':
					send_pong(line[1])

				if line[1] == 'PRIVMSG':
					sender = get_sender(line[0])
					message = get_message(line)
					parse_message(message)

					# This line doesn't work on Windows 10 for some reason. (It works on Linux and Mac OS)
					# It only crashes the program when Twerk says anything... weird. (Twerkspiracy?)
					# Commented this out to fix the problem for now:
					# print(sender + ": " + message) #<--- the broken code. WTF Windows 10.

	except socket.error:
		print("The socket died, connection closed.")

	except socket.timeout:
		print("The socket timed out, connection closed.")
