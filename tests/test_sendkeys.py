from PySide import QtCore, QtGui, QtWebKit


class WebPage(QtWebKit.QWebPage):
    """
    QWebPage that prints Javascript errors.
    """

def javaScriptConsoleMessage(self, message, lineNumber, sourceID):
    print('Javascript error at line number %d' % lineNumber)
    print('%s' % message)
    print('Source ID: %s' % sourceID)


class myWindow(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        self.loadFinished.connect(self.on_loadFinished)
        self.runloadfinished = True
        self.web_page = WebPage()
        self.setPage(self.web_page)
        self.load(QtCore.QUrl('http://stackoverflow.com/'))
def on_loadFinished(self):
    if self.runloadfinished:
        self.sendkeys(QtCore.Qt.Key_Tab)
        self.sendstring('Hello World')
        self.sendkeys(QtCore.Qt.Key_Enter)
        self.sendkeys(QtCore.Qt.Key_Return)
        self.runloadfinished = False

def sendkeys(self, char, modifier=QtCore.Qt.NoModifier):
    event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, char, modifier)
    QtCore.QCoreApplication.postEvent(self, event)

def sendstring(self, string):
    for chara in string:
        print(chara)
        self.sendkeys(char=QtGui.QKeySequence.fromString(str(chara))[0])


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')
    main = myWindow()
    main.show()
    sys.exit(app.exec_())
