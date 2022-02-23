from django.db import models


class Spravochnik(models.Model):
    """Описание модели справочников"""

    title = models.CharField('Наименование', max_length=255)
    short_title = models.CharField('Короткое наименование', max_length=150)
    description = models.TextField('Описание')
    version = models.CharField('Версия', max_length=100)
    date_created = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        unique_together = ('short_title', 'version')
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        ordering = ('-date_created',)

    def __str__(self):
        return f"{self.short_title} {self.version}"


class Element(models.Model):
    """Описание модели элементов справочников"""

    spravochnik = models.ForeignKey(
        Spravochnik, on_delete=models.CASCADE,
        verbose_name='Справочник'
    )
    code = models.CharField('Код', max_length=10)
    elem_value = models.CharField('Значение', max_length=255)

    class Meta:
        unique_together = ('spravochnik', 'code')
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
        ordering = ('-pk',)

    def __str__(self):
        return self.code
