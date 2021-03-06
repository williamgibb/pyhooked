#PyHooked: a pure Python hotkey module


[![Join the chat at https://gitter.im/IronManMark20/pyhooked](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/IronManMark20/pyhooked?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


####About - 
PyHooked is a pure python keyboard and mouse hotkey module that allows the creation of hotkeys in all Python implementations that support sane implementations of ctypes. Instead of messing around with low level Windows calls, just give Hooked a callback and tell it to start listening.

PyHooked supports IronPython (2.7.5+, incl. 2.7.6 RC2), PyPy (5.3.1+) and CPython (Tested:2.7 x86,3.4 x64,3.5 x86; Most are likely to work) currently. It is pure Python, so porting to other Python implementations and versions should be very simple.

####Usage - 
Please see [example.py](https://github.com/ethanhs/pyhooked/blob/master/example.py) for a basic example.

I you are using it with a UI library, please see [example_gui.py](https://github.com/ethanhs/pyhooked/blob/master/example_gui.py)

Please note that the wiki is out of date, and needs to be updated.

####Installing

Just run `$ pip install git+https://github.com/ethanhs/pyhooked.git`


####Alternatives -
[pyHook](http://sourceforge.net/projects/pyhook/) and [pyhk](https://github.com/schurpf/pyhk) inspired the creation of this project. They are great hotkey modules too!

####License - 
PyHooked  Copyright (C) 2015  Ethan Smith
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions;
PyHooked is licensed under the LGPL v3, or at your choice, any later version. This program comes with the lgpl in a .txt file.

#####As of v0.6, the module is LGPL licensed, not under the GPL.

####The Future - 
Here are a few things that I would like to see:
* ~~add support for args for called functions~~  __(DONE)__
* ~~get mouse inputs~~  __(DONE)__
* ~~support all scancodes found [here](https://msdn.microsoft.com/en-us/library/aa299374%28v=vs.60%29.aspx)~~  __(DONE)__
* Jython support
* ????<br>
I am open to feature requests. If you have ideas, let me know (mr.smittye (at) gmail). Or, even better, make your changes and a pull request!
