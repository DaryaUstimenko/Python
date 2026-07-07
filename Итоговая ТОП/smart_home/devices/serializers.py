from rest_framework import serializers
from .models import (
    Room, Device, LightDevice, TVDevice, ACDevice,
    CoffeeMachine, WasherDevice, SocketDevice, Scene, DeviceLog
)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'description', 'floor', 'created_at']


class DeviceSerializer(serializers.ModelSerializer):
    device_type_display = serializers.CharField(source='get_device_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'device_type', 'device_type_display', 'room',
                  'status', 'status_display', 'is_online', 'ip_address',
                  'firmware_version', 'last_seen', 'created_at']


class LightDeviceSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = LightDevice
        fields = ['id', 'device', 'brightness', 'color_temperature',
                  'is_dimmable', 'is_rgb', 'schedule_on', 'schedule_off']


class TVDeviceSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = TVDevice
        fields = ['id', 'device', 'volume', 'channel', 'input_source', 'is_muted']


class ACDeviceSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    mode_display = serializers.CharField(source='get_mode_display', read_only=True)

    class Meta:
        model = ACDevice
        fields = ['id', 'device', 'temperature', 'mode', 'mode_display',
                  'fan_speed', 'swing']


class CoffeeMachineSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = CoffeeMachine
        fields = ['id', 'device', 'water_level', 'beans_level',
                  'strength', 'size', 'is_cleaning']


class WasherDeviceSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = WasherDevice
        fields = ['id', 'device', 'program', 'temperature',
                  'spin_speed', 'time_remaining', 'is_running']


class SocketDeviceSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = SocketDevice
        fields = ['id', 'device', 'power_consumption', 'voltage',
                  'current', 'is_child_lock']


class SceneDeviceSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = Scene
        fields = ['id', 'scene', 'device', 'device_name', 'target_status']


class SceneSerializer(serializers.ModelSerializer):
    devices = SceneDeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Scene
        fields = ['id', 'name', 'description', 'devices', 'is_active', 'created_at']


class DeviceLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = DeviceLog
        fields = ['id', 'device', 'device_name', 'user', 'user_name',
                  'action', 'old_status', 'new_status', 'created_at']