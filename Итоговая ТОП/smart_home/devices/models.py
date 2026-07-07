from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Room(models.Model):
    """Модель комнаты"""
    objects = models.Manager()
    ROOM_TYPES = [
        ("living_room", "Гостиная"),
        ("bedroom", "Спальня"),
        ("kitchen", "Кухня"),
        ("bathroom", "Санузел"),
        ("hallway", "Прихожая"),
        ("study", "Кабинет"),
    ]

    name = models.CharField("Название комнаты", max_length=100)
    room_type = models.CharField("Тип комнаты", max_length=20, choices=ROOM_TYPES)
    description = models.TextField("Описание", blank=True)
    floor = models.IntegerField("Этаж", default=1)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        ordering = ["floor", "name"]

    @property
    def room_type_display(self) -> str:
        """Человекочитаемое название типа комнаты"""
        # Явно преобразуем значение в строку
        room_type_value = str(self.room_type)  # Преобразуем CharField в строку
        return str(dict(self.ROOM_TYPES).get(room_type_value, room_type_value))

    def __str__(self) -> str:
        return f"{str(self.name)} (Этаж {self.floor})"


class Device(models.Model):
    """Базовая модель устройства"""
    objects = models.Manager()
    DEVICE_TYPES = [
        ("light", "Свет"),
        ("tv", "Телевизор"),
        ("ac", "Кондиционер"),
        ("coffee", "Кофемашина"),
        ("washer", "Стиральная машина"),
        ("socket", "Розетка"),
    ]

    STATUS_CHOICES = [
        ("on", "Включено"),
        ("off", "Выключено"),
        ("standby", "Ожидание"),
        ("error", "Ошибка"),
        ("maintenance", "Обслуживание"),
    ]

    name = models.CharField("Название устройства", max_length=200)
    device_type = models.CharField("Тип устройства", max_length=20, choices=DEVICE_TYPES)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="devices", verbose_name="Комната")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="off")
    is_online = models.BooleanField("В сети", default=True)
    ip_address = models.GenericIPAddressField("IP-адрес", null=True, blank=True)
    mac_address = models.CharField("MAC-адрес", max_length=17, blank=True)
    firmware_version = models.CharField("Версия прошивки", max_length=20, default="1.0.0")
    last_seen = models.DateTimeField("Последний раз в сети", auto_now=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"
        ordering = ["room", "device_type", "name"]

    @property
    def device_type_display(self) -> str:
        """Человекочитаемое название типа устройства"""
        # Явно преобразуем значение в строку
        device_type_value = str(self.device_type)
        return str(dict(self.DEVICE_TYPES).get(device_type_value, device_type_value))

    @property
    def status_display(self) -> str:
        """Человекочитаемое название статуса"""
        # Явно преобразуем значение в строку
        status_value = str(self.status)
        return str(dict(self.STATUS_CHOICES).get(status_value, status_value))

    @property
    def status_icon(self) -> str:
        """Иконка статуса"""
        icons = {
            "on": "🟢",
            "off": "🔴",
            "standby": "🟡",
            "error": "🔴",
            "maintenance": "🟠"
        }
        return icons.get(str(self.status), "⚪")

    @property
    def is_active(self) -> bool:
        """Проверка, активно ли устройство"""
        return str(self.status) == "on" and self.is_online

    def toggle_status(self):
        """Переключение статуса устройства"""
        if str(self.status) == "on":
            self.status = "off"
        else:
            self.status = "on"
        self.save()
        return self.status

    def __str__(self) -> str:
        """Строковое представление устройства"""
        return f"{self.device_type_display}: {str(self.name)}"


class LightDevice(Device):
    """Модель освещения"""
    objects = models.Manager()
    brightness = models.IntegerField("Яркость (%)", default=100,
                                     validators=[MinValueValidator(0), MaxValueValidator(100)])
    color_temperature = models.IntegerField("Цветовая температура (K)", default=3000,
                                            validators=[MinValueValidator(2000), MaxValueValidator(6500)])
    is_dimmable = models.BooleanField("С регулировкой яркости", default=True)
    is_rgb = models.BooleanField("Цветной свет", default=False)
    schedule_on = models.TimeField("Время включения", null=True, blank=True)
    schedule_off = models.TimeField("Время выключения", null=True, blank=True)

    class Meta:
        verbose_name = "Освещение"
        verbose_name_plural = "Освещение"

    def set_brightness(self, value: int) -> bool:
        """Установка яркости"""
        if 0 <= value <= 100:
            self.brightness = value
            self.save()
            return True
        return False

    def __str__(self) -> str:
        return f"💡 {str(self.name)} (Яркость: {self.brightness}%)"


class TVDevice(Device):
    """Модель телевизора"""
    objects = models.Manager()
    volume = models.IntegerField("Громкость (%)", default=50,
                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    channel = models.IntegerField("Канал", default=1)
    input_source = models.CharField("Источник сигнала", max_length=50, default="HDMI 1")
    is_muted = models.BooleanField("Звук выключен", default=False)

    class Meta:
        verbose_name = "Телевизор"
        verbose_name_plural = "Телевизоры"

    def set_volume(self, value: int) -> bool:
        """Установка громкости"""
        if 0 <= value <= 100:
            self.volume = value
            self.save()
            return True
        return False

    def toggle_mute(self) -> bool:
        """Включить/выключить звук"""
        self.is_muted = not self.is_muted
        self.save()
        return self.is_muted

    def __str__(self) -> str:
        return f"📺 {str(self.name)} (Канал: {self.channel})"


class ACDevice(Device):
    """Модель кондиционера"""
    objects = models.Manager()
    MODES = [
        ("cool", "Охлаждение"),
        ("heat", "Обогрев"),
        ("fan", "Вентиляция"),
        ("dry", "Осушение"),
        ("auto", "Авто"),
    ]

    temperature = models.IntegerField("Температура (°C)", default=22,
                                      validators=[MinValueValidator(16), MaxValueValidator(30)])
    mode = models.CharField("Режим", max_length=20, choices=MODES, default="auto")
    fan_speed = models.IntegerField("Скорость вентилятора (%)", default=50,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    swing = models.BooleanField("Автоповорот жалюзи", default=False)

    class Meta:
        verbose_name = "Кондиционер"
        verbose_name_plural = "Кондиционеры"

    @property
    def mode_display(self) -> str:
        """Человекочитаемое название режима"""
        # Явно преобразуем значение в строку
        mode_value = str(self.mode)
        return str(dict(self.MODES).get(mode_value, mode_value))

    def set_temperature(self, value: int) -> bool:
        """Установка температуры"""
        if 16 <= value <= 30:
            self.temperature = value
            self.save()
            return True
        return False

    def set_mode(self, mode: str) -> bool:
        """Установка режима"""
        if mode in dict(self.MODES).keys():
            self.mode = mode
            self.save()
            return True
        return False

    def __str__(self) -> str:
        return f"❄️ {str(self.name)} ({self.temperature}°C)"


class CoffeeMachine(Device):
    """Модель кофемашины"""
    objects = models.Manager()
    STRENGTHS = [
        ("weak", "Слабая"),
        ("medium", "Средняя"),
        ("strong", "Крепкая"),
    ]

    SIZES = [
        ("small", "Маленькая"),
        ("medium", "Средняя"),
        ("large", "Большая"),
    ]

    water_level = models.IntegerField("Уровень воды (%)", default=80,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    beans_level = models.IntegerField("Уровень зерен (%)", default=70,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    strength = models.CharField("Крепость", max_length=20, choices=STRENGTHS, default="medium")
    size = models.CharField("Размер порции", max_length=20, choices=SIZES, default="medium")
    is_cleaning = models.BooleanField("Очистка", default=False)

    class Meta:
        verbose_name = "Кофемашина"
        verbose_name_plural = "Кофемашины"

    @property
    def strength_display(self) -> str:
        """Человекочитаемое название крепости"""
        strength_value = str(self.strength)
        return str(dict(self.STRENGTHS).get(strength_value, strength_value))

    @property
    def size_display(self) -> str:
        """Человекочитаемое название размера"""
        size_value = str(self.size)
        return str(dict(self.SIZES).get(size_value, size_value))

    def make_coffee(self) -> tuple:
        """Приготовить кофе"""
        if self.water_level < 10:
            return False, "Недостаточно воды!"
        if self.beans_level < 10:
            return False, "Недостаточно зерен!"
        if str(self.status) != "on":
            return False, "Кофемашина выключена!"

        # Симуляция приготовления
        self.water_level -= 10
        self.beans_level -= 5
        self.save()
        return True, "Кофе готов!"

    def __str__(self) -> str:
        return f"☕ {str(self.name)} ({self.strength_display})"


class WasherDevice(Device):
    """Модель стиральной машины"""
    objects = models.Manager()
    PROGRAMS = [
        ("cotton", "Хлопок"),
        ("synthetic", "Синтетика"),
        ("delicate", "Деликатная"),
        ("quick", "Быстрая"),
        ("wool", "Шерсть"),
    ]

    program = models.CharField("Программа", max_length=20, choices=PROGRAMS, default="cotton")
    temperature = models.IntegerField("Температура (°C)", default=40,
                                      validators=[MinValueValidator(0), MaxValueValidator(95)])
    spin_speed = models.IntegerField("Скорость отжима (об/мин)", default=800,
                                     validators=[MinValueValidator(0), MaxValueValidator(1400)])
    time_remaining = models.IntegerField("Осталось минут", default=0)
    is_running = models.BooleanField("Работает", default=False)

    class Meta:
        verbose_name = "Стиральная машина"
        verbose_name_plural = "Стиральные машины"

    @property
    def program_display(self) -> str:
        """Человекочитаемое название программы"""
        program_value = str(self.program)
        return str(dict(self.PROGRAMS).get(program_value, program_value))

    def start_wash(self) -> tuple:
        """Запустить стирку"""
        if str(self.status) != "on":
            return False, "Машина выключена!"
        if self.is_running:
            return False, "Стирка уже запущена!"

        self.is_running = True
        self.time_remaining = 45
        self.save()
        return True, "Стирка запущена!"

    def stop_wash(self) -> tuple:
        """Остановить стирку"""
        if not self.is_running:
            return False, "Стирка не запущена!"

        self.is_running = False
        self.time_remaining = 0
        self.save()
        return True, "Стирка остановлена!"

    def __str__(self) -> str:
        status = "🔄 Работает" if self.is_running else "⏸ Остановлена"
        return f"🧺 {str(self.name)} ({status})"


class SocketDevice(Device):
    """Модель умной розетки"""
    objects = models.Manager()
    power_consumption = models.FloatField("Потребляемая мощность (Вт)", default=0)
    voltage = models.FloatField("Напряжение (В)", default=220)
    current = models.FloatField("Ток (А)", default=0)
    is_child_lock = models.BooleanField("Защита от детей", default=False)

    class Meta:
        verbose_name = "Розетка"
        verbose_name_plural = "Розетки"

    def get_power_consumption(self) -> float:
        """Получить потребляемую мощность"""
        return self.power_consumption

    def __str__(self) -> str:
        return f"🔌 {str(self.name)} ({self.power_consumption:.1f} Вт)"


class DeviceLog(models.Model):
    """Лог действий с устройствами"""
    objects = models.Manager()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField("Действие", max_length=200)
    old_status = models.CharField("Старый статус", max_length=20, blank=True)
    new_status = models.CharField("Новый статус", max_length=20, blank=True)
    ip_address = models.GenericIPAddressField("IP-адрес", null=True, blank=True)
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)

    class Meta:
        verbose_name = "Лог устройства"
        verbose_name_plural = "Логи устройств"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{str(self.device.name)} - {self.action} ({self.created_at})"


class Scene(models.Model):
    """Сценарий автоматизации"""
    objects = models.Manager()
    name = models.CharField("Название сценария", max_length=100)
    description = models.TextField("Описание", blank=True)
    devices = models.ManyToManyField(Device, through="SceneDevice", related_name="scenes")
    is_active = models.BooleanField("Активен", default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="scenes")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Сценарий"
        verbose_name_plural = "Сценарии"

    def __str__(self) -> str:
        return str(self.name)

    def activate(self) -> bool:
        """Активация сценария"""
        for scene_device in self.scenedevice_set.all():
            device = scene_device.device
            device.status = scene_device.target_status
            device.save()
        return True


class SceneDevice(models.Model):
    """Связь сценария с устройством"""
    objects = models.Manager()
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    target_status = models.CharField("Целевой статус", max_length=20, default="on")

    class Meta:
        verbose_name = "Устройство в сценарии"
        verbose_name_plural = "Устройства в сценариях"
        unique_together = ("scene", "device")

    def __str__(self) -> str:
        return f"{str(self.scene.name)} - {str(self.device.name)}"