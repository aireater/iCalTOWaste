#/usr/bin/env python

import csv, time, datetime

#title           :iCalTOWaste.py
#description     :Create ical and gmail calendar files for city of toronto curbside garbage collection
#author          :eric partington
#date            :2016/07/27
#version         :0.1
#usage           :python iCalTOWaste.py
#notes           :
#python_version  :
#==============================================================================

#global variables
CALENDAR_INPUT_NAME = 'Calendars.csv'
#dict for unqiue pickup days
PICKUP_DAYS = []

#output CSV File blanks with headers for the collection days of the week
#creates a blank file for each collection day in the master file (column 0)
def MakeFiles():
	print "## Creating template files for each pickup date in input file ##"
	global PICKUP_DAYS
	#open the file
	input_file = open(CALENDAR_INPUT_NAME, 'rU')
	data = csv.reader(input_file,delimiter=',')

	#create the template header for the new calendar csv files
	subject = ["Subject"]
	startDate = ["Start Date"]
	allDay = ["All Day Event"]
	description = ["Description"]
	new_line = subject + startDate + allDay + description

    #grab only the unique pickup days from the first column
	for line in data:
		#print line[0]
		if line[0] not in PICKUP_DAYS:
			PICKUP_DAYS.append(line[0])

	#iterate over the unique days to create the template files
	for day in PICKUP_DAYS:
		if day == 'Calendar':
			#skip this item as its just the header line
			print "skipping header"
		else:
			#write the template files by pickup day
			print 'Writing template file for '+day
			csv.writer(open((day +'.csv'), 'w')).writerow(new_line)
			#print day

#Write Solid Waste Calendars to file to csv
def WriteCal():
	print "## Writing calendar files for each pickup date in input file ##"
	#read the Calendars.csv file as input
	input_file = open(CALENDAR_INPUT_NAME, 'rU')
	data = csv.reader(input_file)

	for line in data:
		#split the input file into elements
		[Calendar,WeekStarting,GreenBin,Garbage,Recycling,Yardwaste,ChristmasTree] = line

		if Calendar == "Calendar":
			print "skipping"
			#skip first line as that is header
			data.next()
		else:
			#date formate was changed in the files from 2012
			#2012 format
			#MondayNight,9/2/2012,M,0,M,0,0
			#2016 format
			#MondayNight,01-04-16,M,0,M,0,0

			#day = datetime.datetime.strptime(WeekStarting, '%m/%d/%Y')
			#%m - zero padded month
			#%d - zero padded day
			#%y - year without the century
			day = datetime.datetime.strptime(WeekStarting, '%m-%d-%y')
			#calendars are provided starting with a weekStarting datetime
			#there is the letter in the dict below that maps the pickup day on the week of service
			#so for instance if the pickup date was thursday, tht would be marked with an R
			#so to get the actual pickup date of the week you would need to add the weekstarting and the day of the week to get the date

			dw = {"M": 7, "T":8, "W":9, "R":10, "F":11, "S":12}
			#mark the calendar appointment as allDay
			#may try to change this to 7am as that is when the city wants curbside garbage out by.
			allDay = ["True"]
			if ChristmasTree != "0":
			    subject = ["Christmas Tree/Garbage Day"]
			    description = ["Garbage and Green Bin waste, Christmas tree collection occurs Today. When placing your tree out for collection, please remove all decorations, tinsel, etc and do not place out in any type of bag"]
			    startDate = day + datetime.timedelta(dw[ChristmasTree] - day.weekday())
			    startDate = [datetime.datetime.strftime(startDate, "%m-%d-%y")]
			elif Recycling != "0":
			    subject = ["Recycling Day"]
			    description = ["Recycling and Green Bin - More information on what can be recycled click here: http://www.toronto.ca/garbage/bluebin.htm"]
			    startDate = day + datetime.timedelta(dw[Recycling] - day.weekday())
			    startDate = [datetime.datetime.strftime(startDate, "%m-%d-%y")]
			elif Garbage != "0" and ChristmasTree == "0":
			    subject = ["Garbage Day"]
			    description = ["Garbage, Yard and Green Bin - Basic sorting information here: http://app.toronto.ca/wes/winfo/search.do"]
			    startDate = day + datetime.timedelta(dw[Garbage] - day.weekday())
			    startDate = [datetime.datetime.strftime(startDate, "%m-%d-%y")]

			new_line = subject + startDate + allDay + description
			#append the contents to the file template created above
			csv.writer(open((Calendar +'.csv'), 'a')).writerow(new_line)
			#print Calendar
			#print new_line
	print "## Finished writing CSV calendars ##"
#writes the ics version of the calendar files for use with ical
def WriteIcs():
	#TODO
	#read input file
	#check for output directories
	#write the output file per collection

	# from this link
	#http://www.andyvenet.com/experience-generating-icalendar-files/
	with open("meeting.ics", 'wb') as f:
		f.write('BEGIN:VCALENDAR\n')
		f.write('VERSION:2.0\n')
		f.write('PRODID:-//WA//FRWEB//EN\n')
		f.write('BEGIN:VCALENDAR\n')
		f.write('BEGIN:VEVENT\n')
		summary = 'Python meeting about calendaring'
		f.write('SUMMARY:%s\n' % summary)
		begin_date = datetime.now().strftime("%Y%m%dT%H%M%S")
		uid = '20050115T101010/27346262376@mxm.dk'
		f.write('DTSTART:%s\n' % begin_date)
		f.write('UID:%s\n' % uid)
		location = 'The other side of the moon'
		organizer = 'someone@somewhere.com'
		f.write('LOCATION:%s\n' % location)
		f.write('ORGANIZER:MAILTO:%s\n' % organizer)
		f.write('END:VEVENT\n')
		f.write('END:VCALENDAR')

#main functions
MakeFiles()
WriteCal()
#WriteIcs()
