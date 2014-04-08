__author__ = 'Raghav Sidhanti'

from fog.inout import StdOut


# should run successfully and print to screen
def display_simple_template_no_args():
    msg = 'hello, world!'
    StdOut.template_display(msgs=msg)


# must print something like: TypeError: not all arguments converted during string formatting
def display_simple_template_with_args():
    args = ('h', 'e', 'l', 'l')
    StdOut.template_display(msgs=args)


# should run successfully but nothing should be printed
def display_nonexistent_template():
    template = 'nonexistent'
    StdOut.template_display(template=template)


if __name__ == '__main__':
    display_nonexistent_template()
    #display_simple_template_no_args()
    #display_simple_template_with_args()

