"""
Сервисы для управления устройствами умного дома
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Room, Device, DeviceLog, Scene, LightDevice, TVDevice, ACDevice, CoffeeMachine, WasherDevice, \
    SocketDevice
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DeviceService:
    """Сервис для управления устройствами"""

    @staticmethod
    def get_device(device_id):
        """Получение устройства по ID"""
        try:
            return Device.objects.get(id=device_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_room_devices(room_id):
        """Получение всех устройств в комнате"""
        try:
            room = Room.objects.get(id=room_id)
            return room.devices.all()
        except ObjectDoesNotExist:
            return []

    @staticmethod
    def get_devices_by_type(device_type):
        """Получение устройств по типу"""
        return Device.objects.filter(device_type=device_type)

    @staticmethod
    def toggle_device(device_id, user=None):
        """Включение/выключение устройства"""
        device = DeviceService.get_device(device_id)
        if not device:
            return None, "Устройство не найдено"

        old_status = device.status
        device.toggle_status()

        # Логируем действие
        DeviceService.log_action(device, user, f"Переключение статуса", old_status, device.status)

        return device, "Статус изменен"

    @staticmethod
    def set_device_status(device_id, status, user=None):
        """Установка статуса устройства"""
        device = DeviceService.get_device(device_id)
        if not device:
            return None, "Устройство не найдено"

        if status not in dict(Device.STATUS_CHOICES).keys():
            return None, "Некорректный статус"

        old_status = device.status
        device.status = status
        device.save()

        DeviceService.log_action(device, user, f"Установка статуса {status}", old_status, status)

        return device, "Статус обновлен"

    @staticmethod
    def log_action(device, user, action, old_status, new_status):
        """Логирование действия"""
        DeviceLog.objects.create(
            device=device,
            user=user,
            action=action,
            old_status=old_status,
            new_status=new_status
        )


class LightService:
    """Сервис для управления освещением"""

    @staticmethod
    def set_brightness(device_id, brightness, user=None):
        """Установка яркости"""
        try:
            light = LightDevice.objects.get(id=device_id)
            if light.set_brightness(brightness):
                DeviceService.log_action(light, user,
                                         f"Установка яркости {brightness}%",
                                         light.brightness, brightness)
                return True, "Яркость установлена"
            return False, "Некорректное значение яркости (0-100)"
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"

    @staticmethod
    def get_all_lights():
        """Получение всех осветительных приборов"""
        return LightDevice.objects.all()

    @staticmethod
    def get_room_lights(room_id):
        """Получение освещения в комнате"""
        return LightDevice.objects.filter(room_id=room_id)

    @staticmethod
    def turn_on_room_lights(room_id, user=None):
        """Включение всего освещения в комнате"""
        lights = LightDevice.objects.filter(room_id=room_id)
        count = 0
        for light in lights:
            if light.status != 'on':
                old_status = light.status
                light.status = 'on'
                light.save()
                DeviceService.log_action(light, user, "Включение света (комната)", old_status, 'on')
                count += 1
        return count


class TVService:
    """Сервис для управления телевизором"""

    @staticmethod
    def set_volume(device_id, volume, user=None):
        """Установка громкости"""
        try:
            tv = TVDevice.objects.get(id=device_id)
            if tv.set_volume(volume):
                DeviceService.log_action(tv, user,
                                         f"Установка громкости {volume}%",
                                         tv.volume, volume)
                return True, "Громкость установлена"
            return False, "Некорректное значение (0-100)"
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"

    @staticmethod
    def toggle_mute(device_id, user=None):
        """Включение/выключение звука"""
        try:
            tv = TVDevice.objects.get(id=device_id)
            old_mute = tv.is_muted
            tv.toggle_mute()
            DeviceService.log_action(tv, user,
                                     "Переключение звука",
                                     "Выключен" if old_mute else "Включен",
                                     "Включен" if tv.is_muted else "Выключен")
            return True, "Звук переключен"
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"


class ACService:
    """Сервис для управления кондиционером"""

    @staticmethod
    def set_temperature(device_id, temperature, user=None):
        """Установка температуры"""
        try:
            ac = ACDevice.objects.get(id=device_id)
            if ac.set_temperature(temperature):
                DeviceService.log_action(ac, user,
                                         f"Установка температуры {temperature}°C",
                                         ac.temperature, temperature)
                return True, "Температура установлена"
            return False, "Некорректное значение (16-30)"
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"

    @staticmethod
    def set_mode(device_id, mode, user=None):
        """Установка режима"""
        try:
            ac = ACDevice.objects.get(id=device_id)
            if ac.set_mode(mode):
                DeviceService.log_action(ac, user,
                                         f"Установка режима {mode}",
                                         ac.mode, mode)
                return True, "Режим установлен"
            return False, "Некорректный режим"
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"


class CoffeeService:
    """Сервис для управления кофемашиной"""

    @staticmethod
    def make_coffee(device_id, user=None):
        """Приготовить кофе"""
        try:
            coffee_machine = CoffeeMachine.objects.get(id=device_id)
            success, message = coffee_machine.make_coffee()
            if success:
                DeviceService.log_action(coffee_machine, user,
                                         "Приготовление кофе",
                                         coffee_machine.status, coffee_machine.status)
            return success, message
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"


class WasherService:
    """Сервис для управления стиральной машиной"""

    @staticmethod
    def start_wash(device_id, user=None):
        """Запуск стирки"""
        try:
            washer = WasherDevice.objects.get(id=device_id)
            success, message = washer.start_wash()
            if success:
                DeviceService.log_action(washer, user, "Запуск стирки", washer.status, washer.status)
            return success, message
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"

    @staticmethod
    def stop_wash(device_id, user=None):
        """Остановка стирки"""
        try:
            washer = WasherDevice.objects.get(id=device_id)
            success, message = washer.stop_wash()
            if success:
                DeviceService.log_action(washer, user, "Остановка стирки", washer.status, washer.status)
            return success, message
        except ObjectDoesNotExist:
            return False, "Устройство не найдено"


class SceneService:
    """Сервис для управления сценариями"""

    @staticmethod
    def activate_scene(scene_id, user=None):
        """Активация сценария"""
        try:
            scene = Scene.objects.get(id=scene_id)
            if not scene.is_active:
                return False, "Сценарий неактивен"

            scene.activate()
            return True, "Сценарий выполнен"
        except ObjectDoesNotExist:
            return False, "Сценарий не найден"

    @staticmethod
    def get_scenes():
        """Получение всех сценариев"""
        return Scene.objects.filter(is_active=True)