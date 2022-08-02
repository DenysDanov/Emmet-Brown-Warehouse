from django.db import models


class Category(models.Model):
    name = models.TextField('Назва товару', unique=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return f'Категорія: {self.name}'

class Product(models.Model):
    name = models.TextField('Назва товару')
    SKU = models.TextField('SKU товару')
    category = models.ForeignKey(verbose_name='Категорія', to=Category, on_delete=models.CASCADE)
    price = models.IntegerField('Ціна')
    descr = models.TextField('Опис товару')
    short_descr = models.TextField('Короткий опис товару')
    image = models.ImageField('Іконка товару', upload_to='shop/products/image')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'

    def __str__(self):
        return f'Продукт: {self.name}'
