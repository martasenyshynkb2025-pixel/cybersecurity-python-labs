from rich.console import Console
from rich.table import Table

console = Console()

# Твої дані
surname = "Мисько"
name = "Анастасія Андріївна"
group = "КБ-105"
variant = "17"

# Вивід форматованого тексту
console.print(f"[bold magenta]{surname} {name}[/bold red]")
console.print(f"[blink #d70087]Група: {group}[/blink #005fff]")
console.print(f"[italic #005fff]Варіант: {variant}[/italic #d75f00]", justify="right")

# Таблиця
table = Table(title="Лабораторна робота 1")

table.add_column("Прізвище", justify="right", style="blink #005fff")
table.add_column("Ім'я", justify="right", style="bold red")
table.add_column("Група", justify="right", style="bold #5fd7ff")
table.add_column("Варіант", justify="right", style="italic #d75f00")

table.add_row(surname, name, group, variant)

console.print(table)