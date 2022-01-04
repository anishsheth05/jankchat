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
    [sg.Multiline(chatbox, size=(200, 40), key='Text', autoscroll=True,
                  focus=False, disabled=True)],
    [sg.Text('Enter chat here:'), sg.Input(do_not_clear=True, key='Input', size = (185, 1))],
    [sg.Button('Send'), sg.Button('Exit')]
]

# pops window into existence
window = sg.Window('JankChat v0.0.1', layout)
window.read(timeout=50)
textbox = window['Text']
inputbox = window['Input']
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
            global chatbox  # basically saying we want the global chatbox
            chatbox += '\n' + incoming + '\n'   # adding a newline to it
            textbox.update(chatbox)
            inputbox.update('')


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
        msg: str = values['Input']
        if msg[:1] == '/':  # detects commands
            if msg[1:9] == 'piglatin':  # handles piglatin translation
                words = msg[10:].split(sep=' ')
                for i in range(0, len(words)):
                    word = words[i]
                    if word[0:1] == 'a' or word[0:1] == 'e' or word[0:1] == 'i' \
                       or word[0:1] == 'o' or word[0:1] == 'u' or word[0:1] == 'A' \
                       or word[0:1] == 'E' or word[0:1] == 'I' or word[0:1] == 'O' \
                       or word[0:1] == 'U':
                        words[i] = words[i] + 'yay '
                    elif word[0:1] == 'y' or word[0:1] == 'Y':
                        words[i] = words[i][1:] + words[i][0:1] + 'ay'
                    else:
                        vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y']
                        first_vowel: int = None
                        for vowel in vowels:
                            index = word.find(vowel)
                            if index == -1:
                                continue
                            if first_vowel is None:
                                first_vowel = word.find(vowel)
                            else:
                                first_vowel = min(word.find(vowel), first_vowel)
                        words[i] = words[i][first_vowel:] + words[i][0:first_vowel] + 'ay '
                msg = ''.join(words)
                s.send(msg.encode())
            else:
                s.send(msg.encode())    # sends unrecognized commands to server
        else:
            s.send(msg.encode())  # sends encoded messages
        window.ding()
    