#!/usr/bin/env python3

########################################################################################
__author__ = "Julius Ramos"
__copyright__ = "Copyright 08/20/2018; The Move, Append, and Copy (MAC) Utility Project"
__license__ = "GPL"
__version__ = "1.0.2"
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
        self.search_all = self.SearchAll.IsEnabled()
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
        self.search_all = self.SearchAll.IsEnabled()

        # Ensure that only one operation is set
        if not self.SelectMove.IsEnabled() and not self.SelectAppend.IsEnabled():
            self.SelectCopy.SetValue(True)
            self.SelectCopy.Update()

        if not self.SelectAppend.IsEnabled() and not self.SelectCopy.IsEnabled():
            self.SelectMove.SetValue(True)
            self.SelectMove.Update()

        if not self.SelectMove.IsEnabled() and not self.SelectCopy.IsEnabled():
            self.SelectAppend.SetValue(True)
            self.SelectAppend.Update()

        # Default operation is "copy"
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
