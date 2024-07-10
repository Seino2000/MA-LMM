import os
import zipfile
from pathlib import Path

from omegaconf import OmegaConf

from lavis.common.utils import (
    cleanup_dir,
    get_abs_path,
    get_cache_path,
)

LOCAL_DATA_PATH = {
    "train": "/home/user/Downloads/train_val_videos.zip",
    "test": "/home/user/Downloads/test_videos.zip",
}

def extract_datasets(root, file_path, extract_to):
    """
    Extract the dataset archives from the local file paths
    in the folder provided as parameter
    """
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def merge_datasets(download_path, storage_path):
    """
    Merge datasets in download_path to storage_path
    """

    # Merge train and test datasets
    train_path = os.path.join(download_path, "train_val_videos")
    test_path = os.path.join(download_path, "test_videos")
    train_test_path = storage_path

    print("Merging to {}".format(train_test_path))

    os.makedirs(train_test_path, exist_ok=True)

    for file_name in os.listdir(train_path):
        os.rename(
            os.path.join(train_path, file_name),
            os.path.join(train_test_path, file_name),
        )

    for file_name in os.listdir(test_path):
        os.rename(
            os.path.join(test_path, file_name),
            os.path.join(train_test_path, file_name),
        )

if __name__ == "__main__":

    config_path = get_abs_path('/home/user/2024/main/MA-LMM/MA-LMM/lavis/configs/datasets/msrvtt/defaults_cap.yaml')

    storage_dir = OmegaConf.load('/home/user/2024/main/MA-LMM/MA-LMM/lavis/configs/datasets/msrvtt/defaults_qa.yaml').datasets.msrvtt_cap.build_info.videos.storage

    download_dir = Path(get_cache_path(storage_dir)).parent / "download"
    storage_dir = Path(get_cache_path(storage_dir))

    if storage_dir.exists():
        print(f"Dataset already exists at {storage_dir}. Aborting.")
        exit(0)

    try:
        for k, v in LOCAL_DATA_PATH.items():
            extract_to_dir = download_dir / k
            print(f"Extracting {v} to {extract_to_dir}")
            extract_datasets(download_dir, v, extract_to_dir)
    except Exception as e:
        # remove download dir if failed
        cleanup_dir(download_dir)
        print("Failed to extract datasets. Aborting.")
        print(e)

    try:
        merge_datasets(download_dir, storage_dir)
    except Exception as e:
        # remove storage dir if failed
        cleanup_dir(download_dir)
        cleanup_dir(storage_dir)
        print("Failed to merge datasets. Aborting.")
        print(e)

    cleanup_dir(download_dir)
