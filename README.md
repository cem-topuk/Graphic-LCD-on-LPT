# Graphic-LCD-on-LPT
This library is designed for graphic LCDs with the Toshiba T6963CFG LCD controller. It allows controlling the Graphic LCD via the Parallel port (LPT).

# LCD Parallel Port Connection

__LCD model used JCDISPLAY JM240128DC__. Below, you can find the connections between LCD pins and LPT pins:

- **LPT Pin 1 (STROBE) - LCD Pins 5 and 6:** Used for reading and writing data to the LCD. The STROBE signal connects to the RD and WR pins.

- **RD Pin (LCD Pin 5):** The STROBE signal is directly connected to LPT Pin 1 (STROBE).

- **WR Pin (LCD Pin 6):** The WR pin is connected to the Collector pin of an NPN transistor. This transistor creates a NOT gate, enabling the reverse of the RD signal to be sent to the WR pin (LCD Pin 6). This ensures proper write (WR) and read (RD) operations on the LCD.

- **LPT Pins 2-9 (DATA) - LCD Pins D0-D7:** An 8-bit data bus used to transmit data to the LCD.

- **LPT Pin 14 (AUTOF) - LCD Pin 8:** Used to initiate data writing to the LCD.

- **LPT Pin 16 (INIT) - LCD Pin 10:** Used for initializing and resetting the LCD.

- **LPT Pin 17 (SELIN) - LCD Pin 7:** Used to initiate data writing to the LCD.

- **FS Pin (LCD Pin 19):** The FS (Font Select) pin is connected to the ground (GND). This allows you to select an 8x8 font.

These connections are necessary to properly control the LCD via the parallel port (LPT). Ensure that the connections are made correctly and double-check them when needed.

# Prerequisites

Before using this library to control your Toshiba T6963CFG LCD through the parallel port (LPT), ensure that you have the `pyparallel` library installed. `pyparallel` provides the necessary interface for communicating with the parallel port.

You can install `pyparallel` using `pip` with the following command:

```shell
pip install pyparallel
