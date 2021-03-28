from view import EditorWindow
from model import ObjectsStorage, TextsStorage


class Application(object):
    def __init__(self):
        self.objects_storage = ObjectsStorage()
        self.texts_storage = TextsStorage()
        self.window = EditorWindow(self.objects_storage, self.texts_storage)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    Application().run()
