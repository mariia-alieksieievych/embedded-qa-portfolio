import pytest

@pytest.mark.parametrize("times", [2, 5, 10])
def test_led_on_repeated(device, times):
    for _ in range(times):
        r = device.command ("SET LED ON")
        assert r["status"] == "OK"
        assert r["led"] is True

@pytest.mark.parametrize("times", [2, 5, 10])
def test_reset_repeated(device, times):
    for _ in range(times):
        r = device.command("RESET")
        assert r["status"] == "OK"
        assert r["reset"] is True

@pytest.mark.parametrize("times", [2, 5, 10])
def test_temp_repeated(device, times):
    for _ in range(times):
        r = device.command("GET TEMP")
        assert r["status"] in {"OK", "ERROR"}
        if r["status"] == "OK":
            assert -40 <= r["temperature"] <= 80