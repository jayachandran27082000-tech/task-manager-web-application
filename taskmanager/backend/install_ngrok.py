import urllib.request
import zipfile
from pathlib import Path

url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
output_dir = Path(__file__).resolve().parent
zip_path = output_dir / "ngrok.zip"

print(f"Downloading ngrok from {url} to {zip_path}")
with urllib.request.urlopen(url) as response, open(zip_path, 'wb') as out_file:
    out_file.write(response.read())
print(f"Download complete, {zip_path.stat().st_size} bytes")

if not zip_path.exists() or zip_path.stat().st_size == 0:
    raise RuntimeError("Downloaded ngrok zip is missing or empty")

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print("Extraction complete")
except zipfile.BadZipFile as e:
    raise RuntimeError(f"Downloaded file is not a valid zip: {e}")

zip_path.unlink()
print(f"Extracted ngrok to {output_dir}")
print(f"ngrok path: {output_dir / 'ngrok.exe'}")
