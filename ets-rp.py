from pypresence import Presence
import wmi
import random

import time
import epoch
import datetime

import requests
import ujson as json

f = wmi.WMI()
RPC = Presence("793495110440583178")

print("╔════════════════════════════════════════════════════════════════════════════╗\n"
      "║ Welcome to ETSRP v1.2!                                                     ║\n"
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

while True:
    li = []
    for process in f.Win32_Process():
        li.append(process.Name)

    response = requests.get(url="http://169.254.50.214:25555/api/ets2/telemetry")
    info = json.loads(response.content)

    if "eurotrucks2.exe" in li:

        now = epoch.now()
        RPC.connect()

        if info["game"]["paused"] is True:
            text = "Paused / Idle"
        elif info["game"]["paused"] is False and info["truck"]["make"] != "":
            text = f"Driving with {info['truck']['make']} {info['truck']['model']}"
        elif info["game"]["paused"] is False and info["truck"]["make"] != "" and info["job"]["destinationCity"] != "":
            text = f"Driving with {info['truck']['make']} {info['truck']['model']} to {info['job']['destinationCity']}"
        else:
            rand = random.choice(["in Europe", "with some Truck", "to a City"])
            text = f"Driving {rand}"

        RPC.update(state=text, large_image="ets", large_text="RP Mod by MakufonSkifto",
                   small_image="eu", start=now)

        now_datetime = datetime.datetime.now()
        print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: Showing RP")
        time.sleep(5)

    else:
        now_datetime = datetime.datetime.now()
        try:
            RPC.close()
            print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected, closing RP")
        except AttributeError:
            print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected")

    time.sleep(5)
