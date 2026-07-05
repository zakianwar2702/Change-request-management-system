import urllib.request
html = urllib.request.urlopen('http://127.0.0.1:8000/create/').read().decode('utf-8')
start = html.find('<form')
end = html.find('</form>', start)
print(html[start:end+7])
