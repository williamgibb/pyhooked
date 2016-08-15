class KeyboardEvent(object):
    """Class to describe an event triggered by the keyboard"""

    def __init__(self, current_key=None, event_type=None, pressed_key=None, key_code=None):
        self.current_key = current_key
        self.event_type = event_type
        self.pressed_key = pressed_key
        self.key_code = key_code


class MouseEvent(object):
    """Class to describe an event triggered by the mouse"""

    def __init__(self, current_key=None, event_type=None, mouse_x=None, mouse_y=None):
        self.current_key = current_key
        self.event_type = event_type
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
