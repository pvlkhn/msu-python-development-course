import json


class Oval(object):
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 50

    def __init__(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y


    @staticmethod
    def create_from_string(serialized_oval):
        return Oval(**json.loads(serialized_oval))


    def serialize_to_string(self):
        return json.dumps(self.__dict__)


    def is_clicked(self, click_x, click_y):
        return (
            click_x > self.top_left_x
            and click_x < self.bottom_right_x
            and click_y > self.top_left_y
            and click_y < self.bottom_right_y
        )


    def move(self, dx, dy):
        self.top_left_x += dx
        self.top_left_y += dy
        self.bottom_right_x += dx
        self.bottom_right_y += dy


class ObjectsStorage(object):
    def __init__(self):
        self.stored_objects = []

        # store info about prev clicked object
        self.clicked = None
        self.hover_x = None
        self.hover_y = None


    def append(self, new_object):
        self.stored_objects.append(new_object)


    def __iter__(self):
        for stored_object in self.stored_objects:
            self.current_iter_object = stored_object
            yield stored_object


    def set_clicked(self, clicked_x, clicked_y):
        self.clicked = self.current_iter_object
        self.hover_x = clicked_x
        self.hover_y = clicked_y


    def get_clicked(self):
        return self.clicked


    def forget_clicked(self):
        self.clicked = None
        self.clicked_x = None
        self.clicked_y = None


    def get_hover_pos(self):
        return (self.hover_x, self.hover_y)


    def set_hover_pos(self, hover_x, hover_y):
        self.hover_x = hover_x
        self.hover_y = hover_y


