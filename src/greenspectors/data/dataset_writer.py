import gzip


class BufferedDatasetWriter:

    def __init__(self, storage_location: str, dataset_slice_size: int):
        self._dataset_slice_size = dataset_slice_size
        self._storage_location = storage_location

        self._data = []
        self._current_slice = 0

    def __len__(self):
        return self._current_slice * self._dataset_slice_size + len(self._data)

    def add(self, sample: bytes):
        self._data.append(sample)
        if len(self._data) >= self._dataset_slice_size:
            self._save_dataset_slice()

    def finish(self):
        if len(self._data) > 0:
            self._save_dataset_slice()

    def _save_dataset_slice(self):
        self._current_slice += 1
        dataset_file_name = f"{self._storage_location}/dataset-{self._current_slice:02d}.json.gz"
        with gzip.open(dataset_file_name, 'wb') as f:
            f.write(b'\n'.join(self._data))
        self._data.clear()
