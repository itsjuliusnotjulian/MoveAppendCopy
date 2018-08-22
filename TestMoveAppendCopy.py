import unittest
import time
from datetime import datetime
from MoveAppendCopyLib_v2 import MoveAppendCopy

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%S-%M")


class TestMoveAppendCopy(unittest.TestCase):

    def setUp(self):

        self.source = "Desktop/Python_Jupyter/MEMO"
        self.output = "Desktop/Python_Jupyter/UnitTest_{}".format(timestamp)
        self.partial_name = ""
        self.ext = "ipynb"
        self.search_all = True
        self.opt = "copy"
        self.mac = MoveAppendCopy(self.source, self.output, self.partial_name, self.ext, self.search_all, self.opt)

    def test_move(self):
        ext = "pdf"
        opt = "move"
        self.mac = MoveAppendCopy(self.source, self.output, self.partial_name, ext, self.search_all, opt)
        result = self.mac.select_option()
        self.assertEqual(0, result)
        time.sleep(1)

    def test_append(self):
        source = "Desktop/Jupyter_Notebook"
        ext = "py"
        opt = "append"
        self.mac = MoveAppendCopy(source, self.output, self.partial_name, ext, self.search_all, opt)
        result = self.mac.select_option()
        self.assertEqual(0, result)
        time.sleep(1)

    def test_copy(self):
        new_output = "Desktop/Python_Jupyter/MEMO"
        ext = "pdf"
        opt = "copy"
        self.mac = MoveAppendCopy(self.output, new_output, self.partial_name, ext, self.search_all, opt)
        result = self.mac.select_option()
        self.assertEqual(0, result)
        time.sleep(1)

    def tearDown(self):
        del self.mac

