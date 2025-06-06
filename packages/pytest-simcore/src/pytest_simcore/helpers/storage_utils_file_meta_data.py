from aws_library.s3 import UploadID
from models_library.basic_types import SHA256Str
from models_library.projects_nodes_io import StorageFileID
from simcore_postgres_database.storage_models import file_meta_data
from sqlalchemy.ext.asyncio import AsyncEngine


async def assert_file_meta_data_in_db(
    sqlalchemy_async_engine: AsyncEngine,
    *,
    file_id: StorageFileID,
    expected_entry_exists: bool,
    expected_file_size: int | None,
    expected_upload_id: bool | None,
    expected_upload_expiration_date: bool | None,
    expected_sha256_checksum: SHA256Str | None,
) -> UploadID | None:
    if expected_entry_exists and expected_file_size is None:
        assert True, "Invalid usage of assertion, expected_file_size cannot be None"

    async with sqlalchemy_async_engine.connect() as conn:
        result = await conn.execute(
            file_meta_data.select().where(file_meta_data.c.file_id == f"{file_id}")
        )
        db_data = result.fetchall()
        assert db_data is not None
        assert len(db_data) == (1 if expected_entry_exists else 0), (
            f"{file_id} was not found!"
            if expected_entry_exists
            else f"{file_id} should not exist"
        )
        upload_id = None
        if expected_entry_exists:
            row = db_data[0]
            assert (
                row.file_size == expected_file_size
            ), f"entry in file_meta_data was not initialized correctly, size should be set to {expected_file_size}"
            if expected_upload_id:
                assert (
                    row.upload_id is not None
                ), "multipart upload shall have an upload_id, it is missing!"
            else:
                assert (
                    row.upload_id is None
                ), "single file upload should not have an upload_id"
            if expected_upload_expiration_date:
                assert row.upload_expires_at, "no upload expiration date!"
            else:
                assert row.upload_expires_at is None, "expiration date should be NULL"
            if expected_sha256_checksum:
                assert (
                    SHA256Str(row.sha256_checksum) == expected_sha256_checksum
                ), "invalid sha256_checksum"
            else:
                assert row.sha256_checksum is None, "expected sha256_checksum was None"
            upload_id = row.upload_id
    return upload_id
