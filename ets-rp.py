from pypresence import Presence

import wmi
import socket

import random

import time
import epoch
import datetime

import requests
import ujson as json

f = wmi.WMI()

rpc = Presence("793495110440583178")
rpc.connect()

print("╔════════════════════════════════════════════════════════════════════════════╗\n"
      "║ Welcome to ETSRP v1.5!                                                     ║\n"
      "║                                                                            ║\n"
      "║ ETSRP provides a better version of ETS2's original Discord Rich Presence   ║\n"
      "║                                                                            ║\n"
      "║ Made by MakufonSkifto using pypresence                                     ║\n"
      "║ This may become an actual ETS2 mod soon.                                   ║\n"
      "║ There may be a little ping on the Rich Presence but not too much           ║\n"
      "║                                                                            ║\n"
      "║ If there is a bug in the program, please open an issue at the GitHub       ║\n"
      "║ repository                                                                 ║\n"
      "╚════════════════════════════════════════════════════════════════════════════╝\n")

now = datetime.datetime.now()
print(f"[INFO {now.strftime('%H:%M:%S')}]: Launching Program | Press CTRL + C to exit")
print(f"[INFO {now.strftime('%H:%M:%S')}]: Connecting to Telemetry server")

while True:
    li = []
    now_epoch = epoch.now()
    for process in f.Win32_Process():
        li.append(process.Name)

    if "eurotrucks2.exe" in li:

        try:
            response = requests.get(url=f"http://{socket.gethostbyname(socket.gethostname())}:25555/api/ets2/telemetry")
            info = json.loads(response.content)
        except requests.exceptions.ConnectionError:
            response = None
            info = None

            now_datetime = datetime.datetime.now()
            print(f"[WARNING {now_datetime.strftime('%H:%M:%S')}]: No open ETS Telemetry server found."
                  f" Please download one for more detailed RP."
                  f" Tutorial on downloading it: https://github.com/Funbit/ets2-telemetry-server#installation")

        now_datetime = datetime.datetime.now()

        try:
            if round(info['truck']['speed']) == 0:
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

        except TypeError:
            rand = random.choice(["in Europe", "with some Truck", "to a City"])
            text = f"Driving {rand}"

        rpc.update(state=text, large_image="ets", large_text=speed,
                   small_image="eu", small_text="RP Mod by MakufonSkifto", start=now_epoch)

        print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: Showing RP")

    else:
        now_datetime = datetime.datetime.now()
        try:
            rpc.close()
            print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected, closing RP")
        except AttributeError:
            print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected")

    time.sleep(7)
