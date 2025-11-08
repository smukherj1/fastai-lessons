import requests
import os


def download_file(url, destination_path, force=False):
  """
    Downloads a file from a given URL to a specified local path.

    Args:
        url (str): The URL of the file to download.
        destination_path (str): The local path where the file will be saved.
    """
  if os.path.exists(destination_path):
    if not force:
      print(
          f"Skip downloading {url} to {destination_path} because it already exists."
      )
      return
    print(f"Force downloading {url} to {destination_path}.")
  else:
    print(f"Downloading {url} to {destination_path}.")
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_bytes = None
    if "Content-Length" in response.headers:
      try:
        total_bytes = int(response.headers["Content-Length"])
      except ValueError:
        pass
    downloaded_bytes = 0

    def _report():
      if total_bytes is not None and total_bytes > 0:
        pct = round((downloaded_bytes * 100.0 / total_bytes), 1)
        print(
            f"\rDownloaded {downloaded_bytes} / {total_bytes} bytes ({pct}%).",
            end="")
      else:
        print(f"\rDownloaded {downloaded_bytes} bytes.", end="")

    with open(destination_path, 'wb') as f:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # Filter out keep-alive new chunks
          f.write(chunk)
          downloaded_bytes += len(chunk)
          _report()
    print(
        f"File downloaded ({downloaded_bytes} bytes) successfully from {url} to {destination_path}"
    )
  except requests.exceptions.RequestException as e:
    print(f"Error downloading file: {e}")
