# Embedded QA Portfolio

Портфоліо з тестування embedded-firmware (ESP32 / Arduino Uno) у симуляторі Wokwi: сім практичних робіт курсу QA Embedded, об’єднані одним [Master Test Plan](master-test-plan.pdf).

**Автор:** Марія Алєксєєвич

---

## Project goal

Показати, як я тестую embedded-системи на різних рівнях: GPIO і переривання, UART CLI, I2C-протокол, відновлення після збоїв (WDT, sleep, power loss), мережа й пам’ять, автоматизація на Python / pytest.

Усі збірки навмисно «баговані» (BUGGY). Завдання: знайти дефекти, довести їх доказами (логи, трасування, відео, вивід pytest) і оформити так, щоб їх можна було відтворити. Всі завдання виконувалися як black-box тестування, окрім Pytest Embedded Automation.

## Роботи одним поглядом

| # | Робота | Що тестували | Дефекти | Вердикт | Матеріали |
|---|---|---|---|---|---|
| 01 | Smart Gate Controller | FSM воріт, реле, кінцеві вимикачі, таймаут 10 s | 2 Critical, 2 Major, 1 Medium, 1 Minor | NO-GO | [wokwi](wokwi/01-smart-gate/) · [звіт](bug-reports/01-smart-gate/) |
| 02 | Debounce | Кнопка й шум на GPIO18, RAW vs LOGICAL на логічному аналізаторі | 2 Major | NO-GO | [wokwi](wokwi/02-debounce/) · [pulseview](pulseview/02-debounce/) · [звіт](bug-reports/02-debounce/) |
| 03 | UART CLI | BVA, негативні та довжинні вводи, стани SAVED / DIRTY | 3 Critical, 3 Major, 1 Minor | NO-GO | [wokwi](wokwi/03-uart-cli/) · [звіт](bug-reports/03-uart-cli/) |
| 04 | I2C | I2C-трафік, FAULT → NACK на 0x69, відновлення | 1 Critical | NO-GO| [wokwi](wokwi/04-i2c-mpu6050/) · [pulseview](pulseview/04-i2c-mpu6050/) · [звіт](bug-reports/04-i2c-mpu6050/) |
| 05 | Recovery / Fault Injection | Sleep, WDT, power loss, sensor failure, 15 recovery-циклів | 1 Critical, 3 Major | NO-GO | [wokwi](wokwi/05-recovery/) · [звіт](bug-reports/05-recovery/) |
| 06 | Python / Pytest | 49 автотестів (35 власних) | 1 Critical, 2 Major | NO-GO | [pytest](pytest/) · [wokwi](wokwi/06-pytest/) · [звіт](bug-reports/06-pytest/) |
| 07 | IoT Network / Memory | Reconnect, offline buffer, дублі, витік пам’яті | 2 Critical, 2 Major | NO-GO | [network-stress](network-stress/07-iot-node/) · [wokwi](wokwi/07-iot-node/) · [звіт](bug-reports/07-iot-node/) |

Разом: **27 дефектів** (10 Critical, 14 Major, 3 Medium / Minor), повний перелік у [bug-reports/README.md](bug-reports/README.md).

## System under test

| Підсистема | Плата | Що в ній критичне |
|---|---|---|
| Контролер воріт | Arduino Uno | Реле OPEN / CLOSE, FSM, кінцеві вимикачі |
| Кнопка + debounce | ESP32 DevKit v1 | Логічна подія натискання, критична операція |
| UART CLI | ESP32 Dev| Конфігурація speed / timeout, обробка вводу |
| I2C-датчик | ESP32 + MPU6050 | Зв’язок із датчиком, main loop |
| Recovery-пристрій | ESP32 + DHT22, реле | Safe state реле, persistent state, WDT |
| JSON-пристрій | ESP32 | PWM, LED, safe state після RESET |
| IoT-вузол | ESP32 | Offline-буфер, MQTT publish, free heap |

Версій FW у збірок немає (позначені BUGGY); докладніше в розділі 2 [Master Test Plan](master-test-plan.pdf).

## Test strategy

- **Risk-based:** 16 ризиків із пріоритетами P1–P3, найвищі P1 стосуються безпеки актуаторів, crash / зависань, витоку пам’яті й втрати даних.
- **Техніки:** boundary value analysis, негативне й state / sequence тестування, stress input, fault injection, аналіз протоколів (VCD у PulseView / Surfer).
- **Автоматизація:** pytest із параметризацією (граничні, невалідні й повторювані команди), fixture із RESET до і після кожного тесту.
- **Evidence-first:** кожен дефект має логи, трасування, вивід pytest або відео.
- **Рішення про реліз:** GO / GO WITH RISKS / NO-GO з аргументацією ([розділ 17](master-test-plan.pdf)).
- **Test Matrix:** (ризик → тест → evidence → статус) — Додаток А в [Master Test Plan](master-test-plan.pdf).

## Environment & tools

- Симуляція: Wokwi Simulator 4.1.0, VS Code, PlatformIO IDE 3.3.4
- Логічний аналіз: PulseView, Surfer, capture `wokwi.vcd`
- Автоматизація: Python 3.13.1, pytest 9.1.1, pyserial 3.5, порт `rfc2217://localhost:4000`
- Серіальні логи: PlatformIO Serial Monitor (115200, фільтри `time` + `log2file`)
- Реальне залізо: **не використовувалось** — це відомий ліміт, див. «Residual risks» у [Master Test Plan](master-test-plan.pdf)

## Key scenarios

| Сценарій | Очікувано | Фактично |
|---|---|---|
| Gate: OPEN → LIMIT_OPEN | Стан OPEN, relay OFF | Relay ON, нескінченне повідомлення про кінцевик |
| Debounce: одне натискання | 1 логічна подія | 44 RAW-фронти → 1 логічна подія, 1 дія (**працює**) |
| CLI: ввід 41 символ | `ERROR: command too long` | Crash і reboot (`rst:0xc`) |
| I2C: активація FAULT | Контрольована помилка, потім відновлення | Один NACK на 0x69, система зависла, потрібен перезапуск |
| Recovery: relay ON → hang (WDT) | Relay OFF після reset | Relay ON |
| IoT: NET DOWN → SEND × 12 (capacity 8) | buffer ≤ 8, dropped = 4 | buffer = 12, dropped = 0, ID 1–4 зникли без запису |
| IoT: STRESS 100 × 10 | Heap стабільний | −80 268 B (−22,9 %), ≈80 B на повідомлення |

## Bugs / findings

- 27 дефектів: 10 Critical, 14 Major, 3 Medium / Minor, плюс 3 observations (те, що не можна підтвердити без заліза).
- Найвагоміші: relay ON після WDT (REC-BUG-02), relay ON після LIMIT_OPEN (GATE-BUG-001), рух понад 10 с без ERROR (GATE-BUG-004), crash CLI на довгому вводі (CLI-BUG-04, 06, 07), зависання після I2C NACK (I2C-BUG-01), витік пам’яті й тиха втрата даних (IOT-BUG-03, 04).
- Повний індекс із severity: [bug-reports/README.md](bug-reports/README.md).
- **Нумерація:** ID дефектів унікальні лише в межах роботи, тому в репозиторії повний ID = префікс роботи + оригінальний ID (наприклад `GATE-BUG-001`, `IOT-BUG-01`).

## Evidence

| Тип | Де |
|---|---|
| Повні test sheets / test logs (PDF) | `bug-reports/<робота>/` |
| Логічні аналізатори: VCD, скріншоти PulseView / Surfer | `pulseview/` |
| Вивід pytest, код тестів | `pytest/` |
| Сценарії й логи мережевих стрес-тестів | `network-stress/` |
| Відео та великі логи | Google Drive, посилання в README кожної папки `bug-reports/<робота>/` |

## What I learned / decisions made

- **Симулятор не замінює залізо.** Часові мітки ставить хост, тож час WDT reset (≈11 s) і паузи виводу не були доказом дефекту. Такі випадки я оформлювала як observation і виносила в тести на залізі.
- **Не кожен FAIL — дефект firmware.** У pytest-роботі FAIL розкладено на Test / Environment / Communication / Requirement / Firmware. Приклад: PING відповідає за ≈1,37 s при таймауті клієнта 1 s, це розрив між тестом і вимогою.
- **Ручний тест має межі.** Клік мишею дає імпульс ≈182 ms, тому відхилення короткого шуму (< 1 ms) таким способом не перевірити. Цю прогалину я зафіксувала, а не приховала.
- **Неоднозначні вимоги треба уточнювати.** У CLI сім кейсів лишились зі статусом «потрібне уточнення» (пробіли, ведучі нулі), щоб не ставити хибні PASS / FAIL.
- **Safe state першим.** Дефекти актуаторів і crash'ів у плані мають найвищий пріоритет.

**Наступні кроки:** перевірка на реальному залізі (sleep, WDT, power loss, I2C), автоматизація CLI-матриці в pytest, тест на вичерпання heap.

## Repository structure

```
embedded-qa-portfolio/
├── README.md
├── master-test-plan.pdf
├── wokwi/           # проєкти Wokwi по роботах
├── pulseview/       # VCD, скріншоти, сесії PulseView
├── pytest/          # автотести Python
├── network-stress/  # IoT: сценарії, логи, memory log
├── bug-reports/     # test sheets (PDF) і індекс дефектів
└── resume/          # резюме
```
