# Device Requirements — ESP32 IoT Controller

## System under test
Навчальний IoT-контролер на ESP32:
- DHT22 — датчик;
- кнопка — локальний input;
- LED + relay — output;
- UART/Serial CLI;
- NVS/Preferences — persistent state.

## R1 — Boot
Після старту пристрій переходить у `ACTIVE` та виводить причину reset.

## R2 — Sensor failure
Якщо DHT22 недоступний або повертає некоректні дані:
- firmware не повинна трактувати це як валідне вимірювання;
- у логах має бути явна помилка;
- actuator не повинен переходити у небезпечний стан через invalid data.

## R3 — Button
Один фізичний натиск кнопки повинен створити не більше однієї логічної події.

## R4 — Sleep / Wake
Команда `sleep <N>` переводить пристрій у deep sleep приблизно на N секунд.

Acceptance:
- похибка wake-up ±15%;
- після wake-up пристрій працездатний;
- persistent data залишаються цілісними.

## R5 — Watchdog
Команда `hang` навмисно зависає firmware.

Acceptance:
- WDT перезавантажує пристрій приблизно не пізніше ніж за 5 секунд;
- reset reason дозволяє визначити WDT reset;
- після reset пристрій працездатний;
- actuator після аварійного reset має бути OFF;
- boot loop відсутній.

## R6 — Interrupted save
Команда `powerloss` моделює reboot у критичний момент запису.

Acceptance:
- після reboot має залишитися стара повністю валідна або нова повністю валідна версія стану;
- змішаний/частково оновлений state не допускається;
- corrupted state має виявлятися.

> У Wokwi це fault injection переривання запису, а не аналогове моделювання реального brown-out.

## R7 — Observable evidence
`status` має давати QA:
- state;
- reset reason;
- relay state;
- event counter;
- free heap;
- sensor status.
