from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Service, Room, Category, Guest, ProvisionOfService, Reservation


def index(request):

    current_user = request.user

    if not current_user.is_authenticated:
        return redirect('login')

    if current_user.groups.filter(name="Manager").exists():
        return service_list_manager(request)

    if current_user.groups.filter(name="Clients").exists():
        return service_list_client(request)

    return service_list_guest(request)


def service_list_guest(request):

    services = Service.objects.all()

    context = {
        'services': services
    }

    return render(request, 'index_guest.html', context)


def service_list_client(request):

    services = Service.objects.all()

    context = {
        'services': services
    }

    return render(request, 'index_client.html', context)


def service_list_manager(request):

    services = Service.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        messages.add_message(request, messages.SUCCESS, f"Выведены услуги по запросу: {search_query}.")
        services = services.filter(name__icontains=search_query)

    context = {
        'services': services,
        'search': search_query
    }

    return render(request, 'index_manager.html', context)


def clients(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect('index')

    clients_list = Guest.objects.all().order_by("name")

    sorting = request.GET.get('sort', '')
    if sorting == "asc":
        clients_list = clients_list.order_by("name")
        messages.add_message(request, messages.SUCCESS, "Клиенты сортированы в алфавитном порядке.")
    else:
        clients_list = clients_list.order_by("-name")
        messages.add_message(request, messages.SUCCESS, "Клиенты сортированы в обратном порядке.")

    return render(request, "clients.html", { 'clients' : clients_list, 'sorting': sorting })


def rooms(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect('index')

    rooms_list = Room.objects.all().select_related('category').order_by('id')
    categories = Category.objects.all()

    berths_count_filter = request.GET.get('berths-filter', '')
    category_filter = request.GET.get('category-filter', '')

    if berths_count_filter:
        messages.add_message(request, messages.SUCCESS, f"Применен фильтр по количеству спальных мест: {berths_count_filter}.")
        rooms_list = rooms_list.filter(berths_count = int(berths_count_filter))

    if category_filter:
        messages.add_message(request, messages.SUCCESS, f"Применен фильтр по категории мест: {category_filter}.")
        rooms_list = rooms_list.filter(category__name = category_filter)

    context = {
        'rooms': rooms_list,
        'categories': categories,
        'berths_filter': berths_count_filter,
        'category_filter': category_filter
    }

    return render(request, 'rooms.html', context)


def service_provision(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect('index')

    provisions = ProvisionOfService.objects.all().order_by('-date_of_provision')
    reservations = Reservation.objects.all().order_by('-id')
    services = Service.objects.all()

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation')
        service_id = request.POST.get('service')
        provision_count = request.POST.get('count')
        provision_date = request.POST.get('date-of-provision')

        new_provision = ProvisionOfService()
        new_provision.reservation = reservations.get(id=reservation_id)
        new_provision.service = services.get(id=service_id)
        new_provision.count = provision_count
        new_provision.date_of_provision = provision_date

        new_provision.save()

        messages.add_message(request, messages.SUCCESS, "Запись на услугу оформлена успешно.")

    context = {
        'provisions': provisions,
        'reservations': reservations,
        'services': services
    }

    return render(request, 'service_provision.html', context)


def login_page(request):
    
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=login_input, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f"Вы вошли в аккаунт {login_input} успешно.")
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль.'})
    
    return render(request, 'login.html')


def register_page(request):

    if request.method == 'POST':
        login_input = request.POST.get('login')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')

        if password == password_confirm:
            user = User.objects.create_user(username=login_input, first_name=first_name, last_name=last_name, email=email, password=password)
            clients_group = Group.objects.get_or_create(name="Clients")
            user.groups.add(clients_group[0])
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f"Регистрация прошла успешно.")
            return redirect('index')
        else:
            return render(request, 'register.html', {'error': 'Пароли не совпадают.'})

    return render(request, 'register.html')


def guest_login(request):
    
    guest_user = authenticate(request, username='guest', password='guestpassword')
    login(request, guest_user)

    messages.add_message(request, messages.SUCCESS, f"Вы вошли как гость.")

    return redirect('index')


def logout_page(request):
    
    logout(request)
    return redirect('login')