# 07-iot-node — мережа й пам’ять

**Сценарії:** A (NET DOWN / backoff), B (SEND × 5 офлайн), C (SEND × 12 при capacity 8), D (STRESS 100 × 10), D під час NET DOWN (STRESS 100 × 5).

**Що міститься:** лог-файли сценаріїв (`log2file` із PlatformIO Serial Monitor), таблиця Memory Stability Log, скріншоти BUFFER.

**Ключові результати:** heap 350 868 → 270 600 B (−22,9 %) за 1 000 повідомлень; buffer 12 при capacity 8; ID продубльовано 2–4 рази.
