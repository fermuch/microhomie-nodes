from machine import Pin

from homie.node import HomieNode
from homie import Property


class PIR(HomieNode):

    def __init__(self, pin=4, interval=1):
        super().__init__(interval=interval)
        self.pir = Pin(pin, Pin.IN, pull=Pin.PULL_UP)
        self.last_pir_state = 0

    def __str__(self):
        return 'Last motion State = {}'.format(self.last_pir_state)

    def get_node_properties(self):
        return [b'motion']

    def get_properties(self):
        return (
            Property(b'motion/$name', b'PIR Motion Sensor', True),
            Property(b'motion/$settable', b'false', True),
            Property(b'motion/$datatype', b'boolean', True),
            Property(b'motion/$format', b'true,false', True),
        )

    def has_update(self):
        new_pir_state = self.pir.value()
        if new_pir_state != self.last_pir_state:
            self.last_pir_state = new_pir_state
            return True
        return False

    def get_data(self):
        payload = 'true' if self.last_pir_state == 1 else 'false'
        return (Property(b'motion', payload, True),)
