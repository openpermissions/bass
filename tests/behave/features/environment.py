# -*- coding: utf-8 -*-

# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

"""
Python Behave configuration file

Start the Identity service up before running all the tests.
Then restores the DB to its initial state (please see ../../Makefile)

"""


import logging
import os


REPORT_DIR = os.path.join(os.path.dirname(__file__), '../reports')
ROOT_DIR = os.path.join(os.path.dirname(__file__), '../../..')


def before_scenario(context, scenario):
    """Add entry to the debug log befere starting the scenario
    """
    context.log.debug(
        "\n===============================================================\n"
        "Starting scenario: '%s'\n"
        "================================================================"
        % scenario.name)
    # Initialise context
    context.params = {}
    context.exception = None
    context.result = None


def after_scenario(context, scenario):
    """Add an entry to the debug log after scenario was finished
    """
    context.log.debug(
        "\n===============================================================\n"
        "Finished scenario: '%s'\n"
        "================================================================\n"
        % scenario.name)


def before_all(context):
    """
    Executes the code before all the tests are run
    """
    context.log = _setup_logging()


def _setup_logging():
    """
    set up the logging facility
    """
    # get logger
    log = logging.getLogger('identity_service.Behave')
    # create file handler which logs even debug messages
    # overwrite the old log file
    fh = logging.FileHandler(
        filename='{}/behave-debug.log'.format(REPORT_DIR), mode='w')
    # create console handler with a higher log level
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        '%a %Y-%m-%d %H:%M:%S %z')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    log.addHandler(ch)
    log.addHandler(fh)
    # if not context.config.log_capture:
    # logging.basicConfig(level=logging.DEBUG)
    return log
