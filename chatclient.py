import PySimpleGUI as sg

sg.theme('DarkAmber')

# sets up how the code looks
layout = [
    [sg.Text('Text on row 1')],
    [sg.Text('Enter chat here:'), sg.InputText()],
    [sg.Button('Send'), sg.Button('Exit')]
]

# pops window into existence
window = sg.Window('JankChat v0.0.1', layout)

while True:
    event, values = window.read()       # gets info from window
    if event == sg.WIN_CLOSED or event == 'Exit':
        break       # exit loop if 'x' or exit button clicked
    # HAVE TO ADD the sending and receiving

# closes program after exiting or clicking 'x' out button
window.close()