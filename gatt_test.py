import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

BLUEZ_SERVICE_NAME = 'org.bluez'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'

class GattCharacteristic(dbus.service.Object):
    chrc_properties = {
        'UUID': '00002a00-0000-1000-8000-00805f9b34fb',
        'Service': None,
        'Value': b'Hello, GATT!',
        'Flags': ['read']
    }

    def __init__(self, bus, index, service):
        self.path = f'{service.path}/char{index}'
        self.bus = bus
        self.service = service
        super().__init__(bus, self.path)

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='v')
    def Get(self, property_name):
        return self.chrc_properties[property_name]

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='', out_signature='a{sv}')
    def GetAll(self):
        return self.chrc_properties

class GattService(dbus.service.Object):
    service_properties = {
        'UUID': '00001800-0000-1000-8000-00805f9b34fb',
        'Primary': True
    }

    def __init__(self, bus, index):
        self.path = f'/org/bluez/example/service{index}'
        self.bus = bus
        super().__init__(bus, self.path)
        self.characteristic = GattCharacteristic(bus, 0, self)

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='v')
    def Get(self, property_name):
        return self.service_properties[property_name]

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='', out_signature='a{sv}')
    def GetAll(self):
        return self.service_properties

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    app = GattService(bus, 0)

    mainloop = GLib.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        mainloop.quit()
