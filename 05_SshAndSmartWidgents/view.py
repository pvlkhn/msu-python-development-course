import tkinter
from tkinter import font
from controller import ObjectsViewController, TextsViewController


class EditorWindow(tkinter.Frame):
    def __init__(self, objects_storage, texts_storage, master):
        super().__init__(master=master)

        self.text_part = TextView(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=self.redraw,
            master=self
        )
        self.object_part = ObjectsView(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=self.redraw,
            master=self
        )

        self.redraw()

    def redraw(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="yep")
        self.grid_columnconfigure(1, weight=1, uniform="yep")

        self.text_part.redraw()
        self.text_part.grid(row=0, column=0, sticky="NWSE")

        self.object_part.redraw()
        self.object_part.grid(row=0, column=1, rowspan=2, sticky="NWSE")


class TextView(tkinter.Text):
    def __init__(self, texts_storage, objects_storage, redraw_callback, master):
        super().__init__(master=master, font=font.Font(family="Consolas", size=14, weight="normal"))
        self.texts_storage = texts_storage
        controller = TextsViewController(
            texts_storage=texts_storage,
            objects_storage=objects_storage,
            redraw_callback=redraw_callback,
            get_texts_callback=lambda : self.get("1.0", tkinter.END),
            after_callback=self.after
        )
        self.bind("<KeyPress>", controller.content_changed)
        self.apply_button = tkinter.Button(master, text="Apply", command=controller.apply)
        self.tag_config('warning', foreground="red")


    def redraw(self):
        self.delete("1.0", "end")
        for stored_text in self.texts_storage:
            is_valid = self.texts_storage.is_text_valid(stored_text);
            self.insert(tkinter.END, stored_text  + "\n", '' if is_valid else 'warning')
        self.apply_button.grid(row=1, column=0, sticky="WE")


class ObjectsView(tkinter.Canvas):
    def __init__(self, texts_storage, objects_storage, redraw_callback, master):
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
