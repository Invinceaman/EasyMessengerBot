import pickle
from fbchat import *
from fbchat import TypingStatus
from fbchat.models import *
import asyncio
import re
import random
import urllib.request
from bs4 import BeautifulSoup
import json
import requests
import getpass
from pathlib import Path
import sys
import importlib
from random import randrange
import time
import threading
import utils


def serialize_message(message_object):

	r = {
		'text':message_object.text,
		'reply_to_id':message_object.reply_to_id,
		'forwarded':message_object.forwarded,
		'attachments':message_object.attachments,
		'quick_replies':message_object.quick_replies,
	}

	if(message_object.replied_to == None):
		r['replied_to'] = None
		return r
	else:
		r['replied_to'] = serialize_message(message_object.replied_to)
		return r



class ChatBot(Client):
	#def on_message(self, author_id, message_object, thread_id, thread_type, **kwargs):
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		if(thread_id in self.valid_groups):
			self.markAsDelivered(thread_id, message_object.uid)
			utils.rand_delay(1, 1.5)
			self.markAsRead(thread_id)

			print(serialize_message(message_object))

			if message_object.text != None and author_id != self.uid and message_object.text[0] == "!":
				utils.rand_delay(1, 1.5)
				self.setTypingStatus(status=TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)

				split_message = message_object.text.split(' ')
				if(split_message[0].lower() in self.functions):
					func = self.functions[split_message[0].lower()]
					formatted_text = func(message_object, data=self.data, client_object=self)
					if(split_message[0] in self.data and len(split_message) > 1 and split_message[1].lower() == "!help"):
						utils.rand_delay(.5, 1)
						self.send(Message(text=self.data[split_message[0]]['help']), thread_id=thread_id, thread_type=thread_type)
					elif(formatted_text != None):
						utils.rand_delay(.5, 1)
						self.send(Message(text=formatted_text), thread_id=thread_id, thread_type=thread_type)
				else:
					utils.rand_delay(.5, 1)
					self.send(Message(text="'"+split_message[0]+"' is not a valid command."), thread_id=thread_id, thread_type=thread_type)
				self.setTypingStatus(status=TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)


	# Loads params into varialbes stored in the Client object to be called later.
	def load_params(self):
		self.functions = {}
		self.valid_groups = set([])

		with open('config.json') as f:
			self.data = json.load(f)
		for key, value in self.data['commands'].items():
			my_module = importlib.import_module('modules.'+value['file_path']+'.'+value['file_path'])
			self.functions[key] = my_module.module

		for group in self.data['valid_groups']:
			self.valid_groups.add(int(group))
			self.valid_groups.add(str(group))

		print(self.valid_groups)
		print(self.functions)

		self.start_time = time.time()

if __name__ == '__main__':
	creds = utils.get_login_credentials('auth_details.py')
	cookie_path = 'session.json'
	client = None
	cookies_exist = False
	if(creds == None):
		print("cannot find file containing login credentials.")
	else:
		print("login credentials are available")
		cookies = {}
		cookies = utils.load_json(cookie_path)
		username = creds['username']
		password = creds['password']
		user_agent = creds['user_agent']
		if(cookies == None): # no cookies
			print("cookies unavailable")
			cookies_exist = False
			client = ChatBot(username, password, user_agent=user_agent)
			if(utils.save_json(cookie_path, client.getSession())):
				print("Cookies did not exist before, created new cookie file")
			else:
				print("Failed to create cookie file for some reason")
		else:
			print("cookies available")
			cookies_exist = True
			client = ChatBot(username, password, user_agent=user_agent, session_cookies=cookies)
	
	client.load_params()
	try: 
		client.listen() # run the ting in an infinite loop
	except:
		print("PROGRAM EXIT")