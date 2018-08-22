# -*- coding: utf-8 -*-

########################################################################################
## Python code generated with wxFormBuilder (version Jun 10 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
########################################################################################
__author__ = "Julius Ramos"
__copyright__ = "Copyright 08/19/2018; The Move, Append, and Copy (MAC) Utility Project"
__license__ = "GPL"
__version__ = "1.0.2"
__maintainer__ = "Julius Ramos"
__email__ = "juliusramos918@gmail.com"
__status__ = "Development"
########################################################################################

import wx
import wx.xrc


########################################################################################
## Class MacFrame
########################################################################################


class MacFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Move, Append, Copy Utility (MAC)",
                          pos=wx.DefaultPosition, size=wx.Size(562, 290),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.SourceLabel = wx.StaticText(self, wx.ID_ANY, u"Source:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.SourceLabel.Wrap(-1)
        bSizer1.Add(self.SourceLabel, 0, wx.ALL, 5)

        self.SelectSrcDir = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString,
                                             u"Please select a source directory to get your data from.",
                                             wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        bSizer1.Add(self.SelectSrcDir, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.DestinationLabel = wx.StaticText(self, wx.ID_ANY, u"Destination:", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        self.DestinationLabel.Wrap(-1)
        bSizer1.Add(self.DestinationLabel, 0, wx.ALL, 5)

        self.SelectDstDir = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString,
                                             u"Select a directory to store the output file(s)", wx.DefaultPosition,
                                             wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        bSizer1.Add(self.SelectDstDir, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        gSizer3 = wx.GridSizer(0, 2, 0, 0)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"File Extension:", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText4.Wrap(-1)
        bSizer4.Add(self.m_staticText4, 0, wx.ALL | wx.EXPAND, 5)

        self.SelectFileExt = wx.TextCtrl(self, wx.ID_ANY, u"txt", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTRE)
        bSizer4.Add(self.SelectFileExt, 1, wx.ALL | wx.EXPAND, 5)

        self.SelectPartialName = wx.StaticText(self, wx.ID_ANY, u"Partial Filename:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.SelectPartialName.Wrap(-1)
        bSizer4.Add(self.SelectPartialName, 0, wx.ALL | wx.EXPAND, 5)

        self.PartialName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_CENTRE)
        bSizer4.Add(self.PartialName, 1, wx.ALL | wx.EXPAND, 5)

        gSizer3.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"File Options:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        bSizer2.Add(self.m_staticText3, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.SelectMove = wx.RadioButton(self, wx.ID_ANY, u"Move", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.SelectMove, 1, wx.ALL | wx.EXPAND, 5)

        self.SelectAppend = wx.RadioButton(self, wx.ID_ANY, u"Append", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.SelectAppend, 1, wx.ALL | wx.EXPAND, 5)

        self.SelectCopy = wx.RadioButton(self, wx.ID_ANY, u"Copy", wx.DefaultPosition, wx.DefaultSize, 0)
        self.SelectCopy.SetValue(True)
        bSizer2.Add(self.SelectCopy, 1, wx.ALL | wx.EXPAND, 5)

        gSizer3.Add(bSizer2, 1, wx.EXPAND, 5)

        gSizer1.Add(gSizer3, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.SearchAll = wx.CheckBox(self, wx.ID_ANY, u"Check to include subdirectories", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        bSizer3.Add(self.SearchAll, 0, wx.ALL | wx.ALIGN_RIGHT | wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.StatusIndicator = wx.TextCtrl(self, wx.ID_ANY, u"READY", wx.DefaultPosition, wx.DefaultSize,
                                           wx.TE_CENTRE | wx.TE_READONLY)
        bSizer5.Add(self.StatusIndicator, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.StartButton = wx.Button(self, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.StartButton, 1,
                    wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT,
                    5)

        bSizer3.Add(bSizer5, 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.tear_down)
        self.SelectSrcDir.Bind(wx.EVT_DIRPICKER_CHANGED, self.update_user_options)
        self.SelectDstDir.Bind(wx.EVT_DIRPICKER_CHANGED, self.update_user_options)
        self.SelectFileExt.Bind(wx.EVT_TEXT, self.update_user_options)
        self.SelectFileExt.Bind(wx.EVT_TEXT_ENTER, self.update_user_options)
        self.PartialName.Bind(wx.EVT_TEXT, self.update_user_options)
        self.PartialName.Bind(wx.EVT_TEXT_ENTER, self.update_user_options)
        self.SelectMove.Bind(wx.EVT_RADIOBUTTON, self.update_user_options)
        self.SelectAppend.Bind(wx.EVT_RADIOBUTTON, self.update_user_options)
        self.SelectCopy.Bind(wx.EVT_RADIOBUTTON, self.update_user_options)
        self.SearchAll.Bind(wx.EVT_CHECKBOX, self.update_user_options)
        self.StartButton.Bind(wx.EVT_BUTTON, self.start_process)


    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class

    def tear_down(self, event):
        event.Skip()

    def update_user_options(self, event):
        event.Skip()

    def start_process(self, event):
        event.Skip()


if __name__ == "__main__":
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = MacFrame(None) # A Frame is a top-level window.
    frame.Show(True)     # Show the frame.
    app.MainLoop()
