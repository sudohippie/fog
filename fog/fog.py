__author__ = 'Raghav Sidhanti'

import sys

from command import CommandParser
from command import CommandInvoker
from device import GoogleDrive


def main():
    # parse arguments and get command
    # execute command
    drive = GoogleDrive()

    parser = CommandParser(drive)
    command = parser.parse(sys.argv)

    invoker = CommandInvoker()
    invoker.invoke(command)

if __name__ == "__main__":
    main()
