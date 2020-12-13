import os
import sys
import threading
from AutoClick import Process
from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.resources import resource_add_path
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
#pyinstaller --name AutoClick --onefile --noconsole --icon=Icon.ico main.py
#pyinstaller AutoClick.spec
class MyRoot(GridLayout):
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)


class StartBtn(Widget):
    def __init__(self, **kwargs):
        super(StartBtn, self).__init__(**kwargs)


class AutoClickApp(App):
    isStart = False
    process = None
    btn = None
    threads = []

    def __init__(self, **kwargs):
        super(AutoClickApp, self).__init__(**kwargs)
        self.title = 'Epic 87'

        self.icon = 'Icon.ico'
        Window.size = (200, 200)
        self.process = Process()

    def processStart(self, stop):
        print("start")
        self.btn.text = "stop"
        self.btn.color = 0, 1, 0, 1
        self.process.start(stop)

    def processStop(self):
        print("stop")
        self.btn.text = "start"
        self.btn.color = 1, 0, 0, 1

    def start(self, n):
        self.isStart = not self.isStart
        if self.isStart:
            t = threading.Thread(target=self.processStart,
                                 args=(lambda: not self.isStart,))
            t.start()
            self.threads.append(t)
        else:
            t = threading.Thread(target=self.processStop)
            t.start()
            self.threads.append(t)

    def UIInit(self):
        root = MyRoot()

        startBtn = StartBtn()
        self.btn = startBtn.ids['startbtn']
        self.btn.bind(on_press=self.start)
        root.add_widget(startBtn)

        return root

    def build(self):
        return self.UIInit()

    def on_stop(self):
        self.isStart = False
        for t in self.threads:
            t.join()


def resourcePath():
    # _MEIPASS is a temporary folder for PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)

    return os.path.join(os.path.abspath("."))


if __name__ == '__main__':
    resource_add_path(resourcePath())
    AutoClickApp().run()
