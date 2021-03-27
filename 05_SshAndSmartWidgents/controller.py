from model import Oval


class ObjectsViewController(object):
    def __init__(self, stored_objects, redraw_callback):
        self.stored_objects = stored_objects
        self.redraw_callback = redraw_callback


    def on_click(self, event):
        for stored_object in self.stored_objects:
            if stored_object.is_clicked(event.x, event.y):
                return
        self.add_oval(event.x, event.y)


    def add_oval(self, center_x, center_y):
        oval = Oval(
            top_left_x=(center_x - Oval.DEFAULT_WIDTH / 2),
            top_left_y=(center_y + Oval.DEFAULT_HEIGHT / 2),
            bottom_right_x=(center_x + Oval.DEFAULT_WIDTH / 2),
            bottom_right_y=(center_y - Oval.DEFAULT_HEIGHT / 2)
        )
        self.stored_objects.append(oval)
        self.redraw_callback()


