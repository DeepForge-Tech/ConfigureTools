import argparse
import os
from pathlib import Path

class ConfigureProject():
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.parrent_dir = os.path.abspath(os.path.join(self.current_dir, os.pardir))
        print(self.parrent_dir)
        self.project = ""
        self.projects = ["Gliese","DeepForge-Toolset"]
        self.types_library = ["shared","static"]
        self.dependencies_project = {
            "Gliese": [
                "fmt/11.0.2",
                "andreasbuhr-cppcoro/cci.20230629",
                "jsoncpp/1.9.5",
                "openssl/3.3.1","zlib/1.3.1"
            ]
        }
    
    def printMenu(self,menu) -> None:
        if type(menu) == dict:
            for number,value in menu.items():
                print(number + 1,value,sep=". ")
        elif type(menu) == list:
            for value in menu:
                print(value)
    
    def validate(self,answer,lenth = None,target = None) -> bool:
        if lenth != None:
            return 0 < len(answer) <= lenth
        elif target != None:
            if type(answer) == list:
                target = [value.upper() for value in target]
                return answer in target
            elif type(answer) == dict:
                for key,value in target.items():
                    if answer == str(value).lower():
                        return True
        return False
    
    def writeDependencies(self):
        file = open(os.path.join(self.parrent_dir,"ConanLibraries.txt"), "w")
        content = ""
        for library in self.dependencies_project[self.project]:
            content += library + f":{self.type_library}\n"
        file.write(content)
        file.close()

    def start(self):
        if args.project and args.project in self.projects:
            self.project = args.project
        else:
            menu = dict(enumerate(self.projects))
            self.printMenu(menu)
            while True:
                answer = input("\33[32m==> Change project:\033[0m")
                check = self.validate(answer,len(self.projects))
                if check == True:
                    self.project = menu[int(answer) - 1]
                    break
                else:
                    print("\33[31m==> Invalid answer!\033[0m")

        if args.type_library and args.type_library in self.types_library:
            self.type_library = args.type_library
        else:
            menu = dict(enumerate(self.types_library))
            self.printMenu(menu)
            while True:
                answer = input("\33[32m==> Change type library:\033[0m")
                check = self.validate(answer,len(self.types_library))
                if check == True:
                    self.type_library = menu[int(answer) - 1]
                    break
                else:
                    print("\33[31m==> Invalid answer!\033[0m")
        self.writeDependencies()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-type_library",'--type_library', type=str, help='Type library (static or shared)',required=False)
    parser.add_argument('-project','--project', type=str, help='Project for configure',required=False)
    args = parser.parse_args()
    util = ConfigureProject()
    util.start()