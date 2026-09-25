from typing import List

import requests


def check_ip_country(ip_list: List[str]) -> List[str]:
    """
    Приймає список IP, повертає список країн (код країни).
    """
    countries: List[str] = []
    for ip in ip_list:
        try:
            # Використовуємо ipinfo.io без токена (має ліміти)
            resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                countries.append(data.get('country', 'Unknown'))
            else:
                countries.append('Error')
        except Exception:
            countries.append('Error')
    return countries

ips_v23 = ['51.75.64.23', '185.220.102.8', '92.118.39.65', '167.172.180.40', '112.74.34.48']
print("\n--- IP Country Check ---")
print(f"IPs: {ips_v23}")
print(f"Countries: {check_ip_country(ips_v23)}")