from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
import re

SESSION_TIMEOUT_SEC = 900


class User:
    """Клас користувача з інкапсуляцією пароля та валідацією email."""

    def __init__(
        self, username: str, email: str, role: str = "user", active: bool = True
    ):
        self.username = username
        self.role = role
        self.active = active
        self._email = None
        self.email = email

        self.__password_salt = os.urandom(16)
        self.__password_hash = None

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        pattern = r"^[a-zA-Z][a-zA-Z0-9._-]{2,63}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError(f"Некоректний формат email: {value}")
        self._email = value

    def set_password(self, password: str):
        iterations = 100000
        self.__password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), self.__password_salt, iterations
        )

    def check_password(self, password: str) -> bool:
        if not self.__password_hash:
            return False
        iterations = 100000
        new_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), self.__password_salt, iterations
        )
        return hmac.compare_digest(self.__password_hash, new_hash)

    def deactivate(self):
        self.active = False

    def __str__(self) -> str:
        status = "Active" if self.active else "Inactive"
        return f"User({self.username}, Email: {self.email}, Role: {self.role}, Status: {status})"


class Admin(User):
    """Клас адміністратора (успадкування від User)."""

    def __init__(self, username: str, email: str, permissions: list[str] = None):
        super().__init__(username, email, role="admin")
        self.permissions = set(permissions) if permissions else set()

    def grant_permission(self, permission: str):
        self.permissions.add(permission)

    def revoke_permission(self, permission: str):
        self.permissions.discard(permission)

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str}, Permissions: {list(self.permissions)}"


class Session:
    """Клас сесії користувача з урахуванням таймауту."""

    def __init__(self, ip: str):
        self.ip = ip
        now = datetime.now(timezone.utc)
        self.login_time = now
        self.last_activity = now

    def touch(self):
        self.last_activity = datetime.now(timezone.utc)

    def is_active(self, timeout_sec: int) -> bool:
        if timeout_sec <= 0:
            raise ValueError("Timeout має бути позитивним числом")
        now = datetime.now(timezone.utc)
        return (now - self.last_activity) < timedelta(seconds=timeout_sec)


@dataclass
class AuditEntry:
    """Запис в журналі аудиту."""

    timestamp: datetime
    username: str
    action: str


class AuditLog:
    """Журнал аудиту дій користувачів."""

    def __init__(self):
        self.logs: list[AuditEntry] = []

    def add_log(self, username: str, action: str):
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc),
            username=username,
            action=action,
        )
        self.logs.append(entry)

    def show_all(self):
        print("\n=== Audit Log Entries ===")
        for log in self.logs:
            time_str = log.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"[{time_str}] User: {log.username} | Action: {log.action}")


class UserAccount:
    """Клас облікового запису (композиція User, Session, AuditLog)."""

    def __init__(self, user: User, audit_log: AuditLog = None):
        self.user = user
        self.session: Session = None
        self.audit_log = audit_log if audit_log else AuditLog()

    def login(self, username: str, password: str, ip: str) -> bool:
        if username != self.user.username:
            self.audit_log.add_log(username, "login_failure")
            return False

        if not self.user.active:
            self.audit_log.add_log(username, "login_failure_inactive")
            return False

        if self.user.check_password(password):
            self.session = Session(ip)
            self.session.touch()
            self.audit_log.add_log(self.user.username, "login_success")
            return True

        self.audit_log.add_log(self.user.username, "login_failure")
        return False

    def is_authenticated(self, timeout_sec: int = SESSION_TIMEOUT_SEC) -> bool:
        if not self.session:
            return False
        return self.session.is_active(timeout_sec)

    def logout(self):
        if self.session:
            self.audit_log.add_log(self.user.username, "logout")
            self.session = None

    def __getitem__(self, key: str):
        allowed_keys = {
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
            "active": self.user.active,
        }
        if key in allowed_keys:
            return allowed_keys[key]
        raise KeyError(f"Невідомий ключ: {key}")

    def __setitem__(self, key: str, value):
        if key == "email":
            if not isinstance(value, str):
                raise TypeError("Email повинен бути рядком")
            self.user.email = value
        elif key == "active":
            if not isinstance(value, bool):
                raise TypeError("Active повинен бути bool")
            self.user.active = value
        else:
            raise KeyError(f"Редагування ключа '{key}' заборонено або ключ не існує")
