"""Command-line entry point for Laboratory Work #2."""

import sys
from labs.lab02.task1 import Admin, AuditLog, User, UserAccount


def run_demo():
    print("=== Демонстрація ООП та безпечних сесій (Завдання 1) ===")

    audit = AuditLog()

    user = User("j_doe", "j_doe@corp.ua")
    user.set_password("SecurePass123!")
    account = UserAccount(user, audit)

    print(f"Створено користувача: {user}")

    print("\n1. Спроба успішного входу:")
    if account.login("j_doe", "SecurePass123!", "192.168.1.50"):
        print("[SUCCESS] Успішна авторизація!")

    print(f"Статус автентифікації: {account.is_authenticated()}")

    print("\n2. Спроба входу з невірним паролем:")
    account.login("j_doe", "WrongPassword", "192.168.1.50")

    print("\n3. Валідація зміни email:")
    try:
        account["email"] = "bad_email_format"
    except ValueError as e:
        print(f"[CATCH ERROR] {e}")

    account["email"] = "new_email@corp.ua"
    print(f"Оновлений email: {account['email']}")

    print("\n4. Перевірка прав адміністратора:")
    admin = Admin("admin_user", "admin@corp.ua")
    admin.grant_permission("READ_LOGS")
    admin.grant_permission("DELETE_USERS")
    print(admin)
    print(f"Чи має право DELETE_USERS? {admin.has_permission('DELETE_USERS')}")

    print("\n5. Вихід із системи:")
    account.logout()
    print(f"Статус автентифікації після logout: {account.is_authenticated()}")

    audit.show_all()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "analyze":
        from labs.lab02 import task2

        task2.main(sys.argv[2:])
    else:
        print("Для запуска утиліти використайте одну з команд:")
        print("  python -m labs.lab02.main demo")
        print("  python -m labs.lab02.main analyze --targets <path> --out-csv <path>")


if __name__ == "__main__":
    main()
