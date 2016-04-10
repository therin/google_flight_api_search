import urllib2
import json
import itertools
import smtplib


# Set some variables

apikey = "Insert your API key"

listofstartdates = ["2016-06-20","2016-06-21","2016-06-22","2016-06-23","2016-06-24","2016-06-25","2016-06-26","2016-06-27","2016-06-28","2016-06-29","2016-06-30",
"2016-07-01","2016-07-02","2016-07-03","2016-07-04","2016-07-05","2016-07-06","2016-07-07","2016-07-08","2016-07-09","2016-07-10","2016-07-11","2016-07-12"]

listofenddates = ["2016-07-20","2016-07-21","2016-07-22","2016-07-23","2016-07-24","2016-07-25","2016-07-26","2016-07-27","2016-07-28","2016-07-29","2016-07-30",
"2016-07-31","2016-08-01","2016-08-02","2016-08-03","2016-08-04","2016-08-05","2016-08-06","2016-08-07","2016-08-08","2016-08-09","2016-08-10","2016-08-11"]

minprice = "NZD3700"
flightsfound = []

def checkprice(startdate,enddate,minprice):

	url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=%s" % apikey

	request = {
	"request": {
	"slice": [
	{
	"origin": "AKL",
	"destination": "MOW",
	"date": startdate
	},
	{
	"origin": "MOW",
	"destination": "AKL",
	"date": enddate
	}
	],
	"passengers": {
	"adultCount": 2,
	"infantInLapCount": 0,
	"infantInSeatCount": 0,
	"childCount": 0,
	"seniorCount": 0
	},
	"solutions": 500,
	"maxPrice": minprice,
	"refundable": False
	}
	}

	jsonreq = json.dumps(request, encoding = 'utf-8')

	try:
		req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
		flight = urllib2.urlopen(req)
		response = flight.read()
		result = json.loads(response)
		flight.close()

		try :
			for i in result['trips']['tripOption']:
				#return "Found " + i['saleTotal'] +  "  (from " + startdate + " to " + enddate + ")\n"
				return (i['saleTotal'], "(from " + startdate + " to " + enddate + ")")
		except:
			return ""
			#return "Nothing found for that price (from " + startdate + " to " + enddate + ")"
	except urllib2.HTTPError, err:
		if err.code == 403:
			print "API requsts limit exceeded!"

# Main loop:

for dates in itertools.product(listofstartdates, listofenddates): flightsfound.append(checkprice(dates[0],dates[1],minprice))

# Optional email report with 3 best results:

message = """From: From Flight Bot <sergey@server.com>
To: To Person <sergey@server.com>
Subject: Daily flight search results

{flightsfound}

""".format(flightsfound=''.join(["Price: %s %s \n" % (x[0],x[1]) for x in sorted(flightsfound, key=lambda tup: tup[0])[0:3]]))

smtpObj = smtplib.SMTP('mail.server.com')
smtpObj.sendmail("sergey@server.com", ["sergey@server.com"], message)         
