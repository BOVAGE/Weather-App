import tkinter as tk
from PIL import ImageTk, Image
import requests, json, pprint


baseWidth = 435
baseHeight = 400
root = tk.Tk()
root.geometry(f"{baseWidth}x{baseWidth}+0+0")

def getWeather(cityName: str) -> dict:
    """ makes a request to openweather api"""
    #open weather api key
    apiKey = "e75cab1956638b0ff65b76430f0b708e"
    apiUrl = "https://api.openweathermap.org/data/2.5/weather"
    params = {"appid": apiKey, "q": cityName, "units": "metric"}
    response = requests.get(apiUrl, params = params).text
    weatherDict = json.loads(response)
    #pprint.pprint(weatherDict)
    return weatherDict

def displayWeather(*events):
    """ displays the result to label widgets """
    try:
        weatherData = getWeather(locationEntry.get())
        #print(weatherData)
    except requests.ConnectionError:
        result.set("Check your internet connection")
        
    try:
        name = weatherData["name"]
        temp = weatherData["main"]["temp"]
        country = weatherData["sys"]["country"]
        description = weatherData["weather"][0]["description"].capitalize()
        iconid = weatherData["weather"][0]["icon"]
        iconUrl = f"http://openweathermap.org/img/wn/{iconid}@2x.png"
        #get image for the icons
        #icon = requests.get(iconUrl)
        #icon = tk.PhotoImage(file = icon.content)
        result.set(f"City: {name}\nCondition: {description}\nCountry: {country}\nTemperature(\N{DEGREE SIGN}C): {temp}")
    except KeyError:
        result.set(weatherData.get("message"))
    

backgroundImage = tk.PhotoImage(file = "images/background.png")
backgroundLabel = tk.Label(root, image = backgroundImage)
backgroundLabel.place(relwidth = 1.0, relheight = 1.0)

#frame for entry and button widgets
topFrame = tk.Frame(root, bg = "skyblue", bd = "3")
topFrame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.2)

#frame for text widget
bottomFrame = tk.Frame(root, bg = "skyblue", bd = "5")
bottomFrame.place(relx = 0.1, rely = 0.35, relwidth = 0.8, relheight = 0.6)

locationEntry = tk.Entry(topFrame, fg = "black", font = ("Arial", 18, "bold"))
locationEntry.place(relwidth = 0.7, relheight = 0.9, rely = 0.05)

getWeatherBtn = tk.Button(topFrame, text = "Get Weather", bg = "blue", bd = "4",fg = "#000d33",
                          relief = "raised", font = ("Arial", 12),
                          command = displayWeather)
getWeatherBtn.place(relx = 0.71, rely = 0.05, relwidth = 0.29, relheight = 0.9)
root.bind("<Return>", displayWeather)

result = tk.StringVar()
resultText = tk.Label(bottomFrame, textvariable = result, font = ("Arial", 16))
resultText.place(relwidth = 1.0, relheight = 1.0)

root.mainloop()
