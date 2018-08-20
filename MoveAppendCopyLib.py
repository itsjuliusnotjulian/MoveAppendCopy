#!/usr/bin/env python3

########################################################################################
__author__ = "Julius Ramos"
__copyright__ = "Copyright 08/20/2018; The Move, Append, and Copy (MAC) Utility Project"
__license__ = "GPL"
__version__ = "1.2.0"
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
# Class SearchDirectory
########################################################################################

class SearchDirectory(object):
    """This class is used as a decorator to recursively search through a source directory and its subdirectories.
       Otherwise, it'll execute the original function argument.

    """
    
    def __init__(self, original_func):
        self.original_func = original_func

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

    def __call__(self, *args):
        """ This function call operator.
        Args:
            original_func (method): The operation to execute which can be either move, append, or copy.
                *args (tuple): A tuple containing information for the original function to process.
                    source_dir (str): The full source path to operate a file from.
                    destination_dir (str): The full directory path to operate a file into.
                    names_to_look (str): The name of the file(s) to search for including the partial filename and ext.
                    search_all_within (bool): True to search subdirectories; otherwise, False.
                    output_file (str): The output file to append data into.
        Returns:
            status (int): 0 if passed; -1 if failed.
        """
        source_dir = args[0][0]
        destination_dir = args[0][1]
        names_to_look = args[0][2]
        search_all_within = args[0][3]
        output_file = args[0][4]

        # Obtain all files containing the partial name and/or extension from the source dir
        all_files = glob.glob1("{}/".format(source_dir), names_to_look)

        # Obtain all contents of the current source dir including other directories
        all_contents = os.listdir(source_dir)

        try:
            # Search through all directories inside the source for the file types to move
            for contents in all_contents:
                path = os.path.abspath("{}/{}".format(source_dir, contents))
                basename = os.path.basename(path)
                data = (path, destination_dir, names_to_look, search_all_within, output_file)
                if self._is_sub_directory(path) and search_all_within:
                    # recursively call back the decorator to dig deeper
                    self.__call__(data)
                elif self._is_file(path) and (basename in all_files):
                    # otherwise, execute the operation
                    self.original_func(self, data)
            else:
                status = 0
        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug
        return status


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

    @SearchDirectory
    def _move_file(self, data):
        """This private method is used to move one file from a source path to a output directory.
        Args:
            data (tuple): A tuple containing information for the original function to process.
                source_dir (str): The full source path to operate a file from.
                destination_dir (str): The full directory path to operate a file into.
                names_to_look (str): The name of the file(s) to search for including the partial filename and ext.
                search_all_within (bool): True to search subdirectories; otherwise, False.
                output_file (str): The output file to append data into.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test._move_file(src, dst)

        """
        source_dir = data[0]
        destination_dir = data[1]

        try:
            shutil.move(source_dir, destination_dir)
            status = 0
        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug

        return status

    @SearchDirectory
    def _append_file(self, data):
        """This private method is used to append the contents of user-defined files from a source path into an
           output file.
        Args:
            data (tuple): A tuple containing information for the original function to process.
                source_dir (str): The full source path to operate a file from.
                destination_dir (str): The full directory path to operate a file into.
                names_to_look (str): The name of the file(s) to search for including the partial filename and ext.
                search_all_within (bool): True to search subdirectories; otherwise, False.
                output_file (str): The output file to append data into.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test._append_file(path)

        """
        source_dir = data[0]
        output_file = data[4]

        try:
            with open(source_dir, 'r') as newfile:
                text = newfile.readlines()
                try:
                    with open(output_file, 'a') as myfile:
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

    @SearchDirectory
    def _copy_file(self, data):
        """This private method is used to copy one file from a source path to a output directory.
        Args:
             data (tuple): A tuple containing information for the original function to process.
                source_dir (str): The full source path to operate a file from.
                destination_dir (str): The full directory path to operate a file into.
                names_to_look (str): The name of the file(s) to search for including the partial filename and ext.
                search_all_within (bool): True to search subdirectories; otherwise, False.
                output_file (str): The output file to append data into.
        Returns:
            status (int): 0 if passed; -1 if failed.
        Example:
            test = MoveAppendCopy(src, dst, partial_name, ext)
            status = test._copy_file(src, dst)

        """
        source_dir = data[0]
        destination_dir = data[1]

        try:
            shutil.copy2(source_dir, destination_dir)
            status = 0
        except Exception as err:
            status = -1
            # print("Error: {}".format(err))  # Debug

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
            # Create a tuple of the arguments to insure transfer of all the arguments
            data = (self.source_dir, self.output_dir, self.names_to_look, self.search_all_within, self.output_file)

            # The user-defined option will be executed
            if self.option == 1:
                status = self._move_file(data)
            elif self.option == 2:
                status = self._append_file(data)
            else:
                status = self._copy_file(data)

        except Exception as err:
            status = -1
            # print("Error: {}".format(err))

        return status


def main():
    import sys

    # ## For Debug Only
    # start = time()
    # output = "Desktop/Python_Jupyter"
    # source = "Desktop/Jupyter_Notebook"
    # partial_name = ""
    # ext = "ipynb"
    # search_all = True
    # opt = "move"
    # test = MoveAppendCopy(source, output, partial_name, ext, search_all, opt)
    # #print(test.append_all_to_file())
    # #print(test.move_all_to_dir())
    # print(test.select_option())
    # elapsed_time = time() - start
    # print("Elapsed time in seconds: {}s".format(elapsed_time))

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
