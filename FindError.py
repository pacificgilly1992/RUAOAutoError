from __future__ import absolute_import, division, print_function
from array import array
import numpy as np
import glob
import getpass
import sys, os, time
import datetime
from time import sleep as wait
execfile("EmailError.py")
execfile("SMSError.py")

i=0
eventno=0

iCP_value = np.zeros(4)
iFP_value = np.zeros(4)

tstart = datetime.datetime.now()
authentication = "no"
datafile=glob.glob('../../../../net/vina1s/vol/data1_s/meteorology_2/METFiDAS-Incoming/Level0/2016/*.csv')

while authentication == "no":
	email_username = raw_input("Please enter your username for your account: ")
	email_password = getpass.getpass()

	auth = str(EmailAuthentication(email_username,email_password))

	if auth != "(235, 'Authentication succeeded')":
		print("Authentication Failed. Please Try Again!")
	else: 
		authentication = "yes"
		print("Authentication Succeeded. Now loading error checking module! Please stand by...")
		wait(10)

var = 1
#Aquires the initial amount of data to perform any error checks (Takes 40 minutes to initalise as it takes 10 minutes per refresh of the MetFidas data)
for i in xrange(3):
	ts = time.time()
	os.system('cls' if os.name=='nt' else 'clear')
	print("RUAO Error Detection Module")
	print("#################################################")
	print("Detecting errors since:", tstart)
	print("Number of events processed: ", eventno)
	print("Everything's running okay :)")
	inst_time, iCP, iFP = np.genfromtxt(datafile[-2], dtype=float, delimiter=',', usecols=(0,46,47),  unpack=True, skiprows=4)
	eventno+=1
	iCP_value[i] = iCP[-1]
	iFP_value[i] = iFP[-1]
	ts2 = time.time()
	wait(600-(ts2-ts))

#Set the various tests as valid
iCP_test = 1
iFP_test = 1	
	
while var == 1:
	ts = time.time()
	inst_time, iCP, iFP = np.genfromtxt(datafile[-2], dtype=float, delimiter=',', usecols=(0, 46,47),  unpack=True, skiprows=4)
	
	eventno+=1
	
	os.system('cls' if os.name=='nt' else 'clear')
	print("RUAO Error Detection Module")
	print("#################################################")
	print("Detecting errors since:", tstart)
	print("Number of events processed: ", eventno)
	if iCP_test == 1 and iFP_test == 1:
		print("Everything's running okay :)")
	else:
		print("Error(s) have been detected at RUAO :(")
	
	#Each if statement now determines any errors based off the aquired data
	if (np.abs(np.std(iCP_value)) < 0.01 and iCP_test == 1):
		email_message = 'Subject: RUAO Instrument Error.\nDear James,\n\nAn error has been found with the iCP GEDACS, please confirm with the visual data. \n\nSincerely, RUAO'
		sms_message = '\n\nDear James,\n\nWe have detected an error with the iCP instrument. Please verify the issue manually and correct the issue.\n\nThanks\n\nRUAO'
		EmailError(email_username, email_password, email_message)
		senderrornot(sms_message)
		print("The iCP instrument has a problem with it!")
		iCP_test = 0
		
	if (np.abs(np.std(iFP_value)) < 0.01 and iFP_test == 1):
		email_message = 'Subject: RUAO Instrument Error.\nDear James,\n\nAn error has been found with the iFP GEDACS, please confirm with the visual data. \n\nSincerely, RUAO'
		sms_message = '\n\nDear James,\n\nWe have detected an error with the iFP instrument. Please verify the issue manually and correct the issue.\n\nThanks\n\nRUAO'
		EmailError(email_username, email_password, email_message)
		senderrornot(sms_message)
		print("The iFP instrument has a problem with it!")
		iFP_test = 0
		
	#We reach this statement iff there were no problems detected.
	if iCP_test == 1:
		for j in xrange(3):
			iCP_value[j] = iCP_value[j+1]
		iCP_value[3] = iCP[-1]
	if iFP_test == 1:
		for j in xrange(3):
			iFP_value[j] = iFP_value[j+1]
		iFP_value[3] = iFP[-1]	
	ts2 = time.time()
	wait(600-(ts2-ts))
