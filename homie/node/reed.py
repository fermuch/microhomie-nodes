""""
Reed switch door example
"""

from machine import Pin

from homie.node import HomieNode
from homie import Property


class Reed(HomieNode):

    def __init__(self, pin, interval=1):
        super().__init__(interval=interval)
        self.switch = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.last_status = None

    def __str__(self):
        return 'Door is {}'.format(self.reed_status())

    def properties(self):
        return [b'reed']

    def reed_status(self):
        return 'open' if self.switch.value() else 'closed'

    def get_properties(self):
        return (
            Property(b'reed/$name', b'Reed Sensor', True),
            Property(b'reed/$settable', b'false', True),
            Property(b'reed/$datatype', b'string', True),
            Property(b'reed/$format', b'open,closed', True)
        )

    def has_update(self):
        status = self.switch.value()
        if status != self.last_status:
            self.last_status = status
            return True
        return False

    def get_data(self):
        return (Property(b'reed', self.is_open(), True),)
