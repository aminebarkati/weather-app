import requests
import smtplib
from email.message import EmailMessage
###############################
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import ttkbootstrap.themes.standard as lst
from tkinter.messagebox import showerror, showinfo
####################################
from geopy.geocoders import Nominatim
import geocoder
############################################


def getcity():
    geolocator = Nominatim(user_agent="geoapiExercises")
    g = (geocoder.ip('me')).latlng
    g = str(g[0])+","+str(g[1])
    location = geolocator.reverse(g,  language='en')
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    return {
        "city": city,
        "state": state,
        "country": country
    }


def getloc():
    city = getcity()["city"]
    url1 = "https://foreca-weather.p.rapidapi.com/location/search/"+city

    querystring1 = {"lang": "en"}

    headers1 = {
        "X-RapidAPI-Key": "5cf393376fmsh9ee7aff0371de7bp19a155jsne283f6365e29",
        "X-RapidAPI-Host": "foreca-weather.p.rapidapi.com"
    }

    response1 = requests.request(
        "GET", url1, headers=headers1, params=querystring1)
    data = response1.json()
    loc = data["locations"][0]["id"]
    return str(loc)


def getdata():
    periods = per.get()
    if periods == "0" or not periods.isdigit() or int(periods) > 12:
        showinfo(
            message="periods must be number between 1 and 12 or we set it to 3 automatically")
        periods = "3"
    ##############################################
    loc = getloc()
    ##############################################
    url = "https://foreca-weather.p.rapidapi.com/forecast/3hourly/"+loc
    querystring = {"alt": "0", "tempunit": "C", "windunit": "KMH",
                   "tz": "Central European Standard Time", "periods": periods, "dataset": "full"}

    headers = {
        'x-rapidapi-host': "foreca-weather.p.rapidapi.com",
        'x-rapidapi-key': "5cf393376fmsh9ee7aff0371de7bp19a155jsne283f6365e29"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    weather_data = response.json()
    return weather_data, periods
###############################################


def reformulate():
    weather_data_text.configure(state='normal')
    weather_data_text.delete("1.0", "end")
    weather_data_text.configure(state='disabled')
    data, per = getdata()
    per = int(per)
    main_message = getcity()["city"]+"/" + \
        getcity()["state"]+"/"+getcity()["country"]+"\n"
    for i in range(per):
        time = (data["forecast"][i]["time"])[0:10] + \
            "||"+(data["forecast"][i]["time"])[11:16]
        temperature = str(data["forecast"][i]["temperature"])+"°C"
        symbolPhrase = data["forecast"][i]["symbolPhrase"]
        precipType = data["forecast"][i]["precipType"]
        windSpeed = str(data["forecast"][i]["windSpeed"])+"km/h"
        relHumidity = str(data["forecast"][i]["relHumidity"])+"%"
        windDir = str(data["forecast"][i]["windDir"])+"°"
        cloudiness = str(data["forecast"][i]["cloudiness"])+"%"
        pressure = str(data["forecast"][i]["pressure"])+"Pa"
        visibility = str(data["forecast"][i]["visibility"])+"m"
        main_message = main_message + \
            f"temps : {time}\nTempérature : {temperature}\nvitesse du vent : {windSpeed}\nhumidité relative : {relHumidity}\nsens du vent : {
                windDir}\ndescription : {symbolPhrase}\nnébulosité : {cloudiness}\npression : {pressure}\nvisibilité : {visibility}\nProbablement : {precipType}\n\n"
    weather_data_text.configure(state='normal')
    for i in range(len(main_message)):
        weather_data_text.insert(f"{i}.1", main_message[i])
    weather_data_text.configure(state='disabled')
    return main_message

#########################################################


def retrieve_input():
    input = weather_data_text.get("1.0", 'end-1c')
    return input


def send():
    port = 465
    sender_email = "wisdom.pro69@gmail.com"
    password = "fpmqxifyqodvhxnd"
    rec_email = email_add.get()
    msg = EmailMessage()
    msg['Subject'] = 'meteo'
    msg['From'] = sender_email
    msg['To'] = rec_email
    msg.set_content(retrieve_input())
    print("Starting to send")

    with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
        print("connected")
        server.login(sender_email, password)
        print("logged")
        server.send_message(msg)
        print("email sent!")
        showinfo(message="email sent!")


########################################################
root = ttk.Window(themename="superhero")
root.resizable(False, False)
root.iconbitmap('weather.ico')
root.title('CC Master v3.0 by Wisdom')
window_width = 780
window_height = 570
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
#########################################################################
############################################################################
email_add = tk.StringVar()
per = tk.StringVar()
# themes = ttk.
####################################
my_menu = tk.Menu(root)
root.config(menu=my_menu)
theme_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="themes", menu=theme_menu)


def change(theme):
    ttk.Style(theme)


themes = lst.STANDARD_THEMES
for t in themes and themes:
    theme_menu.add_command(label=t, command=lambda t=t: change(t))
####################################
email_label = ttk.Label(root,
                        text="email:",
                        )
email_label.grid(column=0, row=1, padx=10, pady=10)
email_entry = ttk.Entry(root,
                        textvariable=email_add,
                        bootstyle="success",
                        width=40,
                        )
email_entry.focus()
email_entry.grid(column=1, row=1, padx=10, pady=10)
##################
per_label = ttk.Label(root,
                      text="periods:",
                      )
per_label.grid(column=0, row=2, padx=10, pady=10)
per_entry = ttk.Entry(root,
                      textvariable=per,
                      width=5,
                      bootstyle="light"
                      )
per_entry.grid(column=1, row=2, padx=10, pady=10)
#####################
getdata_but = ttk.Button(
    root,
    text="weather",
    width=15,
    command=reformulate,
    bootstyle="light-outline"
)
getdata_but.grid(column=0, row=3, padx=10, sticky="E")
send_but = ttk.Button(
    root,
    text="send",
    width=15,
    command=send,
    bootstyle="success"
)
send_but.grid(column=1, row=3, padx=10, sticky="E")
##################################
weather_data_text = ttk.ScrolledText(root,
                                     width=35,
                                     height=12,
                                     state="disabled",
                                     font=("Gabriola", 17),
                                     )
weather_data_text.grid(column=5, row=1, rowspan=22, sticky="E", pady=10)

############################################################################
root.mainloop()
