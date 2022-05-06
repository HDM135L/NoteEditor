from Managers import CLS_DataManager
from TKinterface import CLS_NoteEditor

if __name__ == "__main__":
    DM = CLS_DataManager("./Charts/StillAlive")
    CM = DM.chartManagers["Easy"]
    CLS_NoteEditor(CM)