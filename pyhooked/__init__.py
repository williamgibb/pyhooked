"""
This file is part of pyhooked, an LGPL licensed pure Python hotkey module for Windows
Copyright (C) 2016 Ethan Smith

"""

from ctypes import byref
import atexit

from pyhooked import constants
from pyhooked import events
from pyhooked import win32

__version__ = '0.8.0'


class Hook(object):
    """"Main hotkey class used to and listen for hotkeys. Set an event handler to check what keys are pressed."""

    def __init__(self):
        """Initializer of the Hook class, creates class attributes"""
        self.handler = None
        self.pressed_keys = []
        self.keyboard_id = None
        self.mouse_id = None
        self.mouse_is_hook = False
        self.keyboard_is_hook = True

    def hook(self, keyboard=True, mouse=False):
        """Hook mouse and/or keyboard events"""
        self.mouse_is_hook = mouse
        self.keyboard_is_hook = keyboard

        # check that we are going to hook into at least one device
        if not self.mouse_is_hook and not self.keyboard_is_hook:
            raise Exception("You must hook into either the keyboard and/or mouse events")

        if self.keyboard_is_hook:
            def keyboard_low_level_handler(code, event_code, kb_data_ptr):
                """Used to catch keyboard events and deal with the event"""
                try:
                    key_code = 0xFFFFFFFF & kb_data_ptr[0]  # key code
                    current_key = constants.ID_TO_KEY[key_code]
                    event_type = constants.event_types[0xFFFFFFFF & event_code]

                    if event_type == 'key down':  # add key to those down to list
                        self.pressed_keys.append(current_key)

                    if event_type == 'key up':  # remove when no longer pressed
                        self.pressed_keys.remove(current_key)

                    # wrap the keyboard information grabbed into a container class
                    event = events.KeyboardEvent(current_key, event_type, self.pressed_keys, key_code)

                    # if we have an event handler, call it to deal with keys in the list
                    if self.handler:
                        self.handler(event)

                finally:
                    # TODO: fix return here to use non-blocking call
                    return win32.CallNextHookEx(self.keyboard_id, code, event_code, kb_data_ptr)

            keyboard_pointer = win32._callback_pointer(keyboard_low_level_handler)

            self.keyboard_id = win32.SetWindowsHookExA(constants.WH_KEYBOARD_LL,
                                                       keyboard_pointer,
                                                       win32.GetModuleHandleA(None),
                                                       0)

        if self.mouse_is_hook:
            def mouse_low_level_handler(code, event_code, kb_data_ptr):
                """Used to catch and deal with mouse events"""
                try:
                    current_key = constants.MOUSE_ID_TO_KEY[event_code]
                    if current_key != 'Move':  # if we aren't moving, then we deal with a mouse click
                        event_type = constants.MOUSE_ID_TO_EVENT_TYPE[event_code]
                        # the first two members of kb_data_ptr hold the mouse position, x and y
                        event = events.MouseEvent(current_key, event_type, kb_data_ptr[0], kb_data_ptr[1])

                        if self.handler:
                            self.handler(event)

                finally:
                    # TODO: fix return here to use non-blocking call
                    return win32.CallNextHookEx(self.mouse_id, code, event_code, kb_data_ptr)

            mouse_pointer = win32._callback_pointer(mouse_low_level_handler)
            self.mouse_id = win32.SetWindowsHookExA(constants.WH_MOUSE_LL,
                                                    mouse_pointer,
                                                    win32.GetModuleHandleA(None),
                                                    0)

        atexit.register(win32.UnhookWindowsHookEx, self.keyboard_id)
        atexit.register(win32.UnhookWindowsHookEx, self.mouse_id)

        message = win32.wintypes.MSG()
        while self.mouse_is_hook or self.keyboard_is_hook:
            msg = win32.GetMessageW(byref(message), 0, 0, 0)
            if msg == -1:
                self.unhook_keyboard()
                self.unhook_mouse()
                exit(0)

            elif msg == 0:  # GetMessage return 0 only if WM_QUIT
                exit(0)
            else:
                win32.TranslateMessage(byref(message))
                win32.DispatchMessageW(byref(message))

    def unhook_mouse(self):
        """Stop listening to the mouse"""
        if self.mouse_is_hook:
            self.mouse_is_hook = False
            win32.UnhookWindowsHookEx(self.mouse_id)

    def unhook_keyboard(self):
        """Stop listening to the keyboard"""
        if self.keyboard_is_hook:
            self.keyboard_is_hook = False
            win32.UnhookWindowsHookEx(self.keyboard_id)
