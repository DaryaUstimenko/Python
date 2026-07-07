# devices/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Room, Device, LightDevice, TVDevice, ACDevice, CoffeeMachine, WasherDevice, SocketDevice, DeviceLog, \
    Scene
import json


def dashboard(request):
    """Главная панель управления"""
    rooms = Room.objects.all()
    devices = Device.objects.all()

    stats = {
        'total': devices.count(),
        'online': devices.filter(is_online=True).count(),
        'on': devices.filter(status='on').count(),
        'off': devices.filter(status='off').count(),
        'rooms': rooms.count(),
    }

    rooms_data = []
    for room in rooms:
        room_devices = room.devices.all()
        rooms_data.append({
            'room': room,
            'devices': room_devices,
            'count': room_devices.count()
        })

    context = {
        'rooms': rooms_data,
        'stats': stats,
        'total_devices': stats['total'],
        'scenes': Scene.objects.filter(is_active=True)
    }
    return render(request, 'devices/dashboard.html', context)


def device_list(request):
    """Список всех устройств"""
    device_type = request.GET.get('type')
    room_id = request.GET.get('room')

    devices = Device.objects.all()

    if device_type:
        devices = devices.filter(device_type=device_type)
    if room_id:
        devices = devices.filter(room_id=room_id)

    context = {
        'devices': devices,
        'device_types': Device.DEVICE_TYPES,
        'rooms': Room.objects.all(),
        'selected_type': device_type,
        'selected_room': room_id
    }
    return render(request, 'devices/device_list.html', context)


def device_detail(request, device_id):
    """Детальная страница устройства (универсальная)"""
    device = get_object_or_404(Device, id=device_id)

    # Получаем специфичные данные для типа устройства
    specific_data = None
    if device.device_type == 'light':
        specific_data = LightDevice.objects.filter(id=device_id).first()
    elif device.device_type == 'tv':
        specific_data = TVDevice.objects.filter(id=device_id).first()
    elif device.device_type == 'ac':
        specific_data = ACDevice.objects.filter(id=device_id).first()
    elif device.device_type == 'coffee':
        specific_data = CoffeeMachine.objects.filter(id=device_id).first()
    elif device.device_type == 'washer':
        specific_data = WasherDevice.objects.filter(id=device_id).first()
    elif device.device_type == 'socket':
        specific_data = SocketDevice.objects.filter(id=device_id).first()

    # Логи устройства
    logs = DeviceLog.objects.filter(device=device)[:20]

    context = {
        'device': device,
        'specific_data': specific_data,
        'logs': logs,
        'status_choices': Device.STATUS_CHOICES
    }
    return render(request, 'devices/device_detail.html', context)


def toggle_device(request, device_id):
    """Включение/выключение устройства"""
    device = get_object_or_404(Device, id=device_id)

    old_status = device.status
    device.toggle_status()

    # Логируем действие
    DeviceLog.objects.create(
        device=device,
        action="Переключение статуса",
        old_status=old_status,
        new_status=device.status
    )

    messages.success(request, f"{device.name}: {'Включено' if device.status == 'on' else 'Выключено'}")

    next_url = request.META.get('HTTP_REFERER', 'devices:dashboard')
    return redirect(next_url)


@require_http_methods(["POST"])
def control_device(request, device_id):
    """Универсальное управление устройством (AJAX)"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        device = get_object_or_404(Device, id=device_id)

        # Базовые действия
        if action == 'toggle':
            old_status = device.status
            device.toggle_status()
            DeviceLog.objects.create(
                device=device,
                action="Переключение статуса",
                old_status=old_status,
                new_status=device.status
            )
            return JsonResponse({
                'success': True,
                'message': f'Устройство {"включено" if device.status == "on" else "выключено"}',
                'status': device.status
            })

        # Специфичные действия для разных типов устройств
        if device.device_type == 'light':
            light = LightDevice.objects.get(id=device_id)
            if action == 'set_brightness':
                brightness = data.get('brightness')
                if 0 <= brightness <= 100:
                    old_brightness = light.brightness
                    light.brightness = brightness
                    light.save()
                    DeviceLog.objects.create(
                        device=device,
                        action=f"Установка яркости {brightness}%",
                        old_status=str(old_brightness),
                        new_status=str(brightness)
                    )
                    return JsonResponse({'success': True, 'message': f'Яркость установлена на {brightness}%'})

        elif device.device_type == 'tv':
            tv = TVDevice.objects.get(id=device_id)
            if action == 'set_volume':
                volume = data.get('volume')
                if 0 <= volume <= 100:
                    tv.volume = volume
                    tv.save()
                    return JsonResponse({'success': True, 'message': f'Громкость установлена на {volume}%'})
            elif action == 'toggle_mute':
                tv.is_muted = not tv.is_muted
                tv.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Звук {"выключен" if tv.is_muted else "включен"}',
                    'is_muted': tv.is_muted
                })

        elif device.device_type == 'ac':
            ac = ACDevice.objects.get(id=device_id)
            if action == 'set_temperature':
                temperature = data.get('temperature')
                if 16 <= temperature <= 30:
                    ac.temperature = temperature
                    ac.save()
                    return JsonResponse({'success': True, 'message': f'Температура установлена на {temperature}°C'})
            elif action == 'set_mode':
                mode = data.get('mode')
                if mode in dict(ACDevice.MODES).keys():
                    ac.mode = mode
                    ac.save()
                    return JsonResponse({'success': True, 'message': f'Режим изменен на {ac.get_mode_display()}'})

        elif device.device_type == 'coffee':
            coffee = CoffeeMachine.objects.get(id=device_id)
            if action == 'make_coffee':
                success, message = coffee.make_coffee()
                return JsonResponse({'success': success, 'message': message})

        elif device.device_type == 'washer':
            washer = WasherDevice.objects.get(id=device_id)
            if action == 'start':
                success, message = washer.start_wash()
                return JsonResponse({'success': success, 'message': message})
            elif action == 'stop':
                success, message = washer.stop_wash()
                return JsonResponse({'success': success, 'message': message})

        return JsonResponse({'success': False, 'error': 'Неизвестное действие'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def room_detail(request, room_id):
    """Детальная страница комнаты"""
    room = get_object_or_404(Room, id=room_id)
    devices = room.devices.all()

    context = {
        'room': room,
        'devices': devices,
        'device_count': devices.count()
    }
    return render(request, 'devices/room_detail.html', context)


def activate_scene(request, scene_id):
    """Активация сценария"""
    from .models import Scene
    scene = get_object_or_404(Scene, id=scene_id)

    if not scene.is_active:
        messages.error(request, "Сценарий неактивен")
        return redirect('devices:dashboard')

    scene.activate()
    messages.success(request, f'Сценарий "{scene.name}" выполнен!')
    return redirect('devices:dashboard')


def device_stats(request):
    """Статистика устройств (API)"""
    stats = {
        'total': Device.objects.count(),
        'online': Device.objects.filter(is_online=True).count(),
        'offline': Device.objects.filter(is_online=False).count(),
        'on': Device.objects.filter(status='on').count(),
        'off': Device.objects.filter(status='off').count(),
        'standby': Device.objects.filter(status='standby').count(),
        'by_type': {},
        'by_room': {},
    }

    for device_type in dict(Device.DEVICE_TYPES).keys():
        stats['by_type'][device_type] = Device.objects.filter(device_type=device_type).count()

    for room in Room.objects.all():
        stats['by_room'][room.name] = Device.objects.filter(room=room).count()

    return JsonResponse(stats)