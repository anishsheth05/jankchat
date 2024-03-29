import PySimpleGUI as sg
import socket

from PySimpleGUI.PySimpleGUI import InputText

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

sg.theme('DarkAmber')

# sets up how the code looks
layout = [
    [sg.Text('Text on row 1')],
    [sg.Text('Enter chat here:'), sg.InputText()],
    [sg.Button('Send'), sg.Button('Exit')]
]

# pops window into existence
window = sg.Window('JankChat v0.0.1', layout)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.send(b'hello world') 
    while True:
        event, values = window.read(timeout=50)       # gets info from window
        if event == sg.WIN_CLOSED or event == 'Exit':
            break       # exit loop if 'x' or exit button clicked
        if event == 'Send':
            s.send(values[0].encode())  # sends encoded messages
        data = s.recv(1024)
        print('Received', repr(data))

# closes program after exiting or clicking 'x' out button
window.close()
