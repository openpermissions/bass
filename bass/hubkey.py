# -*- coding: utf-8 -*-

# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


"""Generate hub keys

The generated hub key will be of the format

<resolver_id>/<schema_version>/<hub_id>/<repository_id>/<entity_type>/<entity_id>
"""

import re
import uuid
from urlparse import urlparse, urlunparse
from urllib import quote
from collections import OrderedDict
from tornado.options import define, options

define('hub_id', default='hub1')
SEPARATOR = '/'
SCHEMA = 's1'
PROTOCOL = 'https'
ENTITY_TYPES = ['asset', 'offer', 'agreement']

_HOST_LABEL = r'(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])'
_PORT = r'(?::[0-9]{2,5})'
# Safe URL characters or percent encoded. See RFC3986 & RFC1738
_PATH_PART = r'(?:[a-zA-Z0-9\.\-_~!$&\'()*+,;=:@]|%[\da-fA-F]{2})+'
UUID = r'[0-9a-f]{1,64}' # < relaxed definition (useful for fake ids used in tests and in case of minor change of format)

# resolver_id must be a valid hostname, containing letters, digits or hyphens.
# Each label may not begin or end with a hyphen, and may not be more than
# 63 characters. Each label must be separated with a period.
# See RFC1123 & RFC952
# The hub_id may optionally contain a port, e.g. localhost:8000
RESOLVER_ID = r'{protocol}?://{label}(?:\.{label})*{port}?'.format(
    protocol=PROTOCOL, label=_HOST_LABEL, port=_PORT)

PARTS = OrderedDict([
    ('resolver_id', RESOLVER_ID),
    ('schema_version', SCHEMA),
    ('hub_id', options.hub_id),
    ('repository_id', UUID),
    ('entity_type', '|'.join(ENTITY_TYPES)),  # word char or -
    ('entity_id', UUID)  # word char or -
])

# Support for s0 hub key format
PARTS_S0 = OrderedDict([
    ('resolver_id', RESOLVER_ID),
    ('schema_version', '(?i)s0'),
    ('hub_id', options.hub_id),
    ('entity_type', '|'.join(['(?i)creation', '(?i)asset', '(?i)offer'])),
    ('organisation_id', _PATH_PART),
    ('id_type', _PATH_PART),
    ('entity_id', _PATH_PART)
])

PATTERN = '^' + SEPARATOR.join(
    ['(?P<{}>{})'.format(p, r) for p, r in PARTS.items()]) + '$'

PATTERN_S0 = '^' + SEPARATOR.join(
    ['(?P<{}>{})'.format(p, r) for p, r in PARTS_S0.items()]) + '$'


def normalise_part(t):
    k, v = t
    if k != 'entity_id':
        return k, v.lower()
    else:
        return k, v


def parse_hub_key(key):
    """Parse a hub key into a dictionary of component parts

    :param key: str, a hub key
    :returns: dict, hub key split into parts
    :raises: ValueError
    """
    if key is None:
        raise ValueError('Not a valid key')

    match = re.match(PATTERN, key)
    if not match:
        match = re.match(PATTERN_S0, key)
        if not match:
            raise ValueError('Not a valid key')

        return dict(map(normalise_part, zip([p for p in PARTS_S0.keys()], match.groups())))

    return dict(zip(PARTS.keys(), match.groups()))


def is_hub_key(value):
    """Test if a value could be a hub key
    :param value: the value to test if it is a hub key
    :returns: True if it is a hub key
    """
    try:
        parse_hub_key(value)
        return True
    except (ValueError, TypeError):
        return False


def match_part(string, part):
    """Raise an exception if string doesn't match a part's regex

    :param string: str
    :param part: a key in the PARTS dict
    :raises: ValueError, TypeError
    """
    if not string or not re.match('^(' + PARTS[part] + ')$', string):
        raise ValueError('{} should match {}'.format(part, PARTS[part]))


def idna_encode(string):
    """Encode a string as ASCII using IDNA so that it is a valid part of a URI

    See RFC3490.

    :param string: str
    :returns: ASCII string
    """
    return string.encode('idna').decode('ascii')


def url_quote(string):
    """Percent encode a string as ASCII so that it is a valid part of a URI

    :param string: str
    :returns: ASCII string
    """
    return quote(string.encode('utf8'), safe=':/')


def generate_hub_key(resolver_id, hub_id, repository_id, entity_type, entity_id=None):
    """Create and return an array of hub keys
    :param resolver_id: the service that can resolve this key
    :param hub_id: the unique id of the hub
    :param repository_id: the type of id that the provider recognises
    :param entity_type: the type of the entity to which the key refers.
    :param entity_id: ID of entity (UUID)
    :returns: a hub key
    :raises:
    :AttributeError: if a parameter has a bad value
    :TypeError: if a parameter has a bad value
    :ValueError: if a parameter has a bad value
    """
    parsed = urlparse(resolver_id)
    if not parsed.scheme:
        parsed = parsed._replace(scheme=PROTOCOL, netloc=idna_encode(parsed.path.lower()), path=u'')
    else:
        parsed = parsed._replace(netloc=idna_encode(parsed.netloc.lower()))

    resolver_id = urlunparse(parsed)

    hub_id = url_quote(hub_id.lower())

    if not entity_id:
        entity_id = str(uuid.uuid4()).replace('-', '')
    else:
        match_part(entity_id, 'entity_id')

    # If any of these checks fail a ValueError exception is raised
    match_part(resolver_id, 'resolver_id')
    match_part(hub_id, 'hub_id')
    match_part(repository_id, 'repository_id')
    match_part(entity_type, 'entity_type')

    hub_key = SEPARATOR.join(
        [resolver_id, SCHEMA, hub_id, repository_id, entity_type, entity_id])
    return hub_key
