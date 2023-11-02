# birthday/views.py
# Для создания CBV-объектов
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
# reverse_lazy() срабатывает только при непосредственном обращении
# к CBV во время работы веб-сервера, а не на этапе запуска проекта,
# когда импортируются все классы. В момент запуска проекта карта
# маршрутов может быть ещё не сформирована, и использование обычного
# reverse() вызовет ошибку
from django.urls import reverse_lazy

from .forms import BirthdayForm
# Импортируем модель дней рождения.
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


# Создаём миксины.
# И убираем, за ненадобностью... Оставляю, как пример.
# class BirthdayMixin:
    # Указываем модель, с которой работает CBV...
#    model = Birthday
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
#    success_url = reverse_lazy('birthday:list')

# Убираем в связи с переименованием шаблона birthday.html' в
# ожидаемое классом имя.
# class BirthdayFormMixin:
    # Сопутствующий класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    # fields = '__all__'
    # Но виджетом-календарь и контроль имён у нас в отдельной форме
    # Указываем вместо полей имя формы:
#    form_class = BirthdayForm
    # По логике классов CBV, имя шаблона должно быть birthday_form.html
    # Поэтому мы явным образом указываем шаблон:
#    template_name = 'birthday/birthday.html'


# Добавляем миксин первым по списку родительских классов.
# Убрали миксин за ненадобностью
class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
