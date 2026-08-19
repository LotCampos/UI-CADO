from django.db import migrations, models
import django.db.models.deletion
import uuid6


SQL_UUIDV7 = """
CREATE OR REPLACE FUNCTION public.uuidv7()
RETURNS uuid
AS $$
DECLARE
    v_time timestamp with time zone := null;
    v_secs bigint := null;
    v_msec bigint := null;
    v_usec bigint := null;
    v_timestamp bigint := null;
    v_timestamp_hex varchar := null;
    v_random bytea;
    v_random_hex varchar;
    v_bytes bytea;
BEGIN
    v_time := clock_timestamp();
    v_secs := EXTRACT(EPOCH FROM v_time);
    v_msec := mod(EXTRACT(MILLISECONDS FROM v_time)::numeric, 1000::numeric);
    v_usec := mod(EXTRACT(MICROSECONDS FROM v_time)::numeric, 1000::numeric);
    v_timestamp := (v_secs * 1000) + v_msec;
    v_timestamp_hex := lpad(to_hex(v_timestamp), 12, '0');
    v_random := gen_random_bytes(10);
    v_random_hex := encode(v_random, 'hex');
    v_bytes := decode(v_timestamp_hex || v_random_hex, 'hex');
    v_bytes := set_byte(v_bytes, 6, (get_byte(v_bytes, 6) & 15) | 112);
    v_bytes := set_byte(v_bytes, 8, (get_byte(v_bytes, 8) & 63) | 128);
    RETURN encode(v_bytes, 'hex')::uuid;
END $$ LANGUAGE plpgsql VOLATILE;
"""


SQL_OPTIMISTIC_LOCK = """
CREATE OR REPLACE FUNCTION public.func_enforce_optimistic_locking()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.version_lock <> OLD.version_lock + 1 THEN
        RAISE EXCEPTION 'CRITICAL 409: Violación de Optimistic Locking en %. Se esperaba version_lock = % y se recibió = %',
        TG_TABLE_NAME, OLD.version_lock + 1, NEW.version_lock;
    END IF;
    RETURN NEW;
END;
$$;
"""


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    SQL_UUIDV7,
                    reverse_sql="DROP FUNCTION IF EXISTS public.uuidv7();",
                ),
                migrations.RunSQL(
                    SQL_OPTIMISTIC_LOCK,
                    reverse_sql=(
                        "DROP FUNCTION IF EXISTS "
                        "public.func_enforce_optimistic_locking();"
                    ),
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name="Client",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid6.uuid7,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "created_at",
                            models.DateTimeField(
                                auto_now_add=True,
                            ),
                        ),
                        (
                            "version_lock",
                            models.PositiveIntegerField(
                                db_column="version_lock",
                                default=1,
                            ),
                        ),
                        (
                            "rfc",
                            models.CharField(
                                db_column="rfc",
                                max_length=13,
                            ),
                        ),
                        (
                            "business_name",
                            models.CharField(
                                db_column="business_name",
                                max_length=255,
                            ),
                        ),
                        (
                            "is_deleted",
                            models.BooleanField(
                                db_column="is_deleted",
                                default=False,
                            ),
                        ),
                        (
                            "deleted_at",
                            models.DateTimeField(
                                blank=True,
                                db_column="deleted_at",
                                null=True,
                            ),
                        ),
                        (
                            "deleted_by",
                            models.UUIDField(
                                blank=True,
                                db_column="deleted_by",
                                null=True,
                            ),
                        ),
                        (
                            "deletion_reason",
                            models.CharField(
                                blank=True,
                                db_column="deletion_reason",
                                max_length=500,
                                null=True,
                            ),
                        ),
                    ],
                    options={
                        "db_table": "master.clients",
                    },
                ),
                migrations.CreateModel(
                    name="Contact",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid6.uuid7,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "created_at",
                            models.DateTimeField(
                                auto_now_add=True,
                            ),
                        ),
                        (
                            "version_lock",
                            models.PositiveIntegerField(
                                db_column="version_lock",
                                default=1,
                            ),
                        ),
                        (
                            "full_name",
                            models.CharField(
                                db_column="full_name",
                                max_length=255,
                            ),
                        ),
                        (
                            "email",
                            models.EmailField(
                                blank=True,
                                db_column="email",
                                max_length=254,
                                null=True,
                            ),
                        ),
                        (
                            "phone",
                            models.CharField(
                                blank=True,
                                db_column="phone",
                                max_length=50,
                                null=True,
                            ),
                        ),
                        (
                            "job_title",
                            models.CharField(
                                blank=True,
                                db_column="job_title",
                                max_length=150,
                                null=True,
                            ),
                        ),
                        (
                            "is_primary",
                            models.BooleanField(
                                db_column="is_primary",
                                default=False,
                            ),
                        ),
                        (
                            "is_active",
                            models.BooleanField(
                                db_column="is_active",
                                default=True,
                            ),
                        ),
                        (
                            "is_deleted",
                            models.BooleanField(
                                db_column="is_deleted",
                                default=False,
                            ),
                        ),
                        (
                            "deleted_at",
                            models.DateTimeField(
                                blank=True,
                                db_column="deleted_at",
                                null=True,
                            ),
                        ),
                        (
                            "deleted_by",
                            models.UUIDField(
                                blank=True,
                                db_column="deleted_by",
                                null=True,
                            ),
                        ),
                        (
                            "deletion_reason",
                            models.CharField(
                                blank=True,
                                db_column="deletion_reason",
                                max_length=500,
                                null=True,
                            ),
                        ),
                        (
                            "client",
                            models.ForeignKey(
                                db_column="client_id",
                                on_delete=django.db.models.deletion.DO_NOTHING,
                                related_name="contacts",
                                to="master.client",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "master.contacts",
                    },
                ),
                migrations.CreateModel(
                    name="Installation",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid6.uuid7,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "created_at",
                            models.DateTimeField(
                                auto_now_add=True,
                            ),
                        ),
                        (
                            "version_lock",
                            models.PositiveIntegerField(
                                db_column="version_lock",
                                default=1,
                            ),
                        ),
                        (
                            "address",
                            models.TextField(
                                db_column="address",
                            ),
                        ),
                        (
                            "gps_lat",
                            models.DecimalField(
                                blank=True,
                                db_column="gps_lat",
                                decimal_places=6,
                                max_digits=9,
                                null=True,
                            ),
                        ),
                        (
                            "gps_lng",
                            models.DecimalField(
                                blank=True,
                                db_column="gps_lng",
                                decimal_places=6,
                                max_digits=9,
                                null=True,
                            ),
                        ),
                        (
                            "cre_asea_permit",
                            models.CharField(
                                blank=True,
                                db_column="cre_asea_permit",
                                max_length=100,
                                null=True,
                            ),
                        ),
                        (
                            "is_deleted",
                            models.BooleanField(
                                db_column="is_deleted",
                                default=False,
                            ),
                        ),
                        (
                            "deleted_at",
                            models.DateTimeField(
                                blank=True,
                                db_column="deleted_at",
                                null=True,
                            ),
                        ),
                        (
                            "deleted_by",
                            models.UUIDField(
                                blank=True,
                                db_column="deleted_by",
                                null=True,
                            ),
                        ),
                        (
                            "deletion_reason",
                            models.CharField(
                                blank=True,
                                db_column="deletion_reason",
                                max_length=500,
                                null=True,
                            ),
                        ),
                        (
                            "client",
                            models.ForeignKey(
                                db_column="client_id",
                                on_delete=django.db.models.deletion.DO_NOTHING,
                                related_name="installations",
                                to="master.client",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "master.installations",
                    },
                ),
                migrations.CreateModel(
                    name="InstallationContact",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid6.uuid7,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "created_at",
                            models.DateTimeField(
                                auto_now_add=True,
                            ),
                        ),
                        (
                            "version_lock",
                            models.PositiveIntegerField(
                                db_column="version_lock",
                                default=1,
                            ),
                        ),
                        (
                            "contact_role",
                            models.CharField(
                                db_column="contact_role",
                                max_length=100,
                            ),
                        ),
                        (
                            "is_primary",
                            models.BooleanField(
                                db_column="is_primary",
                                default=False,
                            ),
                        ),
                        (
                            "is_active",
                            models.BooleanField(
                                db_column="is_active",
                                default=True,
                            ),
                        ),
                        (
                            "contact",
                            models.ForeignKey(
                                db_column="contact_id",
                                on_delete=django.db.models.deletion.DO_NOTHING,
                                related_name="installation_links",
                                to="master.contact",
                            ),
                        ),
                        (
                            "installation",
                            models.ForeignKey(
                                db_column="installation_id",
                                on_delete=django.db.models.deletion.DO_NOTHING,
                                related_name="contact_links",
                                to="master.installation",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "master.installation_contacts",
                    },
                ),
            ],
        ),
    ]