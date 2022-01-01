import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [
    [sg.Text('Text on row 1')],
    [sg.Text('Enter chat here:'), sg.InputText()],
    [sg.Button('Send'), sg.Button('Exit')]
]

window = sg.Window('JankChat v0.0.1', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()