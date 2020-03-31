#script to waste a phisher's time
#inspired by https://www.youtube.com/watch?v=UtNYzv8gLbs
#this is FOSS - Free and Open Source Software
#use it responsibly okay

import requests
import string
import random
import signal
import sys
from string import digits
import time

total = 0 #ew a global variable

def signal_handler(sig, frame):
  #elegantly handle ctrl-c
  #adapted from https://stackoverflow.com/a/1112350
  
  print('\ntotal sent: ' + str(total))
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

url = 'https://webpage87678.000webhostapp.com/' #where the request goes

uname = '' #will hold fake username
pword = '' #will hold fake password
email = '' #will hold fake email - in practice, just the username plus some "@"


fnames = open('fnames.txt', 'r').read().split() #first names
lnames = open('lnames.txt', 'r').read().split() #last names
email_addrs = open('addrs.txt', 'r').read().split() # common email hosting sites


while(1==1):

  #randomly generate usernames, passwords, and emails
  #one-liners adapted from https://stackoverflow.com/a/2257449

  #get a first name, last name, and random number for the username
  uname = random.choice(fnames) + "." + random.choice(lnames) + str(random.randint(1,9))
  
  #make some numbers and letters here
  pword = ''.join((random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(7,12))))

  #use some common emails
  email = uname + '@' + random.choice(email_addrs)

  if(random.randint(0,1) == 0):
    #every once in a while, make a username that's not thesameas the email
    uname = uname.replace('.','') #take out period
    uname = uname.translate(None, digits) #take out number
    uname = uname + ''.join(str(random.randint(0, 9)) for _ in range(random.randint(1,5))) #add some random numbers to the end


  #the data to update
  #this will vary from site to site
  #currently set to target https://webpage87678.000webhostapp.com/
  dataForm = {
    'wb_form_id': '95a5b61e',
    'message': '', 
    'wb_input_0': 'E-mail Address:',
    'wb_input_0': email,
    'wb_input_1': 'Username:',
    'wb_input_1': uname,
    'wb_input_2': 'Password',
    'wb_input_2': pword
  }

  print('email: ' + email + '\nuname: ' + uname + '\npword: ' + pword)


  try:
    r = requests.post(url, allow_redirects=False, data=dataForm)
    if(r.status_code == 302):
      #yay it went through
      total = total + 1
      print('POST ' + str(total) + ": " + str(r.status_code) + ' success')
    else:
      print(str(r.status_code) + 'failure')
    print('')
  except:
    print('\nconnection failed - retrying...\n')
    time.sleep(1) #wait a second

