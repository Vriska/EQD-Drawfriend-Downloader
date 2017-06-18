from bs4 import BeautifulSoup
import requests
import os
import re
from math import floor
import  time

def Threads(FromYear,FromMonth) : ## makes a list of all drawfriend URL in the link 
    if FromMonth >=  12 :                 #We will be downloading threads month by month thus this is necessary  
        FromYear += floor(FromMonth/12)
        FromMonth = FromMonth % 12 + 1       #Jan is 1 not 0 
    link = r"https://www.equestriadaily.com/search/label/Drawfriend?updated-max="+str(FromYear)+"-"+str(FromMonth)+"-19T17:00:00-07:00&max-results=32&start=20&by-date=false"
    r = requests.get(link)
    soup = BeautifulSoup(str(r.text),"html.parser")
    L = soup.find_all("a",string=re.compile('Drawfriend Stuff'))
    L = [x.get('href') for x in L]
    return L[1:]            #Removes first element which is random trash

def ListGet(x):     # Makes a list of all source (Deviant art) URL for a given draw thread
    try :
        r = requests.get(str(x))
        soup = BeautifulSoup(str(r.text),"html.parser")
        PonyList = soup.find_all("a",string =re.compile('Source'))
        PonyList= [x.get('href') for x in PonyList]
        return PonyList
    except :
        print ('List Derp')

Directory = input("Enter directory , default(hit enter) is ponypics folder in desktop : ")

def GetImage(x) :      # downloads and saves picture from source URL 
    try:
        r = requests.get(str(x))
        soup = BeautifulSoup(r.text,"html.parser")
        title = soup.find("a",class_="title").string
        try :
            author = soup.find("a",class_="u beta username").string       #deviantart stuff
        except :
            author = soup.find("a",class_="u regular username").string
        k = soup.find(class_=("dev-view-deviation"))
        soup = BeautifulSoup(str(k),"html.parser")
        L = soup.find_all("img")
        URL = L[1].get("src")
        r = requests.get(URL)
        global Directory
        Directory = Directory.replace("\\", "\\\\")
        if not Directory:
            if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Desktop\\\ponypics\\')):
                os.makedirs(os.path.join(os.path.expanduser('~'), 'Desktop\\\ponypics\\'))
            FileName = os.path.join(os.path.expanduser('~'), 'Desktop\\\ponypics\\') + title + " by " + author +".png"
        else :
            if not os.path.exists(Directory):
                os.makedirs(Directory)
            FileName = Directory + "\\"  + title + " by " + author +".png"
        try :
            file = open(FileName, 'wb')
        except :
            print ("derpdoo")
        file.write(r.content)
        print (FileName)
    except :
        print ('Whoops')

##UI stuff

Month = int(input('Starting Month : '))  
Year = int(input('Starting year : '))
Num = int(input ('Number of Months forward : '))
Num = Month + Num

StartThread = (input('Thread number to start from ? Defaults to first : '))
if not StartThread:
    StartThread = int(1)
else :
    StartThread = int(StartThread)
StartPic = (input('Pic to start from? Defaults to first : '))
if not StartPic :
    StartPic = int(1)
else :
    StartPic = int(StartPic)

ThreadCounter = 0
for i in range(Month,Num+1):
    for thread in Threads(Year,i)[StartThread-1:]: 
        for pic in ListGet(thread)[StartPic-1:]:
            GetImage(pic)
            print("month = " + str(i)+"   "+str(Threads(Year,i).index(thread)+1)+" of 32    " + str(ListGet(thread).index(pic)+1)+ " out of " + str(len(ListGet(thread))))
            StartPic = 1
            StartThread = 1
            time.sleep(.3)

