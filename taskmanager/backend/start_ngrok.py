from pyngrok import ngrok
import time

# Disconnect any existing tunnels opened by pyngrok
for t in ngrok.get_tunnels():
    try:
        ngrok.disconnect(t.public_url)
    except Exception:
        pass

# Open a new HTTP tunnel to local port 8000
public_url = ngrok.connect(8000, "http").public_url
print(f"PUBLIC_URL={public_url}")
print("Tunnel established. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Shutting down tunnel...")
    for t in ngrok.get_tunnels():
        try:
            ngrok.disconnect(t.public_url)
        except Exception:
            pass
