"""
  Download dataset from url
"""

import hashlib
import os
import tarfile
import zipfile

import requests


def download_dataset(
    url: str, sha1_hash: str, cache_dir: str = os.path.join("..", "data")
) -> str:
    """Download dataset from url"""
    os.makedirs(cache_dir, exist_ok=True)
    file_name = os.path.join(cache_dir, os.path.basename(url))
    if (
        os.path.exists(file_name)
        and hashlib.sha1(open(file_name, "rb").read()).hexdigest() == sha1_hash
    ):
        return file_name
    print(f"Downloading {url} to {file_name}")
    response = requests.get(url, stream=True, verify=True, timeout=30)
    response.raise_for_status()
    with open(file_name, "wb") as f:
        f.write(response.content)
    return file_name


def download_extract(url: str, sha1_hash: str, folder: None | str = None):
    file_name = download_dataset(url, sha1_hash)
    base_dir = os.path.dirname(file_name)
    data_dir, ext = os.path.splitext(file_name)
    if ext == ".zip":
        with zipfile.ZipFile(file_name, "r") as zf:
            zf.extractall(base_dir)
    elif ext == ".gz":
        with tarfile.open(file_name, "r") as tar:
            tar.extractall(base_dir)
    else:
        raise ValueError(f"Unknown file type: {ext}")
    return os.path.join(base_dir, folder) if folder else data_dir
