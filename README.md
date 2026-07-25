# Schedule Scrapper 🚌
*(My first Python project after years of learning CPP)*

I built this to check how web-data scrapping works and I also needed something faster than reaching for my phone every time I need to check when my bus arrives. 

### Who is it for?
- Anyone living in or visiting Gdańsk who uses the bus network.
- Anyone who wants to check bus times without opening a browser or mobile app (strange as it may seem though)
- Anyone learning python who wants to check how html data is scrapped and processed 
- Me

### How does it work?
1. Launch the app.
2. Type a bus-stop name or line number into the top input field.
3. A list of matching stops appears in the middle box (listbox).
4. Double-click a stop to load its data.
   - If you entered a line number, the left panel will show the full schedule.
   - The right panel always shows the real-time departures

### Features:
- Search by **bus-stop name** or **bus-line number**.
- Real-time departures (right panel).
- Full schedule for a specific line at a specific stop (left panel).
- Right-click any stop to open a context menu with options:
  - Add to Favourites
  - Remove from Favourites
  - Display Schedule
  - Show Timetable
- Favourites are saved and highlighted in green.
- Load Favourites button shows your saved stops.

(App init)

<img width="1252" height="788" alt="image" src="https://github.com/user-attachments/assets/72ea36e9-db17-453d-87c7-918caa029c74" />

(Search by bus line number)

<img width="1252" height="793" alt="image" src="https://github.com/user-attachments/assets/6e3a679a-64a4-4501-959d-5e7e9ea4278e" />

(Search by bus-stop name)

<img width="1243" height="301" alt="image" src="https://github.com/user-attachments/assets/33f7af27-6ce0-4432-a6ae-1dbe56eabd8e" />

(Double clicking a bus stop in the list - printing schedule and real-time table)

<img width="1243" height="576" alt="image" src="https://github.com/user-attachments/assets/97d28c11-8237-4e06-839e-7bc8009251f8" />

(Right clicking a bus stop in the list - context menu with options)

<img width="300" height="130" alt="image" src="https://github.com/user-attachments/assets/f8bd09d3-82cf-4787-b6e1-3f5f1954384d" />



(Adding a bus stop to favourite list - highlighting favourite stops in green color )

<img width="1248" height="467" alt="image" src="https://github.com/user-attachments/assets/7dc45a9c-5ddb-47a4-9a4e-3fb664b9bc62" />

(Clicking Load Favourite button- list containing only favourite stops)

<img width="911" height="497" alt="image" src="https://github.com/user-attachments/assets/daee253a-d03e-4a59-b458-acfa69bebbdb" />

### Built with
- Python 3.14.6
- tkinter (GUI)
- requests & BeautifulSoup (API scraping)
- unidecode (Polish character handling)

### Download and install
a) Manual download and running (just download the .py files and run the main one - bus_gui.py)
- MAKE SURE THEY ARE IN AN EMPTY FOLDER TOGETHER !!!
Not running? Make sure to install Python first at: https://www.python.org/downloads/
b) Git -
```
git clone https://github.com/maksymba0/ScheduleScrapper.git
cd ScheduleScrapper
pip install -r requirements.txt
python bus_gui.py
```
Thanks for reading all the way here
