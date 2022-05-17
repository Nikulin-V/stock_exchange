from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe

from users.models import CustomUser
from tinymce.models import HTMLField
from sorl.thumbnail import get_thumbnail


class IndustryManager(models.Manager):
    def get_companies_by_industry(self):
        companies_by_industry = dict()
        for industry in self.get_queryset().filter(companies__is_active=True).all():
            if len(industry.companies.all()) > 0:
                companies_by_industry[industry] = industry.companies.all()
        return companies_by_industry


class Industry(models.Model):
    industries = IndustryManager()

    name = models.CharField('Название отрасли', unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отрасль'
        verbose_name_plural = 'Отрасли'


class Company(models.Model):
    name = models.CharField('Название компании', unique=True, max_length=255)
    is_active = models.BooleanField('Активно', default=True)
    industry = models.ForeignKey(Industry, default='Другое', verbose_name='Отрасль',
                                 on_delete=models.SET_DEFAULT, related_name='companies')
    trust_points = models.IntegerField('Очки доверия', default=0, validators=[MinValueValidator(0)])

    description = HTMLField('Описание', help_text='Опишите компанию', max_length=1024, null=True)
    owners = models.ManyToManyField(CustomUser, verbose_name='Владельцы',
                                    related_name='companies', blank=True)
    upload = models.ImageField(upload_to='uploads/', blank=True,
                               verbose_name='Логотип компании')
    gallery = models.ManyToManyField('companies.Photo', blank=True, verbose_name='Фотографии',
                                     related_name='companies')

    def get_image_x1280(self):
        return get_thumbnail(self.upload, '1280', quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.upload, '400x300', crop='center', quality=51)

    def image_tmb(self):
        if self.upload:
            return mark_safe(f'<img src="{self.upload.url}" width="50">')
        return 'Нет изображения'

    def image_small(self):
        if self.upload:
            return mark_safe(f'<img src="{self.upload.url}" width="150">')
        return 'Нет изображения'

    image_tmb.short_description = 'Логотип'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Photo(models.Model):
    upload = models.ImageField(upload_to='uploads/', null=True)
    is_active = models.BooleanField('Активно', default=True)
    company = models.ForeignKey(Company, verbose_name="Компания",
                                on_delete=models.CASCADE)

    def image(self):
        if self.upload:
            return mark_safe(f'<img src="{self.upload.url}" width="200">')
        return '-'

    def big_image(self):
        if self.upload:
            return mark_safe(f'<img src="{self.upload.url}" width="450">')
        return '-'

    image.short_description = 'Картинка'

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
