from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ProfitableTransactionForm, ExpenditureTransactionForm
from .models import ProfitableTransaction, ExpenditureTransaction
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from datetime import date

def home(request):
    return render(request, 'transaction/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'transaction/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('recorded')
            except IntegrityError:
                return render(request, 'transaction/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Пользователь с таким именем уже существует!'})

        else:
            return render(request, 'transaction/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали!'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'transaction/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'transaction/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные входа!'})
        else:
            login(request, user)
            return redirect('recorded')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def recordedtransactions(request):
    protransactions = ProfitableTransaction.objects.all()
    exptransactions = ExpenditureTransaction.objects.all()

    # Получение списков из qweryset'ов
    valuespro_list = protransactions.values()
    valuesexp_list = exptransactions.values()

    # Задаём переменные общих размеров доходов и расходов, а также счётчики транзакций
    sumpro = 0
    sumexp = 0
    countpro = 0
    countexp = 0


    # Итерируемся по спискам
    for item in valuespro_list:
        valuepro = item['amount']
        sumpro += valuepro
        countpro += 1

    for item in valuesexp_list:
        valueexp = round(item['meter_quantity'] * item['price_per_meter_unit'], 2)
        sumexp += valueexp
        countexp += 1

    # Вычисляем баланс нашей учётной базы
    total_balance = sumpro - sumexp

    # Получаем минимальную дату из БД по доходам
    oldest_date_pro = ProfitableTransaction.objects.aggregate(Min('date'))['date__min']
    if not oldest_date_pro:
        return 0
    # Разница между текущей датой и самой старой датой
    delta_date_pro = (date.today() - oldest_date_pro).days + 1

    # Получаем минимальную дату из БД по расходам
    oldest_date_exp = ExpenditureTransaction.objects.aggregate(Min('date'))['date__min']
    if not oldest_date_exp:
        return 0
    # Разница между текущей датой и самой старой датой
    delta_date_exp = (date.today() - oldest_date_exp).days + 1

    # Находим общий срок ведения учёта
    delta_days = [delta_date_pro, delta_date_exp]
    max_delta_days = max(delta_days)

    # Находим самую первую дату учёта
    if delta_date_pro >= delta_date_exp:
        oldest_of_oldest_dates = oldest_date_pro
    else:
        oldest_of_oldest_dates = oldest_date_exp

    # Вычисляем скорости доходов и затрат
    total_revenue_rate = round(sumpro / max_delta_days, 2)
    total_expense_rate = round(sumexp / max_delta_days, 2)

    # Вычисляем скорость прибыли
    margin_total_rate = total_revenue_rate - total_expense_rate

    # Получаем текущую дату
    today = date.today()

    # Эта переменная для пунктира
    multidash = '- ' * 117

    # Формируем контекст вывода на страницу
    context = {'protransactions': protransactions, 'exptransactions': exptransactions,
               'sumpro': sumpro, 'sumexp': sumexp, 'countpro': countpro, 'countexp': countexp,
               'total_revenue_rate': total_revenue_rate, 'total_expense_rate': total_expense_rate,
               'total_balance': total_balance, 'margin_total_rate': margin_total_rate,
               'today': today, 'max_delta_days': max_delta_days,
               'oldest_of_oldest_dates': oldest_of_oldest_dates, 'multidash': multidash}

    return render(request, 'transaction/recordedtransactions.html', context)


@login_required
def createprotransaction(request):
    if request.method == 'GET':
        return render(request, 'transaction/createprotransaction.html', {'form': ProfitableTransactionForm()})
    else:
        try:
            form = ProfitableTransactionForm(request.POST)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/createprotransaction.html', {'form': ProfitableTransactionForm(),
                                                                             'error': 'Неверные данные!'})



@login_required
def createexptransaction(request):
    if request.method == 'GET':
        return render(request, 'transaction/createexptransaction.html', {'form': ExpenditureTransactionForm()})
    else:
        try:
            form = ExpenditureTransactionForm(request.POST)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/createprotransaction.html', {'form': ExpenditureTransactionForm(),
                                                                             'error': 'Неверные данные!'})

@login_required
def viewprotransaction(request, protransaction_pk):
    protransaction = get_object_or_404(ProfitableTransaction, pk=protransaction_pk)
    form = ProfitableTransactionForm(instance=protransaction)
    if request.method == 'GET':
        return render(request, 'transaction/viewprotransaction.html', {'protransaction': protransaction,
                                                                       'form': form})
    else:
        try:
            form = ProfitableTransactionForm(request.POST, instance=protransaction)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/viewprotransaction.html', {'protransaction': protransaction,
                                                                           'form': form})

@login_required
def viewexptransaction(request, exptransaction_pk):
   exptransaction = get_object_or_404(ExpenditureTransaction, pk=exptransaction_pk)
   form = ExpenditureTransactionForm(instance=exptransaction)
   if request.method == 'GET':
       return render(request, 'transaction/viewexptransaction.html', {'exptransaction': exptransaction,
                                                                       'form': form})
   else:
       try:
           form = ExpenditureTransactionForm(request.POST, instance=exptransaction)
           form.save()
           return redirect('recorded')
       except ValueError:
           return render(request, 'transaction/viewexptransaction.html', {'exptransaction': exptransaction,
                                                                          'form': form})

@login_required
def deleteprotransaction(request, protransaction_pk):
    protransaction = get_object_or_404(ProfitableTransaction, pk=protransaction_pk)
    if request.method == 'POST':
        protransaction.delete()
        return redirect('recorded')

@login_required
def deleteexptransaction(request, exptransaction_pk):
    exptransaction = get_object_or_404(ExpenditureTransaction, pk=exptransaction_pk)
    if request.method == 'POST':
        exptransaction.delete()
        return redirect('recorded')