from django.contrib import admin
from .models import (
    Room, Device, LightDevice, TVDevice, ACDevice,
    CoffeeMachine, WasherDevice, SocketDevice, DeviceLog, Scene, SceneDevice
)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type_display', 'floor', 'created_at']
    list_filter = ['room_type', 'floor']
    search_fields = ['name', 'description']
    ordering = ['floor', 'name']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_type_display', 'room', 'status_display', 'is_online']
    list_filter = ['device_type', 'status', 'is_online', 'room']
    search_fields = ['name', 'ip_address', 'mac_address']
    ordering = ['room', 'device_type', 'name']

    # Добавляем поля для отображения
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'device_type', 'room', 'status')
        }),
        ('Сетевая информация', {
            'fields': ('is_online', 'ip_address', 'mac_address', 'firmware_version'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LightDevice)
class LightDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'brightness', 'color_temperature', 'is_dimmable', 'is_rgb']
    list_filter = ['is_dimmable', 'is_rgb']
    search_fields = ['device_ptr__name']

    def device_name(self, obj):
        return obj.device_ptr.name

    device_name.short_description = 'Название'
    device_name.admin_order_field = 'device_ptr__name'


@admin.register(TVDevice)
class TVDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'volume', 'channel', 'is_muted']
    list_filter = ['is_muted']
    search_fields = ['device_ptr__name']

    def device_name(self, obj):
        return obj.device_ptr.name

    device_name.short_description = 'Название'
    device_name.admin_order_field = 'device_ptr__name'


@admin.register(ACDevice)
class ACDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'temperature', 'mode_display', 'fan_speed', 'swing']
    list_filter = ['mode', 'swing']
    search_fields = ['device_ptr__name']

    def device_name(self, obj):
        return obj.device_ptr.name

    device_name.short_description = 'Название'
    device_name.admin_order_field = 'device_ptr__name'


@admin.register(CoffeeMachine)
class CoffeeMachineAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'water_level', 'beans_level', 'strength_display', 'size_display']
    list_filter = ['strength', 'size']
    search_fields = ['device_ptr__name']

    def device_name(self, obj):
        return obj.device_ptr.name

    device_name.short_description = 'Название'
    device_name.admin_order_field = 'device_ptr__name'


@admin.register(WasherDevice)
class WasherDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'program_display', 'temperature', 'spin_speed', 'is_running']
    list_filter = ['program', 'is_running']
    search_fields = ['device_ptr__name']

    def device_name(self, obj):
        return obj.device_ptr.name

    device_name.short_description = 'Название'
    device_name.admin_order_field = 'device_ptr__name'


@admin.register(SocketDevice)
class SocketDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'power_consumption', 'voltage', 'current', 'is_child_lock']
    list_filter = ['is_child_lock']
    search_fields = ['device_ptr__name']

    def device_name(self, obj):
        return obj.device_ptr.name

    device_name.short_description = 'Название'
    device_name.admin_order_field = 'device_ptr__name'


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ['device', 'action', 'user', 'created_at']
    list_filter = ['device', 'created_at']
    search_fields = ['action', 'device__name']
    readonly_fields = ['created_at']


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(SceneDevice)
class SceneDeviceAdmin(admin.ModelAdmin):
    list_display = ['scene', 'device', 'target_status']
    list_filter = ['target_status']
    search_fields = ['scene__name', 'device__name']


# Настройка заголовков админки
admin.site.site_header = "Умный дом - Администрирование"
admin.site.site_title = "Умный дом"
admin.site.index_title = "Добро пожаловать в систему управления умным домом"