#!/usr/bin/env python3
"""
Verilog Wrapper Generator GUI
A user-friendly graphical interface for generating Verilog wrapper files.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import re
import tempfile
import shutil
from verilog_wrapper_generator import WrapperGenerator
from typing import Dict, List, Optional

class VerilogWrapperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Verilog Wrapper Generator")
        self.root.geometry("800x600")
        
        # Data storage
        self.config_data = {
            'top_module': '',
            'instances': [],
            'top_ports': [],
            'instance_to_top': {},
            'instance_connections': []
        }
        
        # Current step tracking
        self.current_step = 0
        self.steps = [
            "Top Module Configuration",
            "Instance Definition", 
            "Top Port Definition",
            "Instance-to-Top Mapping",
            "Instance Connections",
            "Generate & Review"
        ]
        
        self.setup_ui()
        self.update_step_display()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Step indicator
        self.step_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        self.step_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.step_label = ttk.Label(self.step_frame, text="", font=("Arial", 12, "bold"))
        self.step_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(self.step_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.step_frame.columnconfigure(0, weight=1)
        
        # Content frame
        self.content_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        self.content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        
        # Navigation buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.prev_btn = ttk.Button(nav_frame, text="← Previous", command=self.prev_step)
        self.prev_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.next_btn = ttk.Button(nav_frame, text="Next →", command=self.next_step)
        self.next_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Initialize first step
        self.show_step()
        
    def update_step_display(self):
        """Update the step indicator and progress bar"""
        step_text = f"Step {self.current_step + 1}/{len(self.steps)}: {self.steps[self.current_step]}"
        self.step_label.config(text=step_text)
        
        progress = ((self.current_step + 1) / len(self.steps)) * 100
        self.progress_bar['value'] = progress
        
        # Update button states
        self.prev_btn.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        self.next_btn.config(text="Generate" if self.current_step == len(self.steps) - 1 else "Next →")
        
    def show_step(self):
        """Show the current step's UI"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        step_methods = [
            self.show_top_module_step,
            self.show_instances_step,
            self.show_top_ports_step,
            self.show_instance_to_top_step,
            self.show_instance_connections_step,
            self.show_generate_step
        ]
        
        step_methods[self.current_step]()
        
    def show_top_module_step(self):
        """Step 1: Top Module Configuration"""
        ttk.Label(self.content_frame, text="Enter the top module name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.top_module_entry = ttk.Entry(self.content_frame, width=50)
        self.top_module_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.top_module_entry.insert(0, self.config_data['top_module'])
        
        # Help text
        help_text = """
Examples:
• cpu_system_wrapper
• top_level_module
• main_wrapper

The top module name will be used as the module name in the generated Verilog file.
        """
        help_label = ttk.Label(self.content_frame, text=help_text, foreground="gray")
        help_label.grid(row=2, column=0, sticky=tk.W)
        
    def show_instances_step(self):
        """Step 2: Instance Definition"""
        ttk.Label(self.content_frame, text="Define instances:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Instructions
        instructions = "Format: instance_name | verilog_file.v | param1=value1,param2=value2 (parameters optional)"
        ttk.Label(self.content_frame, text=instructions, foreground="blue").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text area
        self.instances_text = scrolledtext.ScrolledText(self.content_frame, width=70, height=10)
        self.instances_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Load existing data
        instances_text = ""
        for instance in self.config_data['instances']:
            instances_text += f"{instance}\n"
        self.instances_text.insert('1.0', instances_text)
        
        # Example
        example_text = """
Example:
cpu_inst | cpu.v | DATA_WIDTH=32,ADDR_WIDTH=16
memory_inst | memory.v
uart_inst | uart.v | BAUD_RATE=115200
        """
        ttk.Label(self.content_frame, text=example_text, foreground="gray").grid(row=3, column=0, sticky=tk.W)
        
    def show_top_ports_step(self):
        """Step 3: Top Port Definition"""
        ttk.Label(self.content_frame, text="Define top-level ports:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Instructions
        instructions = "Format: direction [width] port_name"
        ttk.Label(self.content_frame, text=instructions, foreground="blue").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text area
        self.top_ports_text = scrolledtext.ScrolledText(self.content_frame, width=70, height=10)
        self.top_ports_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Load existing data
        ports_text = ""
        for port in self.config_data['top_ports']:
            ports_text += f"{port}\n"
        self.top_ports_text.insert('1.0', ports_text)
        
        # Example
        example_text = """
Example:
input sys_clk
input sys_reset
input [7:0] data_in
output [15:0] data_out
output ready
inout [7:0] bidir_port
        """
        ttk.Label(self.content_frame, text=example_text, foreground="gray").grid(row=3, column=0, sticky=tk.W)
        
    def show_instance_to_top_step(self):
        """Step 4: Instance-to-Top Mapping"""
        ttk.Label(self.content_frame, text="Map instance ports to top-level ports:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Instructions
        instructions = "Format: instance.port[range] -> top_port[range] or TIE0/TIE1/FLOAT"
        ttk.Label(self.content_frame, text=instructions, foreground="blue").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text area
        self.instance_to_top_text = scrolledtext.ScrolledText(self.content_frame, width=70, height=10)
        self.instance_to_top_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Load existing data
        mapping_text = ""
        for mapping in self.config_data['instance_to_top']:
            mapping_text += f"{mapping}\n"
        self.instance_to_top_text.insert('1.0', mapping_text)
        
        # Example
        example_text = """
Example:
cpu_inst.clk -> sys_clk
cpu_inst.reset -> sys_reset
cpu_inst.data_in -> data_in
cpu_inst.data_out[15:8] -> data_out[15:8]
cpu_inst.enable -> TIE1
memory_inst.cs -> TIE0
uart_inst.bidir -> FLOAT
        """
        ttk.Label(self.content_frame, text=example_text, foreground="gray").grid(row=3, column=0, sticky=tk.W)
        
    def show_instance_connections_step(self):
        """Step 5: Instance Connections"""
        ttk.Label(self.content_frame, text="Define connections between instances:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Instructions
        instructions = "Format: source_instance.port[range] -> target_instance.port[range]"
        ttk.Label(self.content_frame, text=instructions, foreground="blue").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text area
        self.instance_connections_text = scrolledtext.ScrolledText(self.content_frame, width=70, height=10)
        self.instance_connections_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Load existing data
        connections_text = ""
        for connection in self.config_data['instance_connections']:
            connections_text += f"{connection}\n"
        self.instance_connections_text.insert('1.0', connections_text)
        
        # Example
        example_text = """
Example:
cpu_inst.data_out -> memory_inst.data_in
cpu_inst.addr -> memory_inst.addr
memory_inst.ready -> cpu_inst.mem_ready
cpu_inst.uart_tx -> uart_inst.tx_data
cpu_inst.status[3:0] -> uart_inst.data_in[7:4]
        """
        ttk.Label(self.content_frame, text=example_text, foreground="gray").grid(row=3, column=0, sticky=tk.W)
        
    def show_generate_step(self):
        """Step 6: Generate & Review"""
        ttk.Label(self.content_frame, text="Review Configuration and Generate:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Configuration summary
        summary_frame = ttk.LabelFrame(self.content_frame, text="Configuration Summary", padding="10")
        summary_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        summary_frame.columnconfigure(0, weight=1)
        
        summary_text = scrolledtext.ScrolledText(summary_frame, width=70, height=15, state=tk.DISABLED)
        summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Generate summary
        self.generate_summary(summary_text)
        
        # Generate button
        generate_frame = ttk.Frame(self.content_frame)
        generate_frame.grid(row=2, column=0, pady=(10, 0))
        
        ttk.Button(generate_frame, text="Generate Verilog File", command=self.generate_verilog).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(generate_frame, text="Save Configuration", command=self.save_configuration).grid(row=0, column=1, padx=(10, 0))
        
    def generate_summary(self, text_widget):
        """Generate configuration summary"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete('1.0', tk.END)
        
        summary = f"""Configuration Summary:

Top Module: {self.config_data['top_module']}

Instances ({len(self.config_data['instances'])}):
"""
        for i, instance in enumerate(self.config_data['instances'], 1):
            summary += f"  {i}. {instance}\n"
            
        summary += f"""
Top Ports ({len(self.config_data['top_ports'])}):
"""
        for i, port in enumerate(self.config_data['top_ports'], 1):
            summary += f"  {i}. {port}\n"
            
        summary += f"""
Instance-to-Top Mappings ({len(self.config_data['instance_to_top'])}):
"""
        for i, mapping in enumerate(self.config_data['instance_to_top'], 1):
            summary += f"  {i}. {mapping}\n"
            
        summary += f"""
Instance Connections ({len(self.config_data['instance_connections'])}):
"""
        for i, connection in enumerate(self.config_data['instance_connections'], 1):
            summary += f"  {i}. {connection}\n"
            
        text_widget.insert('1.0', summary)
        text_widget.config(state=tk.DISABLED)
        
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.save_current_step()
            self.current_step -= 1
            self.update_step_display()
            self.show_step()
            
    def next_step(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            if self.validate_current_step():
                self.save_current_step()
                self.current_step += 1
                self.update_step_display()
                self.show_step()
        else:
            # Generate step
            self.generate_verilog()
            
    def validate_current_step(self):
        """Validate current step data"""
        if self.current_step == 0:
            # Top module validation
            if not self.top_module_entry.get().strip():
                messagebox.showerror("Error", "Top module name is required!")
                return False
        elif self.current_step == 1:
            # Instances validation
            if not self.instances_text.get('1.0', tk.END).strip():
                messagebox.showerror("Error", "At least one instance is required!")
                return False
        elif self.current_step == 2:
            # Top ports validation
            if not self.top_ports_text.get('1.0', tk.END).strip():
                messagebox.showerror("Error", "At least one top port is required!")
                return False
        
        return True
        
    def save_current_step(self):
        """Save current step data"""
        if self.current_step == 0:
            self.config_data['top_module'] = self.top_module_entry.get().strip()
        elif self.current_step == 1:
            instances_text = self.instances_text.get('1.0', tk.END).strip()
            self.config_data['instances'] = [line.strip() for line in instances_text.split('\n') if line.strip()]
        elif self.current_step == 2:
            ports_text = self.top_ports_text.get('1.0', tk.END).strip()
            self.config_data['top_ports'] = [line.strip() for line in ports_text.split('\n') if line.strip()]
        elif self.current_step == 3:
            mapping_text = self.instance_to_top_text.get('1.0', tk.END).strip()
            self.config_data['instance_to_top'] = [line.strip() for line in mapping_text.split('\n') if line.strip()]
        elif self.current_step == 4:
            connections_text = self.instance_connections_text.get('1.0', tk.END).strip()
            self.config_data['instance_connections'] = [line.strip() for line in connections_text.split('\n') if line.strip()]
            
    def generate_verilog(self):
        """Generate Verilog wrapper file"""
        try:
            # Save current step
            self.save_current_step()
            
            # Create temporary config directory
            temp_dir = tempfile.mkdtemp()
            config_dir = os.path.join(temp_dir, 'config')
            os.makedirs(config_dir)
            
            # Write config files
            self.write_config_files(config_dir)
            
            # Generate wrapper
            generator = WrapperGenerator()
            wrapper_code = generator.generate_wrapper_from_config(config_dir)
            
            # Save to file
            output_file = filedialog.asksaveasfilename(
                defaultextension=".v",
                filetypes=[("Verilog files", "*.v"), ("All files", "*.*")],
                title="Save Verilog Wrapper"
            )
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(wrapper_code)
                
                messagebox.showinfo("Success", f"Verilog wrapper generated successfully!\n\nFile: {output_file}\n\nReport files generated in ./rpt/ directory")
            
            # Cleanup
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Verilog wrapper:\n{str(e)}")
            
    def write_config_files(self, config_dir):
        """Write configuration files"""
        # Top module
        with open(os.path.join(config_dir, 'top_module.txt'), 'w') as f:
            f.write(self.config_data['top_module'])
            
        # Instances
        with open(os.path.join(config_dir, 'instances.txt'), 'w') as f:
            f.write("# Instances\n\n[INSTANCES]\n")
            for instance in self.config_data['instances']:
                f.write(f"{instance}\n")
                
        # Top ports
        with open(os.path.join(config_dir, 'top_ports.txt'), 'w') as f:
            f.write("# Top Ports\n\n[TOP_PORTS]\n")
            for port in self.config_data['top_ports']:
                f.write(f"{port}\n")
                
        # Instance to top mapping
        with open(os.path.join(config_dir, 'instance_to_top.txt'), 'w') as f:
            f.write("# Instance to Top Mapping\n\n[INSTANCE_TO_TOP]\n")
            for mapping in self.config_data['instance_to_top']:
                f.write(f"{mapping}\n")
                
        # Instance connections
        with open(os.path.join(config_dir, 'instance_connections.txt'), 'w') as f:
            f.write("# Instance Connections\n\n[INSTANCE_CONNECTIONS]\n")
            for connection in self.config_data['instance_connections']:
                f.write(f"{connection}\n")
                
    def save_configuration(self):
        """Save configuration to files"""
        try:
            config_dir = filedialog.askdirectory(title="Select directory to save configuration")
            if config_dir:
                # Save current step
                self.save_current_step()
                
                # Write config files
                self.write_config_files(config_dir)
                
                messagebox.showinfo("Success", f"Configuration saved to:\n{config_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")

def main():
    """Main function"""
    root = tk.Tk()
    app = VerilogWrapperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()