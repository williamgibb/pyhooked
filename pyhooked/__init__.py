"""
This file is part of pyhooked, an LGPL licensed pure Python hotkey module for Windows
Copyright (C) 2016 Ethan Smith

"""
import ctypes
from ctypes import wintypes
from ctypes import CFUNCTYPE, POINTER, c_int, c_uint, c_void_p
from ctypes import byref
import atexit

from pyhooked import constants

__version__ = '0.8.0'

cmp_func = CFUNCTYPE(c_int, c_int, wintypes.HINSTANCE, POINTER(c_void_p))

# redefine names to avoid needless clutter
GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
SetWindowsHookExA = ctypes.windll.user32.SetWindowsHookExA
GetMessageW = ctypes.windll.user32.GetMessageW
DispatchMessageW = ctypes.windll.user32.DispatchMessageW
TranslateMessage = ctypes.windll.user32.TranslateMessage
CallNextHookEx = ctypes.windll.user32.CallNextHookEx
UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx

# specify the argument and return types of functions
GetModuleHandleA.restype = wintypes.HMODULE
GetModuleHandleA.argtypes = [wintypes.LPCWSTR]
SetWindowsHookExA.restype = c_int
SetWindowsHookExA.argtypes = [c_int, cmp_func, wintypes.HINSTANCE, wintypes.DWORD]
GetMessageW.argtypes = [POINTER(wintypes.MSG), wintypes.HWND, c_uint, c_uint]
TranslateMessage.argtypes = [POINTER(wintypes.MSG)]
DispatchMessageW.argtypes = [POINTER(wintypes.MSG)]


def _callback_pointer(handler):
    """Create and return C-pointer"""
    return cmp_func(handler)


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

    def keyboard_low_level_handler(self, code, event_code, kb_data_ptr):
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
            event = KeyboardEvent(current_key, event_type, self.pressed_keys, key_code)

            # if we have an event handler, call it to deal with keys in the list
            if self.handler:
                self.handler(event)

        finally:
            # TODO: fix return here to use non-blocking call
            return CallNextHookEx(self.keyboard_id, code, event_code, kb_data_ptr)

    def mouse_low_level_handler(self, code, event_code, kb_data_ptr):
        """Used to catch and deal with mouse events"""
        try:
            current_key = constants.MOUSE_ID_TO_KEY[event_code]
            if current_key != 'Move':  # if we aren't moving, then we deal with a mouse click
                event_type = constants.MOUSE_ID_TO_EVENT_TYPE[event_code]
                # the first two members of kb_data_ptr hold the mouse position, x and y
                event = MouseEvent(current_key, event_type, kb_data_ptr[0], kb_data_ptr[1])

                if self.handler:
                    self.handler(event)

        finally:
            # TODO: fix return here to use non-blocking call
            return CallNextHookEx(self.mouse_id, code, event_code, kb_data_ptr)

    def hook(self, keyboard=True, mouse=False):
        """Hook mouse and/or keyboard events"""
        self.mouse_is_hook = mouse
        self.keyboard_is_hook = keyboard

        # check that we are going to hook into at least one device
        if not self.mouse_is_hook and not self.keyboard_is_hook:
            raise Exception("You must hook into either the keyboard and/or mouse events")

        if self.keyboard_is_hook:
            keyboard_pointer = _callback_pointer(self.keyboard_low_level_handler)
            self.keyboard_id = SetWindowsHookExA(constants.WH_KEYBOARD_LL,
                                                 keyboard_pointer,
                                                 GetModuleHandleA(None),
                                                 0)

        if self.mouse_is_hook:
            mouse_pointer = _callback_pointer(self.mouse_low_level_handler)
            self.mouse_id = SetWindowsHookExA(constants.WH_MOUSE_LL,
                                              mouse_pointer,
                                              GetModuleHandleA(None),
                                              0)

        atexit.register(UnhookWindowsHookEx, self.keyboard_id)
        atexit.register(UnhookWindowsHookEx, self.mouse_id)

        message = wintypes.MSG()
        while self.mouse_is_hook or self.keyboard_is_hook:
            msg = GetMessageW(byref(message), 0, 0, 0)
            if msg == -1:
                self.unhook_keyboard()
                self.unhook_mouse()
                exit(0)

            elif msg == 0:  # GetMessage return 0 only if WM_QUIT
                exit(0)
            else:
                TranslateMessage(byref(message))
                DispatchMessageW(byref(message))

    def unhook_mouse(self):
        """Stop listening to the mouse"""
        if self.mouse_is_hook:
            self.mouse_is_hook = False
            UnhookWindowsHookEx(self.mouse_id)

    def unhook_keyboard(self):
        """Stop listening to the keyboard"""
        if self.keyboard_is_hook:
            self.keyboard_is_hook = False
            UnhookWindowsHookEx(self.keyboard_id)
