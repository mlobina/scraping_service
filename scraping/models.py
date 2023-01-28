from django.db import models
from django.utils.text import slugify


class City(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название населенного пункта",
        unique=True
    )

    slug = models.CharField(
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
        """Автоматическое формирование слага из переданного названия"""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(City, self).save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название языка программирования",
        unique=True
    )

    slug = models.CharField(
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
        """Автоматическое формирование слага из переданного названия"""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Language, self).save(*args, **kwargs)
