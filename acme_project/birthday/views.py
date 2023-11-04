# birthday/views.py
from django.shortcuts import get_object_or_404
# Для создания CBV-объектов импортируем View-классы:
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
# reverse_lazy() срабатывает только при непосредственном обращении
# к CBV во время работы веб-сервера, а не на этапе запуска проекта,
# когда импортируются все классы. В момент запуска проекта карта
# маршрутов может быть ещё не сформирована, и использование обычного
# reverse() вызовет ошибку
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BirthdayForm
# Импортируем модель дней рождения.
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    ''' Выводит список всех записей '''

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
class BirthdayCreateView(LoginRequiredMixin, CreateView):
    ''' Создаёт запись. '''

    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    ''' Редактирует запись. '''

    model = Birthday
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    ''' Удаляет запись. '''

    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class BirthdayDetailView(DetailView):
    ''' Выводит подробные сведения о записи '''

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
