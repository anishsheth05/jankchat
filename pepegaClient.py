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
msgd = False

# sets up how the code looks
layout = [
    [sg.Text(chatbox, size=(200, 40), key='Text')],
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
            incoming = data.decode("utf-8")
            print(incoming)
            global chatbox  # basically saying we want the global chatbox
            print(chatbox.count('\n'))
            if chatbox.count('\n') > 38:
                print('whyyyyyyy')
                lines = chatbox.splitlines()
                lines = lines[2:]
                lines.append('\n')
                lines.append(incoming + '\n')
                chatbox = str(lines)
            else:
                chatbox += '\n' + incoming + '\n'   # adding a newline to it



close = False
s.connect((HOST, PORT))
th = [Thread(target=receiving, args=()).start()]
while True:
    event, values = window.read(timeout=50)  # gets info from window
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()  # closes program after exiting or clicking 'x' out button
        s.close()
        break  # exit loop if 'x' or exit button clicked
    if event == 'Send':
        s.send(values[0].encode())  # sends encoded messages
        values[0] = ''      # trying to clear input after sending msg
        window.ding()
    textbox = window['Text']
    textbox.update(chatbox)
    





