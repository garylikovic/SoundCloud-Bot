import os
import csv
import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException, InvalidSessionIdException, ElementClickInterceptedException, Ma
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

        
        self.title("SoundCloud Bot v{}".format(appVersion))
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

        with open(SoundCloudCsvPath,'r',encoding='utf-8-sig') as songCsv:
            csvReader = csv.reader(songCsv,delimiter=',')
            for line in csvReader:
                for song in line:
                    songList.append(song)
                    reverseList.append(song)
        
        reverseList.reverse()

    def makesoundCloudThread(self):

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

            driverPath = currentPath +"\geckodriver.exe"

            ffOptions = Options()
            ffOptions.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

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
                    
                    time.sleep(2)

                    # Click play button
                    playButton.click()
                    
                    time.sleep(2)
                    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
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
                        print("File Count and Song Count Met")
                        browser.quit()                          

                except ElementClickInterceptedException:

                    # Failed to click on play button because a Ad needs to play
                    
                    self.outputBox.insert(END,"An Advertisement is playing, waiting for ad \n")

                    # Get the ad play button and click it
                    adButton = browser.find_element(By.XPATH, "/html/body/div[1]/div[4]/section/div/div[3]/button[2]")
                    adButton.click()

                    time.sleep(35)

                    # Ad has played, try to play the song again
    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
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
                    self.outputBox.insert(END,"Browser Window Has Been Closed. Ending Bot. \n ")
                    return
                
                except InvalidSessionIdException:
                    self.outputBox.insert(END,"Browser Window Has Been Closed. Ending Bot. \n ")
                    return
                
                except NoSuchElementException:

                    # Open Song Address
                    browser.get(song)

                    # Wait for page to load
                    time.sleep(5)

                    # Get song title
                    songTitle = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/h1/span').get_attribute("innerHTML")
                    
                    # Find play button and click it
                    playButton = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
                    
                    time.sleep(2)

                    # Click play button
                    playButton.click()
                    
                    time.sleep(2)
                    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
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
                        print("File Count and Song Count Met")
                        browser.quit()  


                except WebDriverException:

                    # Open Song Address
                    browser.get(song)

                    # Wait for page to load
                    time.sleep(5)

                    # Get song title
                    songTitle = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/h1/span').get_attribute("innerHTML")
                    
                    # Find play button and click it
                    playButton = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
                    
                    time.sleep(2)

                    # Click play button
                    playButton.click()
                    
                    time.sleep(2)
                    
                    # Get updated play count
                    playCount = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[2]').get_attribute("innerHTML")
                    
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
                        print("File Count and Song Count Met")
                        browser.quit()      

        # Reset File Counter
        fileCount = 0
          

if __name__ == '__main__':
    app = SoundCloudBot()
    app.mainloop()