from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from tinymce.models import HTMLField
from string import ascii_lowercase
from django.utils.translation import gettext_lazy as _

from companies.managers import *
from rating.models import Rating
from users.models import CustomUser

ALPHABET = set(ascii_lowercase + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ' + '1234567890' + '_')


class Industry(models.Model):
    industries = IndustryManager()

    name = models.CharField('Название отрасли', unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отрасль'
        verbose_name_plural = 'Отрасли'


def validate_string(value):
    if all(letter in ALPHABET for letter in value.lower()):
        return True
    raise ValidationError(
        _('Неверное значение: %(value)s'),
        params={'value': value},
)


class Company(models.Model):
    companies = CompanyManager()

    name = models.CharField('Название компании', unique=True, max_length=255,
                            validators=[validate_string])
    is_active = models.BooleanField('Активно', default=True)
    industry = models.ForeignKey(
        Industry,
        default='Другое',
        verbose_name='Отрасль',
        on_delete=models.SET_DEFAULT,
        related_name='companies',
    )

    description = HTMLField(
        'Описание',
        help_text='Опишите компанию',
        max_length=1024,
        blank=True,
        default='Эта компания ничего о себе не сказала, но мы уверены, что она очень хорошая!',
    )
    stockholders = models.ManyToManyField(
        CustomUser, verbose_name='Акционеры', related_name='companies', blank=True
    )
    upload = models.ImageField(upload_to='uploads/', blank=True, verbose_name='Логотип компании')
    gallery = models.ManyToManyField(
        'companies.Photo',
        blank=True,
        verbose_name='Фотографии',
        related_name='companies',
    )

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
    company = models.ForeignKey(Company, verbose_name="Компания", on_delete=models.CASCADE)

    def image(self):
        if self.upload:
            return mark_safe(f'<img src="{self.upload.url}" width="200">')
        return '-'

    def big_image(self):
        if self.upload:
            return mark_safe(f'<img src="{self.upload.url}" width="500">')
        return '-'

    image.short_description = 'Картинка'

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
