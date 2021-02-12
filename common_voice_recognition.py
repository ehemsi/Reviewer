# This program is used to store the common voice recognition of various commands in the program

import speech_recognition as sr
import csv

r = sr.Recognizer()

data = {}
key = ""

while(1):
    key = input("Enter key: ")
    if key == "end":
        break
    print("Say " + key)
    for i in range(50):
        print(i, end = ': ')
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                voice_data = r.recognize_google(audio, language='en-PH')
            except sr.UnknownValueError:
                print("Didn't recognize. Skipping.")
                continue
            except sr.RequestError:
                print("Service is down. Skipping.")
                continue
            print(voice_data)
            data[voice_data] = key

with open('voice_recognition_data.csv', 'w', newline= "") as csv_file:
    writer = csv.writer(csv_file)
    for key, value in data.items():
        writer.writerow([key,value])


