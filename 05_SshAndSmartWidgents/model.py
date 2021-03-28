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


    @staticmethod
    def handle_resize(coord_from, coord_to, coord_min, coord_max):
        if coord_from > coord_min:
            if coord_to > coord_min:
                coord_max = coord_to
            else:
                coord_max = coord_min
                coord_min = coord_to
        else:
            if coord_to < coord_max:
                coord_min = coord_to
            else:
                coord_min = coord_max
                coord_max = coord_to
        return coord_min, coord_max


    def resize_to(self, from_x, to_x, from_y, to_y):
        self.top_left_x, self.bottom_right_x = self.handle_resize(from_x, to_x, self.top_left_x, self.bottom_right_x)
        self.top_left_y, self.bottom_right_y = self.handle_resize(from_y, to_y, self.top_left_y, self.bottom_right_y)


class ObjectsStorage(object):
    def __init__(self):
        self.objects = []

        # store info about prev clicked object
        self.clicked = None
        self.hover_x = None
        self.hover_y = None

        # handle to last added object unitl it stop resizing
        self.just_added = None


    def append(self, new_object):
        self.clicked = new_object
        self.just_added = new_object
        self.set_hover_pos(new_object.top_left_x, new_object.top_left_y)
        self.objects.append(new_object)


    def __iter__(self):
        for stored_object in self.objects:
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


    def get_just_added(self):
        return self.just_added


    def forget_just_added(self):
        self.just_added = None


class TextsStorage(object):
    def __init__(self):
        self.texts = []


    def __iter__(self):
        for stored_text in self.texts:
            yield stored_text


    def update(self, objects_storage):
        self.texts = []
        for stored_object in objects_storage:
            self.texts.append(stored_object.serialize_to_string())


