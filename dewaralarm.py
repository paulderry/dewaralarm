#
#    dewaralarm.py - An alarm emailer for relay-based alarms for use on Raspberry Pi 2
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import time
import subprocess
import smtplib
import socket 
from email.mime.text import MIMEText
import datetime

# Set the mode to Broadcom Pin-out
GPIO.setmode(GPIO.BCM)

# Define your own pin, we're using 12 because it fit on the breadboard nicely.
BUTTON_PIN=12

# Set the pin mode
GPIO.setup(BUTTON_PIN, GPIO.IN)



def send_alert():

	# This function is basically the same thing presented here: http://raspi.com/projects/remote-monitoring-notification-gmail/

	print('DEBUG: INIT SMPT')

	target = 'yer_email@mailgoesthroughhere.notatld'
	gmail_user = 'thar_email@mailgoesthrougheretwo.notatld'
	gmail_pass = 'shiverthinetimbers'

	smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
	smtpserver.starttls()
     	smtpserver.ehlo # Log-in to mail account (secure with TLS)
     	smtpserver.login(gmail_user, gmail_pass)
	text = 'The cell dewar alarm is active. You might want to consider refilling the dewar.'

	msg = MIMEText(text)
	msg['Subject'] = '[%s] ALARM: Dewar Alarm.'% datetime.datetime.now().strftime("%x - %X")
	msg['From'] = gmail_user
	msg['To'] = target
	print('DEBUG: SENDMAIL')
	smtpserver.sendmail(gmail_user, [target], msg.as_string())
	smtpserver.quit()
def log_alert():
	with open('alarmlog.log','a') as f:
		f.write('[%s] ALARM: DEWAR ALARM.\n' % datetime.datetime.now().strftime("%x %X"))	

def log_restore():
	with open('alarmlog.log','a') as f:
		f.write('[%s] ALARM: RESTORED.\n' % datetime.datetime.now().strftime("%x %X"))

def check_later_loop():
	time.sleep(300) # Check in 5 minutes
	if GPIO.input(BUTTON_PIN) == True:
		print('[%s]\033[1;31m ALARM: DEWAR ALARM.\033[0;37m')% datetime.datetime.now().strftime("%x %X")
		send_alert()
		log_alert()
	else:
		print('[%s]\033[1;32m ALARM: RESTORED.\033[0;37m')% datetime.datetime.now().strftime("%x %X")
		log_restore()


def loop():
	if GPIO.input(BUTTON_PIN) == True:
		print('[%s]\033[1;33m ALARM: TRIGGERED.\033[0;37m')% datetime.datetime.now().strftime("%x %X")
		check_later_loop()

	else:
		time.sleep(1)
if __name__ == '__main__':
	try:
		print('ALARM: READY.')
		while True:
			loop()
	finally:
		GPIO.cleanup()

