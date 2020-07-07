# Simple helper function to just list available modules
def module(message_object, **kwargs):
	if(message_object.text.split(' ')[0].strip() == '!listcommands'):
		formatted_string = ""
		if('data' in kwargs):
			for key,value in kwargs['data']['commands'].items():
				formatted_string+=key+"\n"
		return formatted_string
	else:
		return None