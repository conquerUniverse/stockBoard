# Basic Tests Of Core functionality
import pytest

from scripts.StockData import StockData


def test_sanity_run():
    assert 2==2

def test_dataLoad():
    sd = StockData('alvin369')
    sd.load()
    assert sd.isDataLoaded,"load failed"

def test_dataLoad_invalid_location():
    with pytest.raises(AssertionError):
        StockData('xxxxx')
