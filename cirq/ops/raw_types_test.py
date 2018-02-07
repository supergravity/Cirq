# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from cirq import ops
from cirq.testing import EqualsTester


def test_qubit_id_init():
    q = ops.QubitLoc(3, 4)
    assert q.x == 3
    assert q.y == 4


def test_qubit_id_eq():
    eq = EqualsTester()
    eq.make_equality_pair(lambda: ops.QubitLoc(0, 0))
    eq.make_equality_pair(lambda: ops.QubitLoc(1, 0))
    eq.make_equality_pair(lambda: ops.QubitLoc(0, 1))
    eq.make_equality_pair(lambda: ops.QubitLoc(50, 25))


def test_qubit_id_is_adjacent():
    assert ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(0, 1))
    assert ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(0, -1))
    assert ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(1, 0))
    assert ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(-1, 0))

    assert not ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(+1, -1))
    assert not ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(+1, +1))
    assert not ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(-1, -1))
    assert not ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(-1, +1))

    assert not ops.QubitLoc(0, 0).is_adjacent(ops.QubitLoc(2, 0))

    assert ops.QubitLoc(500, 999).is_adjacent(ops.QubitLoc(501, 999))
    assert not ops.QubitLoc(500, 999).is_adjacent(ops.QubitLoc(5034, 999))


def test_gate_calls_validate():
    class ValiGate(ops.Gate):
        # noinspection PyMethodMayBeStatic
        def validate_args(self, qubits):
            if len(qubits) == 3:
                raise ValueError()

    g = ValiGate()
    q00 = ops.QubitLoc(0, 0)
    q01 = ops.QubitLoc(0, 1)
    q10 = ops.QubitLoc(1, 0)

    _ = g.on(q00)
    _ = g.on(q01)
    _ = g.on(q00, q10)
    with pytest.raises(ValueError):
        _ = g.on(q00, q10, q01)

    _ = g(q00)
    _ = g(q00, q10)
    with pytest.raises(ValueError):
        _ = g(q10, q01, q00)


def test_operation_init():
    q = ops.QubitLoc(4, 5)
    g = ops.Gate()
    v = ops.Operation(g, (q,))
    assert v.gate == g
    assert v.qubits == (q,)


def test_operation_eq():
    g1 = ops.Gate()
    g2 = ops.Gate()
    r1 = [ops.QubitLoc(1, 2)]
    r2 = [ops.QubitLoc(3, 4)]
    r12 = r1 + r2
    r21 = r2 + r1

    eq = EqualsTester()
    eq.make_equality_pair(lambda: ops.Operation(g1, r1))
    eq.make_equality_pair(lambda: ops.Operation(g2, r1))
    eq.make_equality_pair(lambda: ops.Operation(g1, r2))
    eq.make_equality_pair(lambda: ops.Operation(g1, r12))
    eq.make_equality_pair(lambda: ops.Operation(g1, r21))