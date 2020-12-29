from pypresence import Presence
import time
import epoch
import wmi
import datetime

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

    if "eurotrucks2.exe" in li:
        now = epoch.now()

        RPC.connect()

        RPC.update(state="Driving in Europe", large_image="ets", large_text="RP Mod by MakufonSkifto",
                   small_image="eu", start=now)

        now_datetime = datetime.datetime.now()
        print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: Showing RP")
        time.sleep(15)

    else:
        now_datetime = datetime.datetime.now()
        try:
            RPC.close()
            print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected, closing RP")
        except AttributeError:
            print(f"[INFO {now_datetime.strftime('%H:%M:%S')}]: No running ETS2 detected")

    time.sleep(10)
