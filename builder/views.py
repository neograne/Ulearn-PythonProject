from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Avg, Count
from .models import CPU, GPU, Motherboard, RAM, PSU, Case, Build
from .forms import BuildForm, CPUFilterForm, GPUFilterForm, RegistrationForm


def home(request):
    """Главная страница"""
    context = {
        'cpu_count': CPU.objects.count(),
        'gpu_count': GPU.objects.count(),
        'motherboard_count': Motherboard.objects.count(),
        'ram_count': RAM.objects.count(),
        'psu_count': PSU.objects.count(),
        'case_count': Case.objects.count(),
        'build_count': Build.objects.filter(is_public=True).count(),
        'latest_builds': Build.objects.filter(is_public=True)[:3],
    }
    return render(request, 'builder/home.html', context)


# ==================== КАТАЛОГ ====================

def cpu_list(request):
    """Список процессоров"""
    cpus = CPU.objects.all()
    
    # Фильтрация
    socket = request.GET.get('socket')
    manufacturer = request.GET.get('manufacturer')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', '-benchmark_score')
    
    if socket:
        cpus = cpus.filter(socket=socket)
    if manufacturer:
        cpus = cpus.filter(manufacturer__icontains=manufacturer)
    if min_price:
        cpus = cpus.filter(avg_used_price__gte=min_price)
    if max_price:
        cpus = cpus.filter(avg_used_price__lte=max_price)
    
    # Сортировка
    if sort in ['avg_used_price', '-avg_used_price', 'benchmark_score', '-benchmark_score', 'name']:
        cpus = cpus.order_by(sort)
    
    context = {
        'cpus': cpus,
        'socket_choices': CPU.SOCKET_CHOICES,
        'current_socket': socket,
        'current_sort': sort,
    }
    return render(request, 'builder/cpu_list.html', context)


def cpu_detail(request, pk):
    """Детальная страница процессора"""
    cpu = get_object_or_404(CPU, pk=pk)
    # Похожие процессоры (тот же сокет, похожая цена)
    similar = CPU.objects.filter(socket=cpu.socket).exclude(pk=pk)[:4]
    return render(request, 'builder/cpu_detail.html', {'cpu': cpu, 'similar': similar})


def gpu_list(request):
    """Список видеокарт"""
    gpus = GPU.objects.all()
    
    # Фильтрация
    manufacturer = request.GET.get('manufacturer')
    vram = request.GET.get('vram')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', '-benchmark_score')
    
    if manufacturer:
        gpus = gpus.filter(manufacturer__icontains=manufacturer)
    if vram:
        gpus = gpus.filter(vram=vram)
    if min_price:
        gpus = gpus.filter(avg_used_price__gte=min_price)
    if max_price:
        gpus = gpus.filter(avg_used_price__lte=max_price)
    
    if sort in ['avg_used_price', '-avg_used_price', 'benchmark_score', '-benchmark_score', 'name']:
        gpus = gpus.order_by(sort)
    
    context = {
        'gpus': gpus,
        'current_sort': sort,
    }
    return render(request, 'builder/gpu_list.html', context)


def gpu_detail(request, pk):
    """Детальная страница видеокарты"""
    gpu = get_object_or_404(GPU, pk=pk)
    similar = GPU.objects.filter(vram=gpu.vram).exclude(pk=pk)[:4]
    return render(request, 'builder/gpu_detail.html', {'gpu': gpu, 'similar': similar})


def motherboard_list(request):
    """Список материнских плат"""
    motherboards = Motherboard.objects.all()
    
    socket = request.GET.get('socket')
    form_factor = request.GET.get('form_factor')
    sort = request.GET.get('sort', 'name')
    
    if socket:
        motherboards = motherboards.filter(socket=socket)
    if form_factor:
        motherboards = motherboards.filter(form_factor=form_factor)
    
    if sort in ['avg_used_price', '-avg_used_price', 'name']:
        motherboards = motherboards.order_by(sort)
    
    context = {
        'motherboards': motherboards,
        'socket_choices': Motherboard.SOCKET_CHOICES,
        'form_factor_choices': Motherboard.FORM_FACTOR_CHOICES,
        'current_socket': socket,
        'current_form_factor': form_factor,
        'current_sort': sort,
    }
    return render(request, 'builder/motherboard_list.html', context)


def ram_list(request):
    """Список оперативной памяти"""
    rams = RAM.objects.all()
    
    memory_type = request.GET.get('memory_type')
    capacity = request.GET.get('capacity')
    sort = request.GET.get('sort', '-capacity')
    
    if memory_type:
        rams = rams.filter(memory_type=memory_type)
    if capacity:
        rams = rams.filter(capacity=capacity)
    
    if sort in ['avg_used_price', '-avg_used_price', 'capacity', '-capacity', 'speed', '-speed']:
        rams = rams.order_by(sort)
    
    context = {
        'rams': rams,
        'memory_type_choices': RAM.MEMORY_TYPE_CHOICES,
        'current_memory_type': memory_type,
        'current_sort': sort,
    }
    return render(request, 'builder/ram_list.html', context)


def psu_list(request):
    """Список блоков питания"""
    psus = PSU.objects.all()
    
    efficiency = request.GET.get('efficiency')
    min_wattage = request.GET.get('min_wattage')
    sort = request.GET.get('sort', '-wattage')
    
    if efficiency:
        psus = psus.filter(efficiency=efficiency)
    if min_wattage:
        psus = psus.filter(wattage__gte=min_wattage)
    
    if sort in ['avg_used_price', '-avg_used_price', 'wattage', '-wattage']:
        psus = psus.order_by(sort)
    
    context = {
        'psus': psus,
        'efficiency_choices': PSU.EFFICIENCY_CHOICES,
        'current_efficiency': efficiency,
        'current_sort': sort,
    }
    return render(request, 'builder/psu_list.html', context)


def case_list(request):
    """Список корпусов"""
    cases = Case.objects.all()
    
    form_factor = request.GET.get('form_factor')
    sort = request.GET.get('sort', 'name')
    
    if form_factor:
        cases = cases.filter(form_factor=form_factor)
    
    if sort in ['avg_used_price', '-avg_used_price', 'name', 'max_gpu_length']:
        cases = cases.order_by(sort)
    
    context = {
        'cases': cases,
        'form_factor_choices': Case.FORM_FACTOR_CHOICES,
        'current_form_factor': form_factor,
        'current_sort': sort,
    }
    return render(request, 'builder/case_list.html', context)


# ==================== СБОРКИ ====================

def build_list(request):
    """Список публичных сборок"""
    builds = Build.objects.filter(is_public=True).select_related(
        'user', 'cpu', 'gpu', 'motherboard', 'ram', 'psu', 'case'
    )
    return render(request, 'builder/build_list.html', {'builds': builds})


def build_detail(request, pk):
    """Детальная страница сборки"""
    build = get_object_or_404(Build, pk=pk)
    
    # Проверка доступа (приватные сборки видит только владелец)
    if not build.is_public and build.user != request.user:
        messages.error(request, 'Эта сборка приватная.')
        return redirect('build_list')
    
    # Проверка совместимости
    compatibility_errors = check_compatibility(build)
    
    # График распределения бюджета
    budget_chart = generate_budget_chart(build)
    
    context = {
        'build': build,
        'compatibility_errors': compatibility_errors,
        'budget_chart': budget_chart,
        'total_price': build.get_total_price(),
        'total_tdp': build.get_total_tdp(),
        'recommended_psu': build.get_recommended_psu_wattage(),
    }
    return render(request, 'builder/build_detail.html', context)


@login_required
def build_create(request):
    """Создание новой сборки"""
    if request.method == 'POST':
        form = BuildForm(request.POST)
        if form.is_valid():
            build = form.save(commit=False)
            build.user = request.user
            build.save()
            messages.success(request, f'Сборка "{build.name}" успешно создана!')
            return redirect('build_detail', pk=build.pk)
    else:
        form = BuildForm()
    
    return render(request, 'builder/build_form.html', {'form': form, 'title': 'Новая сборка'})


@login_required
def build_edit(request, pk):
    """Редактирование сборки"""
    build = get_object_or_404(Build, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BuildForm(request.POST, instance=build)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сборка обновлена!')
            return redirect('build_detail', pk=build.pk)
    else:
        form = BuildForm(instance=build)
    
    return render(request, 'builder/build_form.html', {'form': form, 'title': 'Редактировать сборку'})


@login_required
def build_delete(request, pk):
    """Удаление сборки"""
    build = get_object_or_404(Build, pk=pk, user=request.user)
    
    if request.method == 'POST':
        name = build.name
        build.delete()
        messages.success(request, f'Сборка "{name}" удалена.')
        return redirect('my_builds')
    
    return render(request, 'builder/build_confirm_delete.html', {'build': build})


@login_required
def my_builds(request):
    """Мои сборки (личный кабинет)"""
    builds = Build.objects.filter(user=request.user).select_related(
        'cpu', 'gpu', 'motherboard', 'ram', 'psu', 'case'
    )
    return render(request, 'builder/my_builds.html', {'builds': builds})


# ==================== АВТОРИЗАЦИЯ ====================

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def check_compatibility(build):
    """Проверка совместимости компонентов"""
    errors = []
    
    # CPU + Motherboard (сокет)
    if build.cpu and build.motherboard:
        if build.cpu.socket != build.motherboard.socket:
            errors.append({
                'type': 'error',
                'message': f'Сокет процессора ({build.cpu.socket}) не совместим с материнской платой ({build.motherboard.socket})'
            })
    
    # RAM + Motherboard (тип памяти)
    if build.ram and build.motherboard:
        if build.ram.memory_type != build.motherboard.memory_type:
            errors.append({
                'type': 'error',
                'message': f'Тип памяти ({build.ram.memory_type}) не поддерживается материнской платой ({build.motherboard.memory_type})'
            })
    
    # GPU + Case (длина)
    if build.gpu and build.case:
        if build.gpu.length > build.case.max_gpu_length:
            errors.append({
                'type': 'error',
                'message': f'Видеокарта ({build.gpu.length}мм) не поместится в корпус (макс. {build.case.max_gpu_length}мм)'
            })
    
    # Motherboard + Case (форм-фактор)
    if build.motherboard and build.case:
        mb_ff = build.motherboard.form_factor
        case_ff = build.case.form_factor
        # ATX корпус поддерживает ATX, mATX, ITX
        # mATX корпус поддерживает mATX, ITX
        # ITX корпус поддерживает только ITX
        compatible = False
        if case_ff == 'ATX':
            compatible = True
        elif case_ff == 'mATX' and mb_ff in ['mATX', 'ITX']:
            compatible = True
        elif case_ff == 'ITX' and mb_ff == 'ITX':
            compatible = True
        
        if not compatible:
            errors.append({
                'type': 'error',
                'message': f'Материнская плата ({mb_ff}) не подходит для корпуса ({case_ff})'
            })
    
    # PSU (мощность)
    if build.psu:
        recommended = build.get_recommended_psu_wattage()
        if build.psu.wattage < recommended:
            errors.append({
                'type': 'warning',
                'message': f'Мощности БП ({build.psu.wattage}Вт) может не хватить. Рекомендуется: {recommended}Вт'
            })
    
    return errors


def generate_budget_chart(build):
    """Генерация графика распределения бюджета (Plotly)"""
    import plotly.graph_objects as go
    
    labels = []
    values = []
    
    components = [
        ('Процессор', build.cpu),
        ('Видеокарта', build.gpu),
        ('Мат. плата', build.motherboard),
        ('RAM', build.ram),
        ('Блок питания', build.psu),
        ('Корпус', build.case),
    ]
    
    for label, component in components:
        if component and component.avg_used_price:
            labels.append(label)
            values.append(float(component.avg_used_price))
    
    if not values:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',
        marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'])
    )])
    
    fig.update_layout(
        title='Распределение бюджета',
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)