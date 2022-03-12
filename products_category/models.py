from django.db import models


# Create your models here.


class ProductCategory(models.Model):
    PACK = (
        ('console', 'console'),
        ('accessories', 'accessories'),
        ('disk', 'disk'),
        ('pc', 'pc'),
        ('other', 'other'),
    )
    title = models.CharField(max_length=150, verbose_name='عنوان')
    name = models.CharField(max_length=150, verbose_name='عنوان در URL')
    pack = models.CharField(max_length=20, choices=PACK, default='other')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title
