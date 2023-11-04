# birthday/models.py
from django.db import models
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse
from django.contrib.auth import get_user_model

# Импортируется функция-валидатор.
from .validators import real_age


User = get_user_model()


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
