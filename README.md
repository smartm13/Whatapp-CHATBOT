# Whatapp-CHATBOT
It is a self-expanding chatbot utilizing yowsup library for whatsapp.
Requirements:
Python environment [linux prefered]


Setup steps:

[sudo] pip install yowsup2

Register your phone number on whatsapp and obtain ur password:

yowsup-cli registration --requestcode sms --phone 91XXXXXXXXXX --cc 91 --mcc 123 --mnc 456

yowsup-cli registration --register 123456 --phone 91XXXXXXXXXX --cc 91  

For indian numbers refer:http://mcc-mnc-india.blogspot.in/

Now enter that phoneno. and password in /run.py:29

Finally execute: python run.py

this is constant listener to whatsapp personal msgs to that number, and will reply only if it matches some command.



For adding features to bot: simply add new python files in same directory as modules.

For example:

  for new feature of imdb, add imdb.py
  
  it must have init and app methods for proper functioning.
  
  app states will be saved by event-manager (events.py) in file db: states-DB.txt and current_apps.txt
  
  which will be made avail to ur new module on event triggers.
  
  it will be triggered when user msgs starts with "imdb"
  
