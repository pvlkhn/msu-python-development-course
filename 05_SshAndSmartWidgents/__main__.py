from view import EditorWindow
from model import ObjectsStorage

class Application(object):
    def __init__(self):
        self.objects_storage = ObjectsStorage()
        self.window = EditorWindow(self.objects_storage)


    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    Application().run()
