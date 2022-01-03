import PySimpleGUI as sg
import socket
from threading import Thread
from PySimpleGUI.PySimpleGUI import InputText

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

sg.theme('DarkAmber')

# global variable to be used for containing the chat
chatbox = """
Type something out and press \'Send\' to send a message!
"""

# sets up how the code looks
layout = [
    [sg.Text('Text on row 1', size=(200, 40))],
    [sg.Text('Enter chat here:'), sg.InputText()],
    [sg.Button('Send'), sg.Button('Exit')]
]

# pops window into existence
window = sg.Window('JankChat v0.0.1', layout)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receiving():
    while True:
        try:
            data = s.recv(1024)
        except:
            break
        if not data:
            break
        else:
            print(data.decode("utf-8"))



close = False
s.connect((HOST, PORT))
th = [Thread(target=receiving).start()]
while True:
    event, values = window.read(timeout=50)  # gets info from window
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()  # closes program after exiting or clicking 'x' out button
        s.close()
        break  # exit loop if 'x' or exit button clicked
    if event == 'Send':
        s.send(values[0].encode())  # sends encoded messages
    





