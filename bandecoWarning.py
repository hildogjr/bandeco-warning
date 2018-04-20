#!/usr/bin/python
# -*- coding: utf-8 -*-
# Print a message using the libraries of the operacional system with the next menu of the university's restaurant. Correct the name of the juices ;-)
#
# Written by Hildo Guillardi Júnior - FEEC - UNICAMP - 05/Apr/2017
# Python 2.7 + Ubuntu 16.04
# Modified on ?/April/2017, working with Limeira's menu and capitalize the text.
# Modified on 08/April/2018 to work with Python 3+.
#
# Installation tips: use the crontab to program the automatic messages
#	cd . # Actual installation files folder
#	modifycronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$2" ; echo "$1 $2" ) | crontab  -u $USER -;}
#	removecronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$1" ) | crontab  -u $USER -;}
#	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#	modifycronjob "15 11,17 * * 1-5" 'eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)";'" DISPLAY=:0; python '$DIR/bandecoWarning.py'" # Lunch & dinner warning
#	sudo service cron start
# This software is released under the GNU-GPL 3.0 or later.

# --------------- User definitions ---------------

preferedFoods = ('estrogonofe (?!vegetariano)[\s\S]+', 'alm[oô]ndega', 'carne alessa', 'carne assada', 'cocada','doce de leite') # Use regular expressions language
notPreferedFoods = ['salsicha', 'steak', 'nuggets']

link = 'https://www.prefeitura.unicamp.br/apps/site/cardapio.php' # Campinas campus
#link = "http://www.pfl.unicamp.br/Restaurante/PF/view/site/cardapio.php" # Limeira campus

timeLunchFinish = 14
timeDinnerFinish = 19


# --------------- Libraries ---------------

from sys import version_info as pyVersion
if pyVersion>(3,0):
	from urllib.request import urlopen # To read internet page on Python 3.
else:
	from urllib2 import urlopen  # To read internet page on Python 2.
from xml.sax.saxutils import unescape as unescapeHTMLcodes
import re # Regular expression engine.
import os # To access OS commands.
import platform # To check the system platform.
import datetime # To get system date-time and calculation with than.
from datetime import datetime, timedelta
from math import ceil
if pyVersion>(3,0):
	from itertools import accumulate as cumsum # Accumulative sum.
else:
	def cumsum(vector):
		vectorAcc = 0
		for item in vector:
			vectorAcc += item
			yield vectorAcc


# --------------- Especific funcitions, definitions 7 etc... ---------------

""" Popular names of the juices
"""
juiceRealName={'uva':'roxo','abacaxi':'plutônio','limão':'branco','tangerina':'laranja 1','acerola':'laranja 2','laranja':'amarelo 1','caju':'amarelo 2','maracujá':'amarelo 3','manga':'amarelo 4'}


""" Ballon system message """
def systemMessage(title,message):
	#os.path.dirname(os.path.abspath(__file__))
	#os.getcwd()
	#print os.path.dirname(os.path.abspath(__file__))
	if platform.system()=='Linux':
		#os.system('eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)"; DISPLAY=:0; notify-send "'+title+'" "'+message+'" -t 8 -u low -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMPfood.png"')
		# Necessary to set some enviroment variables.
		# The maximum message length is 461 continuous characters or 459 if needed '...', each line with 49 maximum characters.
		
		# Count the message to not show the ending (the standard for `notify-send`is not show the beginning if have more than one line).
		NS_MENS_MAX_LEN = 461 # Maximum continuous message for `notify-send`.
		NS_LINE_MAX_LEN = 49.0 # Maximum line characters for `notify-send`. Necessary the `.0`to the division result in real without addition libraries to python (`from __future__ import division`).
		NS_3DOT_LEN = 2  # 3-Dot characters equivalence in `notify-send`.
		messageSpplited = re.split('\r*\n\r*', message)
		messageSpplitedLengths = [ ceil( len(m)/NS_LINE_MAX_LEN ) for m in messageSpplited ]
		if sum( messageSpplitedLengths ) > NS_MENS_MAX_LEN:
			lengthLinesValid = [l for l in list(cumsum( messageSpplitedLengths )) if l >= 5]
			message = '\n'.join( messageSpplited[:range(len(lengthLinesValid))] )
			message = '\n' + messageSpplited[:len(lengthLinesValid)+1][0:lengthLinesValid[-1]+1-NS_3DOT_LEN] + '...'
		
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u critical -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMPfood.png"') # Linux-Ubuntu ballon notification.
	elif platform.system()=='Windows':
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u low -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMPfood.png"') # Linux-Ubuntu ballon notification.
	elif platform.system()=='Darwin':
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u low -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMPfood.png"') # Linux-Ubuntu ballon notification.
	else: # Not tested.
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u low -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMPfood.png"') # Linux-Ubuntu ballon notification.


""" Capitilize una string: in the begging, after ?/!/. and space but not acronym, even when is using multiple spaces, end/letter of acronyms """
def capitalize(s):
	return re.sub(r"(^\s*\w)|(?<!\.\w)([\.?!]\s*)\w|\w(?:\.\w)|(?<=\w\.)\w", lambda x: x.group().upper(), s, flags=re.M)


""" HTML character code to the ascii codes dictionary """
htmlCodesDict = {'&Aacute;':u'\xc1', '&aacute;':u'\xe1', '&Agrave;':u'\xc0', '&Acirc;':u'\xc2', '&agrave;':u'\xe0', '&Acirc;':u'\xc2', '&acirc;':u'\xe2', '&Auml;':u'\xc4', '&auml;':u'\xe4', '&Atilde;':u'\xc3', '&atilde;':u'\xe3', '&Aring;':u'\xc5', '&aring;':u'\xe5', '&Aelig;':u'\xc6', '&aelig;':u'\xe6', '&Ccedil;':u'\xc7', '&ccedil;':u'\xe7', '&Eth;':u'\xd0', '&eth;':u'\xf0', '&Eacute;':u'\xc9', '&eacute;':u'\xe9', '&Egrave;':u'\xc8', '&egrave;':u'\xe8', '&Ecirc;':u'\xca', '&ecirc;':u'\xea', '&Euml;':u'\xcb', '&euml;':u'\xeb', '&Iacute;':u'\xcd', '&iacute;':u'\xed', '&Igrave;':u'\xcc', '&igrave;':u'\xec', '&Icirc;':u'\xce', '&icirc;':u'\xee', '&Iuml;':u'\xcf', '&iuml;':u'\xef', '&Ntilde;':u'\xd1', '&ntilde;':u'\xf1', '&Oacute;':u'\xd3', '&oacute;':u'\xf3', '&Ograve;':u'\xd2', '&ograve;':u'\xf2', '&Ocirc;':u'\xd4', '&ocirc;':u'\xf4', '&Ouml;':u'\xd6', '&ouml;':u'\xf6', '&Otilde;':u'\xd5', '&otilde;':u'\xf5', '&Oslash;':u'\xd8', '&oslash;':u'\xf8', '&szlig;':u'\xdf', '&Thorn;':u'\xde', '&thorn;':u'\xfe', '&Uacute;':u'\xda', '&uacute;':u'\xfa', '&Ugrave;':u'\xd9', '&ugrave;':u'\xf9', '&Ucirc;':u'\xdb', '&ucirc;':u'\xfb', '&Uuml;':u'\xdc', '&uuml;':u'\xfc', '&Yacute;':u'\xdd', '&yacute;':u'\xfd', '&yuml;':u'\xff', '&copy;':u'\xa9', '&reg;':u'\xae', '&trade;':u'\u2122', '&euro;':u'\u20ac', '&cent;':u'\xa2', '&pound;':u'\xa3', '&lsquo;':u'\u2018', '&rsquo;':u'\u2019', '&ldquo;':u'\u201c', '&rdquo;':u'\u201d', '&laquo;':u'\xab', '&raquo;':u'\xbb', '&mdash;':u'\u2014', '&ndash;':u'\u2013', '&deg;':u'\xb0', '&plusmn;':u'\xb1', '&frac14;':u'\xbc', '&frac12;':u'\xbd', '&frac34;':u'\xbe', '&times;':u'\xd7', '&divide;':u'\xf7', '&alpha;':u'\u03b1', '&beta;':u'\u03b2', '&infin':u'\u221e'}


# --------------- Main program ---------------

# If is after the time of the dinner read the next day menu.
if datetime.now().hour >= timeDinnerFinish:
	date_today = datetime.today()
	if date_today.strftime("%a")=='Fri':
		delta = 3
	else:
		delta = 1
	dayFuture = date_today+timedelta(days=delta)
	#print dayFuture.strftime("%Y-%m-%d")
	link = link+'?d='+dayFuture.strftime("%Y-%m-%d")
#	title = 'Próximo'
#else:
#	title = '' # No especial message title.

# Read the page
f = urlopen(link)
page = f.read()
f.close()
del f,link
#page = page.decode('ascii') # Necessary to convert <class byte> array to <str>.

# Separate the diferents menus of the day.
if pyVersion>=(3,0):
	page = page.decode('windows-1252') # UNICAMP use a Windows server fr this servce.
page = re.sub('<!--[\S\s]+?-->','',page) # Remove all the comments to simplify the parse, the Limeira web page is the same of Campinas page but with the vegetarian menu as comment.
#menuSearchString = '<td align="left" valign="top">[\t\r\n\s]*<table [width="[\d%]+" ]*class="fundo_cardapio">([\s\S\d\t\r\n]+?)<\/table>[\t\r\n\s]*<\/td>' # This just works in Campinas menus web page.
menuSearchString = '<td align="left" valign="top">[\t\r\n\s]*<table[\S\s]*? class="fundo_cardapio">([\s\S\d\t\r\n]+?)<\/table>[\t\r\n\s]*<\/td>'
menus = re.findall(menuSearchString,page,flags=re.IGNORECASE)
del page,menuSearchString

# Parse and format the strings.
for count in range(len(menus)):
	menus[count] = re.sub('((<\/td>[\r\n\s]*<\/tr>[\r\n\s]*<tr>[\r\n\s]*<td>))',', ',menus[count]) # Remove multitables between menu same category lines.
	menus[count] = re.sub('\t*\n*\r*(<td>)*(<\/td>)*(<tr>)*(<\/tr>)*(<strong>)*(<\/strong>)*(<br>)*(\s\s+)*(^\s*)*','',menus[count]) # Remove HTML tags, duplicated and initial spaces.
	if pyVersion>=(3,0):
		menus[count] = menus[count].lower()
	else:
		menus[count] = menus[count].decode('windows-1252').lower()#.encode('utf-8') # Change the codec used in the string coding, it was used Windows codec.
	pattern = re.compile('|'.join(htmlCodesDict.keys())) # Compile the pattern to replace the HTML &**; codes found in some pages (Limeira's menus).
	if pyVersion<(3,0):
		menus[count] = pattern.sub(lambda x: htmlCodesDict[x.group()], menus[count]).encode('utf-8')
	#menus[count] = unescapeHTMLcodes(menus[count])
	menus[count] = re.sub(',*\s*prato principal:\s*', ', ', menus[count], re.IGNORECASE)
	menus[count] = re.sub(',*\s*pts',', pts', menus[count], flags=re.IGNORECASE)
	menus[count] = re.sub(',*\s*salada:\s*', ' - ',menus[count], re.IGNORECASE)
	menus[count] = re.sub(',*\s*sobremesa:\s*', '\r\nSOBREMESA: ', menus[count], re.IGNORECASE)
	menus[count] = re.sub(',*\s*suco:\s*', '\r\nSUCO: ', menus[count], re.IGNORECASE)
	menus[count] = re.sub(',*\s*observações:\s*', '\r\n', menus[count], re.IGNORECASE)
	#menus[count] = re.sub('\s*\r\n\s*','\r\n',menus[count])
	#pattern = re.compile('|'.join(juiceRealName.keys()))
	#menus[count] = pattern.sub(lambda x: juiceRealName[x.group()], menus[count])
	juice = re.findall('\r\nSUCO: (\S+)\r\n',menus[count])
	if juice!=[] and juice[0] in juiceRealName:
		menus[count] = re.sub('\r\nSUCO: (\S+)\r\n', '\r\nSUCO: '+juiceRealName[juice[0]]+'\r\n' ,menus[count]) # Real name of the juice
	menus[count] = capitalize(menus[count]) # Capitilize the text to better presentation.

del juice,count

# Filter the lunch and dinner menu, Campinas and Limeira campus (change the format of the page, Limeira don't have vegeratarian option).
title='' # Now, the title receive the "Próximo" to indicate next day.
message=''
if len(menus)==4: # Campinas campus' menu
	#message = 'ALMOÇO:\r\n' +  menus[0] + 'ALMOÇO VEGETARIANO:\r\n' + menus[1] + '\r\n\r\nJANTAR:\r\n' + menus[2] + '\r\n' + 'JANTAR VEGETARIANO:\r\n' + menus[3].
	if datetime.now().hour >= timeDinnerFinish: # Next day lunch menu.
		title += 'Almoço futuro UNICAMP'
		message = menus[0] + '\r\nVEGETARIANO: ' + re.findall('([\S\s]+)\r\nSUCO: ', menus[1], re.IGNORECASE)[0]
	elif datetime.now().hour < timeLunchFinish: # Lunch menu.
		title += 'Almoço UNICAMP'
		message = menus[0] + '\r\nVEGETARIANO: ' + re.findall('([\S\s]+)\r\nSUCO: ', menus[1], re.IGNORECASE)[0]
	else: # Dinner menu.
		title += 'Jantar UNICAMP'
		message = menus[2] + '\r\nVEGETARIANO: ' + re.findall('([\S\s]+)\r\nSUCO: ', menus[3], re.IGNORECASE)[0]	
	message = re.sub('\r\nSUCO: ', ' - SUCO: ', message) # Better and short text view, remove duplicated juice information.
	dessert = re.findall('\r\nSOBREMESA:\s*(\w+)?', message, re.IGNORECASE);
	if len(dessert)==2 and dessert[0]==dessert[1]:
		message = re.sub('\r\nSOBREMESA:\s*\w+$', '', message) # Remove replicated information of dessert (sometimes normal and vegetarian menus have different desserts).
elif len(menus)==2: # Limeira campus' menu.
	#message = 'ALMOÇO:\r\n' +  menus[0] + '\r\n\r\nJANTAR:\r\n' + menus[1]
	if datetime.now().hour >= timeDinnerFinish: # Next day lunch menu.
		title += 'Almoço futuro UNICAMP'
		message = menus[0]
	elif datetime.now().hour < timeLunchFinish: # Lunch menu.
		title += 'Almoço UNICAMP'
		message = menus[0]
	else: # Dinner menu.
		title += 'Jantar UNICAMP'
		message = menus[1]
else:
	title += 'Cardápio'
	message = 'Error!!!'

del menus

# Remove/change unuserfull messages.
messagesRemove = (
	'(\<[\w\s="]+\>)*[a-zãç\s,]+caneca[\s*\!*]*(\<[\/\w\s]+\>)*', # New "caneca" message started in the week of 05/June/2017.
	'o cardápio contém glúte[nm][\s\S]+\.\s*',
	'contém traços de lactose[\s\S]+\.\s*',
	'contém ovos e lactose[\w\s]+\.\s*',
	'o cardápio vegetariano será servido somente no rs',
	'(\s*obs:\s*\.)', # If do not gave any observation, remove "obs:" of the message.
	'<[\S\s]*?>',
	)
for m in messagesRemove:
	message = re.sub(m,'', message, flags=re.IGNORECASE)

message = re.sub('não há cardápio cadastrado\!','Se vira!', message, flags=re.IGNORECASE)

# Look for important foods in the day menu.
for food in preferedFoods:
	if re.search(food, message, flags=re.IGNORECASE):
		title = '\\o/ ' + title
for food in notPreferedFoods:
	if re.search(food, message, flags=re.IGNORECASE):
		title = '=( ' + title
del preferedFoods, notPreferedFoods

systemMessage(title, message) # Put message on the screen.
del title, message
