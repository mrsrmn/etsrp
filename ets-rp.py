from pypresence import Presence

import wmi

import random
import progressbar
import locale

import time
import datetime

import requests
import ujson as json

f = wmi.WMI()

rpc = Presence("793495110440583178")

print("╔════════════════════════════════════════════════════════════════════════════╗\n"
      "║ Welcome to ETSRP v1.8!                                                     ║\n"
      "║                                                                            ║\n"
      "║ ETSRP provides a better version of ETS2's original Discord Rich Presence   ║\n"
      "║                                                                            ║\n"
      "║ Made by MakufonSkifto using pypresence                                     ║\n"
      "║ This may become an actual ETS2 mod soon.                                   ║\n"
      "║ There may be a little ping on the Rich Presence but not too much           ║\n"
      "║                                                                            ║\n"
      "║ If there is a bug in the program or there is a suggestion you want to make,║\n"
      "║ please open an issue at the GitHub repository                              ║\n"
      "╚════════════════════════════════════════════════════════════════════════════╝\n")

locale.setlocale(locale.LC_ALL, "")

now_epoch = int(time.time())  #Epoch time format
now = datetime.datetime.now()

widgets = [f"[INFO {now.strftime('%H:%M:%S')}]: Loading ETSRP: ", progressbar.AnimatedMarker()]
bar = progressbar.ProgressBar(widgets=widgets).start()

for i in range(40):
    time.sleep(0.1)
    bar.update(i)

print(f"\n[INFO {now.strftime('%H:%M:%S')}]: Loaded Program")
rpc.connect()
print(f"\n[INFO {now.strftime('%H:%M:%S')}]: Connecting to Telemetry server")

while True:
    li = []
    for process in f.Win32_Process():
        li.append(process.Name)

    if "eurotrucks2.exe" not in li:
        now_datetime = datetime.datetime.now()
        try:
            response = requests.get(url=f"http://localhost:25555/api/ets2/telemetry")
            info = json.loads(response.content)
            print(f"[ERROR {now_datetime.strftime('%H:%M:%S')}]: Connected")
            print(f"[ERROR {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected, closing program")
            time.sleep(5)
            exit()
        except requests.exceptions.ConnectionError:
            print(f"[WARNING {now_datetime.strftime('%H:%M:%S')}]: Couldn't connect to ETS Telemetry server."
                  f" Please download one for more detailed RP."
                  f" Tutorial on downloading it: https://github.com/Funbit/ets2-telemetry-server#installation")
            print(f"[ERROR {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected, closing program")
            time.sleep(5)
            exit()

    elif "eurotrucks2.exe" in li:
        try:
            response = requests.get(url=f"http://localhost:25555/api/ets2/telemetry")
            info = json.loads(response.content)
        except requests.exceptions.ConnectionError:
            response = None
            info = None

            now_datetime = datetime.datetime.now()
            print(f"[WARNING {now_datetime.strftime('%H:%M:%S')}]: Couldn't connect to ETS Telemetry server."
                  f" Please download one for more detailed RP."
                  f" Tutorial on downloading it: https://github.com/Funbit/ets2-telemetry-server#installation")

        now_datetime = datetime.datetime.now()

        try:
            if round(info['truck']['speed']) != 0 and info['truck']['cruiseControlOn'] is True:
                speed = f"Truck Speed: {round(info['truck']['speed'])} (Cruise Control)"
            elif round(info['truck']['speed']) == 0:
                speed = "Truck Speed: Stopped"
            else:
                speed = f"Truck Speed: {round(info['truck']['speed'])}"
        except TypeError:
            speed = None

        try:
            if info["game"]["paused"] is True:
                text = "Paused / Idle"
                speed = None
            elif info["truck"]["make"] != "" and info["job"]["destinationCity"] != "":
                text = f"Driving with {info['truck']['make']} {info['truck']['model']}" \
                       f" to {info['job']['destinationCity']}"
            elif info["game"]["paused"] is False:
                text = f"Driving with {info['truck']['make']} {info['truck']['model']}"
            else:
                rand = random.choice(["in Europe", "with some Truck", "to a City"])
                text = f"Driving {rand}"

            if info["game"]["paused"] is True:
                dist = None
            elif info["navigation"]["estimatedDistance"] != 0:
                dist = f"Estimated Distance: {round(info['navigation']['estimatedDistance'] / 1000):n}km"
            else:
                dist = None

        except TypeError:
            rand = random.choice(["in Europe", "with some Truck", "to a City"])
            text = f"Driving {rand}"
            dist = None

        rpc.update(state=dist, details=text, large_image="ets", large_text=speed,
                   small_image="eu", small_text="RP Mod by MakufonSkifto", start=now_epoch)

        print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: Showing RP")

    time.sleep(7)
