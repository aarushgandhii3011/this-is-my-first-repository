import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


import matplotlib
matplotlib.use('TkAgg')


class SalesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weekly Sales Data Entry & Plotting GUI")
        self.geometry("1000x700")
        
        self.sales_entries = []
        self.create_widgets()
        self.df = None

    def create_widgets(self):
        input_frame = tk.Frame(self, padx=10, pady=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(input_frame, text="Enter Weekly Sales Data", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
        for i, day in enumerate(days):
            row_frame = tk.Frame(input_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(row_frame, text=f"{day} Sales:", width=15, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(row_frame, width=15)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.sales_entries.append(entry)

       
        button_frame = tk.Frame(input_frame, pady=10)
        button_frame.pack()
        
        tk.Button(button_frame, text="Generate & Plot", command=self.generate_and_plot_data).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Entries", command=self.clear_entries).pack(side=tk.RIGHT, padx=5)

       
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def get_sales_data(self):
        """Retrieves data from entry widgets and validates it."""
        sales = []
        for entry in self.sales_entries:
            try:
         
                sales_value = int(entry.get())
                sales.append(sales_value)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please ensure all sales entries are valid integers.")
                return None
        return sales

    def generate_and_plot_data(self):
        """Processes data, saves to CSV, and displays the plot in the GUI."""
        sales_data = self.get_sales_data()
        if sales_data is None:
            return

       
        data = {
            'Day': [f'Day {i+1}' for i in range(len(sales_data))],
            'Sales': sales_data
        }
        self.df = pd.DataFrame(data)
        
   
        file_name = 'daily_sales.csv'
        file_path = os.path.join(os.getcwd(), file_name) 
        self.df.to_csv(file_path, index=False)
        print(f"\nData saved to {file_path}")

      
        for widget in self.plot_frame.winfo_children():
            widget.destroy() 

        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.df['Day'], self.df['Sales'], marker='o', linestyle='-', color='b')
        ax.set_title('Weekly Sales Trend')
        ax.set_xlabel('Day of the Week')
        ax.set_ylabel('Sales Amount')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clear_entries(self):
        """Clears all input entry fields."""
        for entry in self.sales_entries:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    app = SalesApp()
    app.mainloop()
