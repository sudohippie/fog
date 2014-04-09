__author__ = 'Raghav Sidhanti'

from fog.inout import StdOut


# should run successfully and print to screen
def display_simple_template_no_args():
    msg = 'hello, world!'
    StdOut.display(template=StdOut.IND2, msg=msg)

if __name__ == '__main__':
    display_simple_template_no_args()

