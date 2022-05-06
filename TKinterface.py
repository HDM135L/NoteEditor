from tkinter import *
from tkinter import ttk

from Managers import CLS_ChartManager, CLS_DataManager


class CLS_NoteEditor(object):
    def __init__(self, chartManager: CLS_ChartManager):
        self.chartManager = chartManager
        version = "v0.1"
        self.root = Tk()
        self.root.title("MUNECK Node Editor" + version)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.noteFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.noteFrame.grid(column=1, row=1, columnspan=8, rowspan=9, sticky=(N, W, E, S))
        # note type /radioButton
        self.noteType = StringVar()
        self.noteType.set('flick')
        type_flick = ttk.Radiobutton(self.noteFrame, text='Flick', variable=self.noteType, value='flick')
        type_flick.grid(row=2, column=1, rowspan=1, columnspan=2)
        type_hold = ttk.Radiobutton(self.noteFrame, text='Hold', variable=self.noteType, value='hold')
        type_hold.grid(row=2, column=2, rowspan=1, columnspan=2)
        type_avoid = ttk.Radiobutton(self.noteFrame, text='Avoid', variable=self.noteType, value='avoid')
        type_avoid.grid(row=2, column=3, rowspan=1, columnspan=2)

        # rail /label/radioButton
        ttk.Label(self.noteFrame, text='轨道(Rail):').grid(row=4, column=1, rowspan=1, columnspan=2)
        self.rail = IntVar()
        for i in range(-2, 3):
            rbtn = ttk.Radiobutton(self.noteFrame, text=str(i), variable=self.rail, value=i)
            rbtn.grid(row=4, column=5 + i, rowspan=1, columnspan=1)

        # NoteInfo /label/Entry
        self.startBeat = DoubleVar()
        self.touchBeat = DoubleVar()
        self.timeLengthBeat = DoubleVar()
        ttk.Label(self.noteFrame, text="生成拍子(SpawnBeat):").grid(row=5, column=1, rowspan=1, columnspan=2)
        ttk.Entry(self.noteFrame, textvariable=self.startBeat).grid(row=5, column=3, rowspan=1, columnspan=4)
        ttk.Label(self.noteFrame, text="触线拍子(TouchBeat):").grid(row=6, column=1, rowspan=1, columnspan=2)
        ttk.Entry(self.noteFrame, textvariable=self.touchBeat).grid(row=6, column=3, rowspan=1, columnspan=4)
        ttk.Label(self.noteFrame, text="时间长度(TimeLengthBeat):").grid(row=7, column=1, rowspan=1, columnspan=2)
        ttk.Entry(self.noteFrame, textvariable=self.timeLengthBeat).grid(row=7, column=3, rowspan=1, columnspan=4)
        # button add and save
        add_btn = ttk.Button(self.noteFrame, text="ADD", command=self.add_note_to_noteList)
        add_btn.grid(row=8, column=2, rowspan=2, columnspan=3)
        save_btn = ttk.Button(self.noteFrame, text="SAVE", command=self.save_current_notes_to_data)
        save_btn.grid(row=8, column=5, rowspan=2, columnspan=3)
        self.root.bind("<space>", self.add_note_to_noteList)
        self.root.bind("<Return>", self.save_current_notes_to_data)
        self.root.mainloop()

    def add_note_to_noteList(self, *args):
        self.note_info_check()
        print("add note:")
        print("Type: " + self.noteType.get())
        print("Rail: " + str(self.rail.get()))
        print("start beat: " + str(self.startBeat.get()))
        print("touch Beat: " + str(self.touchBeat.get()))
        print("time length Beat: " + str(self.timeLengthBeat.get()))
        self.chartManager.create_note(None, self.noteType.get(), self.rail.get(), self.startBeat.get()
                                      , self.touchBeat.get(), self.timeLengthBeat.get())

    def save_current_notes_to_data(self):
        self.chartManager.save_chart()

    def note_info_check(self):
        if self.noteType.get() == "flick":
            self.timeLengthBeat.set(0)


if __name__ == "__main__":
    DM = CLS_DataManager("./Charts/StillAlive")
    CM = DM.chartManagers["Easy"]
    CLS_NoteEditor(CM)
"""
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()
"""
