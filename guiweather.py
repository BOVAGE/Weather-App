import tkinter as tk
from PIL import ImageTk, Image
import requests, json, pprint


base_width = 435
base_height = 400
root = tk.Tk()
root.title("Weather App")
root.iconbitmap(r"images\logo.ico")
root.geometry(f"{base_width}x{base_height}+0+0")

def get_weather(city_name: str) -> dict:
    """ makes a request to openweather api"""
    #open weather api key
    api_key = "e75cab1956638b0ff65b76430f0b708e"
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"appid": api_key, "q": city_name, "units": "metric"}
    response = requests.get(api_url, params = params).text
    weather_dict = json.loads(response)
    #pprint.pprint(weather_dict)
    return weather_dict

def display_weather(*events):
    """ displays the result to label widgets """
    try:
        weather_data = get_weather(location_entry.get())
        #print(weather_data)
    except requests.ConnectionError:
        result.set("Check your internet connection")    
    else:
        try:
            name = weather_data["name"]
            temp = weather_data["main"]["temp"]
            country = weather_data["sys"]["country"]
            description = weather_data["weather"][0]["description"].capitalize()
            iconid = weather_data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{iconid}@2x.png"
            #get image for the icons
            #icon = requests.get(icon_url)
            #icon = tk.PhotoImage(file = icon.content)
            result.set(f"City: {name}\nCondition: {description}\nCountry: {country}\nTemperature(\N{DEGREE SIGN}C): {temp}")
        except KeyError:
            result.set(weather_data.get("message"))
    

background_image = tk.PhotoImage(file = "images/background.png")
background_label = tk.Label(root, image = background_image)
background_label.place(relwidth = 1.0, relheight = 1.0)

#frame for entry and button widgets
top_frame = tk.Frame(root, bg = "skyblue", bd = "3")
top_frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.2)

#frame for text widget
bottom_frame = tk.Frame(root, bg = "skyblue", bd = "5")
bottom_frame.place(relx = 0.1, rely = 0.35, relwidth = 0.8, relheight = 0.6)

location_entry = tk.Entry(top_frame, fg = "black", font = ("Arial", 18, "bold"))
location_entry.place(relwidth = 0.7, relheight = 0.9, rely = 0.05)

get_weatherBtn = tk.Button(top_frame, text = "Get Weather", bg = "blue", bd = "4",fg = "#000d33",
                          relief = "raised", font = ("Arial", 12),
                          command = display_weather)
get_weatherBtn.place(relx = 0.71, rely = 0.05, relwidth = 0.29, relheight = 0.9)

root.bind("<Return>", display_weather)

result = tk.StringVar()
result_text = tk.Label(bottom_frame, textvariable = result, font = ("Arial", 16))
result_text.place(relwidth = 1.0, relheight = 1.0)

root.mainloop()
