import os
import csv
import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException, InvalidSessionIdException, ElementClickInterceptedException
import threading
from sys import platform
from selenium.webdriver.firefox.options import Options


# Application version
appVersion = 2.5

# Get current script location
currentPath = os.path.dirname(__file__)
# Set location of the song csv file
SoundCloudCsvPath = currentPath + '/songs.csv'

# Create the lists that will be used to track the songs being played
counterList = []
songList = []
reverseList = []

class SoundCloudBot(Tk):

    def __init__(self):
        super().__init__()

        # Application Title
        self.title("SoundCloud Bot v{}".format(appVersion))
        # Set window size
        self.geometry('700x510')

        # Create drop menu options list
        self.createCounter()

        # Repeat song list counter label
        self.listRepeatCounterLabel = Label(self,text='Repeat list counter:')
        self.listRepeatCounterLabel.place(x=20,y=20)

        # Repeat song list counter combo
        self.listRepeatCounterCombo = ttk.Combobox(self,width=5, values=counterList)
        self.listRepeatCounterCombo.place(x=140,y=20)

        # Button to start the bot loop
        self.startButton = Button(self,text='Start',command=self.makesoundCloudThread)
        self.startButton.place(x=440,y=20)

        # Song Repeat Counter Label
        self.viewCounterLabel = Label(self, text='View Counter:')
        self.viewCounterLabel.place(x=520,y=20)

        # Song Repeat Counter
        self.viewCounter = Label(self,text="0")
        self.viewCounter.place(x=620,y=20)

        # Output for action log
        self.outputBox = Text(self, width=96,height=33)
        self.outputBox.place(x=10,y=60)

    def createCounter(self):

        count = 0

        while count < 1000:
            count += 1
            counterList.append(count)
        
    def createSongList(self):

        # Open the CSV file
        with open(SoundCloudCsvPath,'r',encoding='utf-8-sig') as songCsv:
            # Reader created to get information from open CSV
            csvReader = csv.reader(songCsv,delimiter=',')
            # For each line in the reader, for each song in the line append it to the song list
            for line in csvReader:
                for song in line:
                    songList.append(song)
                    reverseList.append(song)
        # Reverse list so that when the final song is met, the File Counter is increased
        reverseList.reverse()

    def makesoundCloudThread(self):

        # Creating a thread for the bot so the UI does not freeze when running
        for i in range(1):

            self.scThread = threading.Thread(target=self.startSCBot)
            self.scThread.start()

    def startSCBot(self):

        # Make sure the list repeater isnt empty
        if self.listRepeatCounterCombo.get() == "":
            message = MessageBox.showerror(title='No Repeat Value Selected',message='Please select a repeat count to continue!')
            return

        # Compile song list to go through
        self.createSongList()

        # Platform Checking
        # Check if OSX
        if platform == "darwin":
            # Open browser
            browser = webdriver.Firefox()
        # Check if Windows
        elif platform == "win32":
            # Set the gecko driver path
            driverPath = currentPath +"\geckodriver.exe"
            # Create a configuration to find the installation path for FireFox
            ffOptions = Options()
            ffOptions.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
            # Open browser with the configuration
            browser = webdriver.Firefox(executable_path=driverPath,options=ffOptions)

        #loop file count
        fileCount = 0
        # View counter 
        viewCount = int(self.viewCounter.cget("text"))

        # While file loop count is less than selection, repeat
        while fileCount <= int(self.listRepeatCounterCombo.get()):
            
            # For each song in list, repeat
            for song in songList:

                try:

                    # Open Song Address
                    browser.get(song)

                    # Wait for page to load
                    time.sleep(5)

                    # Get song title
                    songTitle = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/h1/span').get_attribute("innerHTML")
                    
                    # Find play button and click it
                    playButton = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Click play button
                    playButton.click()
                    
                    # Wait for page to load
                    time.sleep(2)
                    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Log song and play count
                    self.outputBox.insert(END,"Song: {} | Play Count: {} \n".format(songTitle,playCount))

                    # Increase View Counter
                    viewCount += 1

                    # Update View Counter Value
                    self.viewCounter.config(text = viewCount)

                    # Wait X seconds before moving to next song/ repeating
                    time.sleep(60)

                    # Increase file counter if at the end of the list
                    if song == reverseList[0]:
                        fileCount += 1
                    # End the loop if loop count has been met
                    if fileCount == int(self.listRepeatCounterCombo.get()):
                        # Close the browser, the repeat limit has been met
                        browser.quit()                          

                except ElementClickInterceptedException:

                    # Failed to click on play button because a Ad needs to play
                    self.outputBox.insert(END,"An Advertisement is playing, waiting for ad \n")

                    # Get the ad play button and click it
                    adButton = browser.find_element(By.XPATH, "/html/body/div[1]/div[4]/section/div/div[3]/button[2]")
                    adButton.click()

                    # Wait fot the Ad to play
                    time.sleep(35)

                    # Ad has played, song will now automatically play
    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Log song and play count
                    self.outputBox.insert(END,"Song: {} | Play Count: {} \n".format(songTitle,playCount))

                    # Increase View Counter
                    viewCount += 1

                    # Update View Counter Value
                    self.viewCounter.config(text = viewCount)

                    # Wait X seconds before moving to next song/ repeating
                    time.sleep(60)

                except NoSuchWindowException:
                    # Browser window has been closed, exit bot loop
                    self.outputBox.insert(END,"Browser Window Has Been Closed. Ending Bot. \n ")
                    return
                
                except InvalidSessionIdException:
                    # Browser being closed can also prompt an Invalid Session instead of missing window
                    self.outputBox.insert(END,"Browser Window Has Been Closed. Ending Bot. \n ")
                    return
                
                except NoSuchElementException:

                    # This exception is to catch if the element cannot be located, either the page didnt load fast enough or the internet connection has been lost.

                    # Open Song Address
                    browser.get(song)

                    # Wait for page to load
                    time.sleep(5)

                    # Get song title
                    songTitle = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/h1/span').get_attribute("innerHTML")
                    
                    # Find play button and click it
                    playButton = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Click play button
                    playButton.click()
                    
                    # Wait for page to load
                    time.sleep(2)
                    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Log song and play count
                    self.outputBox.insert(END,"Song: {} | Play Count: {} \n".format(songTitle,playCount))

                    # Increase View Counter
                    viewCount += 1

                    # Update View Counter Value
                    self.viewCounter.config(text = viewCount)

                    # Wait X seconds before moving to next song/ repeating
                    time.sleep(60)

                    
                    # Increase file counter if at the end of the list
                    if song == reverseList[0]:
                        fileCount += 1
                    # End the loop if loop count has been met
                    if fileCount == int(self.listRepeatCounterCombo.get()):
                        # Close the browser, the repeat limit has been met
                        browser.quit()  


                except WebDriverException:

                    # This exception is to catch if the driver fails to load the page and get information from it, either the page didnt load fast enough or the internet connection has been lost.

                    # Open Song Address
                    browser.get(song)

                    # Wait for page to load
                    time.sleep(5)

                    # Get song title
                    songTitle = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/h1/span').get_attribute("innerHTML")
                    
                    # Find play button and click it
                    playButton = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Click play button
                    playButton.click()
                    
                    # Wait for page to load
                    time.sleep(2)
                    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
                    # Wait for page to load
                    time.sleep(2)

                    # Log song and play count
                    self.outputBox.insert(END,"Song: {} | Play Count: {} \n".format(songTitle,playCount))

                    # Increase View Counter
                    viewCount += 1

                    # Update View Counter Value
                    self.viewCounter.config(text = viewCount)

                    # Wait X seconds before moving to next song/ repeating
                    time.sleep(60)

                    
                    # Increase file counter if at the end of the list
                    if song == reverseList[0]:
                        fileCount += 1
                    # End the loop if loop count has been met
                    if fileCount == int(self.listRepeatCounterCombo.get()):
                        # Close the browser, the repeat limit has been met
                        browser.quit()      

        # Reset File Counter
        fileCount = 0
          
# If this script was loaded as the main app, create a instance of the bot and start the main loop
if __name__ == '__main__':
    app = SoundCloudBot()
    app.mainloop()
