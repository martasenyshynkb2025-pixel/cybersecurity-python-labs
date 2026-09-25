#Написати програму, що виконує наступні операції над лог-файлом у csv-форматі
#log_file_variant.csv
import csv
from rich.console import Console
from rich.table import Table
from rich.text import Text
import sys


LOG_CSV = '/Users/apple/Documents/IT/log_file_27.csv'

def unique_sorted(lst):
    """Повертає відсортований унікалізований список (через sort + один прохід). Без set()."""
    if not lst:
        return []
    tmp = lst[:]
    tmp.sort()
    uniq = [tmp[0]]
    for x in tmp[1:]:
        if x != uniq[-1]:
            uniq.append(x)
    return uniq


def print_table(title_str, column_headers, rows, top_n=None):
    """Вивід у стилі з Лаб.1 (Console, Text, Table, стилі, justify='center').
       Якщо top_n заданий — показуємо лише перші top_n рядків.
    """
    console = Console()
    text = Text(title_str, style="bold bright_red")
    table = Table(title=text, header_style="bold bright_green", show_lines=True)


    for header in column_headers:
        table.add_column(header, style="bold magenta", justify="left", no_wrap=False)

    data = rows if (top_n is None) else rows[:top_n]
    for row in data:
        table.add_row(*[str(x) for x in row])

    console.print(table, justify="center")
    if (top_n is not None) and (len(rows) > top_n):
        console.print(f"[italic]Показано перші {top_n} рядків із {len(rows)}.[/italic]\n")
    else:
        console.print('\n')


def main():

    try:
        csvfile = open(LOG_CSV, newline='', encoding='utf-8')
    except FileNotFoundError:
        print(f"[bold red]ПОМИЛКА: Файл '{LOG_CSV}' не знайдено.[/bold red]")
        print(f"Будь ласка, переконайтеся, що файл знаходиться у правильному місці.")
        sys.exit(1)

    reader = csv.reader(csvfile)
    logs_tbl = list(reader)
    csvfile.close()

    if not logs_tbl or len(logs_tbl) <= 1:
        print("Файл порожній або містить лише заголовок:", LOG_CSV)
        return

    headers = logs_tbl[0]
    rows = logs_tbl[1:]


    MIN_FAILS = 6
    MIN_ACCOUNTS_PER_IP = 3



    rows_by_user = rows[:]
    rows_by_user.sort(key=lambda r: r[0])

    suspect_users = []
    if rows_by_user:
        current_user = rows_by_user[0][0]
        fail_count = 0
        for r in rows_by_user:
            user = r[0]
            status = r[3].strip().lower()


            if user != current_user:
                if fail_count >= MIN_FAILS:
                    suspect_users.append(current_user)

                current_user = user
                fail_count = 0


            if status == "fail":
                fail_count += 1


        if fail_count >= MIN_FAILS:
            suspect_users.append(current_user)

    Console().print(
        f"[bold]A) Користувачі з ≥ {MIN_FAILS} невдалими спробами входу (всього {len(suspect_users)}):[/bold] {suspect_users}\n")


    for u in suspect_users:
        u_logs = [r for r in rows if r[0] == u]
        print_table(f"Логи користувача '{u}'", headers, u_logs, top_n=30)


    rows_by_ip = rows[:]
    rows_by_ip.sort(key=lambda r: r[2])

    suspect_ips = []
    if rows_by_ip:
        current_ip = rows_by_ip[0][2]
        users_for_ip = []

        for r in rows_by_ip:
            ip = r[2]
            user = r[0]


            if ip != current_ip:
                uniq_users = unique_sorted(users_for_ip)
                if len(uniq_users) >= MIN_ACCOUNTS_PER_IP:
                    suspect_ips.append(current_ip)


                current_ip = ip
                users_for_ip = [user]
            else:

                users_for_ip.append(user)


        uniq_users = unique_sorted(users_for_ip)
        if len(uniq_users) >= MIN_ACCOUNTS_PER_IP:
            suspect_ips.append(current_ip)

    Console().print(
        f"[bold]B) ІР-адреси з входами у ≥ {MIN_ACCOUNTS_PER_IP} різні акаунти (всього {len(suspect_ips)}):[/bold] {suspect_ips}\n")


    for ip in suspect_ips:
        ip_logs = [r for r in rows if r[2] == ip]
        print_table(f"Логи для IP {ip}", headers, ip_logs, top_n=30)



if name == "__main__":
    main()