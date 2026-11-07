# pytest/

Автотести Python для CLI пристрою (робота 06): 49 тестів, із них 14 надані ментором і 35 власних.

**Що міститься:** папку `automation/`: тести `test_boundaries.py`, `test_commands.py`, `test_repeated.py`, `test_relay.py`, `test_sensor.py`, `conftest.py`, `device.py`, `requirements.txt`.

**Запуск (приклад):**

```
python -m venv .venv
source .venv/bin/activate
pip install pytest pyserial
pytest -v
```

Wokwi-проєкт має бути запущений і слухати порт `rfc2217://localhost:4000` (`DEVICE_PORT`). 
