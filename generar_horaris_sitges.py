# -*- coding: utf-8 -*-
import urllib.request
from icalendar import Calendar, Event
import json
from pytz import timezone
from datetime import datetime

link = "https://sitgesfilmfestival.com/es/service/films/2022"
f = urllib.request.urlopen(link)
dades = json.load(f)
f.close()
	
cal = {}
lt = timezone('Europe/Paris')

sessions=dades['sessions']
locations={}
for location in dades['locations']:
  locations[location['id']]=location['name']['ca']

for sessio in sessions:
  inici=datetime.strptime(sessio['start_date'],"%Y-%m-%dT%H:%M:%S")
  fi=datetime.strptime(sessio['end_date'],"%Y-%m-%dT%H:%M:%S")
  peli=sessio['name']['ca']
  lloc=locations[sessio['locations'][0]]

  print ("Processant "+peli)

  event = Event()        
  event.add('summary', peli)
  event.add('dtstart', inici.replace(tzinfo=lt))
  event.add('dtend', fi.replace(tzinfo=lt))
  event.add('location', lloc)

  if lloc not in cal.keys():
    cal[lloc]=Calendar()
  cal[lloc].add_component(event)

for lloc in cal.keys(): 
  print ("Escrivint calendari per "+lloc)
  f = open(lloc+'.ics', 'wb')
  f.write(cal[lloc].to_ical())
  f.close()
