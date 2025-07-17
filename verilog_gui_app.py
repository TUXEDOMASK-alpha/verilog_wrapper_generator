#!/usr/bin/env python3
"""
Verilog Wrapper Generator Web GUI
Flask-based web interface for creating and managing configuration files
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from verilog_wrapper_generator import WrapperGenerator, ConfigParser
from typing import Dict, List

app = Flask(__name__)

# Global variables
config_dir = "./config"
generator = WrapperGenerator()
config_parser = ConfigParser()

def ensure_config_dir():
    """Ensure config directory exists"""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

@app.route('/')
def index():
    """Main GUI page"""
    return render_template('index.html')

@app.route('/api/config/load')
def load_config():
    """Load all configuration files"""
    try:
        ensure_config_dir()
        
        # Read all config files
        config_files = {
            'top_module': read_config_file('01_top_module.cmd'),
            'instances': read_config_file('02_instances.cmd'),
            'top_ports': read_config_file('03_top_ports.cmd'),
            'instance_to_top': read_config_file('04_instance_to_top.cmd'),
            'instance_connections': read_config_file('05_instance_connections.cmd'),
            'instance_export_ports': read_config_file('06_instance_export_port.cmd')
        }
        
        return jsonify({
            'success': True,
            'config': config_files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/config/save', methods=['POST'])
def save_config():
    """Save configuration files"""
    try:
        ensure_config_dir()
        data = request.json
        
        # Save each config file
        file_mapping = {
            'top_module': '01_top_module.cmd',
            'instances': '02_instances.cmd',
            'top_ports': '03_top_ports.cmd',
            'instance_to_top': '04_instance_to_top.cmd',
            'instance_connections': '05_instance_connections.cmd',
            'instance_export_ports': '06_instance_export_port.cmd'
        }
        
        for config_type, filename in file_mapping.items():
            if config_type in data:
                write_config_file(filename, data[config_type])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/wrapper/generate', methods=['POST'])
def generate_wrapper():
    """Generate wrapper code from configuration"""
    try:
        data = request.json
        
        # Save config temporarily for generation
        temp_config_dir = "./temp_config"
        if not os.path.exists(temp_config_dir):
            os.makedirs(temp_config_dir)
        
        file_mapping = {
            'top_module': '01_top_module.cmd',
            'instances': '02_instances.cmd',
            'top_ports': '03_top_ports.cmd',
            'instance_to_top': '04_instance_to_top.cmd',
            'instance_connections': '05_instance_connections.cmd',
            'instance_export_ports': '06_instance_export_port.cmd'
        }
        
        for config_type, filename in file_mapping.items():
            if config_type in data:
                filepath = os.path.join(temp_config_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(data[config_type])
        
        # Generate wrapper
        wrapper_code = generator.generate_wrapper_from_config(temp_config_dir)
        
        # Read error report if exists
        error_report = ""
        error_file = os.path.join("./rpt", "Error_report.list")
        if os.path.exists(error_file):
            with open(error_file, 'r', encoding='utf-8') as f:
                error_report = f.read()
        
        # Cleanup temp directory
        import shutil
        if os.path.exists(temp_config_dir):
            shutil.rmtree(temp_config_dir)
        
        return jsonify({
            'success': True,
            'wrapper_code': wrapper_code,
            'error_report': error_report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/validate', methods=['POST'])
def validate_config():
    """Validate configuration without generating wrapper"""
    try:
        data = request.json
        
        # Basic validation logic
        errors = []
        warnings = []
        
        # Validate top module
        if 'top_module' in data:
            top_module_content = data['top_module']
            if '[TOP_MODULE_NAME]' not in top_module_content:
                errors.append("Top module name section missing")
        
        # Validate instances
        if 'instances' in data:
            instances_content = data['instances']
            if '[INSTANCES]' not in instances_content:
                errors.append("Instances section missing")
        
        return jsonify({
            'success': True,
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def read_config_file(filename):
    """Read a config file, return empty template if not exists"""
    filepath = os.path.join(config_dir, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Return default templates
        return get_default_template(filename)

def write_config_file(filename, content):
    """Write content to a config file"""
    filepath = os.path.join(config_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def get_default_template(filename):
    """Get default template for config files"""
    templates = {
        '01_top_module.cmd': """# Top Module Configuration
# 생성할 탑 모듈의 이름과 파라미터를 지정합니다.

[TOP_MODULE_NAME]
top_wrapper

[TOP_MODULE_PARAMETERS]
# 형식: PARAM_NAME = PARAM_VALUE
# DATA_WIDTH = 32
# ADDR_WIDTH = 16
""",
        '02_instances.cmd': """# Instance Configuration
# 인스턴스화할 모듈과 그 모듈의 이름 및 파라미터를 지정합니다.
# 형식: 인스턴스명 | 모듈파일경로 | [모듈명] | [파라미터]

[INSTANCES]
# 예시:
# cpu_core | cpu.v | DATA_WIDTH=32,ADDR_WIDTH=16
# memory_ctrl | memory.v | memory_controller | MEM_SIZE=65536
""",
        '03_top_ports.cmd': """# Top Module Port Configuration
# 생성할 탑 모듈의 포트를 지정합니다.
# 형식: 방향 | 포트폭 | 포트명

[TOP_PORTS]
# 예시:
# input | | clk
# input | | reset
# input | [7:0] | data_in
# output | [7:0] | data_out
""",
        '04_instance_to_top.cmd': """# Instance to Top Port Mapping
# 인스턴스의 포트를 탑 모듈의 포트로 연결합니다.
# 형식: 인스턴스명.포트명 -> 탑포트명

[INSTANCE_TO_TOP]
# 예시:
# cpu_core.clk -> clk
# cpu_core.reset -> reset
# cpu_core.data_out -> data_out
""",
        '05_instance_connections.cmd': """# Instance to Instance Connections
# 인스턴스들 간의 연결을 지정합니다.
# 형식: 인스턴스명.포트명 -> 인스턴스명.포트명

[INSTANCE_CONNECTIONS]
# 예시:
# cpu_core.data_out -> memory.data_in
# memory.data_out -> cpu_core.data_in
""",
        '06_instance_export_port.cmd': """# Instance Port Export Configuration
# 인스턴스의 포트를 직접 탑 모듈 포트로 노출시킵니다.
# 형식: 인스턴스명.포트명 [-> 새로운포트명]

[INSTANCE_EXPORT_PORTS]
# 예시:
# cpu_core.debug_signal -> cpu_debug
# uart_if.status
"""
    }
    
    return templates.get(filename, f"# Configuration file: {filename}\n")

if __name__ == '__main__':
    print("Starting Verilog Wrapper Generator Web GUI...")
    print("Open your browser and go to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)