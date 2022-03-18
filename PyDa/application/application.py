"""
Comment legend
ᕙ(`-´)ᕗ - Explanation
ʕ•́ᴥ•̀ʔっ - To do
(ㆆ_ㆆ) - Bug
"""
import PySimpleGUI as sg
import pyttsx3


directory = r"C:\Users\Public\Documents\Github\Jarvis\PyDa\application"
sound_on_img = directory + r"\assets\sound_on.png"

# ᕙ(`▿´)ᕗ Text To Speech setup
# engine = pyttsx3.init()

# ʕ•́ᴥ•̀ʔっ Allow the sound to be switched off ʕ•́ᴥ•̀ʔっ
# sound_off_img = directory + r"\assets\sound_off.png"
# sound = True

# def switch_sound_img(event):
#     if sound:
#         sound_img = sound_off_img
#         # sound = False
#     else:
#         sound_img = sound_on_img
#         # sound = True
#     element = window[event]
#     element.update(image_filename=f'{sound_img}', image_subsample=6)


sg.theme('SystemDefault1')  # ᕙ(`▿´)ᕗ Get the specific theme [Light/Dark][Colour][number optional] ᕙ(`▿´)ᕗ
# ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
phillip_image = directory + r"\assets\Phillip_image.png"
layout = [
    [sg.Multiline("Ask me a question :)", justification='center', autoscroll=True, disabled=True, expand_x=True)],
    [sg.Image(f'{phillip_image}', subsample=2)],
    [sg.Text('Enter a command'), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('', image_filename=f'{sound_on_img}',
                                                     image_subsample=6)],

]

window = sg.Window('JARVIS', layout, element_justification='c')  # ᕙ(`▿´)ᕗ Create the Window ᕙ(`▿´)ᕗ

# ᕙ(`▿´)ᕗ Event Loop to process "events" and get the "values" of the inputs ᕙ(`▿´)ᕗ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # ᕙ(`▿´)ᕗ if user closes window or clicks cancel ᕙ(`▿´)ᕗ
        break
    # ʕ•́ᴥ•̀ʔっ Allow the sound to be switched off ʕ•́ᴥ•̀ʔっ
    # if event == '':
        # switch_sound_img(event)

window.close()
