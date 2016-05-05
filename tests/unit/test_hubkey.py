# -*- coding: utf-8 -*-

# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
"""Unit tests for module create_ids
"""
from itertools import product

from bass.hubkey import *
import pytest

# This is not exhaustive, add more examples as they arise
_PATH_PARTS = ('provider_id', 'id_type', 'id')
_PATH_CHARACTERS = '.-_~!$&\'()*+,;=:@'

VALID_PATH_PARTS = [('test' + c, p) for p, c in
                    product(_PATH_PARTS, _PATH_CHARACTERS)]

VALID_PATH_PARTS.extend([('test' + '%6F', p) for p in _PATH_PARTS])

VALID_PARTS = [
    ('https://openpermissions.org', 'resolver_id'),
    ('https://openpermissions.com', 'resolver_id'),
    ('https://open.perm.issions', 'resolver_id'),
    ('https://localhost', 'resolver_id'),
    ('https://localhost:8006', 'resolver_id'),
    ('https://open-permissions', 'resolver_id'),
    ('https://OPENPERMissions', 'resolver_id'),
    ('https://openpermissions1', 'resolver_id'),
    ('https://9openpermissions', 'resolver_id'),
    ('https://xn--maryevns-eza', 'resolver_id'),  # maryeváns idna encoded
    ('s1', 'schema_version'),
    ('chf', 'hub_id'),
    ('hub1', 'hub_id'),
    ('HUB1', 'hub_id'),
    ('maryev%C3%A1ns', 'hub_id'),  # maryeváns % encoded
    (SCHEMA, 'schema_version'),
    ('asset', 'entity_type'),
    ('offer', 'entity_type'),
    ('agreement', 'entity_type'),
    ('37cd1397e0814e989fa22da6b15fec60', 'repository_id'),
    ('10e4b9612337f237118e1678ec001fa6', 'repository_id'),
    ('37cd1397e0814e989fa22da6b15fec60', 'entity_id'),
    ('10e4b9612337f237118e1678ec001fa6', 'entity_id'),
]

INVALID_PARTS = [
    ('https://test:string', 'resolver_id'),
    ('https://test:', 'resolver_id'),
    ('https://test:1', 'resolver_id'),
    ('https://test:123456', 'resolver_id'),
    ('https://test.com#anchor', 'resolver_id'),
    ('https://test.com/osteuhs', 'resolver_id'),
    ('https://test com', 'resolver_id'),
    ('https://-test.com', 'resolver_id'),
    ('https://test.com-', 'resolver_id'),
    ('https://test-.com', 'resolver_id'),
    ('https://test-', 'resolver_id'),
    ('https://test-:80', 'resolver_id'),
    (u'https://maryeváns', 'resolver_id'),
    ('https://maryev%C3%A1ns', 'resolver_id'),  # maryeváns % encoded
    ('', 'resolver_id'),
    ('openpermissions.org', 'resolver_id'),
    (SCHEMA + '1', 'schema_version'),
    ('', 'hub_id'),
    (u'maryeváns', 'hub_id'),
    ('assets', 'entity_type'),
    ('agreements', 'entity_type'),
    ('offers', 'entity_type'),
    (u'maryeváns', 'entity_type'),
    ('', 'entity_type'),
    (u'maryeváns', 'entity_type'),
    ('', 'entity_id'),
    (u'maryeváns', 'entity_id'),
]


@pytest.mark.parametrize('string,part', VALID_PARTS)
def test_match_valid_parts(string, part):
    match_part(string, part)


@pytest.mark.parametrize('string,part', INVALID_PARTS)
def test_match_invalid_parts(string, part):
    with pytest.raises(ValueError):
        match_part(string, part)


@pytest.mark.parametrize('string,expected', [
    ('maryevans', 'maryevans'),
    (u'maryeváns', 'xn--maryevns-eza'),
    (u'测试', 'xn--0zwm56d')
])
def test_idna_encode(string, expected):
    result = idna_encode(string)
    assert result == expected


@pytest.mark.parametrize('string,expected', [
    ('maryevans', 'maryevans'),
    (u'maryeváns', 'maryev%C3%A1ns')
])
def test_url_quote(string, expected):
    result = url_quote(string)
    assert result == expected


@pytest.mark.parametrize('hub_key', [
    'https://openpermissions.org/s1/chf/37cd1397e0814e989fa22da6b15fec60/asset/37cd1397e0814e989fa22da6b15fec60',
    'https://openpermissions.org/s1/chf/37cd1397e0814e989fa22da6b15fec60/offer/37cd1397e0814e989fa22da6b15fec60',
    'https://openpermissions.org/s1/chf/37cd1397e0814e989fa22da6b15fec60/agreement/37cd1397e0814e989fa22da6b15fec60',
    'https://openpermissions.org/s0/hub1/creation/maryevans/maryevanspictureid/10413373',
    'https://openpermissions.org/s0/hub1/asset/maryevans/maryevanspictureid/10413373',
    'https://openpermissions.org/s0/hub1/offer/maryevans/maryevansofferid/001',
])
def test_is_hub_key_passes(hub_key):
    assert is_hub_key(hub_key)


def test_is_hub_key_fails():
    assert not is_hub_key('1234')


def test_is_hub_key_fails_not_specified():
    assert not is_hub_key(None)


def test_is_hub_key_fails_missing_entity_id():
    assert not is_hub_key('https://openpermissions.org/s1/chf/37cd1397e0814e989fa22da6b15fec60/agreement')


def test_is_hub_key_fails_invalid_entity_type():
    assert not is_hub_key('https://openpermissions.org/s1/chf/37cd1397e0814e989fa22da6b15fec60/footype/e3cc6218db1711e5ab090242ac110013')


def test_parse_valid_hub_key_s0():
    parsed = parse_hub_key('https://openPerMissIoNS.org/S0/hUb1/creATion/4CoRnERs/4CoRnersPicTureID/ID-10413373')
    expected = {
        'resolver_id': 'https://openpermissions.org',
        'schema_version': 's0',
        'hub_id': 'hub1',
        'entity_type': 'creation',
        'organisation_id': '4corners',
        'id_type': '4cornerspictureid',
        'entity_id': 'ID-10413373',
    }
    assert parsed == expected


def test_parse_valid_hub_key_s1():
    parsed = parse_hub_key('https://openpermissions.org/s1/chf/37cd1397e0814e989fa22da6b15fec60/agreement/e3cc6218db1711e5ab090242ac110013')
    expected = {
        'resolver_id': 'https://openpermissions.org',
        'schema_version': 's1',
        'hub_id': 'chf',
        'repository_id': '37cd1397e0814e989fa22da6b15fec60',
        'entity_type': 'agreement',
        'entity_id': 'e3cc6218db1711e5ab090242ac110013',
    }
    assert parsed == expected


def test_invalid_schema():
    with pytest.raises(ValueError):
        key = 'https://resolver-id/schema1/chf/37cd1397e0814e989fa22da6b15fec60/agreement/e3cc6218db1711e5ab090242ac110013'
        parse_hub_key(key)


@pytest.mark.parametrize('part', [p for p in PARTS.keys() if p not in ['schema_version', 'referent_type']])
def test_parse_missing_string(part):
    if part == 'resolver_id':
        part = 'resolver-id'

    key = 'https://resolver-id/s0/hub_id/licensor/provider_id/id_type/id'.replace(part, '')
    with pytest.raises(ValueError):
        parse_hub_key(key)


def test_parse_hub_key_with_a_dash():
    key = 'https://resolver-id/s1/chf/37cd1397e0814e989fa22da6b15fec60/agreement/e3cc6218db1711e5ab090242ac110013'
    parsed = parse_hub_key(key)

    assert parsed['resolver_id'] == 'https://resolver-id'


def test_parse_empty_key():
    with pytest.raises(ValueError):
        parse_hub_key('/' * (len(PATTERN) - 1))


def test_parsing_generated_key():
    key = generate_hub_key(
        'https://a', 'h', '37cd1397e0814e989fa22da6b15fec60', 'agreement')
    parsed = parse_hub_key(key)
    parsed.pop('entity_id')

    assert parsed == {
        'resolver_id': 'https://a',
        'hub_id': 'h',
        'schema_version': SCHEMA,
        'repository_id': '37cd1397e0814e989fa22da6b15fec60',
        'entity_type': 'agreement',
    }


def test_generate_key_with_unicode():
    key = generate_hub_key(
        u'https://测试', u'hüb', u'37cd1397e0814e989fa22da6b15fec60', 'offer')
    parsed = parse_hub_key(key)
    parsed.pop('entity_id')

    assert parsed == {
        'resolver_id': 'https://xn--0zwm56d',
        'hub_id': 'h%C3%BCb',
        'schema_version': SCHEMA,
        'repository_id': '37cd1397e0814e989fa22da6b15fec60',
        'entity_type': 'offer',
    }


def test_generate_key_with_valid_entity_id():
    key = generate_hub_key(
        u'https://openpermissions.org',
        u'hub1',
        u'37cd1397e0814e989fa22da6b15fec6a',
        'asset',
        u'37cd1397e0814e989fa22da6b15fec6b'
    )
    parsed = parse_hub_key(key)

    assert parsed == {
        'resolver_id': 'https://openpermissions.org',
        'hub_id': 'hub1',
        'schema_version': SCHEMA,
        'repository_id': '37cd1397e0814e989fa22da6b15fec6a',
        'entity_type': 'asset',
        'entity_id': '37cd1397e0814e989fa22da6b15fec6b'
    }


def test_generate_key_with_invalid_entity_id():
    with pytest.raises(ValueError) as exc:
        generate_hub_key(
            u'https://openpermissions.org',
            u'hub1',
            u'37cd1397e0814e989fa22da6b15fec6a',
            'asset',
            u'invalidentityid'
        )
    error_msg = '{} should match {}'.format('entity_id', PARTS['entity_id'])
    assert exc.value.message == error_msg
