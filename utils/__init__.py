"""Utility module shared by the SDK unit tests."""

from __future__ import absolute_import
from utils.cmdopts import *
from splunklib import six

def config(option, opt, value, parser):
    assert opt == "--config"
    parser.load(value)

# Default Splunk cmdline rules
RULES_SPLUNK = {
    'config': {
        'flags': ["--config"],
        'action': "callback",
        'callback': config,
        'type': "string",
        'nargs': "1",
        'help': "Load options from config file" 
    },
    'scheme': {
        'flags': ["--scheme"],
        'default': "https",
        'help': "Scheme (default 'https')",
    },
    'host': {
        'flags': ["--host"],
        'default': "localhost",
        'help': "Host name (default 'localhost')" 
    },
    'port': { 
        'flags': ["--port"],
        'default': "8089",
        'help': "Port number (default 8089)" 
    },
    'app': {
        'flags': ["--app"], 
        'help': "The app context (optional)"
    },
    'owner': {
        'flags': ["--owner"], 
        'help': "The user context (optional)"
    },
    'username': {
        'flags': ["--username"],
        'default': None,
        'help': "Username to login with" 
    },
    'password': {
        'flags': ["--password"], 
        'default': None,
        'help': "Password to login with" 
    },
    'version': {
        'flags': ["--version"],
        'default': None,
        'help': 'Ignore. Used by JavaScript SDK.'
    },
    'splunkToken': {
        'flags': ["--bearerToken"],
        'default': None,
        'help': 'Bearer token for authentication'
    },
    'token': {
        'flags': ["--sessionKey"],
        'default': None,
        'help': 'Session key for authentication'
    }
}

FLAGS_SPLUNK = list(RULES_SPLUNK.keys())

# value: dict, args: [(dict | list | str)*]
def dslice(value, *args):
    """Returns a 'slice' of the given dictionary value containing only the
       requested keys. The keys can be requested in a variety of ways, as an
       arg list of keys, as a list of keys, or as a dict whose key(s) represent
       the source keys and whose corresponding values represent the resulting 
       key(s) (enabling key rename), or any combination of the above.""" 
    result = {}
    for arg in args:
        if isinstance(arg, dict):
            for k, v in six.iteritems(arg):
                if k in value: 
                    result[v] = value[k]
        elif isinstance(arg, list):
            for k in arg:
                if k in value: 
                    result[k] = value[k]
        else:
            if arg in value: 
                result[arg] = value[arg]
    return result

def parse(argv, rules=None, config=None, **kwargs):
    """Parse the given arg vector with the default Splunk command rules."""
    parser_ = parser(rules, **kwargs)
    if config is not None:
        parser_.loadenv(config)
    return parser_.parse(argv).result

def parser(rules=None, **kwargs):
    """Instantiate a parser with the default Splunk command rules."""
    rules = RULES_SPLUNK if rules is None else dict(RULES_SPLUNK, **rules)
    return Parser(rules, **kwargs)

