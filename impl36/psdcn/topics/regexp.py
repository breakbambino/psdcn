"""
Topic matcher by rewriting into regular expressions
"""

import re as regexp
from .table import Table

class Regexp(Table):
    def __init__(self):
        super().__init__()

    def _do_match(self, topic, dataname):
        return do_match(topic, dataname)
# class Regexp

def do_match(topic, dataname):
    match = False
    if topic.find('+') == topic.find('#') == -1:
        # No wildcards, so check is simple
        match = (topic == dataname)
    else:
        # We have wildcards. Escape metacharacters, except +
        metachars = '\\.^*?{[]|()'  # Make sure \\ is at beginning of this string
        for c in metachars:
            topic = topic.replace(c, '\\'+c)
        # Now replace wildcards with regular expressions and match
        if topic == '#':
            "# on its own matches everything"
            topic = '.*'
        elif topic == '/#':
            "/# matches everything starting with a slash"
            topic = '/.*'
        else:
            "All other instances subsume the preceding or following slash"
            topic = topic.replace('#/', '(.*?/|^)').replace('/#', '(/.*?|$)')
        topic = topic.replace('+', '[^/#]+?')     # + does not match an empty level
        if regexp.compile(topic+'$').match(dataname) != None:
            match = True
    return match
