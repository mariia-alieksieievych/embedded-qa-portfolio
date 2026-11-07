import pytest

@pytest.mark.parametrize("value", [0, 1, 50, 99, 100])
def test_pwm_valid_boundaries(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "OK"
    assert r["pwm"] == value

@pytest.mark.parametrize("value", [-1, 101, 999])
def test_pwm_invalid_boundaries(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"

# My tests 

@pytest.mark.parametrize("value", [20.1, "value", "?", "20 60", "🫡", [90, 60], "0x10"] )
def test_pwm_invalid_values(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"

@pytest.mark.parametrize("value", [2147483647, 2147483648, 4294967296, 888222010101010101010101002302382737237723727372737273727372737272737273727372737237273])
def test_pwm_huge_values(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"
