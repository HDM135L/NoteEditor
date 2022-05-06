from jsonIO import CLS_JsonReader,CLS_JsonSaver
import os

class CLS_ChartManager(CLS_JsonSaver):
    def __init__(self,path):
        super(CLS_ChartManager, self).__init__(path)
        reader = CLS_JsonReader(path)

        self.chartData = reader.get_content()
        self.chartPath = path

    def save_chart(self):
        self.save_content(self.chartData)

    def add_note(self,noteDict):
        self.chartData["NoteNum"]+=1
        self.chartData["NoteList"].append(noteDict)

class CLS_DataManager(object):
    def __init__(self, rootpath):
        """
        Manage all json data of a song.
        :param rootpath: the root directory path, should be ./Charts/SongName
        """
        self.rootpath = rootpath
        reader = CLS_JsonReader()
        #get metadata
        self.metapath = os.path.join(rootpath, "meta.json")
        reader.reread(self.metapath)
        self.metadata = reader.get_content()
        self.meta_saver = CLS_JsonSaver(self.metapath)

        #get charts
        self.chartManagers = {} #difficulty name to CLS_ChartManager instance
        for difficulty in self.metadata["Difficulties"]:
            dname = difficulty["DifficultyName"]
            chart_identifier = "chart"+ str(difficulty["Difficulty"])+".json"
            chartpath = os.path.join(rootpath, chart_identifier)

            self.chartManagers[dname] = CLS_ChartManager(chartpath)

        reader.close()

    def save_all(self):
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
    notetest = dict(Type="test", Rail=-2, Length=0.0, StartTime=1.0, DelayTime=2.0)
    CM.add_note(notetest)
    CM.save_chart()

# TODO:
#  need to rearrange json by ascending StartTime.
#  delete node option
#  add difficulty
#  add chart file