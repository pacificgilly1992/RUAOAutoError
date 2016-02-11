from twilio.rest import TwilioRestClient 
 
def senderrornot(message="Somethings gone wrong at RUAO"):
 
	ACCOUNT_SID = "ACa9285c43e0f2d8dd9714f396de44246e" 
	AUTH_TOKEN = "f931735f2a0aa775f73eba751f27270e" 

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

	client.messages.create(
		to="+447921012566", 
		from_="+441892805038", 
		body=message,  
	)
	
