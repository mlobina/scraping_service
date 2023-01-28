from django.db import models
from .utils import from_cyrillic_to_eng


class City(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название населенного пункта",
        unique=True
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True
    )

    class Meta:
        verbose_name = "Название населенного пункта"
        verbose_name_plural = "Названия населенных пунктов"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название языка программирования",
        unique=True
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True
    )

    class Meta:
        verbose_name = "Название языка программирования"
        verbose_name_plural = "Названия языков программирования"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)
