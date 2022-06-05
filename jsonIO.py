import json
import os

class StaticContentError(Exception):
    pass
class NoContentError(Exception):
    pass

class CLS_JsonReader(object):
    def __init__(self, path=None):
        '''
        a reader can be reused for reading multiple files

        :param path: optional, path to the file to read
        '''
        if path == None:
            return
        self.f = open(path, 'r', encoding='utf-8')
        content = self.f.read()
        # print(content)
        self.jsDict = json.loads(content)
        # print(self.jsDict)
        print("Successfully loaded json from path")
        return

    def get_content(self):
        return self.jsDict

    def reread(self, path: str):
        self.f = open(path, 'r', encoding='utf-8')
        content = self.f.read()
        self.jsDict = json.loads(content)
        print("Successfully reloaded json from path")
        return

    def close(self):
        self.f.close()
    # def setContentByKey(self,key,value):
    #     self.jsDict[key]=value
    #     print(self.jsDict)


class CLS_JsonSaver(object):
    def __init__(self, path: str):
        '''
        a saver is bind to one json file

        :param path: the path to the target json file
        '''
        self.path = path
        self.locked = False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def save_and_lock(self,content):
        self.save_content(content)
        self.lock()
        return

    def save_content(self, content=None):
        if self.locked:
            print("file locked,saving fail")
            return
        else:
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(content, indent=4))
                print("Successfully saved content parameter!")
        return


if __name__ == '__main__':
    print("This is a usage test example:Please reset the Name attribute of the changed file after running");
    metapath = "./Charts/StillAlive/meta.json"
    loader = CLS_JsonReader(metapath)
    content = loader.get_content()
    content["Name"] = "StillAlive"
    saver = CLS_JsonSaver(metapath)
    saver.save_content(content)
