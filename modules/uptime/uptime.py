import time
import random
import sys

def get_day(seconds):
	day_count, remainder_sec = divmod(seconds, 86400)
	return day_count, remainder_sec, seconds

def module(message_object, **kwargs):
	split_message = message_object.text.split(' ')
	if(split_message[0] == '!uptime'):
		formatted_text = "Could not obtain uptime"
		try:
			if('client_object' in kwargs):
				uptime_days, uptime_seconds, raw_seconds = get_day(time.time()-kwargs['client_object'].start_time)
				formatted_text = 'Current: ' + str(int(uptime_days))+'d:'+time.strftime('%Hh:%Mm:%Ss', time.gmtime(uptime_seconds))
		except:
			print(sys.exc_info()[0])
			formatted_text = "An error has occured with acquiring the time. Check terminal for error log."
		return formatted_text
	else:
		return None