import wolframalpha as wa
import PySimpleGUI as sg
import wikipedia as wp

# ᕙ(`▿´)ᕗ Connect to wolfram ᕙ(`▿´)ᕗ
app_id = 'QW82JW-Q5U44TYEE9'  # get your own at https://products.wolframalpha.com/api/
client = wa.Client(app_id)


sg.theme('DarkBlack1')   # ᕙ(`▿´)ᕗ Get the specific theme [Light/Dark][Colour][number optional] ᕙ(`▿´)ᕗ

# ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
layout = [
            [sg.Text('Enter a command'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')]
]

window = sg.Window('JARVIS', layout) # ᕙ(`▿´)ᕗ Create the Window ᕙ(`▿´)ᕗ

# ᕙ(`▿´)ᕗ Event Loop to process "events" and get the "values" of the inputs ᕙ(`▿´)ᕗ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # ᕙ(`▿´)ᕗ if user closes window or clicks cancel ᕙ(`▿´)ᕗ
        break

    print('You entered ', values[0]) # ᕙ(`▿´)ᕗ Print input ᕙ(`▿´)ᕗ
    res = client.query(values[0])
    
    wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
    wiki_res = wp.summary(values[0],sentences=3)
    sg.Popup("Wolfram Result: " + wolfram_res, "Wikipedia Result: " + wiki_res)

window.close()

