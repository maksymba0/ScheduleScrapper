
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from unidecode import unidecode
from ztm_gdansk import GetBusDataByNumberOrText,  getRealTimeTableForStop, GetBusstopScheduleForLine
import json
from datetime import datetime

def debugtest():
    print("Hello world")

def onTypeEvent(event):

    global favourites

    searchtext = entry.get()
    searchtext = unidecode(searchtext).lower()
    listbox.delete(0,tk.END) 
    #print(searchtext)
    list = GetBusDataByNumberOrText(searchtext)

    list.sort(key=lambda obj: (
        (obj["stopName"] + " " + obj["stopCode"]) not in favourites
    ))

    for obj in list:
        stopName = obj["stopName"] + " " + obj["stopCode"]
        listbox.insert(tk.END, stopName)
    StopListHighlightFavourite()
 
def StopListHighlightFavourite():
    if not favourites:
        return
    current_rows = listbox.get(0,tk.END)

    for i, stoptext in enumerate(current_rows):
        cleantext = stoptext.strip()
        if cleantext in favourites:
            index = listbox.size() - 1
            listbox.itemconfigure(i, background="#E2F0D9", foreground="#385723")
        else:
            listbox.itemconfigure(i, background="#F3F6F1", foreground="#010101")
                    
        
def printrttable(list):
    rttable.delete(1.0,tk.END)
    if list is None:
        return
    for obj in list:
        text = f"{obj["busID"]} | {obj["direction"]} | {obj["etd"]}{"\n"}"
        #print(text)
        rttable.insert(tk.END,text)

def printscheduletable(list): 
    timeSchedule.delete(1.0,tk.END)
    if list is None:
        return
    for obj in list:
        hour = obj["hours"].rjust(2)
        minutes = obj["minutes"]
        minutesText = "   ".join(minutes)
        output = f"{hour} - {minutesText}\n"
        #print(output)
        timeSchedule.insert(tk.END,output)

def justPrintRealtimetable(busstopName):
    global rate_limit
    timePassed = (datetime.now() - lastUpdated).total_seconds()
    print(f"Passed since last {timePassed}")
    if timePassed <= rate_limit:
        #bad case. used spamming
        messagebox.showerror("Error html request", f"Please wait around {round(rate_limit - timePassed,0)} seconds")
        return
    rttable.delete("1.0",tk.END)
    list = getRealTimeTableForStop(unidecode(busstopName))
    if list == None:
        print("Empty list for bus stop " + busstopName)
        return 
    SetStatus(f"Printing real-time table for {busstopName}")
    printrttable(list)  
    SetStatus(f"Printed real-time table for {busstopName}")

def justPrintSchedule(busstopName):
    global rate_limit
    timePassed = (datetime.now() - lastUpdated).total_seconds()
    print(f"Passed since last {timePassed}")
    if timePassed <= rate_limit:
        #bad case. used spamming
        messagebox.showerror("Error html request", f"Please wait around {round(rate_limit - timePassed,0)} seconds")
        return
    rttable.delete("1.0",tk.END) 
    searchtext = entry.get() 
    searchtext = unidecode(searchtext).lower()

    result = GetBusstopScheduleForLine(busstopName, searchtext)
    #print(result)


    if searchtext.isdigit(): #Did user enter the bus-line number?
        print("Field contains numeric data: OK")
        table = GetBusstopScheduleForLine(busstopName, searchtext)
        printscheduletable(table)
    else:
        print("Field not contains non-numeric data: NOT OK")
        printscheduletable(None)

def OnBusStopSelected(busstopName):
    rttable.delete("1.0",tk.END)

    SetStatus(text_=f"Attempting to get Real-Time Table for stop '{busstopName}'")
    list = getRealTimeTableForStop(unidecode(busstopName))
    if list == None:
        print("Empty list for bus stop " + busstopName)
        return 
    try:
        SetStatus(text_=f"Printing Real-Time Table for stop '{busstopName}'")
        printrttable(list) 
        SetStatus(text_=f"Finished printing Real-Time Table for stop '{busstopName}'")    
    except Exception as e:
        print(f"Unable to print timetable: {e}")
        SetStatus(text_=f"Error printing Real-Time Table for stop '{busstopName}'")
        printrttable(None)
    searchtext = entry.get() 
    searchtext = unidecode(searchtext).lower()

    if searchtext.isdigit(): #Did user enter the bus-line number?
        print("Field contains numeric data:" + searchtext)
        SetStatus(text_=f"Attempting to get Schedule for stop '{busstopName}'")
        table = GetBusstopScheduleForLine(busstopName, searchtext)
        SetStatus(text_=f"Printing Schedule for stop '{busstopName}'")
        printscheduletable(table)
        SetStatus(text_=f"Finished printing Schedule for stop '{busstopName}'")    
    else:
        SetStatus(f"Error printing Schedule for stop '{busstopName}'")
        print("Field not contains non-numeric data: " + searchtext)
        printscheduletable(None)
        

lastUpdated = datetime.now()
rate_limit = 6; ## 2.6 seconds
def SetStatus(text_):
    if text_ is None:
        text_ = "idle"
    global Status
    Status.config(text=f"Status: {text_}")
            
def OnDoubleClick(event):
    
    SetStatus(f"Processing request. Please wait'")
    global lastUpdated
    global Status
    global rate_limit
    timePassed = (datetime.now() - lastUpdated).total_seconds()
    print(f"Passed since last {timePassed}")
    if timePassed <= rate_limit:
        #bad case. used spamming
        messagebox.showerror("Error html request", f"Please wait around {(round(rate_limit - timePassed,0))} seconds")
        SetStatus(f"Error processing request. Please wait and try again")
        return
    index = listbox.curselection()
    if index:
        item = listbox.get(index)
        #print(f"Selected {item}")
        OnBusStopSelected(item)
        lastUpdated = datetime.now()

selected_element = ""
favourites = []

 
   

def PreloadFavouriteStops():
    print(f"Loading the favourite stop list")
#Read current favourites
    global favourites
    try:
        with open("favourites.txt","r",encoding="utf-8") as file_:
            favourites = json.load(file_)
    except (FileNotFoundError, json.JSONDecodeError):
        favourites = [] 
def LoadFavouriteStops(event = None):

    global favourites
    print(f"Loading the favourite stop list")
    SetStatus("Loading the favourite stop list")
#Read current favourites
    try:
        with open("favourites.txt","r",encoding="utf-8") as file_:
            favourites = json.load(file_)
    except (FileNotFoundError, json.JSONDecodeError):
        favourites = []
        SetStatus("Failed to load favourite stop list")
#Check if not appearing 
    if favourites: 

        listbox.delete(0,tk.END)
        listbox.selection_clear(0,tk.END)
        
        for obj in favourites:
            listbox.insert(tk.END,obj)
        messagebox.showinfo("Success", "Loaded favourite list")
        SetStatus("Loaded favourite stop list")
        return
    StopListHighlightFavourite()


def ListDelFavourite(event=None):
    global selected_element
    global favourites
    if not selected_element:
        return

    print(f"Removing {selected_element} from the favourite list")
#Read current favourites
    try:
        with open("favourites.txt","r",encoding="utf-8") as file_:
            favourites = json.load(file_)
    except (FileNotFoundError, json.JSONDecodeError):
        favourites = []
#Check if not appearing

    if selected_element in favourites:
        favourites.remove(selected_element)
        with open("favourites.txt", "w", encoding="utf-8") as file:
            json.dump(favourites, file, indent=2)
        messagebox.showinfo("Success", f"Removed {selected_element} from favourites")
    else:
        messagebox.showerror("Failure", f" {selected_element} Not exists in favourite list")
        return
    print("removed from favourite")
    StopListHighlightFavourite()

def ListAddFavourite(event=None):
  
    global selected_element
    global favourites
    if not selected_element:
        return

    print(f"Adding {selected_element} to the favourite list")
    SetStatus(f"Adding {selected_element} to the favourite list")
        
#Read current favourites
    try:
        with open("favourites.txt","r",encoding="utf-8") as file_:
            favourites = json.load(file_)
    except (FileNotFoundError, json.JSONDecodeError):
        favourites = []
#Check if not appearing

    if selected_element not in favourites:
        favourites.append(selected_element)
        with open("favourites.txt", "w", encoding="utf-8") as file:
            json.dump(favourites, file, indent=2)
        messagebox.showinfo("Success", f"Added {selected_element} to favourites")
        SetStatus(f"Added {selected_element} to the favourite list")
    else:
        messagebox.showerror("Failure", "Already exists in favourite list")
        SetStatus(f"Error adding {selected_element} to the favourite list")
        return
    #print("added to favourite")
    StopListHighlightFavourite()

def ListRClickCallback(event):
    if listbox.size() == 0:
        return
    index = listbox.nearest(event.y)
    if index is None:
        return
    listbox.selection_clear(0,tk.END)
    listbox.selection_set(index)
    listbox.activate(index)

    global selected_element
    selected_element = listbox.get(index)

    context_menu.delete(0,tk.END)

    if selected_element in favourites:
        context_menu.add_command(label="❌Remove as favourite", command=ListDelFavourite)
    else:        
        context_menu.add_command(label="➕ Add as favourite", command=ListAddFavourite)
    context_menu.add_command(label="🔎 Check Schedule", command=lambda: on_menu_action("schedule"))
    context_menu.add_command(label="⏲️ Check Timetable", command=lambda: on_menu_action("timetable"))


    context_menu.post(event.x_root, event.y_root)

def on_menu_action(action):

    SetStatus(f"Processing")
    global Status
    global selected_element
    if not selected_element:
        return
    
    print(f"user wants to see {action}")
    if "schedule" in action:
        SetStatus(f"Attempting to print schedule for stop '{selected_element}'")
        justPrintSchedule(selected_element)
    else:
        
        SetStatus(f"Attempting to print real-time table for stop '{selected_element}'")
        justPrintRealtimetable(selected_element)
    


PreloadFavouriteStops()

root = tk.Tk()
root.title("ZTM Schedule Grabber")
root.geometry("1000x600")


label = tk.Label(root,text="Enter bus-line number  or  bus-stop name. ")
label.pack(pady=10)
 
 

entry = tk.Entry(root,width=60)
entry.bind("<KeyRelease>",onTypeEvent)
entry.pack(pady=5)

button = tk.Button(root, text="Load Favourite", command=LoadFavouriteStops, width=16, height=2)
button.pack(pady=5)


frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

frame.rowconfigure(0,weight=1)
frame.rowconfigure(1,weight=1)
frame.columnconfigure(0,weight=1)
frame.columnconfigure(1,weight=1)
frame.columnconfigure(2,weight=1)
#####################                                     FRAME OBJECTS 

normal_font = tkFont.Font(family="Arial", size=12, weight=tkFont.NORMAL)

today = datetime.now().today().strftime("%d/%m/%Y")
label = tk.Label(frame,text=f"Data for day: {today}", font=normal_font)
label.grid(row=0,column=0,padx=5,pady=2,sticky="news")

timeSchedule = tk.Text(frame,width=38 )
timeSchedule.grid(row=1,column=0,padx=5,pady=5,sticky="news")  

listframe = tk.Frame(frame)
listframe.grid(row=1, column=1, padx=5, pady=5, sticky="news")

yscrollbar = tk.Scrollbar(listframe,orient="vertical")
yscrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(listframe,width=24,height=24,yscrollcommand=yscrollbar.set)
listbox.pack(side="top", fill="both", expand=True)
yscrollbar.config(command=listbox.yview) 
 
listbox.bind("<Double-Button-1>", OnDoubleClick)
listbox.bind("<Button-3>",ListRClickCallback )

rttable = tk.Text(frame,width=35 )
rttable.grid(row=1,column=2,padx=5,pady=5,sticky="news")
######################
  
Status = tk.Label(root,text="Updating")
Status.pack()
SetStatus("idle")
 
##################### CONTEXT MENU - BUS STOP LIST

context_menu = tk.Menu(root,tearoff=0)
 




if __name__ == "__main__":
    root.mainloop()

 

 
 