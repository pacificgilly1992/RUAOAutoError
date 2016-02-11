import smtplib
#import emailsms

def EmailError(email_username=None, email_password=None, message="Error"):
	smtpObj = smtplib.SMTP_SSL('smtp.reading.ac.uk', 465)
	smtpObj.ehlo()
	
	smtpObj.login(email_username, email_password)
	smtpObj.sendmail(from_addr='james.gilmore@pgr.reading.ac.uk', to_addrs='james.gilmore@pgr.reading.ac.uk', msg=message)
	smtpObj.quit()
	
def EmailAuthentication(email_username=None, email_password=None):
	try:
		smtpObj = smtplib.SMTP_SSL('smtp.reading.ac.uk', 465)
		auth = smtpObj.login(email_username, email_password)
	except:
		auth = "(535, 'Incorrect')"
	
	return auth