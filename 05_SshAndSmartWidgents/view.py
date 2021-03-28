import tkinter
from tkinter import font
from controller import ObjectsViewController, TextsViewController


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

        self.left_part = TextView(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=self.redraw
        )
        self.right_part = ObjectsView(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=self.redraw
        )

        self.redraw()

    def redraw(self):
        self.left_part.redraw()
        self.left_part.grid(row=0, column=0)

        self.right_part.redraw()
        self.right_part.grid(row=0, column=1)


class TextView(tkinter.Text):
    def __init__(self, texts_storage, objects_storage, redraw_callback, master=get_master()):
        super().__init__(master=master, font=font.Font(family="Consolas", size=14, weight="normal"))
        self.texts_storage = texts_storage
        self.redraw_callback = redraw_callback
        self.controller = TextsViewController(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=redraw_callback
        )
        self.apply_button = tkinter.Button(master, text="Apply", command=self.apply_clicked)
        self.tag_config('warning', background="yellow", foreground="red")


    def redraw(self):
        self.delete("1.0", "end")
        for stored_text in self.texts_storage:
            is_valid = self.texts_storage.is_text_valid(stored_text);
            self.insert(tkinter.END, stored_text  + "\n", '' if is_valid else 'warning')
        self.apply_button.grid(row=1, column=0)

    def apply_clicked(self):
        texts = self.get("1.0", tkinter.END)
        self.controller.apply(texts)


class ObjectsView(tkinter.Canvas):
    def __init__(self, texts_storage, objects_storage, redraw_callback, master=get_master()):
        super().__init__(master=master)
        self.objects_storage = objects_storage

        controller = ObjectsViewController(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=redraw_callback
        )
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
                fill=stored_object.fill_color,
                outline=stored_object.border_color,
                width=stored_object.border_width
            )
