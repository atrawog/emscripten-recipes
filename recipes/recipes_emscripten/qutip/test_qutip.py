""" Smoke tests for the built qutip package. """
import pytest

def assert_qobj_data(q, data, normalize_sign=False):
    """ Assert that a qobj has the given values. """
    import numpy as np
    if normalize_sign:
        sign = np.sign(q.full()[0, 0])
        q = sign * q
    np.testing.assert_allclose(q.full(), data)


def assert_array_data(a, data):
    """ Assert that a numpy array has the given values. """
    import numpy as np
    np.testing.assert_allclose(a, data)


def test_qobj_create():
    from qutip import Qobj

    q = Qobj([[1, 2j], [-2j, 2]])
    assert q.type == "oper"
    assert q.shape == (2, 2)
    assert q.dims == [[2], [2]]
    assert q.isherm is True
    assert_qobj_data(q, [
        [1, 2j],
        [-2j, 2],
    ])

def test_qobj_arithmetic():
    from qutip import Qobj

    op1 = Qobj([[0, 1], [1j, 0]])
    op2 = Qobj([[1, 2j], [-2j, 1]])
    psi = Qobj([[1], [2]])

    assert_qobj_data(op1 * 2, [
        [0, 2],
        [2j, 0],
    ])
    assert_qobj_data(op1 / 2, [
        [0, 0.5],
        [0.5j, 0],
    ])
    assert_qobj_data(op2 + op2, [
        [2, 4j],
        [-4j, 2],
    ])
    assert_qobj_data(op2 + op2, [
        [2, 4j],
        [-4j, 2],
    ])
    assert_qobj_data(op2 - op1, [
        [1, -1+2j],
        [-3j, 1],
    ])
    assert_qobj_data(op1 * op2, [
        [-2j, 1],
        [1j, -2],
    ])
    assert_qobj_data(op1 * psi, [
        [2],
        [1j],
    ])
    assert_qobj_data(op1 ** 2, [
        [1j, 0],
        [0, 1j],
    ])

def test_qobj_methods():
    import pytest
    from qutip import Qobj

    op = Qobj([[1, 2j], [-2j, 2]])

    assert_qobj_data(op.conj(), [
        [1, -2j],
        [2j, 2],
    ])
    assert_qobj_data(op.copy(), [
        [1, 2j],
        [-2j, 2],
    ])
    assert_qobj_data(op.dag(), [
        [1, 2j],
        [-2j, 2],
    ])
    assert_array_data(op.diag(), [1, 2])
    assert_array_data(op.eigenenergies(), [-0.56155281,  3.56155281])
    evals, [ev0, ev1] = op.eigenstates()
    assert_array_data(evals, [-0.56155281,  3.56155281])
    assert_qobj_data(ev0, [
        [0.78820544],
        [0.61541221j],
    ], normalize_sign=True)
    assert_qobj_data(ev1, [
        [0.61541221],
        [-0.78820544j],
    ], normalize_sign=True  )
    assert_qobj_data(op.expm(), [
        [13.6924533, 16.80651518j],
        [-16.80651518j, 22.09571089],
    ])
    assert_qobj_data(op.inv(), [
        [-1, 1.j],
        [-1.j, -0.5],
    ])
    assert op.norm() == pytest.approx(4.123105625617661)
    assert op.tr() == 3
    assert_qobj_data(op.trans(), [
        [1, -2j],
        [2j, 2],
    ])
    assert_qobj_data(op.unit(), [
        [0.24253563, 0.48507125j],
        [-0.48507125j, 0.48507125],
    ])

def test_qobj_creators():
    from qutip import coherent, destroy, sigmax

    assert_qobj_data(coherent(3, 0.25j), [
        [0.96923524],
        [0.24226042j],
        [-0.04350794],
    ])
    assert_qobj_data(destroy(3), [
        [0, 1, 0],
        [0, 0, 1.41421356],
        [0, 0, 0],
    ])
    assert_qobj_data(sigmax(), [
        [0, 1],
        [1, 0],
    ])


def test_qobjevo_create():
    from qutip import QobjEvo, sigmax
    import numpy as np

    q = QobjEvo([[sigmax(), "sin(w * t)"]], args={"w": 0.5})

    assert q.type == "oper"
    assert q.isconstant is False

    assert_qobj_data(q(0), [
        [0, 0],
        [0, 0],
    ])
    assert_qobj_data(q(np.pi), [
        [0, 1],
        [1, 0],
    ])


def test_qobjevo_arithmetic():
    from qutip import Qobj, QobjEvo, sigmax
    import numpy as np

    op1 = QobjEvo([[sigmax(), "sin(w * t)"]], args={"w": 0.5})
    op2 = Qobj([[1j, 0], [0, 1j]])
    psi = Qobj([[1], [2]])

    assert_qobj_data((op1 * 2)(np.pi), [
        [0, 2],
        [2, 0],
    ])
    assert_qobj_data((op1 / 2)(np.pi), [
        [0, 0.5],
        [0.5, 0],
    ])
    assert_qobj_data((op1 + op1)(np.pi), [
        [0, 2],
        [2, 0],
    ])
    assert_qobj_data((op2 - op1)(np.pi), [
        [1j, -1],
        [-1, 1j],
    ])
    assert_qobj_data((op1 * op2)(np.pi), [
        [0, 1j],
        [1j, 0],
    ])
    assert_qobj_data((op1 * psi)(np.pi), [
        [2],
        [1],
    ])


def test_qobjevo_methods():
    from qutip import Qobj, QobjEvo
    import numpy as np

    q = Qobj([[1, 2j], [-2j, 2]])
    op = QobjEvo([[q, "sin(w * t)"]], args={"w": 0.5})

    assert_qobj_data(op.conj()(np.pi), [
        [1, -2j],
        [2j, 2],
    ])
    assert_qobj_data(op.copy()(np.pi), [
        [1, 2j],
        [-2j, 2],
    ])
    assert_qobj_data(op.dag()(np.pi), [
        [1, 2j],
        [-2j, 2],
    ])
    assert_qobj_data(op.trans()(np.pi), [
        [1, -2j],
        [2j, 2],
    ])

def test_sesolve():
    from qutip import sesolve, sigmax, ket
    import numpy as np

    H = sigmax()
    psi0 = ket("0")
    tlist = [0, np.pi]
    result = sesolve(H, psi0, tlist)

    state0, state1 = result.states

    assert_qobj_data(state0, [
        [1],
        [0],
    ])

    assert_qobj_data(state1, [
        [-1],
        [2.10062817e-06j],
    ])

def test_mesolve():
    from qutip import mesolve, sigmax, sigmaz, ket
    import numpy as np

    H = sigmax()
    c_ops = [sigmaz()]
    psi0 = ket("0")
    tlist = [0, np.pi]
    result = mesolve(H, psi0, tlist, c_ops=c_ops)

    state0, state1 = result.states

    assert_qobj_data(state0, [
        [1, 0],
        [0, 0],
    ])

    assert_qobj_data(state1, [
        [0.5050889527242259, -0.018608253517938968j],
        [0.018608253517938968j, 0.4949110472757741],
    ])
