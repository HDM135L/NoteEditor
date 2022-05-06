import json
import os


class CLS_JsonReader(object):
    def __init__(self, path: str):
        self.f = open(path, 'r', encoding='utf-8')
        content = self.f.read()
        # print(content)
        self.jsDict = json.loads(content)
        # print(self.jsDict)
        print("Successfully loaded json from path")
        return

    def get_content(self):
        return self.jsDict

    # def setContentByKey(self,key,value):
    #     self.jsDict[key]=value
    #     print(self.jsDict)


class CLS_JsonSaver(object):
    def __init__(self, path: str, content: dict = ""):
        self.content = content
        self.path = path
        return

    def update_content(self, content):
        self.content = content
        return

    def save_content(self,content=None):
        if content:
            self.content = content
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.content, indent=4))
            print("Successfully saved!")
        return


if __name__ == '__main__':
    print("This is a usage test example:Please reset the Name attribute of the changed file after running");
    metapath = "./Charts/StillAlive/meta.json"
    loader = CLS_JsonReader(metapath)
    content = loader.get_content()
    content["Name"]="Still Alive"
    saver = CLS_JsonSaver(metapath,content)
    saver.save_content()
