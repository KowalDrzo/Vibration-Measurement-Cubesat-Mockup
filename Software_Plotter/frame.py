class Frame:

    time_us = 0
    x = 0
    y = 0
    z = 0

    def toString(self):
        return f"{self.time_us}; {self.x}; {self.y}; {self.z}"
