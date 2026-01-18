from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class CPU(models.Model):
    """Процессор"""
    
    SOCKET_CHOICES = [
        ('AM4', 'AMD AM4'),
        ('AM5', 'AMD AM5'),
        ('LGA1151', 'Intel LGA1151 v2'),
        ('LGA1200', 'Intel LGA1200'),
        ('LGA1700', 'Intel LGA1700'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=100)
    socket = models.CharField('Сокет', max_length=20, choices=SOCKET_CHOICES)
    cores = models.PositiveIntegerField('Количество ядер')
    threads = models.PositiveIntegerField('Количество потоков')
    base_clock = models.FloatField('Базовая частота (GHz)')
    boost_clock = models.FloatField('Турбо частота (GHz)')
    tdp = models.PositiveIntegerField('TDP (Вт)')
    has_integrated_gpu = models.BooleanField('Встроенная графика', default=False)
    benchmark_score = models.PositiveIntegerField('Benchmark Score')
    avg_used_price = models.DecimalField(
        'Средняя цена б/у',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Процессор'
        verbose_name_plural = 'Процессоры'
        ordering = ['-benchmark_score']

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class GPU(models.Model):
    """Видеокарта"""
    
    MEMORY_TYPE_CHOICES = [
        ('GDDR5', 'GDDR5'),
        ('GDDR6', 'GDDR6'),
        ('GDDR6X', 'GDDR6X'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=100)
    vram = models.PositiveIntegerField('Видеопамять (GB)')
    memory_type = models.CharField('Тип памяти', max_length=10, choices=MEMORY_TYPE_CHOICES)
    core_clock = models.PositiveIntegerField('Частота ядра (MHz)')
    tdp = models.PositiveIntegerField('TDP (Вт)')
    length = models.PositiveIntegerField('Длина (мм)')
    benchmark_score = models.PositiveIntegerField('Benchmark Score')
    avg_used_price = models.DecimalField(
        'Средняя цена б/у',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Видеокарта'
        verbose_name_plural = 'Видеокарты'
        ordering = ['-benchmark_score']

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Motherboard(models.Model):
    """Материнская плата"""
    
    SOCKET_CHOICES = [
        ('AM4', 'AMD AM4'),
        ('AM5', 'AMD AM5'),
        ('LGA1151', 'Intel LGA1151 v2'),
        ('LGA1200', 'Intel LGA1200'),
        ('LGA1700', 'Intel LGA1700'),
    ]
    
    FORM_FACTOR_CHOICES = [
        ('ATX', 'ATX'),
        ('mATX', 'Micro-ATX'),
        ('ITX', 'Mini-ITX'),
    ]
    
    MEMORY_TYPE_CHOICES = [
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=100)
    socket = models.CharField('Сокет', max_length=20, choices=SOCKET_CHOICES)
    chipset = models.CharField('Чипсет', max_length=50)
    form_factor = models.CharField('Форм-фактор', max_length=10, choices=FORM_FACTOR_CHOICES)
    memory_type = models.CharField('Тип памяти', max_length=10, choices=MEMORY_TYPE_CHOICES)
    memory_slots = models.PositiveIntegerField('Слотов памяти')
    max_memory = models.PositiveIntegerField('Максимум RAM (GB)')
    avg_used_price = models.DecimalField(
        'Средняя цена б/у',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Материнская плата'
        verbose_name_plural = 'Материнские платы'
        ordering = ['manufacturer', 'name']

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class RAM(models.Model):
    """Оперативная память"""
    
    MEMORY_TYPE_CHOICES = [
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=100)
    memory_type = models.CharField('Тип памяти', max_length=10, choices=MEMORY_TYPE_CHOICES)
    capacity = models.PositiveIntegerField('Объём (GB)')
    modules = models.PositiveIntegerField('Количество модулей')
    speed = models.PositiveIntegerField('Частота (MHz)')
    avg_used_price = models.DecimalField(
        'Средняя цена б/у',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Оперативная память'
        verbose_name_plural = 'Оперативная память'
        ordering = ['-capacity', '-speed']

    def __str__(self):
        return f"{self.manufacturer} {self.name} {self.capacity}GB"


class PSU(models.Model):
    """Блок питания"""
    
    EFFICIENCY_CHOICES = [
        ('80+', '80 Plus'),
        ('Bronze', '80+ Bronze'),
        ('Silver', '80+ Silver'),
        ('Gold', '80+ Gold'),
        ('Platinum', '80+ Platinum'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=100)
    wattage = models.PositiveIntegerField('Мощность (Вт)')
    efficiency = models.CharField('Сертификат', max_length=20, choices=EFFICIENCY_CHOICES)
    is_modular = models.BooleanField('Модульный', default=False)
    avg_used_price = models.DecimalField(
        'Средняя цена б/у',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Блок питания'
        verbose_name_plural = 'Блоки питания'
        ordering = ['-wattage']

    def __str__(self):
        return f"{self.manufacturer} {self.name} {self.wattage}W"


class Case(models.Model):
    """Корпус"""
    
    FORM_FACTOR_CHOICES = [
        ('ATX', 'ATX'),
        ('mATX', 'Micro-ATX'),
        ('ITX', 'Mini-ITX'),
    ]
    
    name = models.CharField('Название', max_length=200)
    manufacturer = models.CharField('Производитель', max_length=100)
    form_factor = models.CharField('Форм-фактор', max_length=10, choices=FORM_FACTOR_CHOICES)
    max_gpu_length = models.PositiveIntegerField('Макс. длина GPU (мм)')
    max_cpu_cooler_height = models.PositiveIntegerField('Макс. высота кулера (мм)')
    avg_used_price = models.DecimalField(
        'Средняя цена б/у',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'
        ordering = ['manufacturer', 'name']

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Build(models.Model):
    """Сборка ПК"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='builds',
        verbose_name='Пользователь'
    )
    name = models.CharField('Название сборки', max_length=200)
    description = models.TextField('Описание', blank=True)
    
    # Связи с компонентами
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Процессор'
    )
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Видеокарта'
    )
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Материнская плата'
    )
    ram = models.ForeignKey(
        RAM,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Оперативная память'
    )
    psu = models.ForeignKey(
        PSU,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Блок питания'
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Корпус'
    )
    
    is_public = models.BooleanField('Публичная сборка', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Сборка'
        verbose_name_plural = 'Сборки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def get_total_price(self):
        """Расчёт общей стоимости сборки"""
        components = [self.cpu, self.gpu, self.motherboard, self.ram, self.psu, self.case]
        total = sum(
            component.avg_used_price
            for component in components
            if component and component.avg_used_price
        )
        return total

    def get_total_tdp(self):
        """Расчёт суммарного энергопотребления"""
        tdp = 0
        if self.cpu:
            tdp += self.cpu.tdp
        if self.gpu:
            tdp += self.gpu.tdp
        # Добавляем примерное потребление остальных компонентов
        tdp += 50  # RAM, накопители, вентиляторы
        return tdp

    def get_recommended_psu_wattage(self):
        """Рекомендуемая мощность БП (с запасом 30%)"""
        return int(self.get_total_tdp() * 1.3)

    def get_benchmark_score(self):
        """Комбинированный показатель производительности"""
        cpu_score = self.cpu.benchmark_score if self.cpu else 0
        gpu_score = self.gpu.benchmark_score if self.gpu else 0
        # Для игр GPU важнее: 60% GPU + 40% CPU
        return int(gpu_score * 0.6 + cpu_score * 0.4)