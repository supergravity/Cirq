# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import cirq
from cirq.contrib.quirk.cells.testing import assert_url_to_circuit_returns
from cirq.contrib.quirk.url_to_circuit import quirk_url_to_circuit


def test_gate_type_swap():
    a, b, c = cirq.LineQubit.range(3)
    assert_url_to_circuit_returns('{"cols":[["Swap","Swap"]]}',
                                  cirq.Circuit(cirq.SWAP(a, b)))
    assert_url_to_circuit_returns('{"cols":[["Swap","X","Swap"]]}',
                                  cirq.Circuit(cirq.SWAP(a, c), cirq.X(b)))

    with pytest.raises(ValueError, match='number of swap gates'):
        _ = quirk_url_to_circuit(
            'https://algassert.com/quirk#circuit={"cols":[['
            '"Swap"]]}')
    with pytest.raises(ValueError, match='number of swap gates'):
        _ = quirk_url_to_circuit(
            'https://algassert.com/quirk#circuit={"cols":[['
            '"Swap","Swap","Swap"]]}')
