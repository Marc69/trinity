# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Import python libs
import ast


def render(json_data, saltenv='base', sls='', **kws):
    '''
Accepts JSON as a string or as a file object and runs it through the JSON
parser.

:rtype: A Python data structure
'''
    if not isinstance(json_data, basestring):
        json_data = json_data.read()

    if json_data.startswith('#!'):
        json_data = json_data[(json_data.find('\n') + 1):]
    if not json_data.strip():
        return {}
    return ast.literal_eval(json_data)
