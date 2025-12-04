from django.db import models
from .const import R2_PUBLIC_URL


class R2PublicURLMixin(models.Model):
    file_field_name = None
    url_field_name = None
    path_prefix = "assets/"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        file_field = getattr(self, self.file_field_name, None)
        if file_field:
            filename = file_field.name.replace(self.path_prefix, "")
            new_url = f"{R2_PUBLIC_URL}{self.path_prefix}{filename}"

            if getattr(self, self.url_field_name) != new_url:
                setattr(self, self.url_field_name, new_url)
                super().save(update_fields=[self.url_field_name])