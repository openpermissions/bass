# -*- coding: utf-8 -*-

# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from behave import given, when, then
from bass.hubkey import generate_hub_key, parse_hub_key, PARTS, is_hub_key
import re


@given(u'parameter "{param}" is "{value}"')
def set_param(context, param, value):
    context.params[param] = value


@given(u'parameter "ids" is array "{ids}"')
def id_is_array(context, ids):
    context.params['ids'] = ids.split(',')


@given(u'parameter "{param}" is overwritten to an empty string')
def all_params_valid_except_one(context, param):
    context.params[param] = ""


@when(u'I generate a hub key')
def generate_a_hub_key(context):
    try:
        context.hub_key = generate_hub_key(**context.params)
    except AttributeError as context.exception:
        pass
    except TypeError as context.exception:
        pass
    except ValueError as context.exception:
        pass


@then(u'no exception should be thrown')
def no_exception_thrown(context):
    assert not context.exception, (
        'Exception not expected. Exception message = {}'.format(context.exception.message)
    )


@then(u'a "{exception_type}" for the "{param}" should be thrown')
def value_error_exception(context, exception_type, param):
    exc_mapper = {
        'value error': ValueError,
        'attribute error': AttributeError,
        'type error': TypeError
    }
    msg = '{} should match {}'.format(param, PARTS[param])
    assert isinstance(context.exception, exc_mapper[exception_type])
    assert context.exception.message == msg


@then(u'the hub key should start with "{start}"')
def entry_in_array_startswith(context, start):
    assert context.hub_key.startswith(start), (
        'Expected "{}" to start with "{}"'.format(context.hub_key, start)
    )


@then(u'the hub key should have a uuid as entity id')
def check_entity_id(context):
    uuid_regex = re.compile('[0-9a-f]{32}\Z', re.I)
    parsed = parse_hub_key(context.hub_key)
    assert re.match(uuid_regex, parsed['entity_id'])


@then(u'the hub key should have "{entity_type}" as entity type')
def check_entity_type(context, entity_type):
    parsed = parse_hub_key(context.hub_key)
    assert parsed['entity_type'] == entity_type


@then(u'a valid hub key should be returned')
def check_entity_type(context):
    assert is_hub_key(context.hub_key)
