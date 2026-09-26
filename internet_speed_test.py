import argparse
import time
from statistics import mean

import httpx


REQUEST_COUNT = 10
TIMEOUT = 60.0
CHUNK_SIZE = 1024 * 1024  # 1 MB


def format_size(size_bytes: float) -> str:
    """Format bytes using decimal units."""

    units = ("B", "KB", "MB", "GB", "TB")
    size = float(size_bytes)

    for unit in units:
        if size < 1000 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1000

    return f"{size:.2f} TB"


def format_speed(speed_bytes_per_sec: float) -> str:
    """Format download speed in B/s, KB/s, MB/s, GB/s."""
    return format_size(speed_bytes_per_sec) + "/s"


def format_bit_speed(speed_bytes_per_sec: float) -> str:
    """Format download speed in bps, Kbps, Mbps, Gbps."""

    units = ("bps", "Kbps", "Mbps", "Gbps", "Tbps")
    bits_per_sec = speed_bytes_per_sec * 8

    speed = float(bits_per_sec)

    for unit in units:
        if speed < 1000 or unit == units[-1]:
            return f"{speed:.2f} {unit}"

        speed /= 1000

    return f"{speed:.2f} Tbps"


def download(client: httpx.Client, url: str) -> tuple[float, int]:
    """Download URL and return elapsed time and downloaded bytes."""

    start = time.perf_counter()
    downloaded = 0

    with client.stream("GET", url) as response:
        response.raise_for_status()

        for chunk in response.iter_bytes(CHUNK_SIZE):
            downloaded += len(chunk)

    elapsed = time.perf_counter() - start

    return elapsed, downloaded


def main() -> int:
    parser = argparse.ArgumentParser(description="Sequential internet download speed test.")
    parser.add_argument("url", help="URL of a large file/image to download")

    args = parser.parse_args()

    times: list[float] = []
    total_bytes = 0

    print(f"URL: {args.url}")
    print(f"Requests: {REQUEST_COUNT}")
    print()

    # Header
    print(
        f"{'Request':>10} | "
        f"{'Data':>12} | "
        f"{'Time':>10} | "
        f"{'Speed':>14} | "
        f"{'Network':>14}"
    )

    print("-" * 72)

    with httpx.Client(timeout=TIMEOUT, follow_redirects=True,) as client:
        for number in range(1, REQUEST_COUNT + 1):
            try:
                elapsed, size = download(client, args.url)

                speed_bytes_per_sec = size / elapsed

                speed = format_speed(speed_bytes_per_sec)
                bit_speed = format_bit_speed(speed_bytes_per_sec)

                times.append(elapsed)
                total_bytes += size

                print(
                    f"{f'[{number}/{REQUEST_COUNT}]':>10} | "
                    f"{format_size(size):>12} | "
                    f"{elapsed:>8.3f} s | "
                    f"{speed:>14} | "
                    f"{bit_speed:>14}"
                )

            except httpx.HTTPError as error:
                print(f"{f'[{number}/{REQUEST_COUNT}]':>10} | {'ERROR':>12} | {str(error)}")

    if not times:
        print("\nNo successful requests.")
        return 1

    average_time = mean(times)
    average_size = total_bytes / len(times)

    # Общая скорость:
    # все скачанные байты / всё время скачивания.

    average_speed_bytes_per_sec = total_bytes / sum(times)

    print()
    print("-" * 72)

    print(f"{'Successful requests':<22}: {len(times)}/{REQUEST_COUNT}")
    print(f"{'Average request time':<22}: {average_time:.3f} s")
    print(f"{'Average data size':<22}: {format_size(average_size)}")
    print(f"{'Total downloaded':<22}: {format_size(total_bytes)}")
    print(f"{'Average speed':<22}: {format_speed(average_speed_bytes_per_sec)}")
    print(f"{'Average network speed':<22}: {format_bit_speed(average_speed_bytes_per_sec)}")
    print("-" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
