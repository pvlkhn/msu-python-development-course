import tkinter
from controller import ObjectsViewController

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
def get_master():
    return tkinter.Tk()


class EditorWindow(tkinter.Frame):
    def __init__(self, master=get_master()):
        super().__init__(master=master)
        self.left_part = TextView()
        self.left_part.grid(row=0, column=0)

        self.right_part = ObjectsView()
        self.right_part.grid(row=0, column=1)


class TextView(tkinter.Text):
    def __init__(self, master=get_master()):
        super().__init__(master=master)


class ObjectsView(tkinter.Canvas):
    def __init__(self, master=get_master()):
        super().__init__(master=master)
        self.stored_objects = []

        controller = ObjectsViewController(stored_objects=self.stored_objects, redraw_callback=self.redraw)
        self.bind("<Button-1>", controller.on_click)

    def redraw(self):
        print(self.stored_objects)