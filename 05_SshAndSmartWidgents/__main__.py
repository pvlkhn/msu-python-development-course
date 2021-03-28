from view import EditorWindow
from model import ObjectsStorage, TextsStorage
import tkinter


class Application(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.objects_storage = ObjectsStorage()
        self.texts_storage = TextsStorage()

        self.title("Minimalistic oval redactor")
        self.minsize(800, 600)

        window = EditorWindow(self.objects_storage, self.texts_storage, master=self)
        window.grid(sticky="NWSE")


if __name__ == '__main__':
    Application().mainloop()
