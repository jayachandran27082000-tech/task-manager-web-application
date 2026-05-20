from pathlib import Path
from subprocess import Popen, PIPE
import time
import re

cloudflared = Path(__file__).resolve().parent / 'cloudflared.exe'
if not cloudflared.exists():
    raise FileNotFoundError(f'cloudflared.exe not found at {cloudflared}')

cmd = [str(cloudflared), 'tunnel', '--url', 'http://127.0.0.1:8000']
process = Popen(cmd, cwd=cloudflared.parent, stdout=PIPE, stderr=PIPE, text=True)

url_pattern = re.compile(r'https://[\w-]+\.trycloudflare\.com')
public_url = None

while True:
    line = process.stdout.readline()
    if not line:
        if process.poll() is not None:
            raise RuntimeError('cloudflared exited unexpectedly')
        time.sleep(0.1)
        continue
    print(line.strip())
    match = url_pattern.search(line)
    if match:
        public_url = match.group(0)
        print(f'PUBLIC_URL={public_url}')
        break

# Keep the tunnel running
while True:
    time.sleep(10)
