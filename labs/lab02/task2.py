import argparse
import csv
import json
import logging
import re
import socket
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)


@dataclass
class ScanResult:
    """Клас даних для збереження результатів сканування хоста."""

    host: str
    port: int
    service: str
    status: str
    response_time: float
    notes: str


def validate_target(host: str) -> bool:
    """Валідація IPv4 адреси або доменного імені за допомогою регулярних виразів[cite: 8]."""
    ip_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    domain_pattern = (
        r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    )

    return bool(re.match(ip_pattern, host) or re.match(domain_pattern, host))


def check_port(host: str, port: int, timeout: float) -> ScanResult:
    """Перевірка доступності порту хоста через socket connection[cite: 8]."""
    service_names = {
        80: "HTTP",
        443: "HTTPS",
        22: "SSH",
        3389: "RDP",
        53: "DNS",
        21: "FTP",
        25: "SMTP",
    }
    service = service_names.get(port, "UNKNOWN")

    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((host, port))
        elapsed_ms = (time.time() - start_time) * 1000
        sock.close()
        return ScanResult(
            host=host,
            port=port,
            service=service,
            status="ONLINE",
            response_time=round(elapsed_ms, 1),
            notes="OK",
        )
    except socket.timeout:
        return ScanResult(
            host=host,
            port=port,
            service=service,
            status="OFFLINE",
            response_time=0.0,
            notes="TIMEOUT Connection timed out",
        )
    except Exception as e:
        return ScanResult(
            host=host,
            port=port,
            service=service,
            status="OFFLINE",
            response_time=0.0,
            notes=f"Error: {e}",
        )


def run_scan(targets_file: str, timeout: float, out_csv: str, verbose: bool) -> None:
    """Запуск аналізу доступності сервісів та експорт результатів[cite: 8]."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    path = Path(targets_file)
    if not path.exists():
        logging.error(f"Файл {targets_file} не знайдено.")
        sys.exit(1)

    logging.info(
        f"Starting service availability scan from target list {targets_file}...\n"
    )

    with open(path, "r", encoding="utf-8") as f:
        targets_data = json.load(f)

    results: list[ScanResult] = []
    online_count = 0
    offline_count = 0

    print(
        f"{'Target Host':<16} {'Port':<8} {'Service':<10} {'Status':<10} {'Response Time':<15} {'Notes'}"
    )
    print("-" * 75)

    for entry in targets_data:
        host = entry.get("host")
        port = entry.get("port")

        if not host or not port or not validate_target(host):
            logging.warning(f"Пропущено некоректну ціль: {host}:{port}")
            continue

        res = check_port(host, port, timeout)
        results.append(res)

        if res.status == "ONLINE":
            online_count += 1
            resp_str = f"{res.response_time} ms"
        else:
            offline_count += 1
            resp_str = "TIMEOUT"

        print(
            f"{res.host:<16} {res.port:<8} {res.service:<10} {res.status:<10} {resp_str:<15} {res.notes}"
        )

    total = online_count + offline_count
    online_pct = (online_count / total * 100) if total > 0 else 0
    offline_pct = (offline_count / total * 100) if total > 0 else 0

    print("\n=== Scan Statistics ===")
    print(f"Total Scanned : {total}")
    print(f"Online        : {online_count} ({online_pct:.1f}%)")
    print(f"Offline       : {offline_count} ({offline_pct:.1f}%)")

    # Збереження звіту в CSV
    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Target Host", "Port", "Service", "Status", "Response Time (ms)", "Notes"]
        )
        for r in results:
            writer.writerow(
                [r.host, r.port, r.service, r.status, r.response_time, r.notes]
            )

    logging.info(f"\nDetailed scan report saved to {out_csv}")


def main():
    parser = argparse.ArgumentParser(
        description="Сканер доступності мережевих сервісів та перевірка портів."
    )
    parser.add_argument(
        "--targets",
        required=True,
        help="Шлях до JSON-файлу зі списком цілей",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Таймаут підключення у секундах (за замовчуванням: 2.0)",
    )
    parser.add_argument(
        "--out-csv",
        required=True,
        help="Шлях до файлу CSV для збереження звіту",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Детальний режим логування",
    )

    args = parser.parse_args()
    run_scan(args.targets, args.timeout, args.out_csv, args.verbose)


if __name__ == "__main__":
    main()
