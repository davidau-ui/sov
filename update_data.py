import urllib.request
import re
import sys
from datetime import datetime

SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTcKU2BGzxpO_BFBAtpkorUk1t1IEch3Qwaog8BdfB0Vza0OSf-LqlIeQYVP_0uMC467_lfrhMhkk8Y/pub?gid=0&single=true&output=csv"

def fetch_csv(url):
    print(f"Descargando CSV desde Google Sheets...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode('utf-8')
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    print(f"  {len(lines)-1} filas de datos descargadas")
    return text.strip()

def embed_csv_in_html(csv_text, html_path='index.html'):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Escape for JS template literal
    escaped = csv_text.replace('\\', '\\\\').replace('`', '\`').replace('${', '\${')
    new_const = f'const EMBEDDED_CSV = `{escaped}`;'

    # Replace existing EMBEDDED_CSV constant
    html_new = re.sub(
        r'const EMBEDDED_CSV = `[\s\S]*?`;',
        new_const,
        html
    )

    if html_new == html:
        print("ERROR: No se encontró EMBEDDED_CSV en index.html")
        sys.exit(1)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_new)

    print(f"  index.html actualizado correctamente ({len(csv_text)} chars de CSV)")

if __name__ == '__main__':
    try:
        csv_text = fetch_csv(SHEETS_URL)
        embed_csv_in_html(csv_text)
        print(f"✓ Listo — {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
