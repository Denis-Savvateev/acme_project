# birthday/models.py
from django.db import models
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse
from django.contrib.auth import get_user_model

# Импортируется функция-валидатор.
from .validators import real_age


User = get_user_model()


class Tag(models.Model):
    '''Описание модели Tag'''
    tag = models.CharField(max_length=20, verbose_name='Тег')

    class Meta():
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag


class Birthday(models.Model):
    ''' Описание модели Birthday '''

    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(
        max_length=20,
        help_text='Необязательное поле',
        blank=True,
        verbose_name='Фамилия'
    )
    # Валидатор указывается в описании поля.
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )

    class Meta():
        verbose_name = 'день рождения'
        verbose_name_plural = 'Дни рождения'
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
