from django.contrib import admin
from .models import CPU, GPU, Motherboard, RAM, PSU, Case, Build


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'manufacturer', 
        'socket', 
        'cores', 
        'threads', 
        'base_clock', 
        'tdp', 
        'benchmark_score', 
        'avg_used_price'
    ]
    list_filter = ['socket', 'manufacturer', 'has_integrated_gpu']
    search_fields = ['name', 'manufacturer']
    ordering = ['-benchmark_score']


@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'manufacturer', 
        'vram', 
        'memory_type', 
        'tdp', 
        'length',
        'benchmark_score', 
        'avg_used_price'
    ]
    list_filter = ['memory_type', 'manufacturer', 'vram']
    search_fields = ['name', 'manufacturer']
    ordering = ['-benchmark_score']


@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'manufacturer', 
        'socket', 
        'chipset', 
        'form_factor', 
        'memory_type', 
        'memory_slots',
        'avg_used_price'
    ]
    list_filter = ['socket', 'form_factor', 'memory_type', 'manufacturer']
    search_fields = ['name', 'manufacturer', 'chipset']


@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'manufacturer', 
        'memory_type', 
        'capacity', 
        'modules', 
        'speed', 
        'avg_used_price'
    ]
    list_filter = ['memory_type', 'capacity', 'manufacturer']
    search_fields = ['name', 'manufacturer']


@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'manufacturer', 
        'wattage', 
        'efficiency', 
        'is_modular', 
        'avg_used_price'
    ]
    list_filter = ['efficiency', 'is_modular', 'manufacturer', 'wattage']
    search_fields = ['name', 'manufacturer']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'manufacturer', 
        'form_factor',
        'max_gpu_length', 
        'max_cpu_cooler_height', 
        'avg_used_price'
    ]
    list_filter = ['form_factor', 'manufacturer']
    search_fields = ['name', 'manufacturer']


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'user', 
        'cpu', 
        'gpu', 
        'motherboard',
        'is_public', 
        'created_at'
    ]
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'