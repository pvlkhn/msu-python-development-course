from view import EditorWindow
from model import ObjectsStorage, TextsStorage
import tkinter


class Application(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, minsize=600)

        self.objects_storage = ObjectsStorage()
        self.texts_storage = TextsStorage()
        self.window = EditorWindow(self.objects_storage, self.texts_storage, master=self)
        self.title("Minimalistic oval redactor")
        self.minsize(800, 600)


if __name__ == '__main__':
    Application().mainloop()
