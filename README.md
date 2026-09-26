# Internet Speed Test

Простой CLI-тест скорости загрузки на Python 3.

Скрипт последовательно скачивает указанный файл 10 раз, измеряет время каждого запроса и рассчитывает скорость загрузки. В конце выводится средняя скорость за все успешные загрузки.

## Features

- Python 3
- HTTP-клиент на базе [httpx](https://www.python-httpx.org/)
- 10 последовательных загрузок
- Поддержка HTTP/HTTPS
- Поддержка редиректов
- Потоковая загрузка без хранения файла на диске
- Измерение времени каждого запроса
- Расчёт скорости в:
  - `B/s`
  - `KB/s`
  - `MB/s`
  - `GB/s`
- Расчёт сетевой скорости в:
  - `bps`
  - `Kbps`
  - `Mbps`
  - `Gbps`
- Автоматический выбор подходящей единицы измерения
- Обработка HTTP-ошибок
- Итоговая статистика по всем успешным запросам

## Requirements

- Python 3.10+
- `httpx`

## Installation

Клонировать репозиторий:

```bash
git clone https://github.com/WilJames/python-internet-speed-test.git
cd internet-speed-test
```


Установить зависимости:

```bash
python -m pip install -r requirements.txt
```

Или установить httpx напрямую:

```bash
python -m pip install httpx
```

## Usage

Запуск:

```bash
python internet_speed_test.py <URL>
```

Например:
```bash
python internet_speed_test.py https://example.com/test.bin
```

Для корректного тестирования рекомендуется использовать большой файл, например 100 MB или больше.

## Example

```bash
URL: https://files.example.com/test_100mb.bin
Requests: 10

   Request |         Data |       Time |          Speed |        Network
------------------------------------------------------------------------
    [1/10] |    100.00 MB |    0.935 s |     106.92 MB/s |     855.36 Mbps
    [2/10] |    100.00 MB |    0.925 s |     108.11 MB/s |     864.88 Mbps
    [3/10] |    100.00 MB |    1.119 s |      89.36 MB/s |     714.88 Mbps
    [4/10] |    100.00 MB |    0.929 s |     107.64 MB/s |     861.12 Mbps
    [5/10] |    100.00 MB |    0.923 s |     108.34 MB/s |     866.72 Mbps
    [6/10] |    100.00 MB |    0.917 s |     109.05 MB/s |     872.40 Mbps
    [7/10] |    100.00 MB |    0.914 s |     109.41 MB/s |     875.28 Mbps
    [8/10] |    100.00 MB |    0.912 s |     109.65 MB/s |     877.20 Mbps
    [9/10] |    100.00 MB |    0.921 s |     108.58 MB/s |     868.64 Mbps
   [10/10] |    100.00 MB |    0.915 s |     109.29 MB/s |     874.32 Mbps

------------------------------------------------------------------------
Successful requests : 10/10
Average request time: 0.941 s
Average data size   : 100.00 MB
Total downloaded    : 1.00 GB
Average speed       : 106.26 MB/s
Average network speed: 850.08 Mbps
------------------------------------------------------------------------
```


## Configuration

Следующие константы можно изменить непосредственно в internet_speed_test.py

```python
REQUEST_COUNT = 10
TIMEOUT = 60.0
CHUNK_SIZE = 1024 * 1024
```

## REQUEST_COUNT

Количество последовательных загрузок:

```python
REQUEST_COUNT = 10
```

## TIMEOUT

Максимально допустимое время для HTTP-операции:

```python
TIMEOUT = 60.0
```

Значение указывается в секундах.

## CHUNK_SIZE

Размер фрагментов, используемых при потоковой передаче ответа:

```python
CHUNK_SIZE = 1024 * 1024
```

Значение по умолчанию 1 MiB.


## License

MIT License

See [LICENSE](https://github.com/WilJames/python-internet-speed-test/blob/main/LICENSE) for details.
