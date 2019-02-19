#!/usr/bin/env python
#
# This is the library for Grove Base Hat.
#
# SH1107G/SSD1327 Classes
#

'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 
'''
from grove.display.base import Display
from upm.pyupm_lcd import *
from grove.i2c import Bus
import mraa
import sys

TYPE_CHAR  = 0
TYPE_GRAY  = 1
TYPE_COLOR = 2

MAX_GRAY = 100

BasicFont = [
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x5F,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x07,0x00,0x07,0x00,0x00,0x00],
        [0x00,0x14,0x7F,0x14,0x7F,0x14,0x00,0x00],
        [0x00,0x24,0x2A,0x7F,0x2A,0x12,0x00,0x00],
        [0x00,0x23,0x13,0x08,0x64,0x62,0x00,0x00],
        [0x00,0x36,0x49,0x55,0x22,0x50,0x00,0x00],
        [0x00,0x00,0x05,0x03,0x00,0x00,0x00,0x00],
        [0x00,0x1C,0x22,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x41,0x22,0x1C,0x00,0x00,0x00,0x00],
        [0x00,0x08,0x2A,0x1C,0x2A,0x08,0x00,0x00],
        [0x00,0x08,0x08,0x3E,0x08,0x08,0x00,0x00],
        [0x00,0xA0,0x60,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x08,0x08,0x08,0x08,0x08,0x00,0x00],
        [0x00,0x60,0x60,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x20,0x10,0x08,0x04,0x02,0x00,0x00],
        [0x00,0x3E,0x51,0x49,0x45,0x3E,0x00,0x00],
        [0x00,0x00,0x42,0x7F,0x40,0x00,0x00,0x00],
        [0x00,0x62,0x51,0x49,0x49,0x46,0x00,0x00],
        [0x00,0x22,0x41,0x49,0x49,0x36,0x00,0x00],
        [0x00,0x18,0x14,0x12,0x7F,0x10,0x00,0x00],
        [0x00,0x27,0x45,0x45,0x45,0x39,0x00,0x00],
        [0x00,0x3C,0x4A,0x49,0x49,0x30,0x00,0x00],
        [0x00,0x01,0x71,0x09,0x05,0x03,0x00,0x00],
        [0x00,0x36,0x49,0x49,0x49,0x36,0x00,0x00],
        [0x00,0x06,0x49,0x49,0x29,0x1E,0x00,0x00],
        [0x00,0x00,0x36,0x36,0x00,0x00,0x00,0x00],
        [0x00,0x00,0xAC,0x6C,0x00,0x00,0x00,0x00],
        [0x00,0x08,0x14,0x22,0x41,0x00,0x00,0x00],
        [0x00,0x14,0x14,0x14,0x14,0x14,0x00,0x00],
        [0x00,0x41,0x22,0x14,0x08,0x00,0x00,0x00],
        [0x00,0x02,0x01,0x51,0x09,0x06,0x00,0x00],
        [0x00,0x32,0x49,0x79,0x41,0x3E,0x00,0x00],
        [0x00,0x7E,0x09,0x09,0x09,0x7E,0x00,0x00],
        [0x00,0x7F,0x49,0x49,0x49,0x36,0x00,0x00],
        [0x00,0x3E,0x41,0x41,0x41,0x22,0x00,0x00],
        [0x00,0x7F,0x41,0x41,0x22,0x1C,0x00,0x00],
        [0x00,0x7F,0x49,0x49,0x49,0x41,0x00,0x00],
        [0x00,0x7F,0x09,0x09,0x09,0x01,0x00,0x00],
        [0x00,0x3E,0x41,0x41,0x51,0x72,0x00,0x00],
        [0x00,0x7F,0x08,0x08,0x08,0x7F,0x00,0x00],
        [0x00,0x41,0x7F,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x20,0x40,0x41,0x3F,0x01,0x00,0x00],
        [0x00,0x7F,0x08,0x14,0x22,0x41,0x00,0x00],
        [0x00,0x7F,0x40,0x40,0x40,0x40,0x00,0x00],
        [0x00,0x7F,0x02,0x0C,0x02,0x7F,0x00,0x00],
        [0x00,0x7F,0x04,0x08,0x10,0x7F,0x00,0x00],
        [0x00,0x3E,0x41,0x41,0x41,0x3E,0x00,0x00],
        [0x00,0x7F,0x09,0x09,0x09,0x06,0x00,0x00],
        [0x00,0x3E,0x41,0x51,0x21,0x5E,0x00,0x00],
        [0x00,0x7F,0x09,0x19,0x29,0x46,0x00,0x00],
        [0x00,0x26,0x49,0x49,0x49,0x32,0x00,0x00],
        [0x00,0x01,0x01,0x7F,0x01,0x01,0x00,0x00],
        [0x00,0x3F,0x40,0x40,0x40,0x3F,0x00,0x00],
        [0x00,0x1F,0x20,0x40,0x20,0x1F,0x00,0x00],
        [0x00,0x3F,0x40,0x38,0x40,0x3F,0x00,0x00],
        [0x00,0x63,0x14,0x08,0x14,0x63,0x00,0x00],
        [0x00,0x03,0x04,0x78,0x04,0x03,0x00,0x00],
        [0x00,0x61,0x51,0x49,0x45,0x43,0x00,0x00],
        [0x00,0x7F,0x41,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x02,0x04,0x08,0x10,0x20,0x00,0x00],
        [0x00,0x41,0x41,0x7F,0x00,0x00,0x00,0x00],
        [0x00,0x04,0x02,0x01,0x02,0x04,0x00,0x00],
        [0x00,0x80,0x80,0x80,0x80,0x80,0x00,0x00],
        [0x00,0x01,0x02,0x04,0x00,0x00,0x00,0x00],
        [0x00,0x20,0x54,0x54,0x54,0x78,0x00,0x00],
        [0x00,0x7F,0x48,0x44,0x44,0x38,0x00,0x00],
        [0x00,0x38,0x44,0x44,0x28,0x00,0x00,0x00],
        [0x00,0x38,0x44,0x44,0x48,0x7F,0x00,0x00],
        [0x00,0x38,0x54,0x54,0x54,0x18,0x00,0x00],
        [0x00,0x08,0x7E,0x09,0x02,0x00,0x00,0x00],
        [0x00,0x18,0xA4,0xA4,0xA4,0x7C,0x00,0x00],
        [0x00,0x7F,0x08,0x04,0x04,0x78,0x00,0x00],
        [0x00,0x00,0x7D,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x80,0x84,0x7D,0x00,0x00,0x00,0x00],
        [0x00,0x7F,0x10,0x28,0x44,0x00,0x00,0x00],
        [0x00,0x41,0x7F,0x40,0x00,0x00,0x00,0x00],
        [0x00,0x7C,0x04,0x18,0x04,0x78,0x00,0x00],
        [0x00,0x7C,0x08,0x04,0x7C,0x00,0x00,0x00],
        [0x00,0x38,0x44,0x44,0x38,0x00,0x00,0x00],
        [0x00,0xFC,0x24,0x24,0x18,0x00,0x00,0x00],
        [0x00,0x18,0x24,0x24,0xFC,0x00,0x00,0x00],
        [0x00,0x00,0x7C,0x08,0x04,0x00,0x00,0x00],
        [0x00,0x48,0x54,0x54,0x24,0x00,0x00,0x00],
        [0x00,0x04,0x7F,0x44,0x00,0x00,0x00,0x00],
        [0x00,0x3C,0x40,0x40,0x7C,0x00,0x00,0x00],
        [0x00,0x1C,0x20,0x40,0x20,0x1C,0x00,0x00],
        [0x00,0x3C,0x40,0x30,0x40,0x3C,0x00,0x00],
        [0x00,0x44,0x28,0x10,0x28,0x44,0x00,0x00],
        [0x00,0x1C,0xA0,0xA0,0x7C,0x00,0x00,0x00],
        [0x00,0x44,0x64,0x54,0x4C,0x44,0x00,0x00],
        [0x00,0x08,0x36,0x41,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x7F,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x41,0x36,0x08,0x00,0x00,0x00,0x00],
        [0x00,0x02,0x01,0x01,0x02,0x01,0x00,0x00],
        [0x00,0x02,0x05,0x05,0x02,0x00,0x00,0x00],
]


class SH1107G_SSD1327(Display):
    MAX_GRAY    = 100
    _REG_CMD    = 0x00
    _REG_DATA   = 0x40
    _PAGE_CNT   = 16
    _PAGE_BYTES = 128
    _TOTAL_BYTES= _PAGE_CNT * _PAGE_BYTES

    def __init__(self, address = 0x3C):
        super(SH1107G_SSD1327, self).__init__()
        # self._bus = Bus()
        self._bus = mraa.I2c(0)
        self._addr = address
        self._bus.address(self._addr)

        if self._bus.writeByte(0):
            print("Check if the LCD SH1107G/SSD1307 inserted, then try again")
            sys.exit(1)
 
        # id = self._bus.read_byte_data(self._addr, SH1107G_SSD1327._REG_CMD)
        id = self._bus.readReg(SH1107G_SSD1327._REG_CMD)
        # print(" id = 0x{:2x}".format(id))
        self._sh1107 = (id & 0x3F) == 0x07
        if not self._sh1107:
            self._ssd1327 = SSD1327(0)
            return

        blk =     [0xAE]   # Display OFF
        blk.append(0xD5)   # Set Dclk
        blk.append(0x50)   # 100Hz
        blk.append(0x20)   # Set row address
        blk.append(0x81)   # Set contrast control
        blk.append(0x80)
        blk.append(0xA0)   # Segment remap
        blk.append(0xA4)   # Set Entire Display ON 
        blk.append(0xA6)   # Normal display
        blk.append(0xAD)   # Set external VCC
        blk.append(0x80)
        blk.append(0xC0)   # Set Common scan direction
        blk.append(0xD9)   # Set phase leghth
        blk.append(0x1F)
        blk.append(0xDB)   # Set Vcomh voltage
        blk.append(0x27)
        blk.append(0xAF)   # Display ON
        blk.append(0xB0)
        blk.append(0x00)
        blk.append(0x10)
        self._cmds(blk)
        self.clear()

    def _cmd(self, cmd):
        try:
            # self._bus.write_byte_data(self._addr,
            self._bus.writeReg(
                                    SH1107G_SSD1327._REG_CMD, cmd)
        except IOError:
            print("*** Check if LCD module inserted ***")
            sys.exit(1)

    def _cmds(self, cmds):
        for c in cmds:
            self._cmd(c)

    def _datas(self, datas):
        length = len(datas)
        data = bytearray(length + 1)
        data[0] = SH1107G_SSD1327._REG_DATA
        for i in range(length):
            data[i + 1] = datas[i]
        try:
            self._bus.write(data)
            # self._bus.write_i2c_block_data(self._addr,
            #                       SH1107G_SSD1327._REG_DATA, datas)
        except IOError:
            print("*** Check if LCD module inserted ***")
            sys.exit(1)

    @property
    def name(self):
        return "SH1107G" if self._sh1107 else "SSD1327"

    def type(self):
        return TYPE_GRAY

    def size(self):
        if not self._sh1107:
            # Gray LCD 96x96
            return 12, 12
        # Gray LCD 128x128
        return 16, 16

    def clear(self):
        if not self._sh1107:
            self._ssd1327.clear()
            return
        zeros = [ 0x0 for dummy in range(SH1107G_SSD1327._TOTAL_BYTES) ]
        self.draw(zeros, SH1107G_SSD1327._TOTAL_BYTES)

    def draw(self, data, bytes):
        if not self._sh1107:
            self._ssd1327.draw(data, bytes)
            return

        # all pages fill with data
        for i in range(SH1107G_SSD1327._PAGE_CNT):
            if i > bytes / SH1107G_SSD1327._PAGE_BYTES:
                return
            self._cmd(BASE_PAGE_START_ADDR + i)
            self._cmd(BASE_LOW_COLUMN_ADDR)
            self._cmd(BASE_HIGH_COLUMN_ADDR)
            # every PAGE fill it's bytes
            # I2C limit to 32 bytes each time
            for k in range(0, SH1107G_SSD1327._PAGE_BYTES, 32):
                begin = i * SH1107G_SSD1327._PAGE_BYTES + k
                end   = begin + 32
                self._datas(data[begin:end])

    def home(self):
        if not self._sh1107:
            self._ssd1327.home()
            return
        self.setCusor(0, 0)

    def setCursor(self, row, column):
        if not self._sh1107:
            self._ssd1327.setCursor(row, column)
            return
        self._cmd(BASE_PAGE_START_ADDR + row)
        self._cmd(0x08 if column % 2 else BASE_LOW_COLUMN_ADDR)
        self._cmd(BASE_HIGH_COLUMN_ADDR + (column >> 1))

    def _putchar(self, c):
        asc = ord(c)
        if asc < 32 or asc > 127:
                asc = ord(' ')
        for i in range(8):
            fontmap = []
            fontmap.append(BasicFont[asc - 32][i])
            self._datas(fontmap)

    def write(self, msg):
        if not self._sh1107:
            self._ssd1327.write(msg)
            return
        for i in range(len(msg)):
            self._putchar(msg[i])

    def _backlight_on(self, en):
        self._cmd(DISPLAY_CMD_ON if en else DISPLAY_CMD_OFF)


def main():
    import time

    lcd = SH1107G_SSD1327()
    rows, cols = lcd.size()
    print("LCD model: {}".format(lcd.name))
    print("LCD type : {} x {}".format(cols, rows))

    lcd.backlight(False)
    time.sleep(1)

    lcd.backlight(True)
    lcd.setCursor(0, 0)
    lcd.write("hello world!")
    lcd.setCursor(0, cols - 1)
    lcd.write('X')
    lcd.setCursor(rows - 1, 0)
    for i in range(cols):
        lcd.write(chr(ord('A') + i))

    time.sleep(3)
    lcd.clear()

if __name__ == '__main__':
    main()
