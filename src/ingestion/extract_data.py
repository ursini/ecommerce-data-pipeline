import io
import os
import boto3
import pandas as pd
from botocore.exceptions import ClientError

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/raw")
BUCKET_BRONZE = "lake-bronze"

DATASETS = [
    "customers",
    "products",
    "orders",
    "order_items",
]


class S3Client:
    def __init__(
        self,
        endpoint_url="http://localhost:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadminpassword",
    ):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def create_bucket_if_not_exists(self, bucket_name: str):
        try:
            self.s3.head_bucket(Bucket=bucket_name)
        except ClientError:
            self.s3.create_bucket(Bucket=bucket_name)

    def upload_df_as_parquet(self, df: pd.DataFrame, bucket_name: str, object_name: str):
        self.create_bucket_if_not_exists(bucket_name)
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False, engine="pyarrow")
        buffer.seek(0)
        self.s3.put_object(Bucket=bucket_name, Key=object_name, Body=buffer.getvalue())

    def read_parquet_to_df(self, bucket_name: str, object_name: str) -> pd.DataFrame:
        response = self.s3.get_object(Bucket=bucket_name, Key=object_name)
        buffer = io.BytesIO(response["Body"].read())
        return pd.read_parquet(buffer, engine="pyarrow")


def extract_and_load_bronze() -> dict[str, pd.DataFrame]:
    s3_endpoint = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
    s3 = S3Client(endpoint_url=s3_endpoint)
    data = {}

    for dataset in DATASETS:
        csv_file = os.path.join(RAW_DATA_PATH, f"{dataset}.csv")
        object_name = f"{dataset}.parquet"

        df = pd.read_csv(csv_file)
        s3.upload_df_as_parquet(df, BUCKET_BRONZE, object_name)
        data[dataset] = s3.read_parquet_to_df(BUCKET_BRONZE, object_name)
        print(f"[Lake Bronze] {object_name} armazenado e validado no bucket '{BUCKET_BRONZE}'.")

    return data


if __name__ == "__main__":
    extract_and_load_bronze()