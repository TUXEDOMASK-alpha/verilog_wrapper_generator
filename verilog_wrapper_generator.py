#!/usr/bin/env python3
"""
Verilog Wrapper Generator Tool

This tool creates Verilog wrapper files by instantiating modules and connecting their ports.
It takes a configuration that specifies module files, instance names, and port mappings.
"""

import re
import json
import argparse
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Port:
    """Represents a Verilog port with its direction and width"""
    name: str
    direction: str  # 'input', 'output', 'inout'
    width: Optional[str] = None  # e.g., '[7:0]' or None for single bit


@dataclass
class Module:
    """Represents a Verilog module with its ports"""
    name: str
    ports: List[Port]
    file_path: str


@dataclass
class Instance:
    """Represents a module instance with port mappings"""
    module: Module
    instance_name: str
    parameters: Dict[str, str]  # parameter_name -> value
    port_mapping: Dict[str, str]  # module_port -> top_port


class VerilogParser:
    """Parser for extracting module information from Verilog files"""
    
    def __init__(self):
        # Regex patterns for parsing Verilog
        self.module_pattern = re.compile(r'module\s+(\w+)\s*\((.*?)\);', re.DOTALL)
        
        # Enhanced patterns for different port declaration styles
        # ANSI style: input [7:0] data, output reg [15:0] result
        self.ansi_port_pattern = re.compile(r'(input|output|inout)\s*(wire|reg)?\s*(\[.*?\])?\s*(\w+(?:\s*,\s*\w+)*)', re.MULTILINE)
        
        # Traditional style: input data; output [15:0] result;
        self.traditional_port_pattern = re.compile(r'(input|output|inout)\s*(\[.*?\])?\s*(\w+(?:\s*,\s*\w+)*)\s*;', re.MULTILINE)
        
        # Port list in module declaration
        self.port_list_pattern = re.compile(r'(\w+)(?:\s*,\s*(\w+))*')
    
    def parse_module(self, file_path: str) -> Module:
        """Parse a Verilog file and extract module information"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Verilog file not found: {file_path}")
        
        # Remove comments
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Find module declaration
        module_match = self.module_pattern.search(content)
        if not module_match:
            raise ValueError(f"No module declaration found in {file_path}")
        
        module_name = module_match.group(1)
        port_list = module_match.group(2)
        
        # Get module content
        module_end = content.find('endmodule')
        if module_end == -1:
            raise ValueError(f"No endmodule found in {file_path}")
        
        module_content = content[module_match.end():module_end]
        
        # Parse ports using enhanced parser
        ports = self._parse_ports(port_list, module_content)
        
        return Module(name=module_name, ports=ports, file_path=file_path)
    
    def _parse_ports(self, port_list: str, module_content: str) -> List[Port]:
        """Enhanced port parsing that handles both ANSI and traditional styles"""
        ports = []
        port_info = {}  # port_name -> Port
        
        # First, try to parse ANSI-style ports (ports with directions in module header)
        ansi_ports = self._parse_ansi_ports(port_list)
        if ansi_ports:
            return ansi_ports
        
        # If not ANSI style, parse traditional style
        # Step 1: Get port names from module declaration
        port_names = []
        if port_list.strip():
            # Remove any existing direction/width info and extract just names
            clean_port_list = re.sub(r'(input|output|inout)\s*(\[.*?\])?\s*', '', port_list)
            port_names = [p.strip() for p in clean_port_list.split(',') if p.strip()]
        
        # Step 2: Find port declarations in module body
        # Traditional style declarations
        traditional_matches = self.traditional_port_pattern.findall(module_content)
        for direction, width, port_names_str in traditional_matches:
            port_names_list = [p.strip() for p in port_names_str.split(',')]
            for port_name in port_names_list:
                if port_name:
                    port_info[port_name] = Port(
                        name=port_name, 
                        direction=direction, 
                        width=width if width else None
                    )
        
        # Step 3: Create ports list maintaining order from module declaration
        if port_names:
            for port_name in port_names:
                if port_name in port_info:
                    ports.append(port_info[port_name])
                else:
                    # Default to input if not found in declarations
                    ports.append(Port(name=port_name, direction='input', width=None))
        else:
            # If no port list, just use what we found in declarations
            ports = list(port_info.values())
        
        return ports
    
    def _parse_ansi_ports(self, port_list: str) -> List[Port]:
        """Parse ANSI-style port declarations"""
        if not port_list.strip():
            return []
        
        ports = []
        
        # Check if this looks like ANSI style (contains direction keywords)
        if not re.search(r'(input|output|inout)', port_list):
            return []
        
        # Split by commas, but be careful with brackets
        port_parts = self._split_port_list(port_list)
        
        current_direction = None
        current_width = None
        
        for part in port_parts:
            part = part.strip()
            if not part:
                continue
            
            # Check for direction change
            direction_match = re.match(r'(input|output|inout)\s*(wire|reg)?\s*(\[.*?\])?\s*(.+)', part)
            if direction_match:
                current_direction = direction_match.group(1)
                current_width = direction_match.group(3)
                remaining = direction_match.group(4)
                
                # Extract port names from remaining part
                port_names = [p.strip() for p in remaining.split(',') if p.strip()]
                for port_name in port_names:
                    ports.append(Port(name=port_name, direction=current_direction, width=current_width))
            else:
                # No direction keyword, use current direction
                if current_direction:
                    port_names = [p.strip() for p in part.split(',') if p.strip()]
                    for port_name in port_names:
                        ports.append(Port(name=port_name, direction=current_direction, width=current_width))
        
        return ports
    
    def _split_port_list(self, port_list: str) -> List[str]:
        """Split port list by commas, respecting brackets"""
        parts = []
        current = ""
        bracket_depth = 0
        
        for char in port_list:
            if char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1
            elif char == ',' and bracket_depth == 0:
                parts.append(current.strip())
                current = ""
                continue
            
            current += char
        
        if current.strip():
            parts.append(current.strip())
        
        return parts


class ConfigParser:
    """Parser for reading configuration files"""
    
    def parse_config_directory(self, config_dir: str) -> Dict:
        """Parse all configuration files from a directory"""
        config = {
            'top_module': 'top_wrapper',
            'instances': [],
            'top_ports': [],
            'instance_connections': [],
            'instance_to_top': {}
        }
        
        import os
        
        # Parse top module name
        top_module_file = os.path.join(config_dir, 'top_module.txt')
        if os.path.exists(top_module_file):
            config['top_module'] = self._parse_top_module(top_module_file)
        
        # Parse instances
        instances_file = os.path.join(config_dir, 'instances.txt')
        if os.path.exists(instances_file):
            config['instances'] = self._parse_instances(instances_file)
        
        # Parse top ports
        top_ports_file = os.path.join(config_dir, 'top_ports.txt')
        if os.path.exists(top_ports_file):
            config['top_ports'] = self._parse_top_ports(top_ports_file)
        
        # Parse instance to top mappings
        instance_to_top_file = os.path.join(config_dir, 'instance_to_top.txt')
        if os.path.exists(instance_to_top_file):
            config['instance_to_top'] = self._parse_instance_to_top(instance_to_top_file)
        
        # Parse instance connections
        instance_connections_file = os.path.join(config_dir, 'instance_connections.txt')
        if os.path.exists(instance_connections_file):
            config['instance_connections'] = self._parse_instance_connections(instance_connections_file)
        
        return config
    
    def _parse_top_module(self, file_path: str) -> str:
        """Parse top module name from file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('[TOP_MODULE_NAME]'):
                continue
            return line
        
        return 'top_wrapper'
    
    def _parse_instances(self, file_path: str) -> List[Dict]:
        """Parse instances from file"""
        instances = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_instances_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('[INSTANCES]'):
                in_instances_section = True
                continue
            
            if in_instances_section and '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    instance_name = parts[0]
                    module_file = parts[1]
                    parameters = {}
                    
                    if len(parts) > 2 and parts[2]:
                        # Parse parameters
                        param_str = parts[2]
                        for param in param_str.split(','):
                            if '=' in param:
                                key, value = param.split('=', 1)
                                parameters[key.strip()] = value.strip()
                    
                    instances.append({
                        'instance_name': instance_name,
                        'file': module_file,
                        'parameters': parameters,
                        'port_mapping': {}
                    })
        
        return instances
    
    def _parse_top_ports(self, file_path: str) -> List[Port]:
        """Parse top ports from file"""
        ports = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_ports_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('[TOP_PORTS]'):
                in_ports_section = True
                continue
            
            if in_ports_section and '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    direction = parts[0]
                    width = parts[1] if parts[1] else None
                    name = parts[2]
                    
                    ports.append(Port(name=name, direction=direction, width=width))
        
        return ports
    
    def _parse_instance_to_top(self, file_path: str) -> Dict[str, str]:
        """Parse instance to top mappings from file"""
        mappings = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_mapping_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('[INSTANCE_TO_TOP]'):
                in_mapping_section = True
                continue
            
            if in_mapping_section and '->' in line:
                parts = [p.strip() for p in line.split('->')]
                if len(parts) == 2:
                    instance_port = parts[0]
                    top_port = parts[1]
                    mappings[instance_port] = top_port
        
        return mappings
    
    def _parse_instance_connections(self, file_path: str) -> List[Dict]:
        """Parse instance connections from file"""
        connections = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_connections_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('[INSTANCE_CONNECTIONS]'):
                in_connections_section = True
                continue
            
            if in_connections_section and '->' in line:
                parts = [p.strip() for p in line.split('->')]
                if len(parts) == 2:
                    source = parts[0]
                    target = parts[1]
                    connections.append({
                        'source': source,
                        'target': target
                    })
        
        return connections
    
    def parse_input_spec(self, file_path: str) -> Dict:
        """Parse input specification file and return configuration"""
        config = {
            'top_module': 'top_wrapper',
            'instances': []
        }
        
        instances = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input specification file not found: {file_path}")
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
            
            # Process sections
            if current_section == 'TOP_MODULE':
                config['top_module'] = line
            
            elif current_section == 'INSTANCES':
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) == 2:
                        instance_name, file_path = parts
                        instances[instance_name] = {
                            'instance_name': instance_name,
                            'file': file_path,
                            'port_mapping': {}
                        }
            
            elif current_section == 'PORT_MAPPING':
                if '->' in line:
                    parts = [p.strip() for p in line.split('->')]
                    if len(parts) == 2:
                        left, right = parts
                        if '.' in left:
                            inst_name, port_name = left.split('.', 1)
                            inst_name = inst_name.strip()
                            port_name = port_name.strip()
                            top_port = right.strip()
                            
                            if inst_name in instances:
                                instances[inst_name]['port_mapping'][port_name] = top_port
        
        config['instances'] = list(instances.values())
        return config


class WrapperGenerator:
    """Generates Verilog wrapper files"""
    
    def __init__(self):
        self.parser = VerilogParser()
        self.config_parser = ConfigParser()
    
    def generate_wrapper_from_spec(self, spec_file: str) -> str:
        """Generate wrapper Verilog code from input specification file"""
        config = self.config_parser.parse_input_spec(spec_file)
        return self.generate_wrapper(config)
    
    def generate_wrapper_from_config(self, config_dir: str) -> str:
        """Generate wrapper Verilog code from configuration directory"""
        config = self.config_parser.parse_config_directory(config_dir)
        return self.generate_wrapper_advanced(config)
    
    def generate_wrapper_advanced(self, config: Dict) -> str:
        """Generate wrapper Verilog code from advanced configuration"""
        top_module_name = config.get('top_module', 'top_wrapper')
        instances_config = config.get('instances', [])
        top_ports = config.get('top_ports', [])
        instance_to_top_config = config.get('instance_to_top', {})
        instance_connections = config.get('instance_connections', [])
        
        # Parse all modules and create instances
        instances = []
        
        for inst_config in instances_config:
            module = self.parser.parse_module(inst_config['file'])
            instance_name = inst_config['instance_name']
            parameters = inst_config.get('parameters', {})
            
            # Build port mapping from instance_to_top
            port_mapping = {}
            for inst_port, top_port in instance_to_top_config.items():
                if inst_port.startswith(f"{instance_name}."):
                    port_name = inst_port.split('.', 1)[1]
                    port_mapping[port_name] = top_port
            
            instance = Instance(module=module, instance_name=instance_name, parameters=parameters, port_mapping=port_mapping)
            instances.append(instance)
        
        # Generate wrapper code
        wrapper_code = self._generate_wrapper_code_advanced(top_module_name, instances, top_ports, instance_connections, instance_to_top_config)
        return wrapper_code
    
    def generate_wrapper(self, config: Dict) -> str:
        """Generate wrapper Verilog code from configuration"""
        top_module_name = config.get('top_module', 'top_wrapper')
        instances_config = config.get('instances', [])
        
        # Parse all modules and create instances
        instances = []
        all_top_ports = {}  # port_name -> Port
        
        for inst_config in instances_config:
            module = self.parser.parse_module(inst_config['file'])
            instance_name = inst_config['instance_name']
            port_mapping = inst_config.get('port_mapping', {})
            
            parameters = inst_config.get('parameters', {})
            instance = Instance(module=module, instance_name=instance_name, parameters=parameters, port_mapping=port_mapping)
            instances.append(instance)
            
            # Collect top-level ports
            for port in module.ports:
                if port.name in port_mapping:
                    top_port_name = port_mapping[port.name]
                    if top_port_name not in all_top_ports:
                        all_top_ports[top_port_name] = Port(
                            name=top_port_name,
                            direction=port.direction,
                            width=port.width
                        )
        
        # Generate wrapper code
        wrapper_code = self._generate_wrapper_code(top_module_name, instances, all_top_ports)
        return wrapper_code
    
    def _extract_port_and_range(self, port_spec: str) -> Tuple[str, Optional[str]]:
        """Extract port name and bit range from port specification"""
        if '[' in port_spec and ']' in port_spec:
            # Has bit range
            port_name = port_spec.split('[')[0]
            bit_range = '[' + port_spec.split('[')[1]
            return port_name, bit_range
        else:
            return port_spec, None
    
    def _generate_wire_name(self, source_spec: str, target_spec: str) -> str:
        """Generate wire name showing source->target direction with w_ prefix"""
        # Extract port names and ranges
        source_port, source_range = self._extract_port_and_range(source_spec)
        target_port, target_range = self._extract_port_and_range(target_spec)
        
        # Clean up port names
        source_clean = source_port.replace('.', '_')
        target_clean = target_port.replace('.', '_')
        
        # Add range information if present
        range_suffix = ""
        if source_range and target_range:
            # Both have ranges - show mapping
            source_bits = source_range.replace('[', '').replace(']', '').replace(':', '_')
            target_bits = target_range.replace('[', '').replace(']', '').replace(':', '_')
            range_suffix = f"_{source_bits}_to_{target_bits}"
        elif source_range:
            # Only source has range
            source_bits = source_range.replace('[', '').replace(']', '').replace(':', '_')
            range_suffix = f"_{source_bits}"
        elif target_range:
            # Only target has range
            target_bits = target_range.replace('[', '').replace(']', '').replace(':', '_')
            range_suffix = f"_to_{target_bits}"
        
        return f"w_{source_clean}_to_{target_clean}{range_suffix}"
    
    def _generate_connection_name(self, connection_spec: str) -> str:
        """Generate connection name handling special cases and bit ranges"""
        # Handle special connections
        if connection_spec in ['TIE0', 'TIE1', 'FLOAT']:
            if connection_spec == 'TIE0':
                return "1'b0"
            elif connection_spec == 'TIE1':
                return "1'b1"
            elif connection_spec == 'FLOAT':
                return "1'bz"
        
        # Handle bit ranges
        if '[' in connection_spec and ']' in connection_spec:
            # This is a partial connection, use the full specification
            return f"w_{connection_spec.replace('.', '_')}"
        
        # Normal connection
        return f"w_{connection_spec.replace('.', '_')}"
    
    def _analyze_port_partial_connections(self, instance: Instance, port: Port, instance_to_top: Dict[str, str], instance_connections: List[Dict]) -> List[str]:
        """Analyze partial connections for a port and return unconnected bit ranges"""
        if not port.width:
            return []  # Not a multibit port
        
        # Parse port width to get bit range
        width_match = re.match(r'\[(\d+):(\d+)\]', port.width)
        if not width_match:
            return []  # Cannot parse width
        
        msb = int(width_match.group(1))
        lsb = int(width_match.group(2))
        
        # Track which bits are connected
        connected_bits = set()
        
        # Check instance-to-top connections
        inst_port_name = f"{instance.instance_name}.{port.name}"
        for mapped_port, top_port_name in instance_to_top.items():
            if mapped_port.startswith(inst_port_name):
                # Extract bit range from mapped port
                if '[' in mapped_port and ']' in mapped_port:
                    # Handle both [msb:lsb] and [bit] formats
                    range_match = re.search(r'\[(\d+):(\d+)\]', mapped_port)
                    single_bit_match = re.search(r'\[(\d+)\]', mapped_port)
                    
                    if range_match:
                        range_msb = int(range_match.group(1))
                        range_lsb = int(range_match.group(2))
                        for bit in range(range_lsb, range_msb + 1):
                            connected_bits.add(bit)
                    elif single_bit_match:
                        bit = int(single_bit_match.group(1))
                        connected_bits.add(bit)
                elif mapped_port == inst_port_name:
                    # Full port connection
                    for bit in range(lsb, msb + 1):
                        connected_bits.add(bit)
        
        # Check instance-to-instance connections
        for connection in instance_connections:
            source_port, source_range = self._extract_port_and_range(connection['source'])
            target_port, target_range = self._extract_port_and_range(connection['target'])
            
            if source_port == inst_port_name:
                if source_range:
                    # Handle both [msb:lsb] and [bit] formats
                    range_match = re.search(r'\[(\d+):(\d+)\]', source_range)
                    single_bit_match = re.search(r'\[(\d+)\]', source_range)
                    
                    if range_match:
                        range_msb = int(range_match.group(1))
                        range_lsb = int(range_match.group(2))
                        for bit in range(range_lsb, range_msb + 1):
                            connected_bits.add(bit)
                    elif single_bit_match:
                        bit = int(single_bit_match.group(1))
                        connected_bits.add(bit)
                else:
                    # Full port connection
                    for bit in range(lsb, msb + 1):
                        connected_bits.add(bit)
            elif target_port == inst_port_name:
                if target_range:
                    # Handle both [msb:lsb] and [bit] formats
                    range_match = re.search(r'\[(\d+):(\d+)\]', target_range)
                    single_bit_match = re.search(r'\[(\d+)\]', target_range)
                    
                    if range_match:
                        range_msb = int(range_match.group(1))
                        range_lsb = int(range_match.group(2))
                        for bit in range(range_lsb, range_msb + 1):
                            connected_bits.add(bit)
                    elif single_bit_match:
                        bit = int(single_bit_match.group(1))
                        connected_bits.add(bit)
                else:
                    # Full port connection
                    for bit in range(lsb, msb + 1):
                        connected_bits.add(bit)
        
        # Find unconnected bit ranges
        unconnected_ranges = []
        all_bits = set(range(lsb, msb + 1))
        unconnected_bits = sorted(all_bits - connected_bits)
        
        # Group consecutive unconnected bits into ranges
        if unconnected_bits:
            range_start = unconnected_bits[0]
            range_end = unconnected_bits[0]
            
            for bit in unconnected_bits[1:]:
                if bit == range_end + 1:
                    range_end = bit
                else:
                    # End of current range, add it
                    if range_start == range_end:
                        unconnected_ranges.append(f"[{range_start}]")
                    else:
                        unconnected_ranges.append(f"[{range_end}:{range_start}]")
                    range_start = bit
                    range_end = bit
            
            # Add final range
            if range_start == range_end:
                unconnected_ranges.append(f"[{range_start}]")
            else:
                unconnected_ranges.append(f"[{range_end}:{range_start}]")
        
        return unconnected_ranges
    
    def _generate_wrapper_code_advanced(self, top_module_name: str, instances: List[Instance], 
                                      top_ports: List[Port], instance_connections: List[Dict], instance_to_top: Dict[str, str]) -> str:
        """Generate wrapper code with advanced configuration"""
        lines = []
        
        # Initialize unconnected port tracking
        unconnected_inputs = []
        unconnected_outputs = []
        unconnected_inouts = []
        
        # Module declaration
        lines.append(f"module {top_module_name} (")
        
        # Top-level ports
        if top_ports:
            port_lines = []
            for port in top_ports:
                width_str = f" {port.width}" if port.width else ""
                port_lines.append(f"    {port.direction}{width_str} {port.name}")
            
            lines.append(",\n".join(port_lines))
        
        lines.append(");")
        lines.append("")
        
        # Generate internal wires for instance connections
        internal_wires = {}  # wire_name -> width
        top_port_names = {port.name for port in top_ports}
        
        # Collect all connection wires with their widths
        for connection in instance_connections:
            source = connection['source']
            target = connection['target']
            
            # Skip special connections
            if target in ['TIE0', 'TIE1', 'FLOAT'] or source in ['TIE0', 'TIE1', 'FLOAT']:
                continue
            
            # Generate wire name based on connection
            wire_name = self._generate_wire_name(source, target)
            
            # Find the port width from the source module
            if '.' in source:
                source_port, source_range = self._extract_port_and_range(source)
                for instance in instances:
                    if source_port.startswith(f"{instance.instance_name}."):
                        port_name = source_port.split('.', 1)[1]
                        for port in instance.module.ports:
                            if port.name == port_name:
                                # Use partial width if range specified
                                if source_range:
                                    # Calculate partial width from range
                                    internal_wires[wire_name] = source_range
                                else:
                                    internal_wires[wire_name] = port.width
                                break
                        break
        
        # Add internal wires for all ports that need wires
        for instance in instances:
            for port in instance.module.ports:
                port_is_mapped = False
                
                # Check if port is mapped to top
                for mapped_port in instance.port_mapping.keys():
                    if mapped_port.split('[')[0] == port.name:
                        port_is_mapped = True
                        break
                
                # Check if port is connected to other instances
                inst_port = f"{instance.instance_name}.{port.name}"
                for connection in instance_connections:
                    if connection['source'].split('[')[0] == inst_port or connection['target'].split('[')[0] == inst_port:
                        port_is_mapped = True
                        break
                
                # Add wire for this port
                wire_name = f"w_{instance.instance_name}_{port.name}"
                if wire_name not in top_port_names:
                    internal_wires[wire_name] = port.width
                
                # If not mapped, also add as unconnected wire
                if not port_is_mapped:
                    wire_name_unconnected = f"w_{instance.instance_name}_{port.name}_unconnected"
                    if wire_name_unconnected not in top_port_names:
                        internal_wires[wire_name_unconnected] = port.width
        
        # Generate wire declarations
        if internal_wires:
            lines.append("// Internal wires")
            for wire_name, width in sorted(internal_wires.items()):
                width_str = f" {width}" if width else ""
                lines.append(f"    wire{width_str} {wire_name};")
            lines.append("")
        
        # Generate tie connections
        tie_connections = []
        for connection in instance_connections:
            if connection['target'] in ['TIE0', 'TIE1', 'FLOAT']:
                tie_connections.append(connection)
        
        for inst_port, top_port in instance_to_top.items():
            if top_port in ['TIE0', 'TIE1', 'FLOAT']:
                tie_connections.append({'source': inst_port, 'target': top_port})
        
        # Generate tie wire assignments and partial connections
        if tie_connections:
            lines.append("// Tie connections")
            for connection in tie_connections:
                source_port, source_range = self._extract_port_and_range(connection['source'])
                
                # Generate descriptive TIE wire names
                if connection['target'] == 'TIE0':
                    wire_name = f"w_{source_port.replace('.', '_')}_tied_to_0"
                elif connection['target'] == 'TIE1':
                    wire_name = f"w_{source_port.replace('.', '_')}_tied_to_1"
                elif connection['target'] == 'FLOAT':
                    wire_name = f"w_{source_port.replace('.', '_')}_float"
                else:
                    wire_name = f"w_{source_port.replace('.', '_')}"
                
                # Handle bit range for TIE assignments
                if source_range:
                    # Extract bit width for proper assignment
                    range_match = re.search(r'\[(\d+):(\d+)\]', source_range)
                    single_bit_match = re.search(r'\[(\d+)\]', source_range)
                    
                    if range_match:
                        msb = int(range_match.group(1))
                        lsb = int(range_match.group(2))
                        width = msb - lsb + 1
                        
                        if connection['target'] == 'TIE0':
                            lines.append(f"    assign {wire_name} = {width}'b{'0' * width};")
                        elif connection['target'] == 'TIE1':
                            lines.append(f"    assign {wire_name} = {width}'b{'1' * width};")
                        elif connection['target'] == 'FLOAT':
                            lines.append(f"    assign {wire_name} = {width}'bz;")
                    elif single_bit_match:
                        if connection['target'] == 'TIE0':
                            lines.append(f"    assign {wire_name} = 1'b0;")
                        elif connection['target'] == 'TIE1':
                            lines.append(f"    assign {wire_name} = 1'b1;")
                        elif connection['target'] == 'FLOAT':
                            lines.append(f"    assign {wire_name} = 1'bz;")
                else:
                    # Single bit assignment
                    if connection['target'] == 'TIE0':
                        lines.append(f"    assign {wire_name} = 1'b0;")
                    elif connection['target'] == 'TIE1':
                        lines.append(f"    assign {wire_name} = 1'b1;")
                    elif connection['target'] == 'FLOAT':
                        lines.append(f"    assign {wire_name} = 1'bz;")
            lines.append("")
        
        # Generate partial bit connections
        partial_connections = []
        for inst_port, top_port in instance_to_top.items():
            if '[' in inst_port or '[' in top_port:
                if top_port not in ['TIE0', 'TIE1', 'FLOAT']:
                    partial_connections.append({'source': inst_port, 'target': top_port})
        
        for connection in instance_connections:
            if ('[' in connection['source'] or '[' in connection['target']) and connection['target'] not in ['TIE0', 'TIE1', 'FLOAT']:
                partial_connections.append(connection)
        
        if partial_connections:
            lines.append("// Partial bit connections")
            for connection in partial_connections:
                source_port, source_range = self._extract_port_and_range(connection['source'])
                target_port, target_range = self._extract_port_and_range(connection['target'])
                
                # For instance-to-top connections, use the target name directly
                if '.' not in connection['target']:
                    # This is a top-level port connection
                    source_wire = f"w_{source_port.replace('.', '_')}"
                    target_wire = connection['target']
                else:
                    # This is an instance-to-instance connection
                    source_wire = f"w_{source_port.replace('.', '_')}"
                    target_wire = f"w_{target_port.replace('.', '_')}"
                
                if source_range and target_range:
                    lines.append(f"    assign {target_wire}{target_range} = {source_wire}{source_range};")
                elif source_range:
                    lines.append(f"    assign {target_wire} = {source_wire}{source_range};")
                elif target_range:
                    lines.append(f"    assign {target_wire}{target_range} = {source_wire};")
            lines.append("")
        
        # Instance declarations
        for instance in instances:
            # Generate parameter string
            param_str = ""
            if instance.parameters:
                param_list = []
                for param_name, param_value in instance.parameters.items():
                    param_list.append(f".{param_name}({param_value})")
                param_str = f" #({', '.join(param_list)})"
            
            lines.append(f"    {instance.module.name}{param_str} {instance.instance_name} (")
            
            port_connections = []
            for port in instance.module.ports:
                connection_name = None
                
                # Check if connected to top port (with bit range support)
                port_matches = [key for key in instance.port_mapping.keys() if key.split('[')[0] == port.name]
                if port_matches:
                    # Handle partial connections
                    mapped_port = port_matches[0]
                    top_port_name = instance.port_mapping[mapped_port]
                    
                    # Check if it's a special connection
                    if top_port_name in ['TIE0', 'TIE1', 'FLOAT']:
                        if top_port_name == 'TIE0':
                            connection_name = f"w_{instance.instance_name}_{port.name}_tied_to_0"
                        elif top_port_name == 'TIE1':
                            connection_name = f"w_{instance.instance_name}_{port.name}_tied_to_1"
                        elif top_port_name == 'FLOAT':
                            connection_name = f"w_{instance.instance_name}_{port.name}_float"
                    else:
                        # Check if partial connection
                        if '[' in mapped_port:
                            connection_name = f"w_{instance.instance_name}_{port.name}"
                        else:
                            connection_name = top_port_name
                else:
                    # Check if connected to another instance
                    inst_port = f"{instance.instance_name}.{port.name}"
                    for connection in instance_connections:
                        source_port, source_range = self._extract_port_and_range(connection['source'])
                        target_port, target_range = self._extract_port_and_range(connection['target'])
                        
                        if source_port == inst_port:
                            if connection['target'] in ['TIE0', 'TIE1', 'FLOAT']:
                                if connection['target'] == 'TIE0':
                                    connection_name = f"w_{instance.instance_name}_{port.name}_tied_to_0"
                                elif connection['target'] == 'TIE1':
                                    connection_name = f"w_{instance.instance_name}_{port.name}_tied_to_1"
                                elif connection['target'] == 'FLOAT':
                                    connection_name = f"w_{instance.instance_name}_{port.name}_float"
                            else:
                                connection_name = self._generate_wire_name(connection['source'], connection['target'])
                            break
                        elif target_port == inst_port:
                            if connection['source'] in ['TIE0', 'TIE1', 'FLOAT']:
                                if connection['source'] == 'TIE0':
                                    connection_name = f"w_{instance.instance_name}_{port.name}_tied_to_0"
                                elif connection['source'] == 'TIE1':
                                    connection_name = f"w_{instance.instance_name}_{port.name}_tied_to_1"
                                elif connection['source'] == 'FLOAT':
                                    connection_name = f"w_{instance.instance_name}_{port.name}_float"
                            else:
                                connection_name = self._generate_wire_name(connection['source'], connection['target'])
                            break
                    
                    # If not connected, use internal wire and check for partial connections
                    if connection_name is None:
                        connection_name = f"w_{instance.instance_name}_{port.name}_unconnected"
                
                # Always analyze partial connections for multibit ports
                if port.width:
                    unconnected_ranges = self._analyze_port_partial_connections(instance, port, instance_to_top, instance_connections)
                    
                    # Add to unconnected ports list with bit range information
                    if unconnected_ranges:
                        for range_info in unconnected_ranges:
                            port_info = f"{instance.instance_name}.{port.name}{range_info}"
                            if port.direction == 'input':
                                unconnected_inputs.append(port_info)
                            elif port.direction == 'output':
                                unconnected_outputs.append(port_info)
                            elif port.direction == 'inout':
                                unconnected_inouts.append(port_info)
                elif connection_name and connection_name.endswith('_unconnected'):
                    # Fully unconnected single-bit port
                    port_info = f"{instance.instance_name}.{port.name}"
                    if port.direction == 'input':
                        unconnected_inputs.append(port_info)
                    elif port.direction == 'output':
                        unconnected_outputs.append(port_info)
                    elif port.direction == 'inout':
                        unconnected_inouts.append(port_info)
                
                port_connections.append(f"        .{port.name}({connection_name})")
            
            lines.append(",\n".join(port_connections))
            lines.append("    );")  
            lines.append("")
        
        lines.append("endmodule")
        
        # Generate unconnected ports report
        self._generate_unconnected_report(unconnected_inputs, unconnected_outputs, unconnected_inouts)
        
        return "\n".join(lines)
    
    def _generate_unconnected_report(self, unconnected_inputs: List[str], unconnected_outputs: List[str], unconnected_inouts: List[str]):
        """Generate unconnected ports report files"""
        import os
        
        # Create rpt directory if it doesn't exist
        rpt_dir = "./rpt"
        if not os.path.exists(rpt_dir):
            os.makedirs(rpt_dir)
        
        # Write unconnected input ports
        with open(os.path.join(rpt_dir, "Unconnected_input.list"), 'w') as f:
            f.write("# Unconnected Input Ports\n")
            f.write("# Format: instance_name.port_name\n")
            f.write("# Generated by Verilog Wrapper Generator\n\n")
            for port in sorted(unconnected_inputs):
                f.write(f"{port}\n")
        
        # Write unconnected output ports
        with open(os.path.join(rpt_dir, "Unconnected_output.list"), 'w') as f:
            f.write("# Unconnected Output Ports\n")
            f.write("# Format: instance_name.port_name\n")
            f.write("# Generated by Verilog Wrapper Generator\n\n")
            for port in sorted(unconnected_outputs):
                f.write(f"{port}\n")
        
        # Write unconnected inout ports
        with open(os.path.join(rpt_dir, "Unconnected_inout.list"), 'w') as f:
            f.write("# Unconnected Inout Ports\n")
            f.write("# Format: instance_name.port_name\n")
            f.write("# Generated by Verilog Wrapper Generator\n\n")
            for port in sorted(unconnected_inouts):
                f.write(f"{port}\n")
    
    def _generate_wrapper_code(self, top_module_name: str, instances: List[Instance], 
                             top_ports: Dict[str, Port]) -> str:
        """Generate the actual Verilog wrapper code"""
        lines = []
        
        # Initialize unconnected port tracking
        unconnected_inputs = []
        unconnected_outputs = []
        unconnected_inouts = []
        
        # Module declaration
        lines.append(f"module {top_module_name} (")
        
        # Top-level ports
        port_lines = []
        for port in top_ports.values():
            width_str = f" {port.width}" if port.width else ""
            port_lines.append(f"    {port.direction}{width_str} {port.name}")
        
        lines.append(",\n".join(port_lines))
        lines.append(");")
        lines.append("")
        
        # Internal wire declarations for unmapped ports
        internal_wires = set()
        for instance in instances:
            for port in instance.module.ports:
                if port.name not in instance.port_mapping:
                    wire_name = f"{instance.instance_name}_{port.name}"
                    internal_wires.add(wire_name)
        
        if internal_wires:
            lines.append("// Internal wires")
            for wire in sorted(internal_wires):
                lines.append(f"    wire {wire};")
            lines.append("")
        
        # Instance declarations
        for instance in instances:
            lines.append(f"    {instance.module.name} {instance.instance_name} (")
            
            port_connections = []
            for port in instance.module.ports:
                if port.name in instance.port_mapping:
                    # Connect to top-level port
                    top_port = instance.port_mapping[port.name]
                    port_connections.append(f"        .{port.name}({top_port})")
                else:
                    # Connect to internal wire and track unconnected ports
                    wire_name = f"{instance.instance_name}_{port.name}"
                    port_connections.append(f"        .{port.name}({wire_name})")
                    
                    # Track unconnected ports for report
                    port_info = f"{instance.instance_name}.{port.name}"
                    if port.direction == 'input':
                        unconnected_inputs.append(port_info)
                    elif port.direction == 'output':
                        unconnected_outputs.append(port_info)
                    elif port.direction == 'inout':
                        unconnected_inouts.append(port_info)
            
            lines.append(",\n".join(port_connections))
            lines.append("    );")
            lines.append("")
        
        lines.append("endmodule")
        
        # Generate unconnected ports report
        self._generate_unconnected_report(unconnected_inputs, unconnected_outputs, unconnected_inouts)
        
        return "\n".join(lines)


def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(description='Generate Verilog wrapper files')
    parser.add_argument('input_file', help='Input specification file (.txt) or JSON configuration file')
    parser.add_argument('-o', '--output', help='Output file path')
    
    args = parser.parse_args()
    
    # Generate wrapper
    try:
        generator = WrapperGenerator()
        
        # Check if input is a directory (config files) or file
        if os.path.isdir(args.input_file):
            # Configuration directory
            wrapper_code = generator.generate_wrapper_from_config(args.input_file)
        elif args.input_file.endswith('.txt'):
            # Input specification file
            wrapper_code = generator.generate_wrapper_from_spec(args.input_file)
        else:
            # JSON configuration file
            try:
                with open(args.input_file, 'r') as f:
                    config = json.load(f)
                wrapper_code = generator.generate_wrapper(config)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in configuration file: {e}")
                return 1
        
        # Output result
        if args.output:
            with open(args.output, 'w') as f:
                f.write(wrapper_code)
            print(f"Wrapper generated: {args.output}")
        else:
            print(wrapper_code)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())