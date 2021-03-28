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
    def __init__(self, objects_storage, texts_storage, master=get_master()):
        super().__init__(master=master)

        self.left_part = TextView(texts_storage=texts_storage, redraw_callback=self.redraw)
        self.right_part = ObjectsView(texts_storage=texts_storage, objects_storage=objects_storage, redraw_callback=self.redraw)

        self.redraw()


    def redraw(self):
        self.left_part.redraw()
        self.left_part.grid(row=0, column=0)

        self.right_part.redraw()
        self.right_part.grid(row=0, column=1)


class TextView(tkinter.Text):
    def __init__(self, texts_storage, redraw_callback, master=get_master()):
        super().__init__(master=master)
        self.texts_storage = texts_storage
        self.redraw_callback = redraw_callback


    def redraw(self):
        self.delete("1.0", "end")
        for stored_text in self.texts_storage:
            self.insert(tkinter.END, stored_text + "\n")


class ObjectsView(tkinter.Canvas):
    def __init__(self, texts_storage, objects_storage, redraw_callback, master=get_master()):
        super().__init__(master=master)
        self.objects_storage = objects_storage

        controller = ObjectsViewController(texts_storage=texts_storage, objects_storage=objects_storage, redraw_callback=redraw_callback)
        self.bind("<Button-1>", controller.on_click)
        self.bind("<Motion>", controller.on_motion)
        self.bind("<ButtonRelease-1>", controller.on_unclick)


    def redraw(self):
        self.delete("all")
        for stored_object in self.objects_storage:
            self.create_oval(
                stored_object.top_left_x,
                stored_object.top_left_y,
                stored_object.bottom_right_x,
                stored_object.bottom_right_y,
                {}
            )

