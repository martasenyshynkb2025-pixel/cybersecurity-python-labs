
USERS = {
    "forensic_lead": {
        "role": "forensic_analyst",
        "clearance": 4,
        "department": "Forensics",
        "active": True,
    },
    "compliance_off": {
        "role": "compliance_officer",
        "clearance": 3,
        "department": "Compliance",
        "active": True,
    },
    "trainee_sec": {
        "role": "trainee",
        "clearance": 1,
        "department": "Training",
        "active": True,
    },
    "vendor_tech": {
        "role": "vendor_support",
        "clearance": 2,
        "department": "Vendor",
        "active": True,
    },
    "archived_usr": {
        "role": "archived",
        "clearance": 1,
        "department": "Archive",
        "active": False,
    },
}

RESOURCES = [
    ("forensic_images", 4),
    ("compliance_reports", 3),
    ("training_videos", 1),
    ("vendor_tools", 2),
    ("evidence_locker", 4),
    ("certification_docs", 1),
    ("audit_findings", 3),
    ("chain_of_custody", 4),
    ("support_tickets", 2),
    ("learning_modules", 1),
]

SECURITY_LEVELS = ("Basic", "Standard", "Protected", "Maximum")
BLOCKED_USERS = {"archived_usr", "terminated_vendor", "security_breach"}


def check_access(username: str, resource_name: str, res_level: int) -> tuple:
    """Перевірка доступу користувача до ресурсу."""
    if username not in USERS:
        return False, "User not found"
    if username in BLOCKED_USERS:
        return False, "User is blocked"

    user_data = USERS[username]
    if not user_data["active"]:
        return False, "Account inactive"

    if user_data["clearance"] >= res_level:
        return True, "Access granted"

    return False, "Insufficient clearance"


def run_task2() -> None:
    """Запуск системи контролю доступу."""
    print("\n--- Завдання 2: Система контролю доступу ---")

    print("\n[Список ресурсів системи]:")
    for res_name, level in RESOURCES:
        level_str = SECURITY_LEVELS[level - 1]
        print(f" - {res_name}: {level_str} (level {level})")

    print("\n[Результати перевірки доступу]:")
    test_users = list(USERS.keys()) + ["non_existent_user"]

    for user in test_users:
        for res_name, level in RESOURCES[:3]:
            allowed, reason = check_access(user, res_name, level)
            status = "ALLOW" if allowed else f"DENY ({reason})"
            print(f"user=[{user}] resource=[{res_name}] -> {status}")


if __name__ == "__main__":
    run_task2()