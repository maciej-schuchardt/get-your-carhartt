import os
import requests, re
from bs4 import BeautifulSoup

def get_proxies() -> list[str]:
    proxies_file = "proxies_list.txt"
    if not os.path.isfile(proxies_file):
        regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
        c = requests.get("https://spys.me/proxy.txt")
        test_str = c.text
        a = re.finditer(regex, test_str, re.MULTILINE)
        with open(proxies_file, 'w') as file:
            for i in a:
                print(i.group(),file=file)
                
        d = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(d.content, 'html.parser')
        td_elements = soup.select('.fpl-list .table tbody tr td')
        ips = []
        ports = []
        for j in range(0, len(td_elements), 8):
            ips.append(td_elements[j].text.strip())
            ports.append(td_elements[j + 1].text.strip())
        with open(proxies_file, "a") as myfile:
            for ip, port in zip(ips, ports):
                proxy = f"{ip}:{port}"
                print(proxy, file=myfile)
    
    with open(proxies_file, "r") as myfile:
        result: list[str] = list((line for line in myfile.readlines()))
    return result
    