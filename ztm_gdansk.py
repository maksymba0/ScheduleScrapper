import json
import requests
from bs4 import BeautifulSoup
import os
import datetime
import re
 


def getSessionID(response_txt):
    
    result = re.search(r"sn=([a-f0-9]+)",response_txt)
    if not result:
        print("not found sn value")
        return None
    return result.group(1)

def getBusData():

    url = "https://files.cloudgdansk.pl/d/otwarte-dane/ztm/stops-with-routes.json?v=1"
    file = None
    try:
        with open("bus_stops.txt", "r" , encoding="utf-8") as file:
            if file.read(1):
                file.seek(0)
                file_data = json.load(file)

                bus_data = []
                for obj in file_data:
                    if "BUS" == obj.get("type"):
                        bus_data.append(obj)
                return file_data
            else:
                print("Trying to load from web... [ Bus-Stops]")
    except (FileNotFoundError):
        print("not found bus_stops.txt - creating") 
   
    response = requests.get(url)
    if response.status_code == 200:
        with open("bus_stops.txt","w") as file_:
            file_.write(response.text)
            print("Successfully saved data")
            return json.load(file_.read())
    else:
        print(f"Failed to get bus stops data. Code {response.status_code}")
    
    
    return None


def getRealTimeTableForStop(stopID):
    if stopID == None:
        print("Invalid BusStop ID: " + stopID)
        return
    
    text = stopID.strip()

    # Is this text?
    if not stopID.isdigit():
        stopID = getStopIDByName(text)

    if stopID <= 0:
        print("Invalid BusStop ID.")
        return
     
 
     
    sn = None
    try:
        with open("output.txt","r",encoding="utf-8") as file:
            sn = getSessionID(file.read())
    except (FileNotFoundError, FileExistsError):
        GetAllData()
        with open("output.txt","r",encoding="utf-8") as file_:
            sn = getSessionID(file_.read())
    if sn == None:
        return None
    
    url = f"https://ztm.gda.pl/rozklady/pobierz_SIP2.php?n[0]={stopID}&sn={sn}&t=&l="

    response = requests.get(url)
    if response.status_code == 200:
        print("RealTime data parsing. Success...")
    else:
        print(f"RealTime data parsing. Failure...{response.status_code}")
        return None
      
    html = BeautifulSoup(response.text, "html.parser")
    
    sip = html.find("ul",class_="sip3")

    list = []

    for child in sip.find_all(recursive=False):
        spans = child.find_all("span")
        
        busID = spans[0].text
        direction = spans[1].text
        etd = spans[3].text
 
        list.append({"busID":busID,"direction":direction,"etd":etd})
    return list

def printRealTimeTable(stopID):
    if stopID == None or stopID <= 0:
        print("Invalid BusStop ID.")
        return
    sn = None
    with open("output.txt","r",encoding="utf-8") as file:
        sn = getSessionID(file.read())
    
    if sn == None:
        return None
    
    url = f"https://ztm.gda.pl/rozklady/pobierz_SIP2.php?n[0]={stopID}&sn={sn}&t=&l="

    response = requests.get(url)
    if response.status_code == 200:
        print("RealTime data parsing. Success...")
    else:
        print(f"RealTime data parsing. Failure...{response.status_code}")
        return
      
    html = BeautifulSoup(response.text, "html.parser")
    
    sip = html.find("ul",class_="sip3")


    for child in sip.find_all(recursive=False):
        spans = child.find_all("span")
        
        busID = spans[0].text
        direction = spans[1].text
        etd = spans[3].text





    
def printSchedule(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")

    target_class = "departures-set"
    bus_ID = ""


    ID_div = soup.find("div",class_="route-number")
    if ID_div:
        print(f"Found the route {bus_ID}")
    else:
        print("Unable to find route")

    target_div = soup.find("div",class_=target_class) 

    if target_div:
        print("Found Schedule Timings.")  
        #For each schedule row
        
        text = ""
        schedules = []

        temporarySchedule = None

        bNewHour = False
        for child in target_div.find_all(recursive=False):
            class_ = child.get("class")
            className = class_[0] if class_ else None
            

            match className:
                case "h":
                    temporarySchedule = {
                        "hour":child.text,
                        "minutes":[]
                    }
                case "m":
                    temporarySchedule["minutes"].append(child.find("a").text.strip())
                case None:
                    schedules.append(temporarySchedule) 
                    temporarySchedule = None
                    bNewHour = True
        print(f"Schedules array contains {len(schedules)} objects")

        for obj in schedules:
            
            hour = obj["hour"]

            minutes_list = obj["minutes"]
            minutes_string = ", ".join(minutes_list)


             
         

    else:
        print("Not found schedule")

def printDate(htmlText):

    soup = BeautifulSoup(htmlText, "html.parser")

    target_class = "rozklad_na_dzien"
    target_div = soup.find("div",class_=target_class)

    if target_div:
        print("Found Date.") 
        strong = target_div.find("strong")
    else:
        print("Not found")


def getStopData(dataJSON, number):
    for object in dataJSON:
        stop_id = object["stopId"]
        if number == stop_id:
            print("Found")
            return object
    return None

def printStopData(stop_):
    stopid = stop_["stopId"]
    stopCode = stop_["stopCode"]
    stopName = stop_["stopName"]
    lines = ", ".join(stop_["lines"])

    text = f"{stopName} {stopCode} ({stopid}) - {lines}"

    #print (text)

def findAllBusStopsByLineNumber(text):
    stops_list = []
    bus_data = getBusData()
    for obj in bus_data: 
        if obj["type"] == "TRAM":
            continue
        lines = obj["lines"]
        for line in lines:
            if line == text:
                stops_list.append(obj)

    return stops_list

def findStopIdByLine(text):
    stops_list = []
    bus_data = getBusData()
    for obj in bus_data: 
        if obj["type"] == "TRAM":
            continue
        lines = obj["lines"]
        for line in lines:
            if line == text:
                stops_list.append(obj)
    if len(stops_list) == 0:
        print(f"Error not found any bus stops for Line ID: {text}")
        return None
    maxIndex = 0
    for index, stopObj in enumerate(stops_list, start=0):
        maxIndex = index
    digit = -1
    while True:
        selectedStop = input(f"Enter the index of the stop (0-{maxIndex})").strip()
        digit = int(selectedStop)
        if selectedStop.isdigit() and digit <= maxIndex and digit >= 0:
            break

    bus_info = stops_list[digit]
    return bus_info["stopId"]
 
from unidecode import unidecode
def findAllBusStopsByName(arg):
    text = arg.strip().lower()
    
    stops_list = []
    bus_data = getBusData()
    for obj in bus_data: 
        name = unidecode(obj["stopName"]).lower()
        if text in name:
            stops_list.append(obj)
    return stops_list

def getStopIDByName(arg):

    directionCode = arg[-2:] if arg[-2:].isdigit() else -1
    text = arg[:-2].strip().lower()
    stops_list = []
    bus_data = getBusData()
    for obj in bus_data: 
        name = unidecode(obj["stopName"]).lower()
        direction = obj["stopCode"]
        if directionCode is not -1:
            if text in name and directionCode == direction:
                stops_list.append(obj)
        else:
            if text in name:
                stops_list.append(obj)
    if len(stops_list) == 0:
        print(f"Not found any bus stop with name '{text}'")
        return -1
  
    bus_info = stops_list[0] 
    return bus_info["stopId"]

def findStopIdByName(arg):

    text = arg[:-2].strip().lower()
    directionCode = arg[-2:] if arg[-2:].isdigit() else -1 
    stops_list = []
    bus_data = getBusData()
    for obj in bus_data: 
        name = unidecode(obj["stopName"]).lower()
        direction = obj["stopCode"]
        if directionCode is not -1:
            if text in name and direction == directionCode:
                return obj["stopId"]
        else:
            if text in name:
                stops_list.append(obj)
    if len(stops_list) == 0:
        print(f"Not found any bus stop with name '{text}'")
        exit()
    maxIndex = 0
    for index, stopObj in enumerate(stops_list, start=0):
        maxIndex = index
    digit = -1
    while True:
        selectedStop = input(f"Enter the index of the stop (0-{maxIndex})").strip()
        digit = int(selectedStop)
        if selectedStop.isdigit() and digit <= maxIndex and digit >= 0:
            break

    if(int(selectedStop) > len(stops_list)):
        print("Invalid stop-list index")
        return
    bus_info = stops_list[digit]
    print(f"Searching for stop at index {digit} - Found {bus_info["stopId"]}")
    return bus_info["stopId"]

    
def GetBusDataByNumberOrText(raw_data):
    input_text =  raw_data.strip()
    isDigit = True if input_text.isdigit() else False
    data = None

    if isDigit:
        #provided bus-line number - find all stops related to this number
        data = findAllBusStopsByLineNumber(input_text)    
    else:
        #provided bus-stop name - find all stops related to this name
        data = findAllBusStopsByName(input_text)
     
    return data

def getBusID(): 
    input_text = input("Please enter the name of the bus stop OR bus-line number.")
    input_text =  input_text.strip()
    isDigit = True if input_text.isdigit() else False
    StopID = None
    if isDigit:
        #provided bus-line number - find all stops related to this number
        StopID = findStopIdByLine(input_text)
    else:
        #provided bus-stop name - find all stops related to this name
        StopID = findStopIdByName(input_text)

    return StopID

import keyboard
import time
from tkinter import messagebox

def getStoplistForLine(response, line):
     
    if response == "":
        print(f"Error obtaining stoplist data. Error code: {response.status_code}")
    else:
        print(f"Received data about stoplist. Code = {response.status_code}")

    stoplist = {"01":[],"02":[]}
     
    data = response
    result = data.find("table",role="presentation")
    
    tables = data.find_all("td", style="vertical-align: top;")
 
    tTable_a = tables[0]
    tTable_b = tables[1]
    #with open("text.txt","w", encoding="utf-8") as file:
       # file.write(tTable.prettify()) 

    td = tTable_a    #will contain 2 tds 
    trs = td.find_all("a")
      
    for tr in trs: 
        name = tr.text.strip() 
        stoplist["01"].append(name)


    td = tTable_b    #will contain 2 tds 
    trs = td.find_all("a")
      
    for tr in trs: 
        name = tr.text.strip() 
        stoplist["02"].append(name)
    return stoplist


def getLastUpdateDateForLine(data, line):
      
    result = data.find("div",class_="validity")
    print(result.find("b").text)
    return result.find("b").text[:-3]

     
from datetime import datetime  
def GetBusstopScheduleForLine(BusStop, i_BusLine):
#Check if was given BusStop INT ( busstopID )  or STR ( busstopName )?
    print(f"args:{BusStop}  i_BusLine")
    stopID = BusStop
    clearText = unidecode(BusStop)
    if not BusStop.isdigit():
        stopID = findStopIdByName(clearText)
        print(f"Retrieved BusID {stopID} for {clearText}")
    else:
        print(f"Searching data for stopID: {stopID} for stop: {clearText}")
#Obtain the last schedule update date
    
    response = ""
    url = f"https://ztm.gda.pl/rozklady/linia-{i_BusLine}.html"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error getting html data for schedule {i_BusLine}.")
        return None
    
    response = BeautifulSoup(response.text,"html.parser")
 
     
    lastUpdate = getLastUpdateDateForLine(response,i_BusLine) 
    
    cleanDate = lastUpdate.strip()
    print(f"cleanDate {cleanDate}")
    realDate = datetime.strptime(cleanDate, "%d.%m.%Y")
    realDate = realDate.strftime("%Y%m%d")
    directionCode = clearText[-2:]
    directionCode = '1' if directionCode[-1:] == '2' else '2' 
    dateYMD = datetime.today().strftime("%Y%m%d")
    
    print(f"Getting stoplist for bus line {i_BusLine} {int(directionCode)}")
    stoplists = getStoplistForLine(response, i_BusLine)
    index = -1
    directionkey = -1

    for DirectionKey, Stops in stoplists.items():
        if BusStop in Stops:
            index = Stops.index(BusStop)
            directionkey = DirectionKey[1:]  #02

    stoporder = index+1  

    url = f"https://ztm.gda.pl/rozklady/rozklad-{i_BusLine}_{realDate}-{stoporder}-{directionkey}-dzien-{dateYMD}.html"
    print("Sending GET request to: " + url)

    response = requests.get(url)

    if(response.status_code == 200):
        print("Successfully obtained schedule data")
        rawdata = BeautifulSoup(response.text,"html.parser")
        departures = rawdata.find("div",class_="departures-set")
        schedules = []
        current = {"hours":"","minutes":[]} 
        for child in departures.find_all(recursive=False): 
            
            class_ = child.get("class")[0] if child.has_attr("class") else None  
            match class_:
                case "h": 
                    if current is not None and current["hours"]:
                        schedules.append(current)  
                    current = {"hours":child.text, "minutes":[]}
                case "m":
                    current["minutes"].append(child.text)      
                case None:
                    continue
        schedules.append(current) #adding the last element. very cool feature              
            
    else:
        print("Failed to obtain schedule data")  
    return schedules

def GetAllData():

    bus_data = getBusData()
 
    output = "output.txt"

    todayDate = datetime.now().strftime("%Y%m%d") 

    url = f"https://ztm.gda.pl/rozklady/linia-2.html"
    try:
        with open(output,"r", encoding="utf-8") as file_:
            if file_.read(1):
                file_.seek(0)
                stat = os.stat(file_.name)
                timestamp = getattr(stat, 'st_birthtime', stat.st_birthtime)
                creation_date = datetime.datetime.fromtimestamp(timestamp)

                print(f"File output (created {creation_date}) exists. Reading...")
    except (FileExistsError, FileNotFoundError):
        print("File is empty or non exists. Creating...")
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Success...Response size: {len(response.text)} + bytes")

            with open(output,"w", encoding="utf-8") as file:
                file.write(response.text) 
            printDate(response.text)

        else:
            print(f"Response failed with code: {response.status_code}")
    else:
        print(f"Found {output}. Opening")
 