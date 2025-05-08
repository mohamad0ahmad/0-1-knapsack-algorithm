import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import knapsack
from styles import COLORS, FONTS, configure_styles

class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Solver")
        self.root.geometry("1100x900")
        self.root.configure(bg=COLORS['background'])

        configure_styles()

        main_frame = ttk.Frame(root, padding="15", style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="0/1 Knapsack Problem Solver", style='Title.TLabel').pack(pady=(0, 15))

        input_frame = ttk.LabelFrame(main_frame, text=" Input Parameters ", padding="15", style='Card.TLabelframe')
        input_frame.pack(fill=tk.X, pady=5)

        capacity_frame = ttk.Frame(input_frame, style='Custom.TFrame')
        capacity_frame.pack(fill=tk.X, pady=5)

        ttk.Label(capacity_frame, text="Knapsack Capacity:", style='Header.TLabel').pack(side=tk.LEFT, padx=5)

        self.capacity_entry = ttk.Entry(capacity_frame, width=15, style='Custom.TEntry', font=FONTS['input'])
        self.capacity_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Items List", style='Header.TLabel').pack(pady=(10, 5), anchor=tk.W)

        self.items_table = ttk.Treeview(input_frame, columns=('weight', 'value'), show='headings', height=6, style='Custom.Treeview')
        self.items_table.heading('weight', text='Weight', anchor=tk.CENTER)
        self.items_table.heading('value', text='Value', anchor=tk.CENTER)
        self.items_table.column('weight', width=120, anchor=tk.CENTER)
        self.items_table.column('value', width=120, anchor=tk.CENTER)
        self.items_table.pack(fill=tk.X, padx=5, pady=5)

        control_frame = ttk.Frame(input_frame, style='Custom.TFrame')
        control_frame.pack(fill=tk.X, pady=10)

        input_subframe = ttk.Frame(control_frame, style='Custom.TFrame')
        input_subframe.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_subframe, text="Weight:", style='Body.TLabel').pack(side=tk.LEFT)

        self.weight_entry = ttk.Entry(input_subframe, width=8, style='Custom.TEntry', font=FONTS['input'])
        self.weight_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_subframe, text="Value:", style='Body.TLabel').pack(side=tk.LEFT)

        self.value_entry = ttk.Entry(input_subframe, width=8, style='Custom.TEntry', font=FONTS['input'])
        self.value_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_subframe, text="Add Item", command=self.add_item, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_subframe, text="Remove Selected", command=self.remove_item, style='Warning.TButton').pack(side=tk.LEFT, padx=5)

        button_subframe = ttk.Frame(control_frame, style='Custom.TFrame')
        button_subframe.pack(side=tk.RIGHT, padx=5)

        ttk.Button(button_subframe, text="Clear All", command=self.clear_items, style='Warning.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_subframe, text="Solve", command=self.solve, style='Success.TButton').pack(side=tk.RIGHT, padx=5)

        results_frame = ttk.LabelFrame(main_frame, text=" Results ", padding="15", style='Card.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.stats_frame = ttk.Frame(results_frame, style='Custom.TFrame')
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.stats_label = ttk.Label(self.stats_frame, text="Items: 0 | Selected: 0 | Max Value: $0", style='Stats.TLabel')
        self.stats_label.pack()

        viz_frame = ttk.Frame(results_frame, style='Custom.TFrame')
        viz_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.fig.patch.set_facecolor(COLORS['card'])
        self.ax.set_facecolor(COLORS['card'])
        self.ax.tick_params(colors=COLORS['text'])
        self.ax.xaxis.label.set_color(COLORS['text'])
        self.ax.yaxis.label.set_color(COLORS['text'])
        self.ax.title.set_color(COLORS['text'])

        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        details_frame = ttk.Frame(results_frame, style='Custom.TFrame')
        details_frame.pack(fill=tk.X, pady=(10, 0))

        self.details_text = tk.Text(details_frame, height=4, wrap=tk.WORD, bg=COLORS['card'], fg=COLORS['text'], font=FONTS['body'], relief=tk.FLAT)
        self.details_text.pack(fill=tk.X)

    def add_item(self):
        try:
            weight = float(self.weight_entry.get())
            value = float(self.value_entry.get())
            if weight <= 0 or value <= 0:
                raise ValueError("Values must be positive")
            self.items_table.insert('', tk.END, values=(weight, value))
            self.weight_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")

    def remove_item(self):
        selected_item = self.items_table.selection()
        if selected_item:
            self.items_table.delete(selected_item)

    def clear_items(self):
        for item in self.items_table.get_children():
            self.items_table.delete(item)

    def solve(self):
        try:
            capacity = float(self.capacity_entry.get())
            if capacity <= 0:
                raise ValueError("Capacity must be positive")
            items = [tuple(map(float, self.items_table.item(child)['values'])) for child in self.items_table.get_children()]
            if not items:
                raise ValueError("No items added")
            W, V = zip(*items)
            max_value, selected_items = knapsack(capacity, W, V)
            self.stats_label.config(text=f"Items: {len(items)} | Selected: {len(selected_items)} | Max Value: ${max_value}")
            self.display_details(capacity, W, V, selected_items)
            self.visualize_solution(capacity, W, V, selected_items)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")

    def display_details(self, capacity, W, V, selected_items):
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        if not selected_items:
            self.details_text.insert(tk.END, "No items were selected in the optimal solution.")
        else:
            self.details_text.insert(tk.END, "Selected Items:\n", 'header')
            total_weight = 0
            for idx in selected_items:
                w = round(W[idx])
                v = V[idx]
                self.details_text.insert(tk.END, f"- Item {idx+1}: Weight = {w}, Value = {v}\n")
                total_weight += w
            self.details_text.insert(tk.END, f"\nTotal Weight: {total_weight}/{int(round(capacity))}", 'highlight')
        self.details_text.tag_config('header', foreground=COLORS['highlight'], font=FONTS['header'])
        self.details_text.tag_config('highlight', foreground=COLORS['success'], font=FONTS['header'])
        self.details_text.config(state=tk.DISABLED)

    def visualize_solution(self, capacity, W, V, selected_items):
        self.ax.clear()
        colors = [COLORS['success'] if i in selected_items else COLORS['error'] for i in range(len(W))]
        weights = [int(round(w)) for w in W]
        self.ax.bar(range(len(W)), weights, color=colors, alpha=0.7)
        self.ax.axhline(y=int(round(capacity)), color=COLORS['highlight'], linestyle='--', linewidth=2, label='Capacity')
        for i, (w, v) in enumerate(zip(weights, V)):
            self.ax.text(i, w + 0.1, f"${v}", ha='center', va='bottom', color=COLORS['text'])
        self.ax.set_title('Knapsack Solution')
        self.ax.set_xlabel('Item Index')
        self.ax.set_ylabel('Weight')
        self.ax.set_xticks(range(len(W)))
        self.ax.set_xticklabels([f"Item {i+1}" for i in range(len(W))])
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()
