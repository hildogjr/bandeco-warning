# -*- coding: utf-8 -*-
# Check the day menu of the university restaurant and print a message in the system using the libraries od the operacional system. Correct the name of the juices ;-)
#
# Written by Hildo Guillardi Júnior - FEEC - UNICAMP - 05/Apr/2017
# Python 2.7 + Ubuntu 16.04
#
# Installation tips: use the crontab to program the automatic messages
#	cd . # Actual installation files folder
#	addcronjob(){( crontab -l -u $USER 2>/dev/null | grep -v -F "$2" ; echo "$1 $2" ) | crontab  -u $USER -}
#	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#	addcronjob "0 11 * * 1-5" "python $DIR/bandecoWarning.py" # Lunch warning
#	addcronjob "0 17 * * 1-5" "python $DIR/bandecoWarning.py" # Dinner warning


# --------------- User definitions

importantFoods = ('estrogonofe (?!vegetariano)[\s\S]+', 'carne assada', 'carne assada[\s\S]+farofa', 'cocada','doce de leite','uva','SUCO: Roxo') # Use regular expressions language

link = "http://catedral.prefeitura.unicamp.br/cardapio.php"
#link = "http://www.pfl.unicamp.br/Restaurante/PF/view/site/cardapio.php"

timeLunchFinish = 14

# --------------- Libraries

import urllib # To read internet page
import re # Regular expression
import os # To access OS commands
import platform # To check the system platform
import datetime # To get system date-time and calculation with than
from datetime import datetime

# --------------- Especific funcitions, definitions 7 etc...

def ballonMessage(title,message):
	#os.path.dirname(os.path.abspath(__file__))
	#os.getcwd()
	if platform.system()=='Linux':
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u critical -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMP.png"') # Linux-Ubuntu ballon notification
	elif platform.system()=='Windows':
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u critical -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMP.png"') # Linux-Ubuntu ballon notification
	elif platform.system()=='Darwin':
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u critical -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMP.png"') # Linux-Ubuntu ballon notification
	else: # Not tested
		os.system('notify-send "'+title+'" "'+message+'" -t 8 -u critical -i "'+os.path.dirname(os.path.abspath(__file__))+'/logoUNICAMP.png"') # Linux-Ubuntu ballon notification

juiceRealName={'uva':'Roxo','abacaxi':'Plutônio','limão':'Branco','caju':'Branco 2','tangerina':'Laranja','laranja':'Amarelo 1','maracujá':'Amarelo 2','manga':'Amarelo 3'}


# --------------- Main program

f = urllib.urlopen(link)
page = f.read()
f.close()
del f,link

# Separate the diferents menus of the day
menuSearchString = '<td align="left" valign="top">[\t\n\s]*<table width="[\d%]+" class="fundo_cardapio">([\s\S\d\t\n]+?)<\/table>[\t\n\s]*<\/td>'
menus = re.findall(menuSearchString,page,re.IGNORECASE)
del page,menuSearchString

# Parse and format the strings
for count in range(len(menus)):
	menus[count] = re.sub('\t*\n*\r*(<td>)*(<\/td>)*(<tr>)*(<\/tr>)*(<strong>)*(<\/strong>)*(<br>)*','',menus[count]) # Remove HTML tags
	menus[count] = menus[count].decode('windows-1252').lower().encode('utf-8') # Change the codec used in the string coding, it was used Windows codec
	#menus[count] = menus[count].lower()
	menus[count] = re.sub(' *prato principal:',', ',menus[count],re.IGNORECASE)
	menus[count] = re.sub(' *pts',', pts',menus[count],re.IGNORECASE)
	menus[count] = re.sub(' *salada:',' - ',menus[count],re.IGNORECASE)
	menus[count] = re.sub(' *sobremesa:','\r\nSOBREMESA: ',menus[count],re.IGNORECASE)
	menus[count] = re.sub(' *suco:','\r\nSUCO: ',menus[count],re.IGNORECASE)
	menus[count] = re.sub(' *observações:','\r\n',menus[count],re.IGNORECASE)
	#menus[count] = re.sub('\s*\r\n\s*','\r\n',menus[count])
	menus[count] = re.sub(' +',' ',menus[count]) # Remove doblo spaces
	menus[count] = re.sub('^ +','',menus[count]) # Remove initial spaces
	juice = re.findall('\r\nSUCO: (\S+)\r\n',menus[count])
	if juice[0] in juiceRealName:
		menus[count] = re.sub('\r\nSUCO: (\S+)\r\n', '\r\nSUCO: '+juiceRealName[juice[0]]+'\r\n' ,menus[count]) # Real name of the juice

# Filter the lunch and dinner menu, Campinas and Limeira campus (change the format of the page, Limeira don't have vegeratarian option)
titulo=''
message='' 
if len(menus)==4: # Campinas campus' menu
	#message = 'ALMOÇO:\r\n' +  menus[0] + 'ALMOÇO VEGETARIANO:\r\n' + menus[1] + '\r\n\r\nJANTAR:\r\n' + menus[2] + '\r\n' + 'JANTAR VEGETARIANO:\r\n' + menus[3]
	if datetime.now().hour < timeLunchFinish:
		message = menus[0] + '\r\nVEGETARIANO: ' #+ re.findall('([\S\s]+)\r\nSUCO: ',menus[1],re.IGNORECASE)[0]
		message = re.sub('\r\nSUCO: ', ' - SUCO: ', message)
		titulo = 'Almoço UNICAMP:'
	else:
		message = menus[2] + '\r\nVEGETARIANO: ' + re.findall('([\S\s]+)\r\nSUCO: ',menus[3],re.IGNORECASE)[0]
		titulo = 'Jantar UNICAMP:'
elif len(menus)==2: # Limeira campus' menu
	#message = 'ALMOÇO:\r\n' +  menus[0] + '\r\n\r\nJANTAR:\r\n' + menus[1]
	if datetime.now().hour < timeLunchFinish:
		message = menus[0]
		titulo = 'Almoço UNICAMP:'
	else:
		message = menus[1]
		titulo = 'Almoço UNICAMP:'
else:
	message = 'Error!!!'
	titulo = 'Cardápio:'
del menus

# Remove unuserfull messages
message = re.sub('traga sua caneca!','',message,re.IGNORECASE)
message = re.sub('o cardápio contém glútem no pão e na barra de cereal.','',message,re.IGNORECASE)
message = re.sub('o cardápio contém glútem no pão e na salsicha.','',message,re.IGNORECASE)
message = re.sub('o cardápio contém glútem no pão.','',message,re.IGNORECASE)

# Look for important foods in the day menu
for importantFood in importantFoods:
	if re.search(importantFood,message,re.IGNORECASE):
		titulo = '\\o/ ' + titulo + '\\o/'

ballonMessage(titulo,message) # Put message on the screen
