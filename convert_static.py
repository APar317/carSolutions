import re
import os

root = r'd:\carSolution'
files = ['home.py','about.py','services.py','pricing.py','packages.py','appointment.py']
port_map = {
    '8000': 'index.html',
    '8001': 'services.html',
    '8002': 'pricing.html',
    '8003': 'packages.html',
    '8004': 'appointment.html',
    '8005': 'about.html',
}

for fname in files:
    path = os.path.join(root, fname)
    if not os.path.exists(path):
        continue
    text = open(path, 'r', encoding='utf-8').read()
    m = re.search(r'([A-Z_]+PAGE)\s*=\s*"""(.*)"""', text, re.S)
    if not m:
        print('no page found in', fname)
        continue
    html = m.group(2)
    # Replace absolute local URLs with relative page links
    for port, page in port_map.items():
        html = html.replace(f'http://localhost:{port}/', page)
        html = html.replace(f'http://localhost:{port}', page)
    html = html.replace('href="#" class="nav-link">Home', 'href="index.html" class="nav-link">Home')
    html = html.replace('href="#" class="btn btn-primary">About Us', 'href="about.html" class="btn btn-primary">About Us')
    html = html.replace('href="#" class="btn btn-secondary">Check Services', 'href="services.html" class="btn btn-secondary">Check Services')
    html = html.replace('href="http://localhost:8005" class="btn btn-primary">About Us', 'href="about.html" class="btn btn-primary">About Us')
    html = html.replace('href="http://localhost:8001" class="btn btn-secondary">Check Services', 'href="services.html" class="btn btn-secondary">Check Services')
    outname = 'index.html' if fname == 'home.py' else fname.replace('.py', '.html')
    outpath = os.path.join(root, outname)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print('written', outname)
