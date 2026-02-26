import serial
import time

# open serial terminal, adapt to yours
with serial.Serial('/dev/tty.usbserial-14620', 9600, timeout=1) as ser:
    try:
        # set address for the module
        ser.write(b'SetAddress!1\n')
        time.sleep(0.1)  # Kleine Pause, um sicherzustellen, dass das Gerät genug Zeit hat
        line = ser.readline().decode('utf-8').strip()
        print(f"Response to SetAddress: {line}")

        # get address for the module
        ser.write(b'GetAddress!\n')
        time.sleep(0.1)  # small break
        line = ser.readline().decode('utf-8').strip()
        print(f"Current Address: {line}")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
