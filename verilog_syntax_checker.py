#!/usr/bin/env python3
"""
Simple Verilog syntax checker for basic validation
"""

import re
import sys
from typing import List, Dict, Tuple


class VerilogSyntaxChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def check_file(self, file_path: str) -> bool:
        """Check Verilog file for basic syntax errors"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False
        
        # Remove comments
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Check basic syntax
        self._check_module_structure(content)
        self._check_port_declarations(content)
        self._check_wire_declarations(content)
        self._check_instance_declarations(content)
        self._check_assign_statements(content)
        self._check_parentheses_balance(content)
        self._check_semicolons(content)
        
        return len(self.errors) == 0
    
    def _check_module_structure(self, content: str):
        """Check module declaration and endmodule"""
        module_matches = re.findall(r'module\s+(\w+)', content)
        endmodule_matches = re.findall(r'endmodule', content)
        
        if len(module_matches) == 0:
            self.errors.append("No module declaration found")
        elif len(module_matches) > 1:
            self.errors.append("Multiple module declarations found")
        
        if len(endmodule_matches) == 0:
            self.errors.append("No endmodule found")
        elif len(endmodule_matches) > 1:
            self.errors.append("Multiple endmodule statements found")
        
        if len(module_matches) != len(endmodule_matches):
            self.errors.append("Mismatched module/endmodule count")
    
    def _check_port_declarations(self, content: str):
        """Check port declarations in module header"""
        # Find module port list
        module_pattern = r'module\s+\w+\s*\((.*?)\);'
        module_match = re.search(module_pattern, content, re.DOTALL)
        
        if module_match:
            port_list = module_match.group(1).strip()
            if port_list:
                # Check for proper port declarations
                port_lines = [line.strip() for line in port_list.split(',') if line.strip()]
                for i, port_line in enumerate(port_lines):
                    if not re.match(r'(input|output|inout)\s+', port_line):
                        self.errors.append(f"Invalid port declaration at line {i+1}: {port_line}")
    
    def _check_wire_declarations(self, content: str):
        """Check wire declarations"""
        wire_pattern = r'wire\s*(\[.*?\])?\s*(\w+(?:\s*,\s*\w+)*)\s*;'
        wire_matches = re.findall(wire_pattern, content)
        
        # Check for proper wire syntax
        for width, names in wire_matches:
            if width:
                # Check bit range syntax
                if not re.match(r'\[\d+:\d+\]', width):
                    self.warnings.append(f"Unusual bit range format: {width}")
    
    def _check_instance_declarations(self, content: str):
        """Check module instance declarations"""
        # Remove module port list to avoid false positives
        content_no_module = re.sub(r'module\s+\w+\s*\(.*?\);', '', content, flags=re.DOTALL)
        
        # Find instance declarations (skip module declarations)
        instance_pattern = r'(\w+)\s*(#\(.*?\))?\s*(\w+)\s*\((.*?)\);'
        instance_matches = re.findall(instance_pattern, content_no_module, re.DOTALL)
        
        for module_name, params, inst_name, port_connections in instance_matches:
            # Skip built-in statements and declarations
            if module_name in ['wire', 'reg', 'assign', 'always', 'initial', 'input', 'output', 'inout']:
                continue
            
            # Skip if this looks like a module declaration
            if inst_name in ['input', 'output', 'inout'] or '(' in inst_name:
                continue
                
            # Check port connections
            if port_connections.strip():
                connections = [conn.strip() for conn in port_connections.split(',') if conn.strip()]
                for conn in connections:
                    if not re.match(r'\.\w+\(.*?\)', conn):
                        self.errors.append(f"Invalid port connection in {inst_name}: {conn}")
    
    def _check_assign_statements(self, content: str):
        """Check assign statements"""
        assign_pattern = r'assign\s+([^;]+);'
        assign_matches = re.findall(assign_pattern, content)
        
        for assign_stmt in assign_matches:
            if '=' not in assign_stmt:
                self.errors.append(f"Invalid assign statement: assign {assign_stmt}")
    
    def _check_parentheses_balance(self, content: str):
        """Check balanced parentheses"""
        paren_count = 0
        brace_count = 0
        bracket_count = 0
        
        for char in content:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            elif char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
        
        if paren_count != 0:
            self.errors.append(f"Unbalanced parentheses: {paren_count}")
        if brace_count != 0:
            self.errors.append(f"Unbalanced braces: {brace_count}")
        if bracket_count != 0:
            self.errors.append(f"Unbalanced brackets: {bracket_count}")
    
    def _check_semicolons(self, content: str):
        """Check for common semicolon issues"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('//'):
                # Check for missing semicolons on certain statements
                if (line.startswith('assign') and not line.endswith(';') and 
                    not line.endswith(',') and not line.endswith('(')):
                    self.warnings.append(f"Line {i+1}: assign statement might be missing semicolon")
                
                if (line.startswith('wire') and not line.endswith(';') and 
                    not line.endswith(',') and not line.endswith('(')):
                    self.warnings.append(f"Line {i+1}: wire declaration might be missing semicolon")
    
    def print_results(self):
        """Print check results"""
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ No syntax errors found!")
        
        return len(self.errors) == 0


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verilog_syntax_checker.py <verilog_file>")
        return 1
    
    checker = VerilogSyntaxChecker()
    result = checker.check_file(sys.argv[1])
    checker.print_results()
    
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())