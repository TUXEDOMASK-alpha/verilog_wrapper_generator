#!/usr/bin/env python3
"""
Verilog Wrapper Generator Web GUI
A web-based user interface for generating Verilog wrapper files.
Uses only Python standard library - no additional pip installations required.
"""

import http.server
import socketserver
import urllib.parse
import json
import os
import tempfile
import shutil
import webbrowser
import threading
import time
from verilog_wrapper_generator import WrapperGenerator

class VerilogWrapperWebHandler(http.server.SimpleHTTPRequestHandler):
    """Web handler for Verilog Wrapper Generator"""
    
    def __init__(self, *args, **kwargs):
        # Initialize session data
        self.session_data = {
            'current_step': 0,
            'config_data': {
                'top_module': '',
                'instances': [],
                'top_ports': [],
                'instance_to_top': [],
                'instance_connections': []
            }
        }
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve the main HTML page"""
        html_content = self.get_html_content()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_api_get(self):
        """Handle API GET requests"""
        if self.path == '/api/status':
            self.send_json_response(self.session_data)
        else:
            self.send_error(404)
    
    def handle_api_post(self):
        """Handle API POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/update_step':
                self.session_data['current_step'] = data.get('step', 0)
                self.session_data['config_data'].update(data.get('config_data', {}))
                self.send_json_response({'status': 'success'})
            
            elif self.path == '/api/generate':
                result = self.generate_verilog(data.get('config_data', {}))
                self.send_json_response(result)
            
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_json_response({'status': 'error', 'message': str(e)})
    
    def send_json_response(self, data):
        """Send JSON response"""
        json_data = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(json_data)))
        self.end_headers()
        self.wfile.write(json_data.encode())
    
    def generate_verilog(self, config_data):
        """Generate Verilog wrapper file"""
        try:
            # Create temporary config directory
            temp_dir = tempfile.mkdtemp()
            config_dir = os.path.join(temp_dir, 'config')
            os.makedirs(config_dir)
            
            # Write config files
            self.write_config_files(config_dir, config_data)
            
            # Generate wrapper
            generator = WrapperGenerator()
            wrapper_code = generator.generate_wrapper_from_config(config_dir)
            
            # Read report files
            reports = self.read_reports()
            
            # Cleanup
            shutil.rmtree(temp_dir)
            
            return {
                'status': 'success',
                'verilog_code': wrapper_code,
                'reports': reports
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def write_config_files(self, config_dir, config_data):
        """Write configuration files"""
        # Top module
        with open(os.path.join(config_dir, 'top_module.txt'), 'w') as f:
            f.write(config_data.get('top_module', ''))
            
        # Instances
        with open(os.path.join(config_dir, 'instances.txt'), 'w') as f:
            f.write("# Instances\n\n[INSTANCES]\n")
            for instance in config_data.get('instances', []):
                if instance.strip():
                    f.write(f"{instance}\n")
                    
        # Top ports
        with open(os.path.join(config_dir, 'top_ports.txt'), 'w') as f:
            f.write("# Top Ports\n\n[TOP_PORTS]\n")
            for port in config_data.get('top_ports', []):
                if port.strip():
                    f.write(f"{port}\n")
                    
        # Instance to top mapping
        with open(os.path.join(config_dir, 'instance_to_top.txt'), 'w') as f:
            f.write("# Instance to Top Mapping\n\n[INSTANCE_TO_TOP]\n")
            for mapping in config_data.get('instance_to_top', []):
                if mapping.strip():
                    f.write(f"{mapping}\n")
                    
        # Instance connections
        with open(os.path.join(config_dir, 'instance_connections.txt'), 'w') as f:
            f.write("# Instance Connections\n\n[INSTANCE_CONNECTIONS]\n")
            for connection in config_data.get('instance_connections', []):
                if connection.strip():
                    f.write(f"{connection}\n")
    
    def read_reports(self):
        """Read report files if they exist"""
        reports = {}
        report_dir = './rpt'
        
        if os.path.exists(report_dir):
            for report_file in ['Unconnected_input.list', 'Unconnected_output.list', 'Unconnected_inout.list']:
                file_path = os.path.join(report_dir, report_file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        reports[report_file] = f.read()
        
        return reports
    
    def get_html_content(self):
        """Generate HTML content for the main page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verilog Wrapper Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .progress-section {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            transition: width 0.3s ease;
        }
        
        .step-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .content {
            padding: 30px;
        }
        
        .step-container {
            display: none;
        }
        
        .step-container.active {
            display: block;
        }
        
        .step-title {
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus, .form-group textarea:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .form-group textarea {
            height: 200px;
            resize: vertical;
            font-family: 'Courier New', monospace;
        }
        
        .help-text {
            margin-top: 10px;
            padding: 15px;
            background: #e8f4f8;
            border-left: 4px solid #3498db;
            border-radius: 5px;
            font-size: 14px;
            color: #2c3e50;
        }
        
        .example-text {
            margin-top: 10px;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #6c757d;
            border-radius: 5px;
            font-size: 14px;
            color: #6c757d;
            font-family: 'Courier New', monospace;
            white-space: pre-line;
        }
        
        .navigation {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }
        
        .nav-button {
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .nav-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .nav-button.prev {
            background: #6c757d;
            color: white;
        }
        
        .nav-button.prev:hover:not(:disabled) {
            background: #5a6268;
        }
        
        .nav-button.next {
            background: #007bff;
            color: white;
        }
        
        .nav-button.next:hover:not(:disabled) {
            background: #0056b3;
        }
        
        .nav-button.generate {
            background: #28a745;
            color: white;
        }
        
        .nav-button.generate:hover:not(:disabled) {
            background: #218838;
        }
        
        .result-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #e9ecef;
        }
        
        .result-title {
            font-size: 1.5em;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .result-content {
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .download-button {
            margin-top: 15px;
            padding: 10px 20px;
            background: #17a2b8;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s ease;
        }
        
        .download-button:hover {
            background: #138496;
        }
        
        .error-message {
            color: #dc3545;
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }
        
        .success-message {
            color: #155724;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #6c757d;
        }
        
        .loading::after {
            content: "...";
            animation: dots 1.5s steps(3, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: "."; }
            40% { content: ".."; }
            60% { content: "..."; }
            80%, 100% { content: ""; }
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid #e9ecef;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 14px;
            color: #6c757d;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            color: #007bff;
            border-bottom-color: #007bff;
        }
        
        .tab:hover {
            color: #0056b3;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Verilog Wrapper Generator</h1>
            <p>Create Verilog wrapper files with ease</p>
        </div>
        
        <div class="progress-section">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="step-info">
                <span id="stepText">Step 1/6: Top Module Configuration</span>
                <span id="progressText">0%</span>
            </div>
        </div>
        
        <div class="content">
            <!-- Step 1: Top Module Configuration -->
            <div class="step-container active" id="step0">
                <div class="step-title">🏗️ Top Module Configuration</div>
                <div class="form-group">
                    <label for="topModule">Top Module Name:</label>
                    <input type="text" id="topModule" placeholder="e.g., cpu_system_wrapper">
                </div>
                <div class="help-text">
                    <strong>Instructions:</strong><br>
                    Enter the name for your top-level wrapper module. This will be the module name in the generated Verilog file.
                </div>
                <div class="example-text">Examples:
• cpu_system_wrapper
• top_level_module
• main_wrapper</div>
            </div>
            
            <!-- Step 2: Instance Definition -->
            <div class="step-container" id="step1">
                <div class="step-title">📦 Instance Definition</div>
                <div class="form-group">
                    <label for="instances">Instance Definitions:</label>
                    <textarea id="instances" placeholder="instance_name | verilog_file.v | param1=value1,param2=value2"></textarea>
                </div>
                <div class="help-text">
                    <strong>Format:</strong> instance_name | verilog_file.v | param1=value1,param2=value2<br>
                    Parameters are optional. Each instance should be on a separate line.
                </div>
                <div class="example-text">cpu_inst | cpu.v | DATA_WIDTH=32,ADDR_WIDTH=16
memory_inst | memory.v
uart_inst | uart.v | BAUD_RATE=115200</div>
            </div>
            
            <!-- Step 3: Top Port Definition -->
            <div class="step-container" id="step2">
                <div class="step-title">🔌 Top Port Definition</div>
                <div class="form-group">
                    <label for="topPorts">Top-Level Ports:</label>
                    <textarea id="topPorts" placeholder="direction [width] port_name"></textarea>
                </div>
                <div class="help-text">
                    <strong>Format:</strong> direction [width] port_name<br>
                    Supported directions: input, output, inout. Width is optional for single-bit signals.
                </div>
                <div class="example-text">input sys_clk
input sys_reset
input [7:0] data_in
output [15:0] data_out
output ready
inout [7:0] bidir_port</div>
            </div>
            
            <!-- Step 4: Instance-to-Top Mapping -->
            <div class="step-container" id="step3">
                <div class="step-title">🔗 Instance-to-Top Mapping</div>
                <div class="form-group">
                    <label for="instanceToTop">Instance to Top Port Mapping:</label>
                    <textarea id="instanceToTop" placeholder="instance.port[range] -> top_port[range]"></textarea>
                </div>
                <div class="help-text">
                    <strong>Format:</strong> instance.port[range] -> top_port[range]<br>
                    Special connections: TIE0, TIE1, FLOAT. Bit ranges are optional.
                </div>
                <div class="example-text">cpu_inst.clk -> sys_clk
cpu_inst.reset -> sys_reset
cpu_inst.data_in -> data_in
cpu_inst.data_out[15:8] -> data_out[15:8]
cpu_inst.enable -> TIE1
memory_inst.cs -> TIE0
uart_inst.bidir -> FLOAT</div>
            </div>
            
            <!-- Step 5: Instance Connections -->
            <div class="step-container" id="step4">
                <div class="step-title">🔄 Instance Connections</div>
                <div class="form-group">
                    <label for="instanceConnections">Instance-to-Instance Connections:</label>
                    <textarea id="instanceConnections" placeholder="source_instance.port[range] -> target_instance.port[range]"></textarea>
                </div>
                <div class="help-text">
                    <strong>Format:</strong> source_instance.port[range] -> target_instance.port[range]<br>
                    Connect ports between different instances. Bit ranges are optional.
                </div>
                <div class="example-text">cpu_inst.data_out -> memory_inst.data_in
cpu_inst.addr -> memory_inst.addr
memory_inst.ready -> cpu_inst.mem_ready
cpu_inst.uart_tx -> uart_inst.tx_data
cpu_inst.status[3:0] -> uart_inst.data_in[7:4]</div>
            </div>
            
            <!-- Step 6: Generate & Review -->
            <div class="step-container" id="step5">
                <div class="step-title">⚡ Generate & Review</div>
                <div class="form-group">
                    <label>Configuration Summary:</label>
                    <div id="configSummary" class="result-content"></div>
                </div>
                
                <div id="generationResult" class="result-section" style="display: none;">
                    <div class="tabs">
                        <button class="tab active" onclick="showTab('verilog')">Generated Verilog</button>
                        <button class="tab" onclick="showTab('reports')">Unconnected Ports</button>
                    </div>
                    
                    <div id="verilogTab" class="tab-content active">
                        <div class="result-title">Generated Verilog Code</div>
                        <div id="verilogCode" class="result-content"></div>
                        <button class="download-button" onclick="downloadVerilog()">Download Verilog File</button>
                    </div>
                    
                    <div id="reportsTab" class="tab-content">
                        <div class="result-title">Unconnected Ports Report</div>
                        <div id="reportsContent" class="result-content"></div>
                        <button class="download-button" onclick="downloadReports()">Download Reports</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="navigation">
            <button class="nav-button prev" id="prevBtn" onclick="prevStep()" disabled>← Previous</button>
            <button class="nav-button next" id="nextBtn" onclick="nextStep()">Next →</button>
        </div>
    </div>

    <script>
        // Application state
        let currentStep = 0;
        let configData = {
            top_module: '',
            instances: [],
            top_ports: [],
            instance_to_top: [],
            instance_connections: []
        };
        
        const steps = [
            "Top Module Configuration",
            "Instance Definition",
            "Top Port Definition", 
            "Instance-to-Top Mapping",
            "Instance Connections",
            "Generate & Review"
        ];
        
        let generatedVerilog = '';
        let generatedReports = {};
        
        // Initialize the application
        function init() {
            updateProgress();
            loadConfigData();
        }
        
        // Update progress bar and step info
        function updateProgress() {
            const progress = ((currentStep + 1) / steps.length) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('stepText').textContent = `Step ${currentStep + 1}/${steps.length}: ${steps[currentStep]}`;
            document.getElementById('progressText').textContent = Math.round(progress) + '%';
            
            // Update button states
            document.getElementById('prevBtn').disabled = currentStep === 0;
            const nextBtn = document.getElementById('nextBtn');
            nextBtn.textContent = currentStep === steps.length - 1 ? 'Generate' : 'Next →';
            nextBtn.className = currentStep === steps.length - 1 ? 'nav-button generate' : 'nav-button next';
        }
        
        // Show specific step
        function showStep(step) {
            // Hide all steps
            document.querySelectorAll('.step-container').forEach(container => {
                container.classList.remove('active');
            });
            
            // Show current step
            document.getElementById(`step${step}`).classList.add('active');
            
            // Load step-specific data
            if (step === 5) {
                generateConfigSummary();
            }
        }
        
        // Load configuration data into UI
        function loadConfigData() {
            document.getElementById('topModule').value = configData.top_module;
            document.getElementById('instances').value = configData.instances.join('\\n');
            document.getElementById('topPorts').value = configData.top_ports.join('\\n');
            document.getElementById('instanceToTop').value = configData.instance_to_top.join('\\n');
            document.getElementById('instanceConnections').value = configData.instance_connections.join('\\n');
        }
        
        // Save current step data
        function saveCurrentStepData() {
            switch(currentStep) {
                case 0:
                    configData.top_module = document.getElementById('topModule').value.trim();
                    break;
                case 1:
                    configData.instances = document.getElementById('instances').value.split('\\n').filter(line => line.trim());
                    break;
                case 2:
                    configData.top_ports = document.getElementById('topPorts').value.split('\\n').filter(line => line.trim());
                    break;
                case 3:
                    configData.instance_to_top = document.getElementById('instanceToTop').value.split('\\n').filter(line => line.trim());
                    break;
                case 4:
                    configData.instance_connections = document.getElementById('instanceConnections').value.split('\\n').filter(line => line.trim());
                    break;
            }
        }
        
        // Validate current step
        function validateCurrentStep() {
            switch(currentStep) {
                case 0:
                    if (!document.getElementById('topModule').value.trim()) {
                        alert('Top module name is required!');
                        return false;
                    }
                    break;
                case 1:
                    if (!document.getElementById('instances').value.trim()) {
                        alert('At least one instance is required!');
                        return false;
                    }
                    break;
                case 2:
                    if (!document.getElementById('topPorts').value.trim()) {
                        alert('At least one top port is required!');
                        return false;
                    }
                    break;
            }
            return true;
        }
        
        // Generate configuration summary
        function generateConfigSummary() {
            const summary = `Configuration Summary:

Top Module: ${configData.top_module}

Instances (${configData.instances.length}):
${configData.instances.map((inst, i) => `  ${i+1}. ${inst}`).join('\\n')}

Top Ports (${configData.top_ports.length}):
${configData.top_ports.map((port, i) => `  ${i+1}. ${port}`).join('\\n')}

Instance-to-Top Mappings (${configData.instance_to_top.length}):
${configData.instance_to_top.map((mapping, i) => `  ${i+1}. ${mapping}`).join('\\n')}

Instance Connections (${configData.instance_connections.length}):
${configData.instance_connections.map((conn, i) => `  ${i+1}. ${conn}`).join('\\n')}`;
            
            document.getElementById('configSummary').textContent = summary;
        }
        
        // Navigation functions
        function prevStep() {
            if (currentStep > 0) {
                saveCurrentStepData();
                currentStep--;
                showStep(currentStep);
                updateProgress();
            }
        }
        
        function nextStep() {
            if (currentStep < steps.length - 1) {
                if (validateCurrentStep()) {
                    saveCurrentStepData();
                    currentStep++;
                    showStep(currentStep);
                    updateProgress();
                }
            } else {
                // Generate Verilog
                generateVerilog();
            }
        }
        
        // Generate Verilog wrapper
        function generateVerilog() {
            saveCurrentStepData();
            
            // Show loading
            const resultDiv = document.getElementById('generationResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<div class="loading">Generating Verilog wrapper</div>';
            
            // Send generation request
            fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    config_data: configData
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    generatedVerilog = data.verilog_code;
                    generatedReports = data.reports;
                    showGenerationResult();
                } else {
                    showError(data.message);
                }
            })
            .catch(error => {
                showError('Network error: ' + error.message);
            });
        }
        
        // Show generation result
        function showGenerationResult() {
            const resultDiv = document.getElementById('generationResult');
            resultDiv.innerHTML = `
                <div class="tabs">
                    <button class="tab active" onclick="showTab('verilog')">Generated Verilog</button>
                    <button class="tab" onclick="showTab('reports')">Unconnected Ports</button>
                </div>
                
                <div id="verilogTab" class="tab-content active">
                    <div class="result-title">Generated Verilog Code</div>
                    <div id="verilogCode" class="result-content"></div>
                    <button class="download-button" onclick="downloadVerilog()">Download Verilog File</button>
                </div>
                
                <div id="reportsTab" class="tab-content">
                    <div class="result-title">Unconnected Ports Report</div>
                    <div id="reportsContent" class="result-content"></div>
                    <button class="download-button" onclick="downloadReports()">Download Reports</button>
                </div>
            `;
            
            document.getElementById('verilogCode').textContent = generatedVerilog;
            
            // Format reports
            let reportsText = '';
            for (const [filename, content] of Object.entries(generatedReports)) {
                reportsText += `=== ${filename} ===\\n${content}\\n\\n`;
            }
            document.getElementById('reportsContent').textContent = reportsText || 'No unconnected ports found.';
            
            // Show success message
            const successDiv = document.createElement('div');
            successDiv.className = 'success-message';
            successDiv.textContent = 'Verilog wrapper generated successfully!';
            resultDiv.appendChild(successDiv);
        }
        
        // Show error message
        function showError(message) {
            const resultDiv = document.getElementById('generationResult');
            resultDiv.innerHTML = `<div class="error-message">Error: ${message}</div>`;
            resultDiv.style.display = 'block';
        }
        
        // Tab switching
        function showTab(tabName) {
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabName + 'Tab').classList.add('active');
        }
        
        // Download functions
        function downloadVerilog() {
            const blob = new Blob([generatedVerilog], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${configData.top_module || 'wrapper'}.v`;
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function downloadReports() {
            let reportsText = '';
            for (const [filename, content] of Object.entries(generatedReports)) {
                reportsText += `=== ${filename} ===\\n${content}\\n\\n`;
            }
            
            const blob = new Blob([reportsText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'unconnected_ports_report.txt';
            a.click();
            URL.revokeObjectURL(url);
        }
        
        // Initialize when page loads
        window.onload = init;
    </script>
</body>
</html>
        """

def main():
    """Main function to start the web server"""
    PORT = 8000
    
    # Create custom handler with session management
    handler = VerilogWrapperWebHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"🚀 Verilog Wrapper Generator Web UI started!")
            print(f"📱 Open your web browser and go to: http://localhost:{PORT}")
            print(f"🌐 Server running on port {PORT}")
            print(f"🛑 Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            def open_browser():
                time.sleep(1)  # Wait for server to start
                try:
                    webbrowser.open(f'http://localhost:{PORT}')
                except:
                    pass
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print(f"💡 Try using a different port or check if port {PORT} is already in use")

if __name__ == "__main__":
    main()