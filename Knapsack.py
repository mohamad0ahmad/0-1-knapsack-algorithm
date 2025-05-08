import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Modern color scheme
COLORS = {
    'background': '#3A3B3C',
    'foreground': '#E4E6EB',
    'accent': '#5778A8',
    'success': '#6DA56F',
    'warning': '#D4A15F',
    'error': '#C75D5D',
    'highlight': '#5D8EC7',
    'text': '#E4E6EB',
    'card': '#242526'
}

# Font settings
FONTS = {
    'title': ('Segoe UI', 14, 'bold'),
    'header': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 11),
    'button': ('Segoe UI', 11, 'bold'),
    'input': ('Segoe UI', 11)  # Larger font for weight/value inputs
}

def knapsack(capacity, W, V):
    if W is None or V is None or len(W) != len(V) or capacity < 0:
        raise ValueError("Invalid input")
    
    capacity = int(round(capacity))
    N = len(W)
    
    DP = [[0] * (capacity + 1) for _ in range(N + 1)]
    
    for i in range(1, N + 1):
        w = int(round(W[i - 1]))
        v = V[i - 1]
        for sz in range(1, capacity + 1):
            DP[i][sz] = DP[i - 1][sz]
            if sz >= w and DP[i - 1][sz - w] + v > DP[i][sz]:
                DP[i][sz] = DP[i - 1][sz - w] + v
    
    sz = capacity
    items_selected = []
    for i in range(N, 0, -1):
        if DP[i][sz] != DP[i - 1][sz]:
            item_index = i - 1
            items_selected.append(item_index)
            sz -= int(round(W[item_index]))
    
    items_selected.reverse()
    return DP[N][capacity], items_selected

class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Solver")
        self.root.geometry("1100x900")
        self.root.configure(bg=COLORS['background'])
        
        self.configure_styles()
        
        # Main container
        main_frame = ttk.Frame(root, padding="15", style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            main_frame, 
            text="0/1 Knapsack Problem Solver", 
            style='Title.TLabel'
        ).pack(pady=(0, 15))
        
        # Input Section
        input_frame = ttk.LabelFrame(
            main_frame, 
            text=" Input Parameters ", 
            padding="15", 
            style='Card.TLabelframe'
        )
        input_frame.pack(fill=tk.X, pady=5)
        
        # Capacity input
        capacity_frame = ttk.Frame(input_frame, style='Custom.TFrame')
        capacity_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            capacity_frame, 
            text="Knapsack Capacity:", 
            style='Header.TLabel'
        ).pack(side=tk.LEFT, padx=5)
        
        self.capacity_entry = ttk.Entry(
            capacity_frame, 
            width=15, 
            style='Custom.TEntry',
            font=FONTS['input']
        )
        self.capacity_entry.pack(side=tk.LEFT, padx=5)
        
        # Items Table
        ttk.Label(
            input_frame, 
            text="Items List", 
            style='Header.TLabel'
        ).pack(pady=(10, 5), anchor=tk.W)
        
        self.items_table = ttk.Treeview(
            input_frame, 
            columns=('weight', 'value'), 
            show='headings', 
            height=6,
            style='Custom.Treeview'
        )
        self.items_table.heading('weight', text='Weight', anchor=tk.CENTER)
        self.items_table.heading('value', text='Value', anchor=tk.CENTER)
        self.items_table.column('weight', width=120, anchor=tk.CENTER)
        self.items_table.column('value', width=120, anchor=tk.CENTER)
        self.items_table.pack(fill=tk.X, padx=5, pady=5)
        
        # Items manipulation controls
        control_frame = ttk.Frame(input_frame, style='Custom.TFrame')
        control_frame.pack(fill=tk.X, pady=10)
        
        # Weight/Value inputs (with larger font)
        input_subframe = ttk.Frame(control_frame, style='Custom.TFrame')
        input_subframe.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            input_subframe, 
            text="Weight:", 
            style='Body.TLabel'
        ).pack(side=tk.LEFT)
        
        self.weight_entry = ttk.Entry(
            input_subframe, 
            width=8, 
            style='Custom.TEntry',
            font=FONTS['input']
        )
        self.weight_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            input_subframe, 
            text="Value:", 
            style='Body.TLabel'
        ).pack(side=tk.LEFT)
        
        self.value_entry = ttk.Entry(
            input_subframe, 
            width=8, 
            style='Custom.TEntry',
            font=FONTS['input']
        )
        self.value_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_subframe, 
            text="Add Item", 
            command=self.add_item,
            style='Accent.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_subframe, 
            text="Remove Selected", 
            command=self.remove_item,
            style='Warning.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Action buttons (Solve and Clear)
        button_subframe = ttk.Frame(control_frame, style='Custom.TFrame')
        button_subframe.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_subframe, 
            text="Clear All", 
            command=self.clear_items,
            style='Warning.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_subframe, 
            text="Solve", 
            command=self.solve,
            style='Success.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(
            main_frame, 
            text=" Results ", 
            padding="15",
            style='Card.TLabelframe'
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Stats in one line
        self.stats_frame = ttk.Frame(results_frame, style='Custom.TFrame')
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = ttk.Label(
            self.stats_frame, 
            text="Items: 0 | Selected: 0 | Max Value: $0", 
            style='Stats.TLabel'
        )
        self.stats_label.pack()
        
        # Visualization
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
        
        # Details
        details_frame = ttk.Frame(results_frame, style='Custom.TFrame')
        details_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.details_text = tk.Text(
            details_frame, 
            height=4, 
            wrap=tk.WORD,
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=FONTS['body'],
            relief=tk.FLAT
        )
        self.details_text.pack(fill=tk.X)
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame styles
        style.configure('Custom.TFrame', background=COLORS['background'])
        style.configure('Card.TLabelframe', 
                      background=COLORS['background'],
                      foreground=COLORS['highlight'],
                      bordercolor=COLORS['accent'])
        style.configure('Card.TLabelframe.Label', 
                      background=COLORS['background'],
                      foreground=COLORS['highlight'],
                      font=FONTS['header'])
        
        # Label styles
        style.configure('Title.TLabel', 
                      background=COLORS['background'],
                      foreground=COLORS['highlight'],
                      font=FONTS['title'])
        style.configure('Header.TLabel', 
                      background=COLORS['background'],
                      foreground=COLORS['highlight'],
                      font=FONTS['header'])
        style.configure('Body.TLabel', 
                      background=COLORS['background'],
                      foreground=COLORS['text'],
                      font=FONTS['body'])
        style.configure('Stats.TLabel', 
                      background=COLORS['background'],
                      foreground=COLORS['highlight'],
                      font=('Segoe UI', 11, 'bold'))
        
        # Entry styles
        style.configure('Custom.TEntry',
                      fieldbackground=COLORS['card'],
                      foreground=COLORS['text'],
                      insertcolor=COLORS['text'],
                      font=FONTS['input'])  # Larger font for inputs
        
        # Button styles
        style.configure('Custom.TButton',
                      background=COLORS['card'],
                      foreground=COLORS['text'])
        style.configure('Accent.TButton',
                      background=COLORS['accent'],
                      foreground=COLORS['text'],
                      font=FONTS['button'])
        style.configure('Success.TButton',
                      background=COLORS['success'],
                      foreground=COLORS['text'],
                      font=FONTS['button'])
        style.configure('Warning.TButton',
                      background=COLORS['warning'],
                      foreground=COLORS['text'],
                      font=FONTS['button'])
        
        # Treeview styles
        style.configure('Custom.Treeview',
                      background=COLORS['card'],
                      foreground=COLORS['text'],
                      fieldbackground=COLORS['card'])
        style.map('Custom.Treeview',
                 background=[('selected', COLORS['accent'])])
        style.configure('Custom.Treeview.Heading',
                      background=COLORS['accent'],
                      foreground=COLORS['text'],
                      font=FONTS['body'])
    
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
            
            items = []
            for child in self.items_table.get_children():
                weight, value = self.items_table.item(child)['values']
                items.append((float(weight), float(value)))
            
            if not items:
                raise ValueError("No items added")
            
            W = [item[0] for item in items]
            V = [item[1] for item in items]
            
            max_value, selected_items = knapsack(capacity, W, V)
            
            # Update stats in one line
            self.stats_label.config(
                text=f"Items: {len(items)} | Selected: {len(selected_items)} | Max Value: ${max_value}"
            )
            
            self.display_details(capacity, W, V, selected_items)
            self.visualize_solution(capacity, W, V, selected_items)
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
    
    def display_details(self, capacity, W, V, selected_items):
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        if not selected_items:
            self.details_text.insert(tk.END, "No items were selected in the optimal solution.")
            self.details_text.config(state=tk.DISABLED)
            return
        
        self.details_text.insert(tk.END, "Selected Items:\n", 'header')
        
        total_weight = 0
        for idx in selected_items:
            item_weight = int(round(W[idx]))
            self.details_text.insert(tk.END, 
                                   f"- Item {idx+1}: Weight = {item_weight}, Value = {V[idx]}\n")
            total_weight += item_weight
        
        self.details_text.insert(tk.END, f"\nTotal Weight: {total_weight}/{int(round(capacity))}", 'highlight')
        
        self.details_text.tag_config('header', 
                                   foreground=COLORS['highlight'], 
                                   font=('Segoe UI', 11, 'bold'))
        self.details_text.tag_config('highlight', 
                                   foreground=COLORS['success'], 
                                   font=('Segoe UI', 11, 'bold'))
        self.details_text.config(state=tk.DISABLED)
    
    def visualize_solution(self, capacity, W, V, selected_items):
        self.ax.clear()
        
        all_items = list(range(len(W)))
        colors = [COLORS['success'] if i in selected_items else COLORS['error'] for i in all_items]
        weights = [int(round(w)) for w in W]
        
        bars = self.ax.bar(all_items, weights, color=colors, alpha=0.7)
        self.ax.axhline(
            y=int(round(capacity)), 
            color=COLORS['highlight'], 
            linestyle='--', 
            linewidth=2, 
            label='Capacity'
        )
        
        for i, (w, v) in enumerate(zip(weights, V)):
            self.ax.text(
                i, w + 0.1, f"${v}", 
                ha='center', 
                va='bottom',
                color=COLORS['text']
            )
        
        self.ax.set_title('Knapsack Solution', pad=20, color=COLORS['text'])
        self.ax.set_xlabel('Item Index', color=COLORS['text'])
        self.ax.set_ylabel('Weight', color=COLORS['text'])
        self.ax.set_xticks(all_items)
        self.ax.set_xticklabels([f"Item {i+1}" for i in all_items], color=COLORS['text'])
        self.ax.legend(facecolor=COLORS['card'], edgecolor=COLORS['card'])
        self.ax.grid(True, linestyle='--', alpha=0.3, color=COLORS['accent'])
        
        for spine in self.ax.spines.values():
            spine.set_color(COLORS['accent'])
        
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackGUI(root)
    root.mainloop()