import tkinter as tk

def KeyPress(event):
    print("La touche '%s' a ete presse" % event.keysym)

def KeyRelease(event):
    print("La touche '%s' a ete release" % event.keysym)

def intelWidget(widget):
    console.log(widget)
""" x, y, x_root, y_root
    state,
    keysym, keycode
"""

# def escapeWindow(event):
#     print("{} / {}".format(event.keysym, event.keycode))
#     print(event.widget)
#     event.widget.quit

def closeWindow(event):
    print("la fenetre a ete ferme")
    print(event)

def openWindow():
    top = tk.Toplevel()
    label_w = tk.Label(top, text='Bonjour')
    label_w.bind('<Destroy>', closeWindow)
    #top.bind('<Escape>', closeWindow)
    label_w.pack()

app = tk.Tk()
app.geometry('320x240')

entry_w = tk.Entry(app)
entry_w.bind('<KeyPress>', KeyPress)
entry_w.bind('<KeyRelease>', KeyRelease)
entry_w.pack()

button_w = tk.Button(app, text='Ouvrir une fenetre', command=openWindow)
button_w.pack()


app.bind_class('Entry', '<Double-Button-1>', KeyPress) #double click

app.bind_all('<Double-Button-1>', KeyPress) #double click

app.event_add('<<click>>', '<Button-1>','<Button-2>','<Button-3>')
app.bind('<<click>>', lambda event:
    print('click')
)



app.mainloop()
