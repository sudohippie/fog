__author__ = 'Raghav Sidhanti'

from string import Template

# info
REMOTE_EXISTS = '$drive is tracked. Try "remote rm" to un-track and try again or $help.'
HOME_EXISTS = 'Already initialized, configuration will be overwritten.'
HELP = '"help" for usage'
MARK = '*'
NO_MARK = ' '
STATUS = '[$mark] $drive'
GOOGLE_ID = 'Enter Google client id:'
GOOGLE_SECRET = 'Enter Google client secret:'
GOOGLE_CONSENT = 'Google requires your consent. Check your default browser to accept access privileges.'
OVERWRITE = 'File $file exists and will be overwritten.'
YES = 'yes'
NO = 'no'

# prompt
PROMPT = '$info Continue ($yes/$no)?:'

# error
MISSING_FILE = 'File not found on $location.'
MISSING_REMOTE = '$drive is not tracked. Try "remote add" to track and try again or $help.'
MISSING_CHECKOUT = 'No checkout. Try $help.'
MISSING_HOME = 'Not a fog directory (missing .fog). Try "init" to initialize or $help.'
MISSING_IMPLEMENTATION = 'Unfortunately $drive is not yet implemented. We are working on it.'
INVALID_DRIVE_NAME = 'Invalid drive $drive. Try "branch" for drive names or $help.'
INVALID_ARGS = 'Invalid input argument(s). Try $help.'
INVALID_CREDENTIALS = 'Invalid credentials.'


def get(msg, **kwargs):

    if kwargs is None:
        kwargs = {}

    if kwargs.get('help', None) is None:
        kwargs['help'] = HELP
    if kwargs.get('yes', None) is None:
        kwargs['yes'] = YES
    if kwargs.get('no', None) is None:
        kwargs['no'] = NO

    s = Template(msg)
    return s.substitute(kwargs)
