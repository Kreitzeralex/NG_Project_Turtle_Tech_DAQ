#!/usr/bin/env python

# This code was written by Alex Kreitzer, Will Bradford, and Megan Caulfield for use in the 2021-22 Section 1 Buoy for Northrop Grumman

import time
# import serial
# import adafruit_gps
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Connects to our database
import mysql.connector






#Database and RFID section of code
db = mysql.connector.connect(
  host="localhost",
  user="JMUWAM",
  passwd="rockcity",
  database="Section1DAQ"
)

cursor = db.cursor()
reader = SimpleMFRC522()

# Infinite loop that searches for nearby RFID tags to read
try:
  while True:
    
    print('Searching for Creatures...')
    
    # Defines collected RFID UID as a variable 
    id, text = reader.read()
    
    #Defining the command to insert collected data into our RFID table in the RFID_UID column in our database
    sql_insert = "INSERT INTO RFID (RFID_UID, Sent) VALUES (%s, %s)"

    # Converts collected RFID UID into list format
    data = [id, 0]
    
    # Inputs data into database
    cursor.execute(sql_insert, data)

    # Saving the changes to the database that we have made
    db.commit()
    
    # Tells the user if the data was saved with no errors
    print('Data Saved')

    # Puts the reader to sleep every 5 seconds
    # The reader will collect new data every 5 seconds if there is a tag within its range
    # Change the 5 to any number you desire and the reader will collect data after that many seconds has passed
    time.sleep(5)

finally: 
  GPIO.cleanup()
