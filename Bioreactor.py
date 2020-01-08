class Bioreactor: #container to hold and send values when updated to the MSP board
    def __init__(self):
        self.serial_port = None
        self.speed, self.ph, self.temperature = 0, 0, 0
        
    def update(self):
        if self.serial_port is not None and self.serial_port.running:
            self.serial_port.send_data('<ph,{}>'.format(self.ph))
            self.serial_port.send_data('<temperature,{}>'.format(self.temperature))
            self.serial_port.send_data('<speed,{}>'.format(self.speed))
            return True
        else: return False
