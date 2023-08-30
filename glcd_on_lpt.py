"""
Author: Cem Topuk
Description: 
    This Python library is designed for controlling graphic LCDs with the Toshiba T6963CFG controller
    through a parallel port (LPT). It provides the necessary functions to interact with and display 
    graphics on the LCD.

Usage:
    1. Connect your Toshiba T6963CFG LCD to your computer's parallel port (LPT).
    2. Import this library into your Python project.
    3. Create an instance of the 'LCD' class, e.g., 'lcd = glcd_on_lpt.LCD()'.
    4. Use the methods provided by the 'lcd' object to draw graphics, text, and control the LCD.
    5. Don't forget to clean up and release resources using 'cleanup()' when done.

Note:
    - This library assumes that you have the necessary hardware setup to interface with the LCD
      via the parallel port. Make sure to check your connections and configurations.
    - Please refer to the Toshiba T6963CFG controller's datasheet for more details on commands
      and configuration settings.
"""

import parallel
#import time

T6963CFG_SET_CURSOR_POINTER =          0x21
T6963CFG_SET_OFFSET_REGISTER =         0x22
T6963CFG_SET_ADDRESS_POINTER =         0x24

T6963CFG_SET_TEXT_HOME_ADDRESS =       0x40
T6963CFG_SET_TEXT_AREA =               0x41
T6963CFG_SET_GRAPHIC_HOME_ADDRESS =    0x42
T6963CFG_SET_GRAPHIC_AREA =            0x43

T6963CFG_MODE_SET =                    0x80
T6963CFG_EXT_CG_MODE =                 0x08
T6963CFG_OR_MODE =                     0x00
T6963CFG_XOR_MODE =                    0x01
T6963CFG_AND_MODE =                    0x03
TEXT_ATTR_MODE =                       0x04

T6963CFG_DISPLAY_MODE =                0x90
T6963CFG_CURSOR_BLINK_ON =             0x01
T6963CFG_CURSOR_DISPLAY_ON =           0x02
T6963CFG_TEXT_DISPLAY_ON =             0x04
T6963CFG_GRAPHIC_DISPLAY_ON =          0x08

T6963CFG_CURSOR_PATTERN_SELECT =       0xA0
T6963CFG_CURSOR_1_LINE =               0x00
T6963CFG_CURSOR_2_LINE =               0x01
T6963CFG_CURSOR_3_LINE =               0x02
T6963CFG_CURSOR_4_LINE =               0x03
T6963CFG_CURSOR_5_LINE =               0x04
T6963CFG_CURSOR_6_LINE =               0x05
T6963CFG_CURSOR_7_LINE =               0x06
T6963CFG_CURSOR_8_LINE =               0x07

T6963CFG_SET_DATA_AUTO_WRITE =         0xB0
T6963CFG_SET_DATA_AUTO_READ =          0xB1
T6963CFG_AUTO_RESET =                  0xB2

T6963CFG_DATA_WRITE_AND_INCREMENT =    0xC0
T6963CFG_DATA_READ_AND_INCREMENT =     0xC1
T6963CFG_DATA_WRITE_AND_DECREMENT =    0xC2
T6963CFG_DATA_READ_AND_DECREMENT =     0xC3
T6963CFG_DATA_WRITE_AND_NONVARIALBE =  0xC4
T6963CFG_DATA_READ_AND_NONVARIABLE =   0xC5

T6963CFG_SCREEN_PEEK =                 0xE0
T6963CFG_SCREEN_COPY =                 0xE8

GLCD_NUMBER_OF_LINES =              128
GLCD_PIXELS_PER_LINE =              240
GLCD_FONT_WIDTH =                   8   # Depends on the state of the FS pin L = 8, H = 6

GLCD_GRAPHIC_AREA =                 int(GLCD_PIXELS_PER_LINE / GLCD_FONT_WIDTH)
GLCD_TEXT_AREA =                    int(GLCD_PIXELS_PER_LINE / GLCD_FONT_WIDTH)
GLCD_GRAPHIC_SIZE =                 GLCD_GRAPHIC_AREA * GLCD_NUMBER_OF_LINES
GLCD_TEXT_SIZE =                    GLCD_TEXT_AREA * int(GLCD_NUMBER_OF_LINES / 8)

GLCD_TEXT_HOME =                    0
GLCD_GRAPHIC_HOME =                 GLCD_TEXT_HOME + GLCD_TEXT_SIZE

GLCD_OFFSET_REGISTER =              2
GLCD_EXTERNAL_CG_HOME =             int(GLCD_OFFSET_REGISTER) << 11
GLCD_EXTERNAL_CG_CAPABILITY =       256 #Byte

#DELAY_TIME =                        0.00000005 # 50 ns

class LCD:
    def __init__(self):
        self.p = parallel.Parallel()
        self.GLCD_init()

    def GLCD_init(self):
        self.p.setInitOut(0)        # LPT Pin 16  - LCD Pin 10          NOT Reset
        self.p.setSelect(1)         # LPT Pin 17 - LCD Pin 7            NOT CE
        self.p.setAutoFeed(0)       # LPT Pin 14 - LCD Pin 8            C/Not D
        #time.sleep(DELAY_TIME)
        self.p.setDataDir(0)
        self.p.setData(0)
        self.p.setInitOut(1)        # LPT Pin 16  - LCD Pin 10          NOT Reset

        self.GLCD_write(int(GLCD_TEXT_HOME & 0xFF), 0)
        self.GLCD_write(int(GLCD_TEXT_HOME >> 8), 0)
        self.GLCD_write(T6963CFG_SET_TEXT_HOME_ADDRESS, 1)

        self.GLCD_write(GLCD_TEXT_AREA, 0)
        self.GLCD_write(0, 0)
        self.GLCD_write(T6963CFG_SET_TEXT_AREA, 1)

        self.GLCD_write(int(GLCD_GRAPHIC_HOME & 0x00FF), 0)
        self.GLCD_write(int(GLCD_GRAPHIC_HOME >> 8), 0)
        self.GLCD_write(T6963CFG_SET_GRAPHIC_HOME_ADDRESS, 1)

        self.GLCD_write(GLCD_GRAPHIC_AREA, 0)
        self.GLCD_write(0, 0)
        self.GLCD_write(T6963CFG_SET_GRAPHIC_AREA, 1)

        self.GLCD_write(GLCD_OFFSET_REGISTER, 0)
        self.GLCD_write(0, 0)
        self.GLCD_write(T6963CFG_SET_OFFSET_REGISTER, 1)

        self.GLCD_write(0, 0)
        self.GLCD_write(0, 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)

        self.GLCD_write(T6963CFG_DISPLAY_MODE  | T6963CFG_GRAPHIC_DISPLAY_ON   | T6963CFG_TEXT_DISPLAY_ON , 1)#| T6963CFG_CURSOR_DISPLAY_ON, 1)

        self.GLCD_write(T6963CFG_MODE_SET | T6963CFG_OR_MODE, 1)

    def check_status(self):
        self.p.setSelect(1)         # LPT Pin 17 - LCD Pin 7            NOT CE
        self.p.setDataDir(0)        # Read Mode
        self.p.setDataStrobe(0)     # LPT Pin 1 - LCD Pin 5 and 6       W/Not R
        self.p.setAutoFeed(1)       # LPT Pin 14 - LCD Pin 8            C/Not D
        #time.sleep(DELAY_TIME)
        self.p.setSelect(0)         # LPT Pin 17 - LCD Pin 7            NOT CE
        #time.sleep(DELAY_TIME)
        self.sta_check = 0
        while True:
            self.data = self.p.getData()
            self.sta_check = self.data & 0x03
            #time.sleep(DELAY_TIME)
            if self.sta_check == 3:
                break
        #time.sleep(DELAY_TIME)
        self.p.setSelect(1)         # LPT Pin 17 - LCD Pin 7            NOT CE
        #time.sleep(DELAY_TIME)

    def GLCD_write(self, data, c_d):    # If c_d is 1, it is command mode, and 0 is data mode.
        self.check_status()
        self.p.setDataDir(1)        # Write Mode
        self.p.setAutoFeed(c_d)     # LPT Pin 14 - LCD Pin 8            C/Not D
        self.p.setDataStrobe(1)     # LPT Pin 1 - LCD Pin 5 and 6       W/Not R
        self.p.setData(int(data))
        #time.sleep(DELAY_TIME)
        self.p.setSelect(0)         # LPT Pin 17 - LCD Pin 7            NOT CE
        #time.sleep(DELAY_TIME)
        self.p.setSelect(1)         # LPT Pin 17 - LCD Pin 7            NOT CE

    def GLCD_read(self, c_d):   # If c_d is 1, it is command mode, and 0 is data mode.
        self.check_status()
        self.p.setAutoFeed(c_d)     # LPT Pin 14 - LCD Pin 8            C/Not D
        self.p.setDataStrobe(0)     # LPT Pin 1 - LCD Pin 5 and 6       W/Not R
        self.p.setSelect(0)         # LPT Pin 17 - LCD Pin 7            NOT CE
        #time.sleep(DELAY_TIME)
        data = self.p.getData()
        #time.sleep(DELAY_TIME)
        self.p.setSelect(1)         # LPT Pin 17 - LCD Pin 7            NOT CE
        return data

    def GLCD_clear_text(self):
        self.GLCD_write(GLCD_TEXT_HOME, 0)
        self.GLCD_write(GLCD_TEXT_HOME >> 8, 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)

        for i in range(0, GLCD_TEXT_SIZE):
            self.GLCD_write(0, 0)
            self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1)

    def GLCD_clear_CG(self):
        self.GLCD_write(GLCD_EXTERNAL_CG_HOME & 0xFF, 0)
        self.GLCD_write(GLCD_EXTERNAL_CG_HOME >> 8, 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)

        for i in range(0, GLCD_EXTERNAL_CG_CAPABILITY*8):
            self.GLCD_write(0, 0)
            self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1)
    
    def GLCD_char_CG(self, id):
        self.GLCD_write(0x80 + id, 0)                           # Adjust standard ASCII to T6963CFG ASCII
        self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1);  # '0x80 + id's range 0 to 255
    
    def GLCD_clear_graphic(self):
        self.GLCD_write(GLCD_GRAPHIC_HOME & 0xFF, 0)
        self.GLCD_write(GLCD_GRAPHIC_HOME >> 8, 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)

        for i in range(0, GLCD_GRAPHIC_SIZE):
            self.GLCD_write(0, 0)
            self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1)

    def GLCD_write_char(self, ch):
        self.GLCD_write(ch - 32, 0)
        self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1)
    
    def GLCD_write_string(self, text):
        for char in text:
            self.GLCD_write_char(ord(char))

    def GLCD_define_character(self, charCode, defChar):
        address = GLCD_EXTERNAL_CG_HOME + (8 * charCode)
        self.GLCD_write(int(address & 0xFF), 0)
        self.GLCD_write(int(address >> 8), 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)
        for index in defChar:
            self.GLCD_write(int(index & 0xFF), 0)
            self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1)
    
    def GLCD_set_cursor_pointer(self, x, y):
        self.GLCD_write(x, 0)
        self.GLCD_write(y, 0)
        self.GLCD_write(T6963CFG_SET_CURSOR_POINTER, 1)

    def GLCD_set_offset_register(self, data):
        self.GLCD_write(data, 0)
        self.GLCD_write(0, 0)
        self.GLCD_write(T6963CFG_SET_OFFSET_REGISTER, 1)

    def GLCD_set_address_pointer(self, x, y):
        address = GLCD_TEXT_HOME +  x + (GLCD_TEXT_AREA * y)
        self.GLCD_write(int(address & 0xFF), 0)
        self.GLCD_write(int(address >> 8), 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)

    def GLCD_set_pixel(self, x, y, color):
        address = int(GLCD_GRAPHIC_HOME + (x / GLCD_FONT_WIDTH) + (GLCD_GRAPHIC_AREA * y))

        self.GLCD_write(int(address & 0x00FF), 0)
        self.GLCD_write(int(address >> 8), 0)
        self.GLCD_write(T6963CFG_SET_ADDRESS_POINTER, 1)

        self.GLCD_write(T6963CFG_DATA_READ_AND_NONVARIABLE, 1)
        tmp = self.GLCD_read(0)

        if color:
            tmp |= (1 <<  (GLCD_FONT_WIDTH - 1 - (x % GLCD_FONT_WIDTH)))
        else:
            tmp &= ~(1 <<  (GLCD_FONT_WIDTH - 1 - (x % GLCD_FONT_WIDTH)))

        self.GLCD_write(tmp, 0)
        self.GLCD_write(T6963CFG_DATA_WRITE_AND_INCREMENT, 1)

    def GLCD_close(self):
        self.GLCD_clear_text()
        self.GLCD_clear_graphic()
        self.p.setInitOut(0)        # LPT Pin 16  - LCD Pin 10          NOT Reset
        self.p.setSelect(0)         # LPT Pin 17 - LCD Pin 7            NOT CE
        self.p.setData(0)
        self.p.setDataStrobe(0)     # LPT Pin 1 - LCD Pin 5 and 6       W/Not R
        self.p.setAutoFeed(0)       # LPT Pin 14 - LCD Pin 8            C/Not D
        #time.sleep(DELAY_TIME)
        self.p.setInitOut(1)        # LPT Pin 16  - LCD Pin 10          NOT Reset

    def GLCD_draw_rectangle(self, x, y, b, a, color):
        for i in range(0, int(a)):
            self.GLCD_set_pixel(int(x), int(y+i), color)
            self.GLCD_set_pixel(int(x+b-1), int(y+i), color)
        for i in range(0, int(b)):
            self.GLCD_set_pixel(int(x+i), int(y), color)
            self.GLCD_set_pixel(int(x+i), int(y+a-1), color)

    def GLCD_draw_circle(self, cx, cy ,radius, color):
        x = int(radius)
        y = 0
        xchange = 1 - 2 * int(radius)
        ychange = 1
        radiusError = 0
        while x >= y:
            self.GLCD_set_pixel(int(cx)+x, int(cy)+y, color)
            self.GLCD_set_pixel(int(cx)-x, int(cy)+y, color)
            self.GLCD_set_pixel(int(cx)-x, int(cy)-y, color)
            self.GLCD_set_pixel(int(cx)+x, int(cy)-y, color)
            self.GLCD_set_pixel(int(cx)+y, int(cy)+x, color)
            self.GLCD_set_pixel(int(cx)-y, int(cy)+x, color)
            self.GLCD_set_pixel(int(cx)-y, int(cy)-x, color)
            self.GLCD_set_pixel(int(cx)+y, int(cy)-x, color)
            y += 1
            radiusError += ychange
            ychange += 2
            if 2 * radiusError + xchange > 0:
                x -= 1
                radiusError += xchange
                xchange += 2

    def GLCD_draw_line(self, x1, y1, x2, y2, color):
        TwoDxAccumulatedError = 0
        TwoDyAccumulatedError = 0

        Dx = int(x2-x1)
        Dy = int(y2-y1)

        TwoDx = int(Dx + Dx)
        TwoDy = int(Dy + Dy)

        CurrentX = int(x1)
        CurrentY = int(y1)

        Xinc = 1
        Yinc = 1

        if Dx < 0:
            Xinc = -1
            Dx = -Dx
            TwoDx = -TwoDx

        if Dy < 0:
            Yinc = -1
            Dy = -Dy
            TwoDy = -TwoDy

        self.GLCD_set_pixel(int(x1), int(y1), color)

        if Dx != 0 and Dy != 0:

            if Dy <= Dx:
                TwoDxAccumulatedError = 0
                while CurrentX != x2:
                    CurrentX += Xinc
                    TwoDxAccumulatedError += TwoDy
                    if TwoDxAccumulatedError > Dx:
                        CurrentY += Yinc
                        TwoDxAccumulatedError -= TwoDx
                    self.GLCD_set_pixel(CurrentX, CurrentY, color)
            else:
                TwoDyAccumulatedError = 0
                while CurrentY != y2:
                    CurrentY += Yinc
                    TwoDyAccumulatedError += TwoDx
                    if TwoDyAccumulatedError > Dy:
                        CurrentX += Xinc
                        TwoDyAccumulatedError -= TwoDy
                    self.GLCD_set_pixel(CurrentX, CurrentY, color)

