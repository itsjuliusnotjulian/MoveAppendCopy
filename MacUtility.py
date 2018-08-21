#!/usr/bin/env python3

########################################################################################
__author__ = "Julius Ramos"
__copyright__ = "Copyright 08/20/2018; The Move, Append, and Copy (MAC) Utility Project"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Julius Ramos"
__status__ = "Development"
########################################################################################

import wx
import wx.xrc
import threading
from MacFrame import MacFrame
from MoveAppendCopyLib import MoveAppendCopy
from datetime import datetime


########################################################################################
# Class MacUtility
########################################################################################
class MacUtility(MacFrame):
    def __init__(self, parent):
        MacFrame.__init__(self, parent)

        self.source = self.SelectSrcDir.GetPath()
        self.output = self.SelectDstDir.GetPath()
        self.partial_name = self.PartialName.GetValue()
        self.ext = self.SelectFileExt.GetValue()
        self.search_all = self.SearchAll.IsChecked()
        self.opt = "copy"
        self.mac = MoveAppendCopy(self.source, self.output, self.partial_name, self.ext, self.search_all, self.opt)

    def tear_down(self, event):
        self.Destroy()

    def update_user_options(self, event):
        self.StatusIndicator.SetBackgroundColour((0, 255, 0))  # GREEN
        self.StatusIndicator.SetValue("READY")
        self.source = self.SelectSrcDir.GetPath()
        self.output = self.SelectDstDir.GetPath()
        self.partial_name = self.PartialName.GetValue()
        self.ext = self.SelectFileExt.GetValue()
        self.search_all = self.SearchAll.IsChecked()

        if not self.SelectMove.IsChecked() and not self.SelectAppend.IsChecked():
            self.SelectCopy.SetValue(True)
            self.SelectCopy.Update()
        elif self.SelectMove.IsChecked() or self.SelectAppend.IsChecked():
            if self.SelectCopy.IsChecked():
                self.SelectCopy.SetValue(False)
            self.SelectCopy.Update()
            
        if not self.SelectAppend.IsChecked() and not self.SelectCopy.IsChecked():
            self.SelectMove.SetValue(True)
            self.SelectMove.Update()
        elif self.SelectAppend.IsChecked() or self.SelectCopy.IsChecked():
            if self.SelectMove.IsChecked():
                self.SelectMove.SetValue(False)
            self.SelectMove.Update()

        if not self.SelectMove.IsChecked() and not self.SelectCopy.IsChecked():
            self.SelectAppend.SetValue(True)
            self.SelectAppend.Update()
        elif self.SelectMove.IsChecked() or self.SelectCopy.IsChecked():
            if self.SelectAppend.IsChecked():
                self.SelectAppend.SetValue(False)
            self.SelectAppend.Update()

        if self.SelectMove.GetValue():
            self.opt = "move"
        elif self.SelectAppend.GetValue():
            self.opt = "append"
        elif self.SelectCopy.GetValue():
            self.opt = "copy"
        else:
            self.opt = "copy"

        self.Update()
        self.mac = MoveAppendCopy(self.source, self.output, self.partial_name, self.ext, self.search_all, self.opt)

    def start_process(self, event):
        try:
            status = -1
            while status:
                self.StatusIndicator.SetBackgroundColour((255, 255, 0))  # YELLOW
                self.StatusIndicator.SetValue("SEARCHING")
                status = self.mac.select_option()
                if not status:
                    self.StatusIndicator.SetBackgroundColour((255, 0, 0))  # RED
                    self.StatusIndicator.SetValue("DONE")
                    break
            self.Update()
        except Exception as err:
            status = -1
            print("Error: {}".format(err))

        return status


if __name__ == "__main__":
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = MacUtility(None)  # A Frame is a top-level window.
    frame.Show(True)  # Show the frame.
    app.MainLoop()