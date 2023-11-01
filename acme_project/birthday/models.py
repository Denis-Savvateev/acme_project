# birthday/models.py
from django.db import models

# Импортируется функция-валидатор.
from .validators import real_age


class Birthday(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(
        max_length=20,
        help_text='Необязательное поле',
        blank=True,
        verbose_name='Фамилия'
    )
    # Валидатор указывается в описании поля.
    birthday = models.DateField('Дата рождения', validators=(real_age,))

    class Meta():
        verbose_name = 'день рождения'
        verbose_name_plural = 'Дни рождения'
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )
