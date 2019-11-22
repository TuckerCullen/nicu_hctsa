
import minio

minio_client = minio.Minio(
        "minionas.uvadcos.io",
        access_key = "breakfast",
        secret_key = "breakfast",
        secure=False
        )

minio_client.fget_object(
        bucket_name="breakfast",
        object_name="NICU Vitals/UVA_6738_vitals.mat",
        file_path="users/tuckcullen/nicu/UVA_6738_vitals.mat"
        )

minio_client.list_objects_v2(
        bucket_name="breakfast",
        prefix="NICU Vitals",
        recursive=True
        )
