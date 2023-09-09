from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import date


class Image(models.Model):
    """Модель для хранения картинки категории"""

    src = models.ImageField(
        upload_to="category/pictures/",
        default="category/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Описание картинки", null=True
    )

    def __str__(self):
        return self.src.name

    class Meta:
        verbose_name = "Изображение категории"
        verbose_name_plural = "Изображения категории"


class SubImage(models.Model):
    """Модель для хранения картинки подкатегории"""

    src = models.ImageField(
        upload_to="subcategory/pictures/",
        default="subcategory/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Описание картинки", null=True
    )

    def __str__(self):
        return self.src.name


class Subcategory(models.Model):
    """Модель подкатегории"""

    title = models.CharField(max_length=100)
    image = models.ForeignKey(SubImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """Модель категории"""

    title = models.CharField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    subcategories = models.ManyToManyField(
        Subcategory, related_name="category", blank=True
    )

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def set_default_image(sender, instance, **kwargs):
    """Обрабатывает запрос для категории перед сохранением в БД"""
    if not instance.image:
        instance.image = Image.objects.create()


@receiver(pre_save, sender=Subcategory)
def set_default_category_subimage(sender, instance, **kwargs):
    """Обрабатывает запрос для подкатегории перед сохранением в БД"""
    if not instance.image:
        instance.image = SubImage.objects.create()


class ProductImage(models.Model):
    src = models.ImageField(
        upload_to="products/pictures/",
        default="products/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Описание картинки", null=True
    )

    def __str__(self):
        return self.src.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="Почта")
    text = models.TextField()
    rate = models.IntegerField(verbose_name="Оценка")
    date = models.CharField(max_length=100, null=True, default=date.today(), blank=True)


class Specification(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)


class Sale(models.Model):
    salePrice = models.IntegerField(null=False, verbose_name="Процент скидки %")
    dateFrom = models.DateField(verbose_name="Начало скидки")
    dateTo = models.DateField(verbose_name="Конец скидки")

    def __str__(self) -> str:
        return f"{self.salePrice} %"


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    count = models.IntegerField(null=True)
    date = models.CharField(max_length=100, default=date.today(), blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    fullDescription = models.TextField(null=True, blank=True)
    freeDelivery = models.BooleanField(default=False)
    images = models.ManyToManyField(ProductImage, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reviews = models.ManyToManyField(Review, blank=True)
    specifications = models.ManyToManyField(Specification, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    sale = models.ForeignKey(Sale, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def get_price(self):
        if self.sale:
            if self.sale.dateFrom <= date.today() <= self.sale.dateTo:
                return float(self.price) * (1 - self.sale.salePrice / 100)
        return self.price

    def __str__(self) -> str:
        return f"{self.title}"


'''
@receiver(post_save, sender=Product)
def set_default_product_image(sender, instance, **kwargs):
    """Обрабатывает запрос для продукта после сохранени в БД"""
    """Сейчас просто создает стандартную фотку, НО не прикрепляет ее к продукту"""
    if not instance.images.exists():
        default_image = ProductImage.objects.create()
        default_image.save()
        instance.images.add(default_image)
        instance.save()
'''

'''
@receiver(post_save, sender=Product)
def set_default_product_image(sender, instance, **kwargs):
    """Обрабатывает запрос для продукта после сохранени в БД"""
    """Сейчас просто создает стандартную фотку, НО не прикрепляет ее к продукту"""
    if len(instance.images.all()) == 0:
        print('work post_save')
        default_image = ProductImage.objects.create()
        default_image.save()
        instance.images.add(default_image)
'''
