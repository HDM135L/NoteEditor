from typing import List, Any

from jsonIO import CLS_JsonReader, CLS_JsonSaver
import os


class CLS_Note(object):
    def __init__(self, noteinfo: dict, bpm, offset):
        # self.idx = -1
        self.bpm, self.offset = bpm, offset
        if noteinfo is None:
            return
        # self.noteinfo = noteinfo
        # notetest = dict(Type="test", Rail=-2, Length=0.0, StartTime=1.0, DelayTime=2.0)
        self.type = noteinfo["Type"]
        self.rail = noteinfo["Rail"]
        self.timeLengthBeat = self.time2beat(noteinfo["Length"])
        self.spawnBeat = self.time2beat(noteinfo["StartTime"] - noteinfo["DelayTime"])
        self.touchBeat = self.time2beat(noteinfo["StartTime"])

    def time2beat(self, time):
        return (time - self.offset) * self.bpm / 60

    def beat2time(self, beat):
        return self.offset + beat / self.bpm * 60

    def get_info(self):
        st = self.beat2time(self.touchBeat)
        dt = st - self.beat2time(self.spawnBeat)
        tl = self.beat2time(self.timeLengthBeat) - self.offset
        return dict(Type=self.type, Rail=self.rail, Length=tl, StartTime=st, DelayTime=dt)


class CLS_ChartManager(CLS_JsonSaver):
    noteList: List[CLS_Note]

    def __init__(self, path):
        super(CLS_ChartManager, self).__init__(path)
        reader = CLS_JsonReader(path)

        self.chartData = reader.get_content()
        self.chartPath = path
        self.bpm = 120  # NOTE: This is a test bpm, bind to tk variable
        self.startOffset = 0

        self.noteList = []
        self.noteNum = self.chartData["NoteNum"]
        self.load_all_notes()

    def save_chart(self):  # NOTE: API function (external use)
        """
        save all current existing note into chart data.
        (Export API)
        """
        self.chartData["NoteNum"] = self.noteNum
        newChartData = [0] * self.noteNum
        for idx in range(self.noteNum):
            newChartData[idx] = self.noteList[idx].get_info()
        self.chartData["NoteList"] = newChartData
        self.save_content(self.chartData)
        print("successfully saved current noteList")

    def create_note(self, noteinfo=None, Type=None, Rail=None, SpawnBeat=None, TouchBeat=None,
                    TimeLengthBeat=None):  # NOTE: API function (external use)
        """
        construct a new note and add to self.noteList.
        (Export API)

        :param noteinfo: create note with a dict of std noteinfo, if None, need the following 5 variables to construct a new note.
        """
        # create note in either way
        if noteinfo:
            newnote = CLS_Note(noteinfo, self.bpm, self.startOffset)
        else:
            newnote = CLS_Note(None, self.bpm, self.startOffset)
            newnote.type, newnote.rail = Type, Rail
            newnote.spawnBeat, newnote.touchBeat, newnote.timeLengthBeat = SpawnBeat, TouchBeat, TimeLengthBeat
        self.add_note(newnote)
        print("successfully add note to noteList,remember to save it to json!")
        return

    def add_note(self, note: CLS_Note):
        # note.idx = self.noteNum
        self.noteNum += 1
        self.noteList.append(note)

    def load_all_notes(self):
        idx = 0
        self.noteList = [0] * self.chartData["NoteNum"]
        for noteInfo in self.chartData["NoteList"]:
            self.noteList[idx] = CLS_Note(noteInfo, self.bpm, self.startOffset)
            # self.noteList[idx].idx = idx
            idx += 1
        return


class CLS_DataManager(object):
    def __init__(self, rootpath):
        """
        Manage all json data of a song.
        :param rootpath: the root directory path, should be ./Charts/SongName
        """
        self.rootpath = rootpath
        reader = CLS_JsonReader()
        # get metadata
        self.metapath = os.path.join(rootpath, "meta.json")
        reader.reread(self.metapath)
        self.metadata = reader.get_content()
        self.meta_saver = CLS_JsonSaver(self.metapath)

        # get charts
        self.chartManagers = {}  # difficulty name to CLS_ChartManager instance
        for difficulty in self.metadata["Difficulties"]:
            dname = difficulty["DifficultyName"]
            chart_identifier = "chart" + str(difficulty["Difficulty"]) + ".json"
            chartpath = os.path.join(rootpath, chart_identifier)

            self.chartManagers[dname] = CLS_ChartManager(chartpath)

        reader.close()

    def save_all_data(self):
        '''
        should not be used when lock feature is used.
        :return:
        '''
        self.save_meta()
        for CM in self.chartManagers:
            CM.save_chart()
        print(f"Saving complete.Saved meta and {len(self.chartManagers)} charts")
        return

    def save_meta(self):
        self.meta_saver.save_content(self.metadata)

    def save_chart_by_difficulty(self, difficulty):
        self.chartManagers[difficulty].save_chart()


if __name__ == "__main__":
    DM = CLS_DataManager("./Charts/StillAlive")
    CM = DM.chartManagers["Easy"]

    # change note
    print(CM.noteList[0].get_info())
    CM.noteList[0].spawnBeat -= 1
    print(CM.noteList[0].get_info())

    # add note
    # notetest = dict(Type="test", Rail=-2, Length=0.0, StartTime=1.0, DelayTime=2.0)
    # CM.add_note(notetest)

    # save all
    CM.save_chart()

# TODO:
#  need to rearrange json by ascending StartTime.
#  delete node option
#  can add difficulty and corresponding chart file
