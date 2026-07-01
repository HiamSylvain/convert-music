import json

with open("cookies.json") as f:
    cookies = json.load(f)

with open("cookies.txt", "w") as f:
    f.write("# Netscape HTTP Cookie File\n")
    for cookie in cookies:
        domain = cookie['domain']
        flag = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = cookie.get('path', '/')
        secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
        expiry = cookie.get('expiry', 0)
        name = cookie['name']
        value = cookie['value']
        
        f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")