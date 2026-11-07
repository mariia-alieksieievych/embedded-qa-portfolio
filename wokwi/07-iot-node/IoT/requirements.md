# Device Requirements — IoT Network Node

## R1 Network states
Node має мати observable states: DISCONNECTED, CONNECTING, CONNECTED, BACKOFF.

## R2 Auto-reconnect
Після втрати broker/network node не повинен зависати.
Retry має використовувати backoff і не створювати reconnect storm.

## R3 Offline buffering
Коли publish неможливий, telemetry зберігається у локальному buffer.

## R4 Buffer boundary
Capacity = 8 messages.
При overflow діє явна policy: DROP_OLDEST.
Drop має бути observable у counter/log.

## R5 Recovery
Після `NET UP` node відновлює CONNECTED і відправляє buffered messages.

## R6 Duplicates
Одне telemetry message ID не повинно бути успішно publish більше одного разу у цьому навчальному протоколі.

## R7 Memory stability
При повторних SEND/STRESS free heap не повинен демонструвати систематичне незворотне падіння.

## R8 Evidence
`STATUS` має показувати network state, buffer occupancy/capacity, sent, dropped,
duplicates, reconnect attempts і free heap.

## Fault injection commands
- `NET DOWN`
- `NET UP`
- `SEND`
- `STRESS <N>`
- `BUFFER`
- `STATUS`
- `RESET STATS`
