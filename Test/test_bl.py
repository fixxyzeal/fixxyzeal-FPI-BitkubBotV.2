from BL.trading import *


def test_GetPrice():
    assert GetPrice("THB_BTC") > 0


def test_GetMyBalances():
    assert any(GetMyBalances())


def test_GetMyOrder():
    assert any(GetMyOrder('THB_SNT'))


def test_CancelOrder():
    assert CancelOrder('') > 0


def test_SellOrder():
    assert SellOrder('', 0, 0) > 0


def test_BuyOrder():
    assert BuyOrder('', 0, 0) > 0


def test_Trading():
    assert Trading("GALA", 0.1, 1, 0.05) == "OK"
