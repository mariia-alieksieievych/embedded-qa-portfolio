# Bug reports — індекс дефектів

Повні баг-репорти (кроки, expected / actual, середовище, evidence) лежать у test sheets у підпапках до кожної роботи. Тут — зведений індекс.

**Про ID.** У вихідних звітах ID повторюються між роботами (BUG-001, BUG-01, Bug-01). Тому повний ID тут = префікс роботи + оригінальний ID зі звіту:

| Префікс | Робота | Папка |
|---|---|---|
| `GATE` | Smart Gate Controller | [01-smart-gate](01-smart-gate/) |
| `DEB`| Debounce| [02-debounce](02-debounce/) |
| `CLI` | UART CLI | [03-uart-cli](03-uart-cli/) |
| `I2C` | I2C (MPU6050) | [04-i2c-mpu6050](04-i2c-mpu6050/) |
| `REC` | Recovery / Fault Injection | [05-recovery](05-recovery/) |
| `PYT` | Python / Pytest | [06-pytest](06-pytest/) |
| `IOT` | IoT Network / Memory | [07-iot-node](07-iot-node/) |

**Підсумок:** 27 дефектів — 10 Critical, 14 Major, 3 Medium / Minor; плюс 3 observations (не підтверджені без реального заліза). Статус усіх дефектів: відкриті.

| ID | Назва | Severity |
|---|---|---|
| GATE-BUG-001 | OPEN relay лишається ON після LIMIT_OPEN | Critical |
| GATE-BUG-002 | Перехід CLOSED → STOPPED після STOP | Medium |
| GATE-BUG-003 | ERROR не спрацьовує, коли активні обидва кінцеві вимикачі | Major |
| GATE-BUG-004 | OPENING триває понад 10 s без ERROR | Critical |
| GATE-BUG-005 | OPEN LED лишається ON після RESET і STOP | Minor |
| GATE-BUG-006 | OPEN під час CLOSING і CLOSE під час OPENING без safe stop | Major |
| DEB-BUG-001 | Вікно debounce 1 ms: імпульс NOISE ≈182,68 ms прийнято як натискання (обмеження: короткий шум вручну не відтворити) | Major |
| DEB-BUG-002 | Шум під час критичної операції створює нову логічну подію й завершує операцію | Major |
| CLI-BUG-01 | `set speed 256` дає speed=255 замість ERROR | Major |
| CLI-BUG-02 | `set timeout 0` прийнято замість ERROR | Major |
| CLI-BUG-03 | Верхній регістр `STATUS` приймається | Minor |
| CLI-BUG-04 | Crash і reboot при вводі довше 40 символів (пов’язаний із CLI-BUG-06) | Critical |
| CLI-BUG-05 | Вводи `так` і `???` приймаються як валідні (у звіті названо «спецсимволи та Unicode») | Major |
| CLI-BUG-06 | Crash після 5 довгих вводів; після reboot `help` і `status` повертають unknown command | Critical |
| CLI-BUG-07 | Crash «parser state mismatch while configuration is dirty» | Critical |
| I2C-BUG-01 | Один NACK на 0x69 вішає систему: немає контрольованої обробки помилки і відновлення без перезапуску | Critical |
| REC-BUG-01 | `sleep 5` прокидає пристрій через ≈1,4 s замість 5 s ±15 % (виміряно за мітками хоста) | Major |
| REC-BUG-02 | Relay ON після WDT reset | Critical |
| REC-BUG-03 | Пошкоджений стан після power loss під час збереження не виявляється (counter = 101) | Major |
| REC-BUG-04 | 0.0 °C / 0.0 % приймається як валідне вимірювання | Major |
| PYT-BUG-01 | `SET PWM 100` повертає INVALID_VALUE | Major |
| PYT-BUG-02 | RESET не повертає safe state (led true, pwm 255) | Critical |
| PYT-BUG-03 | GET TEMP повертає невалідний JSON (немає закриваючої дужки) | Major |
| IOT-BUG-01 | Backoff падає з 500 до 50 ms, retry кожні ≈55 ms (reconnect storm) | Major |
| IOT-BUG-02 | Повідомлення публікуються повторно після reconnect | Major |
| IOT-BUG-03 | Буфер перевищує capacity (12 / 8), найстаріші повідомлення губляться без запису | Critical |
| IOT-BUG-04 | Витік пам’яті ≈80 B на повідомлення | Critical |

**Observations** (потребують перевірки на залізі): `I2C-OBS-01` (перемикач FAULT без маркування ON / OFF), `REC-OBS-01` (повний WDT reset ≈11 s), `REC-OBS-02` (зайвий reset ≈0,65 s після `sleep 30`).
