import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import time
import threading
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
stop_loop = False
nitrate_current = 0.0
doc_A_current = 0.0
doc_B_current = 0.0
turbidity_current = 0.0
mess_interval = 0
sample_name = ""
data = []  # Initialization of data list

# Function to start measurements
def start_messungen():
    global stop_loop, nitrate_current, doc_A_current, doc_B_current, turbidity_current, mess_interval, sample_name
    try:
        nitrate_current = float(entry_nitrate.get())
        doc_A_current = float(entry_doc_A.get())
        doc_B_current = float(entry_doc_B.get())
        turbidity_current = float(entry_turbidity.get())
        mess_interval = int(entry_interval.get())
        sample_name = entry_sample.get()

        if not (0 < nitrate_current <= 20) or not (0 < doc_A_current <= 1) or not (0 < doc_B_current <= 1) or not (0 < turbidity_current <= 20):
            messagebox.showerror("Error", "Current values must be between 0 and 20 mA for nitrate and 0 and 1 mA for DOC and 0 and 20 mA for turbidity.")
            return

        if mess_interval <= 0:
            messagebox.showerror("Error", "Measurement interval must be greater than 0.")
            return

        stop_loop = False
        threading.Thread(target=run_messungen).start()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please check the entered values.")

# Function to stop measurements
def stop_messungen():
    global stop_loop
    stop_loop = True

# Function to perform measurements
def run_messungen():
    port_name = '/dev/tty.usbserial-14620'  # Adjust the port name if necessary
    baud_rate = 9600
    timeout = 1

    with serial.Serial(port_name, baud_rate, timeout=timeout) as ser:
        while not stop_loop:
            
# Set the voltage for the nitrate LED
            ser.write(f'SetCurrent!1!{nitrate_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage nitrate: {line}")
            else:
                print("No response received.")

            time.sleep(1)
            
# Receive the voltage arriving at the nitrate sensor
            voltages_nitrate = []
            for _ in range(5):
                ser.write(b'GetVoltage!1\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_nitrate.append(voltage)
                else:
                    print("No response received.")
                time.sleep(0.1)

            
# Calculate the average voltage for the nitrate sensor
            average_voltage_nitrate = sum(voltages_nitrate) / len(voltages_nitrate) if voltages_nitrate else 0

# Reset the voltage for the nitrate back to 0
            ser.write(f'SetCurrent!1!0\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage nitrate: {line}")
            else:
                print("No response received.")

            time.sleep(1)            
# A Set the voltage for the DOC LED
            ser.write(f'SetCurrent!3!{doc_A_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage DOC: {line}")
            else:
                print("No response received.")

            time.sleep(1)
            
# A Receive the voltage at the DOC sensor
            voltages_doc_A = []
            for _ in range(5):
                ser.write(b'GetVoltage!3\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_doc_A.append(voltage)
                else:
                    print("No response received.")
                time.sleep(0.1)

            
# A Calculate the average voltage for the DOC sensor
            average_voltage_doc_A = sum(voltages_doc_A) / len(voltages_doc_A) if voltages_doc_A else 0

# B Set the voltage for the DOC LED
            ser.write(f'SetCurrent!3!{doc_B_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage DOC: {line}")
            else:
                print("No response received.")

            time.sleep(1)
            
            # A Receive the voltage at the DOC sensor
            voltages_doc_B = []
            for _ in range(5):
                ser.write(b'GetVoltage!3\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_doc_B.append(voltage)
                else:
                    print("No response received.")
                time.sleep(0.1)

            
# A Calculate the average voltage for the DOC sensor
            average_voltage_doc_B = sum(voltages_doc_B) / len(voltages_doc_B) if voltages_doc_B else 0

# B Reset the voltage for the DOC LED back to 0
            ser.write(f'SetCurrent!3!0\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage DOC: {line}")
            else:
                print("No response received.")

            time.sleep(1)
            
# Set the voltage for the turbidity LED
            ser.write(f'SetCurrent!5!{turbidity_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage turbidity: {line}")
            else:
                print("No response received.")

            time.sleep(1)
            
# Receive the voltage at the turbidity sensor
            voltages_turbidity = []
            for _ in range(5):
                ser.write(b'GetVoltage!5\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_turbidity.append(voltage)
                else:
                    print("No response received.")
                time.sleep(0.1)

            
# Calculate the average voltage for the turbidity sensor
            average_voltage_turbidity = sum(voltages_turbidity) / len(voltages_turbidity) if voltages_turbidity else 0

# Reset the voltage for the turbidity LED back to 0
            ser.write(f'SetCurrent!5!0\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received response output voltage turbidity: {line}")
            else:
                print("No response received.")

            time.sleep(1)            
# Add measurement data to the table
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            global data  # Declare as global variable
            data.append([current_time, sample_name, average_voltage_nitrate, average_voltage_doc_A, average_voltage_doc_B, average_voltage_turbidity, nitrate_current, doc_A_current, turbidity_current])
            update_table()
            update_plot(average_voltage_nitrate, average_voltage_doc_A, average_voltage_doc_B, average_voltage_turbidity)

            # Wait the measurement interval
            time.sleep(mess_interval)

# Function to update the table
def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in data:
        tree.insert("", "end", values=item)

# Function to export data as Excel file
def export_to_excel():
    df = pd.DataFrame(data, columns=["Time", "Sample name", "Average voltage nitrate", "Average voltage DOC A", "Average voltage DOC B","Average voltage turbidity",  "Nitrate current (mA)", "DOC current A (mA)", "DOC current B (mA)", "Turbidity current (mA)"])
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"Data successfully exported as {file_path}.")

# Function to update the plot
def update_plot(nitrate_current, doc_A_current, doc_B_current, turbidity_current):
    ax.clear()
    global time_data, nitrate_currents, doc_A_currents, turbidity_currents  # Declare as global variables
    time_data.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    nitrate_currents.append(nitrate_current)
    doc_A_currents.append(doc_A_current)
    doc_B_currents.append(doc_B_current)
    turbidity_currents.append(turbidity_current)
    ax.plot(time_data, nitrate_currents, label='Nitrate voltage')
    ax.plot(time_data, doc_A_currents, label='DOC A voltage')
    ax.plot(time_data, doc_B_currents, label='DOC B voltage')
    ax.plot(time_data, turbidity_currents, label='Turbidity voltage')
    ax.legend()
    canvas.draw()

# Creating the user interface
root = tk.Tk()
root.title("Measurement Data Acquisition")

frame_input = ttk.Frame(root, padding="5")
frame_input.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Input fields for measurement parameters

ttk.Label(frame_input, text="DOC A Current (mA):").grid(row=0, column=0, padx=5, pady=5)
entry_doc_A = ttk.Entry(frame_input)
entry_doc_A.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="DOC B Current (mA):").grid(row=0, column=2, padx=5, pady=5)
entry_doc_B = ttk.Entry(frame_input)
entry_doc_B.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame_input, text="Nitrate Current (mA):").grid(row=1, column=0, padx=5, pady=5)
entry_nitrate = ttk.Entry(frame_input)
entry_nitrate.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Turbidity Current (mA):").grid(row=1, column=2, padx=5, pady=5)
entry_turbidity = ttk.Entry(frame_input)
entry_turbidity.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(frame_input, text="Measurement interval (s):").grid(row=2, column=0, padx=5, pady=5)  # Added
entry_interval = ttk.Entry(frame_input)
entry_interval.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Sample name:").grid(row=2, column=2, padx=5, pady=5)  # Added
entry_sample = ttk.Entry(frame_input)
entry_sample.grid(row=2, column=3, padx=5, pady=5)

# Buttons to start, stop and export measurements
start_button = ttk.Button(root, text="Start", command=start_messungen)
start_button.grid(row=0, column=1, padx=3, pady=3)

stop_button = ttk.Button(root, text="Stop", command=stop_messungen)
stop_button.grid(row=1, column=1, padx=3, pady=3)

export_button = ttk.Button(root, text="Export", command=export_to_excel)
export_button.grid(row=2, column=1, padx=3, pady=3)

# Create the plot
fig, ax = plt.subplots(figsize=(3.5, 2))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, pady=10)

time_data = []  # Initialization of time data list
nitrate_currents = []  # Initialization of nitrate voltage list
doc_A_currents = []  # Initialization of DOC voltage list
doc_B_currents = []  # Initialization of DOC voltage list
turbidity_currents = []  # Initialization of turbidity voltage list

# Create the table
frame_table = ttk.Frame(root)
frame_table.grid(row=8, column=0, columnspan=3, pady=10)

tree = ttk.Treeview(frame_table, columns=("Time", "Sample name", "Average voltage nitrate", "Average voltage DOC A", "Average voltage DOC B", "Average voltage turbidity", "Nitrate current (mA)", "DOC current A (mA)", "DOC current B (mA)", "Turbidity current (mA)"))
tree.heading("#0", text="Index")
tree.heading("Time", text="Time")
tree.heading("Sample name", text="Sample name")
tree.heading("Average voltage nitrate", text="Average voltage nitrate")
tree.heading("Average voltage DOC A", text="Average voltage DOC A")
tree.heading("Average voltage DOC B", text="Average voltage DOC B")
tree.heading("Average voltage turbidity", text="Average voltage turbidity")
tree.heading("Nitrate current (mA)", text="Nitrate current (mA)")
tree.heading("DOC current A (mA)", text="DOC current A (mA)")
tree.heading("DOC current B (mA)", text="DOC current B (mA)")
tree.heading("Turbidity current (mA)", text="Turbidity current (mA)")
tree.pack(fill=tk.BOTH, expand=True)

# Start the main loop
root.mainloop()
