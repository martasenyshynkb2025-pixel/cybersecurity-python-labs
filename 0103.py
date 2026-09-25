from rich.console import Console
from rich.table import Table

console = Console()


surname = "Сенишин"
name = "Марта"
group = "КБ-105"
variant = "23"


console.print(f"[bold magenta]{surname} {name}[/bold magenta]")
console.print(f"[blink #d70087]Група: {group}[/blink #d70087]")
console.print(f"[italic #005fff]Варіант: {variant}[/italic #005fff]", justify="right")


table = Table(title="Лабораторна робота 1")

table.add_column("Прізвище", justify="right", style="bold magenta")
table.add_column("Ім'я", justify="right", style="bold magenta")
table.add_column("Група", justify="right", style="blink #d70087")
table.add_column("Варіант", justify="right", style="italic #005fff")

table.add_row(surname, name, group, variant)

console.print(table)