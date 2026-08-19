from django.db import models

from core.models import UICadoBaseModel


class MasterBaseModel(UICadoBaseModel):
    """
    Abstract persistence foundation for MASTER entities.

    Physical MASTER baseline:
        id
        created_at
        version_lock

    MASTER entities intentionally do not contain:
        updated_at
        state_version
        workflow state
        SLA state
    """

    # MASTER physical schema does not contain updated_at.
    updated_at = None

    version_lock = models.PositiveIntegerField(
        default=1,
        db_column="version_lock",
    )

    class Meta:
        abstract = True


class Client(MasterBaseModel):
    rfc = models.CharField(
        max_length=13,
        db_column="rfc",
    )

    business_name = models.CharField(
        max_length=255,
        db_column="business_name",
    )

    is_deleted = models.BooleanField(
        default=False,
        db_column="is_deleted",
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_column="deleted_at",
    )

    deleted_by = models.UUIDField(
        null=True,
        blank=True,
        db_column="deleted_by",
    )

    deletion_reason = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column="deletion_reason",
    )

    class Meta:
        db_table = "master.clients"

    def __str__(self) -> str:
        return f"{self.business_name} ({self.rfc})"


class Contact(MasterBaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        db_column="client_id",
        related_name="contacts",
    )

    full_name = models.CharField(
        max_length=255,
        db_column="full_name",
    )

    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        db_column="email",
    )

    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column="phone",
    )

    job_title = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        db_column="job_title",
    )

    is_primary = models.BooleanField(
        default=False,
        db_column="is_primary",
    )

    is_active = models.BooleanField(
        default=True,
        db_column="is_active",
    )

    is_deleted = models.BooleanField(
        default=False,
        db_column="is_deleted",
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_column="deleted_at",
    )

    deleted_by = models.UUIDField(
        null=True,
        blank=True,
        db_column="deleted_by",
    )

    deletion_reason = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column="deletion_reason",
    )

    class Meta:
        db_table = "master.contacts"

    def __str__(self) -> str:
        return self.full_name


class Installation(MasterBaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        db_column="client_id",
        related_name="installations",
    )

    address = models.TextField(
        db_column="address",
    )

    gps_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        db_column="gps_lat",
    )

    gps_lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        db_column="gps_lng",
    )

    cre_asea_permit = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="cre_asea_permit",
    )

    is_deleted = models.BooleanField(
        default=False,
        db_column="is_deleted",
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_column="deleted_at",
    )

    deleted_by = models.UUIDField(
        null=True,
        blank=True,
        db_column="deleted_by",
    )

    deletion_reason = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column="deletion_reason",
    )

    class Meta:
        db_table = "master.installations"

    def __str__(self) -> str:
        return self.address


class InstallationContact(MasterBaseModel):
    installation = models.ForeignKey(
        Installation,
        on_delete=models.DO_NOTHING,
        db_column="installation_id",
        related_name="contact_links",
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.DO_NOTHING,
        db_column="contact_id",
        related_name="installation_links",
    )

    contact_role = models.CharField(
        max_length=100,
        db_column="contact_role",
    )

    is_primary = models.BooleanField(
        default=False,
        db_column="is_primary",
    )

    is_active = models.BooleanField(
        default=True,
        db_column="is_active",
    )

    class Meta:
        db_table = "master.installation_contacts"

    def __str__(self) -> str:
        return f"{self.installation_id} -> {self.contact_id}"