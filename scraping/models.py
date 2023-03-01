from django.db import models
from django.utils.text import slugify

def default_urls():
    return {'work': '', 'hh': '', 'avito': ''}


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


class Vacancy(models.Model):
    url = models.URLField(
        unique=True
    )
    title = models.CharField(
        max_length=250,
        verbose_name="Название вакансии"
    )
    company = models.CharField(
        max_length=250,
        verbose_name="Компания"
    )
    description = models.TextField(
        verbose_name="Описание вакансии"
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        verbose_name="Название населенного пункта"
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name="Название языка программирования"
    )
    timestamp = models.DateField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Название вакансии"
        verbose_name_plural = "Названия вакансий"
        ordering = ['-timestamp']

    def __str__(self):
        return self.title
class Error(models.Model):
    timestamp = models.DateField(
        auto_now_add=True
    )
    data = models.JSONField()

    class Meta:
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"

    def __str__(self):
        return f'{self.timestamp} - {self.data}'


class Url(models.Model):
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        verbose_name="Название населенного пункта"
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name="Название языка программирования"
    )
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
