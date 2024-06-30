from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import date


class Image(models.Model):

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

    class Meta:
        verbose_name = "Изображение подкатегории"
        verbose_name_plural = "Изображения подкатегории"


class Subcategory(models.Model):

    title = models.CharField(max_length=100)
    image = models.ForeignKey(SubImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Category(models.Model):

    title = models.CharField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    subcategories = models.ManyToManyField(
        Subcategory, related_name="category", blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


@receiver(pre_save, sender=Category)
def set_default_image(sender, instance, **kwargs):
    if not instance.image:
        instance.image = Image.objects.create()


@receiver(pre_save, sender=Subcategory)
def set_default_category_subimage(sender, instance, **kwargs):
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

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продукта"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Review(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="Почта")
    text = models.TextField()
    rate = models.IntegerField(verbose_name="Оценка")
    date = models.CharField(max_length=100, null=True, default=date.today(), blank=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Specification(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class Sale(models.Model):
    salePrice = models.IntegerField(null=False, verbose_name="Процент скидки %")
    dateFrom = models.DateField(verbose_name="Начало скидки")
    dateTo = models.DateField(verbose_name="Конец скидки")

    def __str__(self) -> str:
        return f"{self.salePrice} %"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


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

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
