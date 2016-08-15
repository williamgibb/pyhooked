import ctypes
from ctypes import wintypes
from ctypes import CFUNCTYPE, POINTER, c_int, c_uint, c_void_p

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
