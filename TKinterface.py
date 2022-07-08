from tkinter import *
from tkinter import ttk

from Managers import CLS_ChartManager, CLS_DataManager


class CLS_AddNote(object):
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
        self.root.bind("<Return>", self.add_note_to_noteList)
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

    def note_info_check(self):
        if self.noteType.get() == "flick":
            self.timeLengthBeat.set(0)

class CLS_DelNote(object):
    def __init__(self, chartManager: CLS_ChartManager):
        self.chartManager = chartManager
        version = "v0.1"
        self.root = Tk()
        self.root.title("MUNECK Node Editor" + version)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.noteFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.noteFrame.grid(column=1, row=1, columnspan=8, rowspan=9, sticky=(N, W, E, S))

        self.id = IntVar()
        ttk.Label(self.noteFrame, text="删除NOTE编号(NoteID to be deleted):").grid(row=5, column=1, rowspan=1, columnspan=2)
        ttk.Entry(self.noteFrame, textvariable=self.id).grid(row=5, column=3, rowspan=1, columnspan=4)
        # button add and save
        add_btn = ttk.Button(self.noteFrame, text="DEL", command=self.deleteNote)
        add_btn.grid(row=8, column=2, rowspan=2, columnspan=3)
        self.root.bind("<Return>", self.deleteNote)
        self.root.mainloop()
        
    def deleteNote(self, *args):
        self.chartManager.delete_note(self.id.get())
        self.root.destroy()

class CLS_ModNote(object):
    def __init__(self, chartManager: CLS_ChartManager):
        self.chartManager = chartManager
        version = "v0.1"
        self.root = Tk()
        self.root.title("MUNECK Node Editor" + version)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.noteFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.noteFrame.grid(column=1, row=1, columnspan=8, rowspan=9, sticky=(N, W, E, S))

        #noteID /label/entry
        self.id = IntVar()
        ttk.Label(self.noteFrame, text="更改NOTE编号(NoteID to be modified):").grid(row=2, column=1, rowspan=1, columnspan=2)
        ttk.Entry(self.noteFrame, textvariable=self.id).grid(row=2, column=3, rowspan=1, columnspan=2)
        btn = ttk.Button(self.noteFrame, text="Confirm", 
        command=lambda: self.getNote(self.id.get()))
        btn.grid(row=2, column=5, rowspan=1, columnspan=2)
        # note type /radioButton
        self.noteType = StringVar()
        self.noteType.set('flick')
        type_flick = ttk.Radiobutton(self.noteFrame, text='Flick', variable=self.noteType, value='flick')
        type_flick.grid(row=3, column=1, rowspan=1, columnspan=2)
        type_hold = ttk.Radiobutton(self.noteFrame, text='Hold', variable=self.noteType, value='hold')
        type_hold.grid(row=3, column=2, rowspan=1, columnspan=2)
        type_avoid = ttk.Radiobutton(self.noteFrame, text='Avoid', variable=self.noteType, value='avoid')
        type_avoid.grid(row=3, column=3, rowspan=1, columnspan=2)

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
        add_btn = ttk.Button(self.noteFrame, text="MOD", command=self.modifyNote)
        add_btn.grid(row=8, column=2, rowspan=2, columnspan=3)
        self.root.bind("<Return>", self.modifyNote)
        self.root.mainloop()

    def modifyNote(self, *args):
        self.note_info_check()
        self.chartManager.modify_note(self.id.get(), None, self.noteType.get(), self.rail.get(), self.startBeat.get()
                                    , self.touchBeat.get(), self.timeLengthBeat.get())

    def getNote(self, num):
        info = self.chartManager.noteList[num - 1].get_info()
        self.noteType.set(info[0])
        self.rail.set(info[1])
        self.startBeat.set(info[2])
        self.touchBeat.set(info[3])
        self.timeLengthBeat.set(info[4])

    def note_info_check(self):
        if self.noteType.get() == "flick":
            self.timeLengthBeat.set(0)

class CLS_AdjOffset(object):
    def __init__(self, chartManager: CLS_ChartManager):
        self.chartManager = chartManager
        version = "v0.1"
        self.root = Tk()
        self.root.title("MUNECK Node Editor" + version)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.noteFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.noteFrame.grid(column=1, row=1, columnspan=8, rowspan=9, sticky=(N, W, E, S))

        self.offset = IntVar()
        ttk.Label(self.noteFrame, text="偏移值(Offset) in seconds:").grid(row=5, column=1, rowspan=1, columnspan=2)
        ttk.Entry(self.noteFrame, textvariable=self.offset).grid(row=5, column=3, rowspan=1, columnspan=4)
        # button add and save
        add_btn = ttk.Button(self.noteFrame, text="ADJ", command=self.adjOffset)
        add_btn.grid(row=8, column=2, rowspan=2, columnspan=3)
        self.root.bind("<Return>", self.adjOffset)
        self.root.mainloop()
        
    def adjOffset(self, *args):
        self.chartManager.startOffset = self.offset.get()

class CLS_ChooseDifficulty(object):
    def __init__(self, dataManager: CLS_DataManager):
        self.dataManager = dataManager
        self.difficultyNames = []
        for difficulty in self.dataManager.metadata["Difficulties"]:
            dname = difficulty["DifficultyName"]
            self.difficultyNames.append(dname)

        version = "v0.1"
        self.root = Tk()
        self.root.title("MUNECK Node Editor" + version)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # self.noteFrame = ttk.Frame(self.root, padding="3 3 12 12")
        # self.noteFrame.grid(column=10, row=10, columnspan=8, rowspan=9, sticky=(N, W, E, S))

        # self.offset = IntVar()
        # ttk.Label(self.noteFrame, text="偏移值(Offset) in seconds:").grid(row=5, column=1, rowspan=1, columnspan=2)
        # ttk.Entry(self.noteFrame, textvariable=self.offset).grid(row=5, column=3, rowspan=1, columnspan=4)
        # # button add and save
        
        self.difficulty = StringVar()
        combobox = ttk.Combobox(self.root, textvariable = self.difficulty)
        combobox['value'] = tuple(self.difficultyNames)
        combobox['state'] = "readonly"
        combobox.current(0)
        combobox.grid(column = 1, row = 1)
        # combobox.bind("<<ComboboxSelected>>", self.getDifficultyName)
        button = ttk.Button(self.root, text='confirm', command=self.quit)
        button.grid(row=1, column=2)
        # btn = ttk.Button(self.noteFrame, text="Confirm", command=self.getDifficultyName())
        # btn.grid(row=8, column=2, rowspan=2, columnspan=3)
        # self.root.bind("<Return>", self.adjOffset)
        self.root.mainloop()
        
    def quit(self, *args):
        self.root.destroy()