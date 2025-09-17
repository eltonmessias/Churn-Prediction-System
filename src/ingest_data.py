import os
import zipfile
from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path


class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        pass


class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        file_path = Path(file_path)
        if file_path.suffix != ".zip":
            raise ValueError("File extension must be .zip")

        project_root = Path(__file__).resolve().parents[1]
        extract_dir = project_root / "data/extracted_data"
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        extracted_files = os.listdir(extract_dir)
        csv_files = [f for f in extracted_files if f.endswith(".csv")]

        if len(csv_files) == 0:
            raise ValueError("No .csv files found in extracted_data")
        if len(csv_files) > 1:
            raise ValueError("More than one .csv file found in extracted_data")

        csv_file_path = extract_dir / csv_files[0]
        df = pd.read_csv(csv_file_path)

        return df


class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        """Return the appropriate DataIngestor based on file extension."""
        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"No ingestor available for file extension {file_extension}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "data" / "raw" / "dataset.zip"

    factory = DataIngestorFactory()
    ingestor = factory.get_data_ingestor(".zip")

    df = ingestor.ingest(file_path)
    print(df.head())
