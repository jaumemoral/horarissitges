# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from pytz import timezone
from datetime import datetime, timedelta

link = "https://sitgesfilmfestival.com/cat/programa"
f = urllib.urlopen(link)
html_doc=f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
f.close()
	
cal = {}
cal['Prado']=Calendar()
cal['Retiro']=Calendar()
cal['Auditori']=Calendar()
cal['Tramuntana']=Calendar()
cal['Brigadoon']=Calendar()
lt = timezone('Europe/Paris')

taula=soup.find("table")
files=taula.find_all("tr")
for fila in files:
  tds=fila.find_all("td")
  if len(tds)>=4:
    hora=tds[1].text.strip().replace("\n\n"," ")
    inici=datetime.strptime(hora,"%d-%m-%Y %H:%M")
    peli=tds[2].text.strip().replace("\n","/")
    lloc=tds[3].text.strip().split()[0]
    durada=tds[5].text.strip().replace("\'","")
    if len(durada)==0: durada=120
    fi=inici+timedelta(minutes=int(durada))

    event = Event()        
    event.add('summary', peli)
    event.add('dtstart', inici.replace(tzinfo=lt))
    event.add('dtend', fi.replace(tzinfo=lt))
    event.add('location', lloc)

    cal[lloc].add_component(event)

for lloc in cal.keys(): 
  f = open(lloc+'.ics', 'wb')
  f.write(cal[lloc].to_ical())
  f.close()
