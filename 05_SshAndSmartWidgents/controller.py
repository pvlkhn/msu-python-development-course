from model import Oval


class ObjectsViewController(object):
    def __init__(self, texts_storage, objects_storage, redraw_callback):
        self.texts_storage = texts_storage
        self.objects_storage = objects_storage
        self.redraw_callback = redraw_callback


    def on_unclick(self, event):
        self.objects_storage.forget_clicked()
        self.objects_storage.forget_just_added()


    def on_motion(self, event):
        prev_clicked = self.objects_storage.get_clicked()
        if prev_clicked is None:
            return

        prev_hover_x, prev_hover_y = self.objects_storage.get_hover_pos()

        if prev_clicked == self.objects_storage.get_just_added():
            prev_clicked.resize_to(prev_hover_x, event.x, prev_hover_y, event.y)
        else:
            prev_clicked.move(event.x - prev_hover_x, event.y - prev_hover_y)

        self.objects_storage.set_hover_pos(event.x, event.y)
        self.texts_storage.update(self.objects_storage)
        self.redraw_callback()


    def on_click(self, event):
        for stored_object in self.objects_storage:
            if stored_object.is_clicked(event.x, event.y):
                self.objects_storage.set_clicked(event.x, event.y)
                return

        self.add_oval(event.x, event.y)


    def add_oval(self, center_x, center_y):
        oval = Oval(
            top_left_x=center_x,
            top_left_y=center_y,
            bottom_right_x=center_x,
            bottom_right_y=center_y
        )
        self.objects_storage.append(oval)
        self.redraw_callback()

