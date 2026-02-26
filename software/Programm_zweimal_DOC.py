import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import time
import threading
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Globale Variablen
stop_loop = False
nitrate_current = 0.0
doc_A_current = 0.0
doc_B_current = 0.0
turbidity_current = 0.0
mess_interval = 0
sample_name = ""
data = []  # Initialisierung der Datenliste

# Funktion zum Starten der Messungen
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
            messagebox.showerror("Fehler", "Stromwerte müssen zwischen 0 und 20 mA für Nitrat und 0 und 1 mA für DOC und 0 und 20 mA für turbidity sein.")
            return

        if mess_interval <= 0:
            messagebox.showerror("Fehler", "Messintervall muss größer als 0 sein.")
            return

        stop_loop = False
        threading.Thread(target=run_messungen).start()
    except ValueError:
        messagebox.showerror("Fehler", "Ungültige Eingabe. Bitte überprüfen Sie die eingegebenen Werte.")

# Funktion zum Beenden der Messungen
def stop_messungen():
    global stop_loop
    stop_loop = True

# Funktion zur Durchführung der Messungen
def run_messungen():
    port_name = '/dev/tty.usbserial-14620'  # Passen Sie den Portnamen an
    baud_rate = 9600
    timeout = 1

    with serial.Serial(port_name, baud_rate, timeout=timeout) as ser:
        while not stop_loop:
            
# Setze die Spannung für die Nitrat LED
            ser.write(f'SetCurrent!1!{nitrate_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung Nitrat: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)

            
# Empfange die Spannung, die am Nitratsensor ankommt
            voltages_nitrate = []
            for _ in range(5):
                ser.write(b'GetVoltage!1\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_nitrate.append(voltage)
                else:
                    print("Keine Antwort empfangen.")
                time.sleep(0.1)

            
# Berechne den Mittelwert der Spannungen für den Nitratsensor
            average_voltage_nitrate = sum(voltages_nitrate) / len(voltages_nitrate) if voltages_nitrate else 0

# Setze die Spannung für die Nitrat zurück auf 0
            ser.write(f'SetCurrent!1!0\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung Nitrat: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)            
# A Setze die Spannung für die DOC LED
            ser.write(f'SetCurrent!3!{doc_A_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung DOC: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)

            
# A Empfange die Spannung am DOC-Sensor
            voltages_doc_A = []
            for _ in range(5):
                ser.write(b'GetVoltage!3\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_doc_A.append(voltage)
                else:
                    print("Keine Antwort empfangen.")
                time.sleep(0.1)

            
# A Berechne den Mittelwert der Spannungen für den DOC-Sensor
            average_voltage_doc_A = sum(voltages_doc_A) / len(voltages_doc_A) if voltages_doc_A else 0

# B Setze die Spannung für die DOC LED
            ser.write(f'SetCurrent!3!{doc_B_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung DOC: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)
            
            # A Empfange die Spannung am DOC-Sensor
            voltages_doc_B = []
            for _ in range(5):
                ser.write(b'GetVoltage!3\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_doc_B.append(voltage)
                else:
                    print("Keine Antwort empfangen.")
                time.sleep(0.1)

            
# A Berechne den Mittelwert der Spannungen für den DOC-Sensor
            average_voltage_doc_B = sum(voltages_doc_B) / len(voltages_doc_B) if voltages_doc_B else 0

# B Setze die Spannung für die DOC LED wieder auf 0
            ser.write(f'SetCurrent!3!0\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung DOC: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)
            
# Setze die Spannung für die turbidity LED
            ser.write(f'SetCurrent!5!{turbidity_current}\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung Turbidity: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)

            
# Empfange die Spannung am turbidity-Sensor
            voltages_turbidity = []
            for _ in range(5):
                ser.write(b'GetVoltage!5\n')
                line = ser.readline().decode('utf-8')
                if line:
                    voltage = float(line.strip())
                    voltages_turbidity.append(voltage)
                else:
                    print("Keine Antwort empfangen.")
                time.sleep(0.1)

            
# Berechne den Mittelwert der Spannungen für den turbidity-Sensor
            average_voltage_turbidity = sum(voltages_turbidity) / len(voltages_turbidity) if voltages_turbidity else 0

# Setze die Spannung für die turbidity LED wieder auf 0
            ser.write(f'SetCurrent!5!0\n'.encode('utf-8'))
            time.sleep(0.1)
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Empfangene Antwort Ausgangsspannung Turbidity: {line}")
            else:
                print("Keine Antwort empfangen.")

            time.sleep(1)            
# Füge die Messdaten zur Tabelle hinzu
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            global data  # Deklarieren als globale Variable
            data.append([current_time, sample_name, average_voltage_nitrate, average_voltage_doc_A, average_voltage_doc_B, average_voltage_turbidity, nitrate_current, doc_A_current, turbidity_current])
            update_table()
            update_plot(average_voltage_nitrate, average_voltage_doc_A, average_voltage_doc_B, average_voltage_turbidity)

            # Warte das Messintervall ab
            time.sleep(mess_interval)

# Funktion zum Aktualisieren der Tabelle
def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in data:
        tree.insert("", "end", values=item)

# Funktion zum Exportieren der Daten als Excel-Datei
def export_to_excel():
    df = pd.DataFrame(data, columns=["Uhrzeit", "Probenname", "Mittelwert der Spannung Nitrat", "Mittelwert der Spannung DOC A", "Mittelwert der Spannung DOC B","Mittelwert der Spannung Truebung",  "Nitrat Strum (mA)", "DOC Strom (mA)",  "Turbidity Strom (mA)"])
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Erfolg", f"Daten erfolgreich als {file_path} exportiert.")

# Funktion zum Aktualisieren des Diagramms
def update_plot(nitrate_current, doc_A_current, doc_B_current,turbidity_current):
    ax.clear()
    global time_data, nitrate_currents, doc_A_currents, turbidity_currents  # Deklarieren als globale Variablen
    time_data.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    nitrate_currents.append(nitrate_current)
    doc_A_currents.append(doc_A_current)
    doc_B_currents.append(doc_B_current)
    turbidity_currents.append(turbidity_current)
    ax.plot(time_data, nitrate_currents, label='Nitrat Spannung')
    ax.plot(time_data, doc_A_currents, label='DOC A Spannung')
    ax.plot(time_data, doc_B_currents, label='DOC B Spannung')
    ax.plot(time_data, turbidity_currents, label='Turbidity Spannung')
    ax.legend()
    canvas.draw()

# Erstellen der Benutzeroberfläche
root = tk.Tk()
root.title("Messdaten Erfassung")

frame_input = ttk.Frame(root, padding="5")
frame_input.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Eingabefelder für die Messparameter

ttk.Label(frame_input, text="DOC A Strom (mA):").grid(row=0, column=0, padx=5, pady=5)
entry_doc_A = ttk.Entry(frame_input)
entry_doc_A.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="DOC B Strom (mA):").grid(row=0, column=2, padx=5, pady=5)
entry_doc_B = ttk.Entry(frame_input)
entry_doc_B.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame_input, text="Nitrat Strom (mA):").grid(row=1, column=0, padx=5, pady=5)
entry_nitrate = ttk.Entry(frame_input)
entry_nitrate.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Turbidity Strom (mA):").grid(row=1, column=2, padx=5, pady=5)
entry_turbidity = ttk.Entry(frame_input)
entry_turbidity.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(frame_input, text="Messintervall (s):").grid(row=2, column=0, padx=5, pady=5)  # Hinzugefügt
entry_interval = ttk.Entry(frame_input)
entry_interval.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Probenname:").grid(row=2, column=2, padx=5, pady=5)  # Hinzugefügt
entry_sample = ttk.Entry(frame_input)
entry_sample.grid(row=2, column=3, padx=5, pady=5)

# Buttons zum Starten, Stoppen und Exportieren der Messungen
start_button = ttk.Button(root, text="Start", command=start_messungen)
start_button.grid(row=0, column=1, padx=3, pady=3)

stop_button = ttk.Button(root, text="Stop", command=stop_messungen)
stop_button.grid(row=1, column=1, padx=3, pady=3)

export_button = ttk.Button(root, text="Exportieren", command=export_to_excel)
export_button.grid(row=2, column=1, padx=3, pady=3)

# Erstellen des Diagramms
fig, ax = plt.subplots(figsize=(3.5, 2))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, pady=10)

time_data = []  # Initialisierung der Zeitdatenliste
nitrate_currents = []  # Initialisierung der Nitratspannungsliste
doc_A_currents = []  # Initialisierung der DOC-Spannungsliste
doc_B_currents = []  # Initialisierung der DOC-Spannungsliste
turbidity_currents = []  # Initialisierung der turbidity-Spannungsliste

# Erstellen der Tabelle
frame_table = ttk.Frame(root)
frame_table.grid(row=8, column=0, columnspan=3, pady=10)

tree = ttk.Treeview(frame_table, columns=("Uhrzeit", "Probenname", "Mittelwert der Spannung Nitrat", "Mittelwert der Spannung DOC A", "Mittelwert der Spannung DOC B", "Mittelwert der Spannung Turbidity","Nitrat Strom (mA)", "DOC Strom A (mA)", "DOC Strom B (mA)", "Turbidity Strom (mA)"), show="headings")
tree.heading("Uhrzeit", text="Uhrzeit")
tree.heading("Probenname", text="Probenname")
tree.heading("Mittelwert der Spannung Nitrat", text="Mittelwert der Spannung Nitrat")
tree.heading("Mittelwert der Spannung DOC A", text="Mittelwert der Spannung DOC A")
tree.heading("Mittelwert der Spannung DOC B", text="Mittelwert der Spannung DOC B")
tree.heading("Mittelwert der Spannung Turbidity", text="Mittelwert der Spannung Turbidity")
tree.heading("Nitrat Strom (mA)", text="Nitrat Strom (mA)")
tree.heading("DOC Strom A (mA)", text="DOC Strom A (mA)")
tree.heading("DOC Strom B (mA)", text="DOC Strom B (mA)")
tree.heading("Turbidity Strom (mA)", text="Turbidity Strom (mA)")
tree.pack(fill=tk.BOTH, expand=True)

# Starten der Hauptschleife
root.mainloop()
