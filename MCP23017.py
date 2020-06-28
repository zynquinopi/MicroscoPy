import time
import pigpio
 
class MCP23017(object):
    DEFAULT_ADDRESS  = 0x20
 
    REG_IODIRA   = 0x00
    REG_IODIRB   = 0x01
    REG_IPOLA    = 0x02
    REG_IPOLB    = 0x03
    REG_GPINTENA = 0x04
    REG_GPINTENB = 0x05
    REG_DEFVALA  = 0x06
    REG_DEFVALB  = 0x07
    REG_INTCONA  = 0x08
    REG_INTCONB  = 0x09
    REG_IOCONA   = 0x0A
    REG_IOCONB   = 0x0B
    REG_GPPUA    = 0x0C
    REG_GPPUB    = 0x0D
    REG_INTFA    = 0x0E
    REG_INTFB    = 0x0F
    REG_INTCAPA  = 0x10
    REG_INTCAPB  = 0x11
    REG_GPIOA    = 0x12
    REG_GPIOB    = 0x13
    REG_OLATA    = 0x14
    REG_OLATB    = 0x15

    def __init__(self, pi):
        self.pi = pi
        self._device = pi.i2c_open(1, self.DEFAULT_ADDRESS)
        # self.pi.i2c_write_device(self._device, [self.REG_IODIRA, 0xFF])
        # self.pi.i2c_write_device(self._device, [self.REG_IODIRB, 0xFF])
  
 
    def cancel(self):
        if self._device is not None:
            self.pi.i2c_close(self._device) 
            self._device = None

    def set_mode(self, port, pin_num, dir, inten=0):
        if   port is "A":
            reg_iodir = self.REG_IODIRA
            reg_gppu  = self.REG_GPPUA
            reg_inten = self.REG_GPINTENA
        elif port is "B":
            reg_iodir = self.REG_IODIRB
            reg_gppu  = self.REG_GPPUB
            reg_inten = self.REG_GPINTENB

        pin_num_oh = 2 ** pin_num
        iodir_val_old = self._read_reg(reg_iodir, 1)[0]
        gppu_val_old  = self._read_reg(reg_gppu, 1)[0]
        inten_val_old = self._read_reg(reg_inten, 1)[0]

        if   dir is "INPUT":
            iodir_val = iodir_val_old | pin_num_oh
        elif dir is "INPUL":
            iodir_val = iodir_val_old | pin_num_oh
            gppu_val = gppu_val_old | pin_num_oh
        elif dir is "OUTPUT":
            iodir_val = iodir_val_old & (~pin_num_oh & 0xFF)            


        reg_data = [reg_iodir, iodir_val]
        self.pi.i2c_write_device(self._device, reg_data)
        if dir is "INPUL":
            self.pi.i2c_write_device(self._device, [reg_gppu, gppu_val])

        if inten is 1:
            inten_val = inten_val_old | pin_num_oh
            self.pi.i2c_write_device(self._device, [reg_inten, inten_val])


    def write(self, port, pin_num, val):
        if port is "A":
            reg_olat = self.REG_OLATA
            reg_iodir = self.REG_GPIOA
        elif port is "B":
            reg_olat = self.REG_OLATB
            reg_iodir = self.REG_GPIOB

        pin_num_oh = 2 ** pin_num
        gpio_val_old = self._read_reg(reg_iodir, 1)[0]

        if val is 0:
            gpio_val = gpio_val_old & (~pin_num_oh & 0xFF)
        elif val is 1:
            gpio_val = gpio_val_old or pin_num_oh

        reg_data = [reg_olat, gpio_val]
        self.pi.i2c_write_device(self._device, reg_data)


    def _read_reg(self, reg, num):
        wc,data =  self.pi.i2c_read_i2c_block_data(self._device, reg, num)
        return data

    def read(self, port, pin_num):
        if port is "A":
            reg_gpio = self.REG_GPIOA
        elif port is "B":
            reg_gpio = self.REG_GPIOB
        val = (self._read_reg(reg_gpio, 1)[0] >> pin_num) & 0x01
        return val


if __name__ == "__main__":
    pi = pigpio.pi()
    if not pi.connected:
       exit(0)
    
    exp = MCP23017(pi)
    exp.set_mode("A", 0, "INPUT", 1)
    exp.set_mode("B", 4, "OUTPUT")
    while True:
        # exp.write("B", 4, 1)
        # time.sleep(1)
        # exp.write("B", 4, 0)
        # time.sleep(1)
        # print(exp.read("A", 0))
        time.sleep(2)

    # dac.cancel()
    pi.stop() 