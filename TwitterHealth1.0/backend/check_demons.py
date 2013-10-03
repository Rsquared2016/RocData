"""
Checks demon status db and emails alerts
"""

import couchdb
import datetime
import smtplib
import string
import sys
import time
from dateutil import parser

def log(s):
    print '%s: %s' % (datetime.datetime.today(), s)

def updateTimes(db):
    demons = db.view('_all_docs')
    #print 'Found %d demon entries' % len(demons)
    for row in demons:
        demon = db[row.id]
        last_update = parser.parse(demon['last_update'])
        now = datetime.datetime.utcnow()
        timeDelta = (now - last_update).seconds
        #print demon['_id'], last_update, now, timeDelta
        if timeDelta > 4000:
            emailAlert('Demon %s is probably down :-(' % (demon['_id']))

def emailAlert(alert):
    SUBJECT = alert
    TO = "sadileka@gmail.com"
    FROM = "demon@166.78.236.179"
    text = "To stop receiving these emails, either fix the demon, or delte its entry in http://166.78.236.179:5984/_utils/database.html?demon_status/_all_docs"
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
        ), "\r\n")
    server = smtplib.SMTP('localhost')
    server.sendmail(FROM, [TO], BODY)
    server.quit()

        
if __name__ == '__main__':
    couch = couchdb.Server('http://166.78.236.179:5984/')
    couch.resource.credentials = ('admin', 'admin')
    db = couch['demon_status']

    while True:
        try:
            updateTimes(db)
        except:
            emailAlert('Databse is probably down :-(')
            exit(1)
        time.sleep(300)
