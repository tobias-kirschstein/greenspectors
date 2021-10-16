import gzip
import json
from glob import glob
from pathlib import Path

from greenspectors.env import TWITTER_ARCHIVE_DATASET_PATH


class TwitterArchiveDataLoader:

    def __init__(self):
        self._data_location = TWITTER_ARCHIVE_DATASET_PATH
        self._archives = [Path(archive_path).stem for archive_path in glob(f"{self._data_location}/*")]

    def __iter__(self):
        for archive_name in self._archives:
            for archive_slice in self._get_archive_slices(archive_name):
                with gzip.open(archive_slice) as f:
                    for line in f.readlines():
                        yield json.loads(line)

    def _get_archive_slices(self, archive_name: str):
        return glob(f"{self._data_location}/{archive_name}/*.json.gz")
