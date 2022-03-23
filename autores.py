from __future__ import print_function
import sys
import win32ui
import time

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(489, 152)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(400, 120, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 461, 101))
        self.groupBox.setObjectName("groupBox")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(80, 20, 371, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(16, 20, 51, 21))
        self.label.setObjectName("label")
        self.width = QtWidgets.QLineEdit(self.groupBox)
        self.width.setGeometry(QtCore.QRect(80, 60, 113, 20))
        self.width.setPlaceholderText("")
        self.width.setObjectName("width")
        self.Height = QtWidgets.QLineEdit(self.groupBox)
        self.Height.setGeometry(QtCore.QRect(330, 60, 113, 20))
        self.Height.setObjectName("Height")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 71, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(260, 60, 71, 20))
        self.label_3.setObjectName("label_3")
        self.logLabel = QtWidgets.QLabel(Dialog)
        self.logLabel.setGeometry(QtCore.QRect(10, 120, 381, 21))
        self.logLabel.setObjectName("logLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Start"))
        self.groupBox.setTitle(_translate("Dialog", "ToolBox"))
        self.label.setText(_translate("Dialog", "App Name :"))
        self.label_2.setText(_translate("Dialog", "Width"))
        self.label_3.setText(_translate("Dialog", "Height"))
        self.logLabel.setText(_translate("Dialog", "..."))
        self.pushButton.clicked.connect(lambda: self.BtnStartHandler(self.lineEdit.text(), int(self.width.text()), int(self.Height.text())))

    def BtnStartHandler(self, appName, width, height):
        print('Primary screen resolution: {}x{}'.format(
            *ScreenRes.get()
            ))
        while True:
            if WindowExists(appName):
                ScreenRes.set(width, height)
                print("Success")
                break
            else:
                print("Waiting...")
                time.sleep(5)

class ScreenRes(object):
    @classmethod
    def set(cls, width=None, height=None, depth=32):
        if width and height:
            print('Setting resolution to {}x{}'.format(width, height, depth))
        else:
            print('Setting resolution to defaults')

        if sys.platform == 'win32':
            cls._win32_set(width, height, depth)
        elif sys.platform.startswith('linux'):
            cls._linux_set(width, height, depth)
        elif sys.platform.startswith('darwin'):
            cls._osx_set(width, height, depth)

    @classmethod
    def get(cls):
        if sys.platform == 'win32':
            return cls._win32_get()
        elif sys.platform.startswith('linux'):
            return cls._linux_get()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get()

    @classmethod
    def get_modes(cls):
        if sys.platform == 'win32':
            return cls._win32_get_modes()
        elif sys.platform.startswith('linux'):
            return cls._linux_get_modes()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get_modes()

    @staticmethod
    def _win32_get_modes():
        '''
        Get the primary windows display width and height
        '''
        import win32api
        from pywintypes import DEVMODEType, error
        modes = []
        i = 0
        try:
            while True:
                mode = win32api.EnumDisplaySettings(None, i)
                modes.append((
                    int(mode.PelsWidth),
                    int(mode.PelsHeight),
                    int(mode.BitsPerPel),
                    ))
                i += 1
        except error:
            pass

        return modes

    @staticmethod
    def _win32_get():
        '''
        Get the primary windows display width and height
        '''
        import ctypes
        user32 = ctypes.windll.user32
        screensize = (
            user32.GetSystemMetrics(0), 
            user32.GetSystemMetrics(1),
            )
        return screensize

    @staticmethod
    def _win32_set(width=None, height=None, depth=32):
        '''
        Set the primary windows display to the specified mode
        '''
        # Gave up on ctypes, the struct is really complicated
        #user32.ChangeDisplaySettingsW(None, 0)
        import win32api
        from pywintypes import DEVMODEType
        if width and height:

            if not depth:
                depth = 32

            mode = win32api.EnumDisplaySettings()
            mode.PelsWidth = width
            mode.PelsHeight = height
            mode.BitsPerPel = depth

            win32api.ChangeDisplaySettings(mode, 0)
        else:
            win32api.ChangeDisplaySettings(None, 0)


    @staticmethod
    def _win32_set_default():
        '''
        Reset the primary windows display to the default mode
        '''
        # Interesting since it doesn't depend on pywin32
        import ctypes
        user32 = ctypes.windll.user32
        # set screen size
        user32.ChangeDisplaySettingsW(None, 0)

    @staticmethod
    def _linux_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _linux_get():
        raise NotImplementedError()

    @staticmethod
    def _linux_get_modes():
        raise NotImplementedError()

    @staticmethod
    def _osx_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _osx_get():
        raise NotImplementedError()

    @staticmethod
    def _osx_get_modes():
        raise NotImplementedError()

def WindowExists(classname):
    try:
        win32ui.FindWindow(classname, None)
    except win32ui.error:
        return False
    else:
        return True



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())