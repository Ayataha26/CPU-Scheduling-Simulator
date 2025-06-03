from tkinter import messagebox
import tkinter as tk
import matplotlib.pyplot as plt
import random


class Process:
    def __init__(self):
        self.AT = 0
        self.BT = 0
        self.ST = [0] * 20
        self.WT = 0
        self.FT = 0
        self.TAT = 0
        self.pos = 0
        self.RT = 0


quantum = 0


def is_valid_arrival_time(value):
    try:
        num = int(value)
        if num < 0:
            return False
        return True
    except ValueError:
        return False


def is_positive_integer(value, allow_zero=False):
    if not allow_zero and value == '0':
        return False
    try:
        num = int(value)
        if num <= 0:
            return False
        return True
    except ValueError:
        return False


def validate_input():
    processes = processes_entry.get()
    arrival_times = arrival_entry.get().split(',')
    burst_times = burst_entry.get().split(',')
    if not processes.lstrip('-').isdigit():
        messagebox.showerror(
            "Process Error : Character Error", "The number of process mustn't be character.")
        return False
    elif not is_positive_integer(processes):
        messagebox.showerror(
            "Process Error : Sign Error", "Number of processes must be a positive integer.")
        return False

    if len(arrival_times) != int(processes) or len(burst_times) != int(processes):
        messagebox.showerror(
            "Error", "Number of arrival/burst times must match the number of processes.")
        return False

    for arr_time in arrival_times:
        if not arr_time.lstrip('-').isdigit():
            messagebox.showerror(
                "Arrival time Error : Character Error", "The arrival time mustn't be character.")
            return False
        elif not is_valid_arrival_time(arr_time):
            messagebox.showerror(
                "Arrival time Error : Sign Error", "Arrival time must be a non-negative integer.")
            return False

    for burst_time in burst_times:
        if not burst_time.lstrip('-').isdigit():
            messagebox.showerror(
                "Burst time Error : Character Error", "Burst time mustn't be character.")
            return False
        elif not is_positive_integer(burst_time):
            messagebox.showerror(
                "Burst time Error : Sign Error", "Burst time must be a positive integer.")
            return False

        if not quantum_entry.get().lstrip('-').isdigit():
            messagebox.showerror(
                "Quantum time Error : Character Error", "Quantum time mustn't be character.")
            return False
        elif not is_positive_integer(quantum_entry.get()):
            messagebox.showerror(
                "Quantum time Error : Sign Error", "Quantum time must be a positive integer.")
            return False

    return True


gantt_chart = []


def calculate():
    if not validate_input():
        return

    global quantum

    number_of_processes = int(processes_entry.get())
    processes = [Process() for _ in range(number_of_processes)]

    for i in range(number_of_processes):
        processes[i].pos = i + 1

    arrival_times = arrival_entry.get().split(',')
    burst_times = burst_entry.get().split(',')

    for i in range(number_of_processes):
        processes[i].AT = int(arrival_times[i])
        processes[i].BT = int(burst_times[i])

    quantum = int(quantum_entry.get())

    c = number_of_processes
    s = [[-1] * 20 for _ in range(number_of_processes)]
    time = 0
    mini = float('inf')
    b = [0] * number_of_processes
    a = [0] * number_of_processes
    global gantt_chart

    for i in range(number_of_processes):
        b[i] = processes[i].BT
        a[i] = processes[i].AT

    tot_wt = tot_tat = tot_rt = 0
    flag = False

    while c != 0:
        mini = float('inf')
        flag = False

        for i in range(number_of_processes):
            p = time + 0.1
            if a[i] <= p and mini > a[i] and b[i] > 0:
                index = i
                mini = a[i]
                flag = True

        if not flag:
            time += 1
            gantt_chart.append((None, 1))
            continue

        j = 0
        while s[index][j] != -1:
            j += 1

        if s[index][j] == -1:
            s[index][j] = time
            processes[index].ST[j] = time

        if j == 0:
            processes[index].RT = time - processes[index].AT
            tot_rt += processes[index].RT

        if b[index] <= quantum:
            time += b[index]
            gantt_chart.append((processes[index].pos, b[index]))
            b[index] = 0
        else:
            time += quantum
            gantt_chart.append((processes[index].pos, quantum))
            b[index] -= quantum

        if b[index] > 0:
            a[index] = time + 0.1

        if b[index] == 0:
            c -= 1
            processes[index].FT = time
            processes[index].WT = processes[index].FT - \
                processes[index].AT - processes[index].BT
            tot_wt += processes[index].WT
            processes[index].TAT = processes[index].BT + processes[index].WT
            tot_tat += processes[index].TAT

    # Format the result text with centered numbers
    result_text = (
        f"Process_id   |   Arrival time   |   Burst time   |   Waiting time   |   Turnaround time   |   Response time   |\n"
        f"----------------------------------------------------------------------------------------------------------------------------------------------------\n"
    )

    for i in range(number_of_processes):
        result_text += (
            f"{str(processes[i].pos)}\t\t| "
            f"{str(processes[i].AT)}\t| "
            f"{str(processes[i].BT)}\t\t| "
            f"{str(processes[i].WT)}\t\t| "
            f"{str(processes[i].TAT)}\t\t| "
            f"{str(processes[i].RT)}\t\n"
        )
    result_text += "----------------------------------------------------------------------------------------------------------------------------------------------------\n"
    total_wt = sum(p.WT for p in processes)
    total_tat = sum(p.TAT for p in processes)
    total_rt = sum(p.RT for p in processes)

    result_text += (
        f"Total\n\tTotal waiting time: {total_wt} \n\tTotal turaround time: {total_tat}\n\tTotal response time: {total_rt}")

    avg_wt = tot_wt / number_of_processes
    avg_tat = tot_tat / number_of_processes
    avg_rt = tot_rt / number_of_processes

    result_text += (
        f"\n\nAverage values\n\tAverage waiting time: {avg_wt} \n\tAverage turaround time: {avg_tat}\n\tAverage response time: {avg_rt}")

    result_textbox.delete("1.0", tk.END)
    result_textbox.insert(tk.END, result_text)


gantt_data = gantt_chart


def gantt_chart_GUI():

    # Increment x-axis ticks by two
    x_ticks = range(0, sum([burst for _, burst in gantt_data]) + 1, 2)

    # Define a dictionary to map process IDs to colors
    process_colors = {
        "p1": "tab:blue",
        "p2": "tab:orange",
        "p3": "tab:green",
        "p4": "tab:red",
        "p5": "tab:purple",
        # Add more colors as needed for additional processes
    }

    fig, gnt = plt.subplots()
    gnt.set_title('Round Robin CPU Scheduling')
    gnt.set_xlim(0, sum([burst for _, burst in gantt_data]))
    gnt.set_ylim(0, 10)
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_yticks([5])
    # gnt.set_yticklabels(['Processes'])
    # Set the x-axis ticks to be incremented by two units
    gnt.set_xticks(x_ticks)

    process_colors = {}  # Empty dictionary to store process ID and color pairs

    # Plot Gantt chart
    for i in range(len(gantt_data)):
        process_id = gantt_data[i][0]

        # Check if process ID has a color assigned
        if process_id not in process_colors:
            # Generate a new color (replace with your preferred color generation method)
            # Generate random hex color (example)
            color = '#%06x' % (random.randint(0, 16777215))
            # Add process ID and color to the dictionary
            process_colors[process_id] = color

        color = process_colors[process_id]  # Use the assigned color

        # Use default color if not found in the dictionary
        # color = process_colors.get(process_id, "tab:blue")
        gnt.broken_barh([(sum([burst for _, burst in gantt_data[:i]]),
                        gantt_data[i][1])], (4, 2), facecolors=color)
        gnt.text(sum([burst for _, burst in gantt_data[:i]]) + gantt_data[i]
                 [1] / 2, 5.5, process_id, ha='center', va='center', color='white')

    # Add lines to separate the processes
    for i in range(len(gantt_data) - 1):
        gnt.axvline(sum([burst for _, burst in gantt_data[:i + 1]]),
                    color='black', linestyle='-', linewidth=1)

    plt.show()


# Create a Tkinter window
root = tk.Tk()
root.title("Round Robin Scheduler")

# Label and Entry widgets for input
processes_label = tk.Label(root, text="Number of Processes:")
processes_label.grid(row=0, column=0, padx=10, pady=5)
# Create an entry widget for the number of processes
processes_entry = tk.Entry(root)
# Make sure this line is present
processes_entry.grid(row=0, column=1, padx=10, pady=5)

arrival_label = tk.Label(root, text="Arrival Times (comma separated):")
arrival_label.grid(row=1, column=0, padx=10, pady=5)
arrival_entry = tk.Entry(root)
arrival_entry.grid(row=1, column=1, padx=10, pady=5)

burst_label = tk.Label(root, text="Burst Times (comma separated):")
burst_label.grid(row=2, column=0, padx=10, pady=5)
burst_entry = tk.Entry(root)
burst_entry.grid(row=2, column=1, padx=10, pady=5)

quantum_label = tk.Label(root, text="Quantum Number:")
quantum_label.grid(row=3, column=0, padx=10, pady=5)
quantum_entry = tk.Entry(root)
quantum_entry.grid(row=3, column=1, padx=10, pady=5)

calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=4, columnspan=2, padx=10, pady=5)

Gui_button = tk.Button(root, text="Show Gantt Chart", command=gantt_chart_GUI)
Gui_button.grid(row=5, columnspan=2, padx=10, pady=5)

# Text widget for displaying results
result_textbox = tk.Text(root, width=90, height=20, font=("Arial", 10))
result_textbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
