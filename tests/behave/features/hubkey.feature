# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

Feature: Creating hub key is successful

  Background:
    Given parameter "resolver_id" is "copyrighthub.org"
    Given parameter "hub_id" is "hub1"


  Scenario Outline: create a valid "<entity_type>" hub key
    Given parameter "repository_id" is "92bc723b1eb04b7fa13a5879b1ee990a"
      And parameter "entity_type" is "<entity_type>"

     When I generate a hub key

     Then no exception should be thrown
      And a valid hub key should be returned
      And the hub key should start with "https://copyrighthub.org/s1/hub1/92bc723b1eb04b7fa13a5879b1ee990a/"
      And the hub key should have "<entity_type>" as entity type
      And the hub key should have a uuid as entity id

    Examples:
    |entity_type      |
    |asset            |
    |offer            |
    |agreement        |


  Scenario Outline: generate a hub key with a missing parameter
    Given parameter "repository_id" is "92bc723b1eb04b7fa13a5879b1ee990d"
      And parameter "entity_type" is "asset"
      And parameter "<param>" is overwritten to an empty string

    When I generate a hub key
    Then a "<exception>" for the "<param>" should be thrown

    Examples:
    |param         |exception  |
    |resolver_id   |value error|
    |hub_id        |value error|
    |repository_id |value error|
    |entity_type   |value error|
