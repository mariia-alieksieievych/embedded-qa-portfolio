import pytest

@pytest.mark.parametrize("command", ["SET PWM ", "SET PWM80", "SET PWM", "set pwm 20"])
def test_invalid_pwm(device, command):
    r = device.command(command)
    assert r["status"] == "ERROR"
    assert r["code"] == "UNKNOWN_COMMAND"

@pytest.mark.parametrize("command", ["SET LED", "SET LED ", "SET LED 40", "SET LED ONOFF", "set led on"])
def test_invalid_led(device,command):
    r = device.command(command)
    assert r["status"] == "ERROR"
    assert r["code"] == "UNKNOWN_COMMAND"

@pytest.mark.parametrize("command", ["ping", "status", "GET TEMP 50", "reset", "UNKNOWN_COMMAND", " "])
def test_invalid_commands(device, command): 
    r = device.command(command)
    assert r["status"] == "ERROR"
    assert r["code"] == "UNKNOWN_COMMAND"