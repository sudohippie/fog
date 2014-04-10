__author__ = 'Raghav Sidhanti'

import sys

from command import CommandParser
from command import CommandInvoker


def main():
    # parse arguments and get command
    parser = CommandParser()
    command = parser.parse(sys.argv[1:])

    # execute command
    invoker = CommandInvoker()
    invoker.invoke(command)

if __name__ == "__main__":
    main()
