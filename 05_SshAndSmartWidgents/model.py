import json

class Oval(object):
	DEFAULT_WIDTH = 40
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
			self.click_x > self.top_left_x
			and self.click_x < self.bottom_right_x
			and self.click_y > self.top_left_y
			and self.click_y < self.bottom_right_y
		)
