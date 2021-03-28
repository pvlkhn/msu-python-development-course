import json


class Oval(object):
    DEFAULT_BORDER_WIDTH = 1
    DEFAULT_BORDER_COLOR = "white"
    DEFAULT_FILL_COLOR = "green"

    def __init__(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y,
                    fill_color=DEFAULT_FILL_COLOR, border_color=DEFAULT_BORDER_COLOR, border_width=DEFAULT_BORDER_WIDTH):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width

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

    def update(self, texts_storage):
        self.objects = []
        for text in texts_storage:
            try:
                self.objects.append(Oval.create_from_string(text))
            except:
                texts_storage.set_text_invalid(text)

    def __iter__(self):
        for stored_object in self.objects:
            yield stored_object

    def set_clicked(self, clicked_object, clicked_x, clicked_y):
        self.clicked = clicked_object
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
        self.invalid_texts = set()

    def __iter__(self):
        for stored_text in self.texts:
            yield stored_text

    def is_text_valid(self, text):
        return text not in self.invalid_texts

    def update(self, objects_storage):
        self.texts = []
        self.invalid_texts = set()
        for stored_object in objects_storage:
            self.texts.append(stored_object.serialize_to_string())

    def set_texts(self, texts):
        self.texts = texts.strip().split("\n")

    def set_text_invalid(self, text):
        self.invalid_texts.add(text)
