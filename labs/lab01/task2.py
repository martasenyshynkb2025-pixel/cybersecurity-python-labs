"""Task 2: Multilevel access control system for laboratory work #1."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER

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

SECURITY_LEVELS = (
    "Basic",
    "Standard",
    "Protected",
    "Maximum",
)

BLOCKED_USERS = {
    "archived_usr",
    "terminated_vendor",
    "security_breach",
}


def get_security_level_name(level: int) -> str:
    """Return a text name for a numeric security level."""
    return SECURITY_LEVELS[level - 1]


def print_resources() -> None:
    """Print all resources with text security level names."""
    print("Resources:")
    for resource_name, security_level in RESOURCES:
        level_name = get_security_level_name(security_level)
        print(f" - {resource_name}: {level_name} (level {security_level})")


def check_access(username: str, resource_level: int) -> tuple[bool, str]:
    """Check whether a user can access a resource."""
    if username not in USERS:
        return False, "User not found"
    if username in BLOCKED_USERS:
        return False, "User is blocked"

    user = USERS[username]
    if not user["active"]:
        return False, "Account inactive"

    if user["clearance"] >= resource_level:
        return True, ""

    return False, "Insufficient clearance"


def print_access_result(username: str, resource_name: str, resource_level: int) -> None:
    """Print one access-check result."""
    allowed, reason = check_access(username, resource_level)
    if allowed:
        print(f"user={username} resource={resource_name} -> ALLOW")
    else:
        print(f"user={username} resource={resource_name} -> DENY ({reason})")


def print_access_checks() -> None:
    """Check access for every user against every resource."""
    print("Access checks:")
    for username in USERS:
        for resource_name, resource_level in RESOURCES:
            print_access_result(username, resource_name, resource_level)


def run_task2() -> None:
    """Run Task 2 for Variant 5."""
    print("Laboratory Work #1 - Task 2")
    print(f"Student: {STUDENT_NAME}")
    print(f"Group: {GROUP_NAME}")
    print(f"Variant: {VARIANT_NUMBER}\n")
    print_resources()
    print()
    print_access_checks()


if __name__ == "__main__":
    run_task2()