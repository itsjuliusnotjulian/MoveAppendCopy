#!/usr/bin/env python3

########################################################################################
__author__ = "Julius Ramos"
__copyright__ = "Copyright 08/19/2018; The Move, Append, and Copy (MAC) Utility Project"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Julius Ramos"
__status__ = "Development"
########################################################################################

import os
import glob
import re
import shutil
import functools
from datetime import datetime
from time import time
from os.path import expanduser


########################################################################################
# Class MoveAppendCopy
########################################################################################


class MoveAppendCopy(object):
    """The MoveAppendCopy class is a simple collection of methods that can be used for either moving,
       appending, or copying a file(s) from a root source directory to a destination directory.

    """
    options = {"move": 1,
               "append": 2,
               "copy": 3,
               }

    home = str(expanduser("~"))

    def __init__(self, src_dir_name="", out_dir_name="", partial_name="", ext="txt", search_all=False, opt="copy"):

        # Specifying the source directory
        if MoveAppendCopy.home not in src_dir_name:
            self.source_dir = os.path.abspath("{}/{}/".format(MoveAppendCopy.home, src_dir_name))
        elif not src_dir_name:
            self.source_dir = MoveAppendCopy.home
        else:
            self.source_dir = os.path.abspath(src_dir_name)

        # Specifying the destination directory
        if MoveAppendCopy.home not in out_dir_name:
            self.output_dir = os.path.abspath("{}/{}/".format(MoveAppendCopy.home, out_dir_name))
        elif not out_dir_name:
            self.output_dir = MoveAppendCopy.home
        else:
            self.output_dir = os.path.abspath(out_dir_name)

        self.partial_name = partial_name
        self.extension = ext

        try:
            self.option = MoveAppendCopy.options[str(opt).lower()]
        except KeyError:
            self.option = MoveAppendCopy.options["copy"]

        # Set to False if only if the search should be limited to the specified source; else True
        self.search_all_within = search_all

        # Ensure that the destination directory exists; if not, it will be created
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%S-%M")
        if partial_name:
            self.names_to_look = "*{}*.{}".format(self.partial_name, self.extension)
            self.output_file = "{}/{}_{}.{}".format(self.output_dir, self.partial_name, timestamp, self.extension)
        else:
            self.names_to_look = "*.{}".format(self.extension)
            self.output_file = "{}/OutputFile_{}.{}".format(self.output_dir, timestamp, self.extension)

    def _is_sub_directory(self, path=""):
        """This private method is used to check to if a path is a directory or a file.
        Args:
            path (str): The full directory path.
        Returns:
            result (bool): True if directory; else False.

        """
        result = os.path.isdir(path)
        return result

    def _is_file(self, path=""):
        """This private method is used to check to if a path is a file or a directory.
        Args:
            path (str): The full file path.
        Returns:
            result (bool): True if file; else False.

        """
        result = os.path.isfile(path)
        return result

    def _move_file(self, src="", dst=""):
        """This private method is used to move one file from a source path to a output directory.
        Args:
            src (str): The full source path to move a file from.
            dst (str): The full directory path to move a file into.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test._move_file(src, dst)

        """
        try:
            shutil.move(src, dst)
            status = 0
        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug

        return status

    def _append_file(self, path=""):
        """This private method is used to append the contents of user-defined files from a source path into an
           output file.
        Args:
            path (str): The full file path of the file to append into an output file.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test._append_file(path)

        """
        try:
            with open(path, 'r') as newfile:
                text = newfile.readlines()
                try:
                    with open(self.output_file, 'a') as myfile:
                        myfile.writelines(text)
                        # Ensure a newline is created after every appended file
                        myfile.write("\n")
                    status = 0
                except Exception as err:
                    status = -1
                    print("Error: {}".format(err))

        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug

        return status

    def _copy_file(self, src="", dst=""):
        """This private method is used to copy one file from a source path to a output directory.
        Args:
            src (str): The full source path to move a file from.
            dst (str): The full directory path to move a file into.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test._copy_file(src, dst)

        """
        try:
            shutil.copy2(src, dst)
            status = 0
        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug

        return status

    def move_all_to_dir(self, source_dir=""):
        """This method is used to move all the user-defined file types from a source directory into an
           output directory.
        Args:
            source_dir (str): The full file path of the file to move into the output directory.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test.move_all_to_dir(source_dir)

        """
        if source_dir:
            source_dir = source_dir
        else:
            source_dir = self.source_dir

        # Obtain all files containing the partial name and/or extension from the source dir
        all_files = glob.glob1("{}/".format(source_dir), self.names_to_look)

        # Obtain all contents of the current source dir including other directories
        all_contents = os.listdir(source_dir)

        try:
            # Search through all directories inside the source for the file types to move
            for contents in all_contents:
                path = os.path.abspath("{}/{}".format(source_dir, contents))
                basename = os.path.basename(path)
                if self._is_sub_directory(path) and self.search_all_within:
                    self.move_all_to_dir(path)
                elif self._is_file(path) and (basename in all_files):
                    self._move_file(path, self.output_dir)
            else:
                # Successfully moved all files to the output directory
                status = 0

        except Exception as err:
            status = -1
            print("Error: {}".format(err))  # Debug

        return status

    def append_all_to_file(self, source_dir=""):
        """The method is used to append contents all the user-defined file types from a source directory into
           an output file.
        Args:
            source_dir (str): The full file path of the file to append to the output file.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test.append_all_to_file(source_dir)

        """
        if source_dir:
            source_dir = source_dir
        else:
            source_dir = self.source_dir

        # Obtain all files containing the partial name and/or extension from the source dir
        all_files = glob.glob1("{}/".format(source_dir), self.names_to_look)

        # Obtain all contents of the current source dir including other directories
        all_contents = os.listdir(source_dir)

        try:
            # Search through all directories inside the source for the file types to append
            for contents in all_contents:
                path = os.path.abspath("{}/{}/".format(source_dir, contents))
                basename = os.path.basename(path)
                if self._is_sub_directory(path) and self.search_all_within:
                    self.append_all_to_file(path)
                elif self._is_file(path) and (basename in all_files):
                    self._append_file(path)
            else:
                # Successfully appended all source files to an output file
                status = 0

        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug

        return status

    def copy_all_to_dir(self, source_dir=""):
        """The method is used to copy all the user-defined file types from a source directory into an
           output directory.
        Args:
            source_dir (str): The full file path of the file to copy into the output directory.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test.copy_all_to_dir(source_dir)

        """
        if source_dir:
            source_dir = source_dir
        else:
            source_dir = self.source_dir

        # Obtain all files containing the partial name and/or extension from the source dir
        all_files = glob.glob1("{}/".format(source_dir), self.names_to_look)

        # Obtain all contents of the current source dir including other directories
        all_contents = os.listdir(source_dir)

        try:
            # Search through all directories inside the source for the file types to copy
            for contents in all_contents:
                path = os.path.abspath("{}/{}/".format(source_dir, contents))
                basename = os.path.basename(path)
                if self._is_sub_directory(path) and self.search_all_within:
                    self.copy_all_to_dir(path)
                elif self._is_file(path) and (basename in all_files):
                    self._copy_file(path, self.output_dir)
            else:
                # Successfully copied all source files to an output directory
                status = 0

        except Exception as err:
            status = -1
            # print("Error: {}".format(err))

        return status

    def select_option(self):
        """The method is used to execute one of three options: move all, append all, or copy all the user-defined
           file types from a source directory into an output directory. By default, the "copy" operation is performed.
        Args:
            None
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test.select_option()

        """
        try:
            # The user-defined option will be executed
            if self.option == 1:
                status = self.move_all_to_dir(self.source_dir)
            elif self.option == 2:
                status = self.append_all_to_file(self.source_dir)
            else:
                status = self.copy_all_to_dir(self.source_dir)

        except Exception as err:
            status = -1
            # print("Error: {}".format(err))

        return status


def main():
    import sys
    #   ## For Debug Only
    #   start = time()
    #   start = time()
    #   output = "Desktop/Python_Jupyter"
    #   source = "Desktop/Jupyter_Notebook"
    #   partial_name = ""
    #   ext = "ipynb"
    #   search_all = True
    #   opt = "move"
    #   test = MoveAppendCopy(source, output, partial_name, ext, search_all, opt)
    #   #print(test.append_all_to_file())
    #   #print(test.move_all_to_dir())
    #   print(test.select_option())
    #   elapsed_time = time() - start
    #   print("Elapsed time in seconds: {}s".format(elapsed_time))

    start = time()
    source = sys.argv[1]
    output = sys.argv[2]
    partial_name = sys.argv[3]
    ext = sys.argv[4]
    search_all = sys.argv[5]
    opt = sys.argv[6]

    test = MoveAppendCopy(source, output, partial_name, ext, search_all, opt)
    print(test.select_option())
    elapsed_time = time() - start
    print("Elapsed time in seconds: {}s".format(elapsed_time))


if __name__ == "__main__":
    main()
