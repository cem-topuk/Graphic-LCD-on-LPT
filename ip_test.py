import glcd_on_lpt as glol
import time
import subprocess
import re

class LINUX_sys:
    def __init__(self):
        pass
    def get_ip(self, device):
        result = subprocess.run(['ip', 'a'], stdout=subprocess.PIPE, text=True)

        output_lines = result.stdout.splitlines()

        ip_pattern = re.compile(r'inet (\d+\.\d+\.\d+\.\d+)/\d+ brd')#re.compile(r'inet (\d+\.\d+\.\d+\.\d+)')
        ip_address = None
        device_counter = 0
        for line in output_lines:
            if line.startswith(f"{device}:"):
                device_counter += 1
            if device_counter == 1 and "inet" in line:
                match = ip_pattern.search(line)
                if match:
                    ip_address = match.group(1)
                    break
        if ip_address:
            return ip_address
        else:
            return "Unable to read IP address"
        
if __name__ == "__main__":
    lcd = glol.LCD()
    lcd.GLCD_clear_text()
    lcd.GLCD_clear_graphic()
    linux = LINUX_sys()
    ip_address = linux.get_ip(3)
    print(f"{ip_address}")
    
    # Draw some graphics
    lcd.GLCD_draw_rectangle((240/2)-50, (128/2)-50, 100, 100, 1)
    lcd.GLCD_draw_circle(240/2, 128/2, 45, 1)
    lcd.GLCD_draw_line(0, 0, 240, 128, 1)
    lcd.GLCD_draw_line(0, 128, 240, 0, 1)

    for s in range(10, 100, 10):
        lcd.GLCD_draw_Hline(10, s, 50, 1)
        lcd.GLCD_draw_Vline(s, 10, 50, 1)
        lcd.GLCD_draw_line(0, s+5, 240, s+5, 1)
        lcd.GLCD_draw_line(s+5, 0, s+5, 128, 1)

    time.sleep(3)
    lcd.GLCD_clear_graphic()
    lcd.GLCD_set_address_pointer(0, 0)
    lcd.GLCD_write_string("###Hello, LCD!***")
    time.sleep(2)
    lcd.GLCD_clear_text()
    lcd.GLCD_set_address_pointer(0, 1)
    lcd.GLCD_write_string(f'LAN IP: {ip_address}')
    #time.sleep(2)
    #lcd.GLCD_clear_text()
    """
    # Demo test numbers
    for count in range(0, 147):
        ch = f'{count}'
        #lcd.GLCD_write_char(ord(ch[0]))
        lcd.GLCD_write_string(f'{count} ')
        timer.sleep(0.1)
    """
    while True:
        user_input = input("'q' for exit: ")
        if user_input.lower() == 'q':
            lcd.GLCD_close()
            break
