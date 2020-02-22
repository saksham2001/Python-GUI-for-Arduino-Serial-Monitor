import tkinter as tk
from tkinter import ttk
import serial

LARGE_FONT = ("Verdana", 15)  # 36

count = 0

ser = None

file = None


class app(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)  # shove stuff in use grid for organising

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tk.Tk.wm_title(self, "Arduino Serial")

        self.frames = {}  # Dictionary to store all the frames

        for f in (StartPage, PageOne):

            frame = f(container, self)

            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky="nsew")  # north south east west

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.data = ""

        label = tk.Label(self, text="Arduino Serial Monitor", font=LARGE_FONT)
        label.grid(row=1, column=1)

        port_label = tk.Label(self, text="Port:", font=LARGE_FONT)
        port_label.grid(row=2, column=0)

        port_entry = tk.Entry(self)
        port_entry.grid(row=2,column=1)
        port_entry.insert(10, "COM3")

        baud_label = tk.Label(self, text="Baudrate:", font=LARGE_FONT)
        baud_label.grid(row=3, column=0)

        baud_entry = tk.Entry(self)
        baud_entry.grid(row=3, column=1)
        baud_entry.insert(10, 9600)

        con_button = tk.Button(self, text="Connect", command=lambda: connect(port_entry.get(), baud_entry.get()))  # throwaway function
        con_button.grid(row=4, column=1)

        playback_button = tk.Button(self, text="Playback Data", command=lambda: controller.show_frame(PageOne))
        playback_button.grid(row=5, column=1)

        data_canvas = tk.Frame(self)
        data_canvas.grid(row=1, column=3, rowspan=5, columnspan=4)

        sbar = tk.Scrollbar(data_canvas, orient="vertical")
        sbar.grid(row=1, column=4, sticky="ns")

        self.data_label = tk.Text(data_canvas, font=LARGE_FONT, yscrollcommand=sbar.set, height=10, width=20)
        self.data_label.grid(row=1, column=1)
        self.data_label.grid_propagate(0)

        sbar.config(command=self.data_label.yview)

        self.after(500, self.label_update)

    def label_update(self):
        self.data += get_data()
        self.data_label.insert(tk.END, get_data())
        self.data_label.see("end")
        self.after(500, self.label_update)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Data Playback", font=LARGE_FONT)
        label.grid(pady=10, padx=10, row=1, column=1)

        psbar = ttk.Scrollbar(self, orient="vertical")
        psbar.grid(row=2, column=3, sticky="ns")

        self.text_field = tk.Text(self, font=LARGE_FONT, yscrollcommand=psbar.set, height=5, width=48)
        self.text_field.grid(row=2, column=1)
        self.text_field.propagate(0)

        psbar.config(command=self.text_field.yview)

        update_button = tk.Button(self, text="Update", command=self.update_playback)
        update_button.grid(row=3, column=1)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.grid(row=4, column=1)

    def update_playback(self):
        with open("data.txt", "r") as file:
            data = file.read()
        self.text_field.insert(tk.END, data)
        self.text_field.config(state="disabled")


def connect(port, br):
    global count
    global ser
    global file
    try:
        ser = serial.Serial(port, baudrate=br, timeout=1)
        count = 1
        print("Connected")
        file = open("data.txt", "r+")
    except:
        print("No Board Found")


def get_data():
    global count
    global ser
    global file
    if count > 0:
        alt = ser.readline().decode('ascii')
        file.write(alt)
        return alt
    else:
        return ""


def send_data(data):
    global ser
    global file
    if get_data() == "":
        pass
    else:
        ser.write(data)
        ser.flush()


app1 = app()

app1.mainloop()