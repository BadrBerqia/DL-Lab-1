from __future__ import annotations

import shutil
from pathlib import Path

import kagglehub


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATASETS = {
    "nyse": "dgawlik/nyse",
    "predictive_maintenance": "shivamb/machine-predictive-maintenance-classification",
}


def copy_dataset(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for local_name, handle in DATASETS.items():
        print(f"Téléchargement de {handle}...")
        cached_path = Path(kagglehub.dataset_download(handle))
        destination = RAW_DATA_DIR / local_name
        copy_dataset(cached_path, destination)
        files = sorted(path.name for path in destination.rglob("*") if path.is_file())
        print(f"{local_name}: {len(files)} fichier(s) copié(s) dans {destination}")
        for file_name in files:
            print(f"  - {file_name}")


if __name__ == "__main__":
    main()
