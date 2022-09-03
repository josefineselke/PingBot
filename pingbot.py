#works with windows, linux and macOS

import PySimpleGUI as sg
import re
import subprocess
import platform
import time


def ping(host):
    #returns True if host is reachable, else False

    parameter = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    need_new_shell = False if platform.system().lower() == "windows" else True
    command = "ping " + parameter + " " + host

    return subprocess.call(command, shell=need_new_shell) == 0



if __name__ == "__main__":

    sg.theme("DarkGrey1")
    column1 = [
        [
            sg.Text("IP-Address")
        ],
        [
            sg.Text("Time")
        ],
        [
            sg.Text("Ping Count")
        ],
        [
            sg.Text("")
        ],
    ]

    column2 = [
        [
            sg.In(size=(25, 1), key="IP")
        ],
        [
            sg.In(size=(25, 1), key="TIME", default_text="1")
        ],
        [
            sg.Text("0", key="COUNT")
        ],
        [
            sg.Button("Start", enable_events=True, key="START"),
            sg.Button("Close", enable_events=True, key="CLOSE")
        ]
    ]

    window = sg.Window("Pingbot", [[sg.Column(column1), sg.Column(column2)]])

    while True:
        event, value = window.read()
        if event == "CLOSE" or event == sg.WIN_CLOSED:
            break

        elif event == "START":
            window["START"].update(disabled=True)
            #we need to test if the IP address is a valid number
            REGEX_IPV4 = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            if not re.match(REGEX_IPV4, value["IP"]):
                sg.PopupError("No valid IP address, please try again!")
                continue

            #Timer needs to be an integer between 1 and 1000
            try:
                times = int(value["TIME"])
                if times not in range(1, 1000):
                    sg.PopupError("Time parameter not in accepted range, try again!")
                    continue
            except ValueError:
                sg.PopupError("Time parameter not int, try again!")
                continue

            for j in range(times):
                if not ping(value["IP"]):
                    window["COUNT"].update(j+1)
                    window.refresh()
                    time.sleep(5)
                    continue
                else:
                    sg.Popup("The Server is available!")
                    break

        window["START"].update(disabled=False)

    window.close()
