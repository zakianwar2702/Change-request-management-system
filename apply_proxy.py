from pathlib import Path
import json

root = Path('.')
package_path = root / 'package.json'
dashboard_path = root / 'src' / 'pages' / 'Dashboard.jsx'

pkg = json.loads(package_path.read_text(encoding='utf-8'))
pkg['proxy'] = 'http://127.0.0.1:8000'
package_path.write_text(json.dumps(pkg, indent=2) + '\n', encoding='utf-8')

text = dashboard_path.read_text(encoding='utf-8')
text = text.replace('fetch("http://127.0.0.1:8000/api/summary/")', 'fetch("/api/summary/")')
dashboard_path.write_text(text, encoding='utf-8')

print('Updated package.json and Dashboard.jsx for React proxy')
