#!/usr/bin/env python3
"""
Simple Verilog Wrapper Generator Web GUI
A working web-based interface for generating Verilog wrapper files.
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

# Global session data (for simplicity in this test version)
session_data = {
    'current_step': 0,
    'config_data': {
        'top_module': '',
        'instances': [],
        'top_ports': [],
        'instance_to_top': [],
        'instance_connections': []
    }
}

class VerilogWrapperWebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        html_content = self.get_html_content()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_api_get(self):
        if self.path == '/api/status':
            self.send_json_response(session_data)
        else:
            self.send_error(404)
    
    def handle_api_post(self):
        global session_data
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/update_step':
                session_data['current_step'] = data.get('step', 0)
                if 'config_data' in data:
                    session_data['config_data'].update(data['config_data'])
                self.send_json_response({'status': 'success'})
            
            elif self.path == '/api/generate':
                result = self.generate_verilog(data.get('config_data', {}))
                self.send_json_response(result)
            
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_json_response({'status': 'error', 'message': str(e)})
    
    def send_json_response(self, data):
        json_data = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(json_data)))
        self.end_headers()
        self.wfile.write(json_data.encode())
    
    def generate_verilog(self, config_data):
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
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verilog Wrapper Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .header { text-align: center; margin-bottom: 30px; }
        .step-indicator { margin-bottom: 20px; padding: 10px; background: #e9ecef; border-radius: 5px; }
        .step-content { margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        textarea { height: 150px; font-family: monospace; }
        .navigation { display: flex; justify-content: space-between; margin-top: 20px; }
        button { padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .prev-btn { background: #6c757d; color: white; }
        .next-btn { background: #007bff; color: white; }
        .generate-btn { background: #28a745; color: white; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .help-text { font-size: 14px; color: #666; margin-top: 5px; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .code { background: #f8f8f8; padding: 10px; border-radius: 4px; overflow-x: auto; font-family: monospace; }
        .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Verilog Wrapper Generator</h1>
            <p>Create Verilog wrapper files with ease</p>
        </div>
        
        <div class="step-indicator">
            <div>Step <span id="currentStep">1</span> of 6: <span id="stepName">Top Module Configuration</span></div>
            <div style="margin-top: 5px; background: #ddd; height: 10px; border-radius: 5px;">
                <div id="progressBar" style="background: #007bff; height: 100%; border-radius: 5px; width: 16.67%;"></div>
            </div>
        </div>
        
        <div class="step-content">
            <!-- Step 1: Top Module -->
            <div id="step1" class="step">
                <h3>🏗️ Top Module Configuration</h3>
                <div class="form-group">
                    <label for="topModule">Top Module Name:</label>
                    <input type="text" id="topModule" placeholder="e.g., cpu_system_wrapper">
                    <div class="help-text">Enter the name for your top-level wrapper module</div>
                </div>
            </div>
            
            <!-- Step 2: Instances -->
            <div id="step2" class="step hidden">
                <h3>📦 Instance Definition</h3>
                <div class="form-group">
                    <label for="instances">Instance Definitions:</label>
                    <textarea id="instances" placeholder="instance_name | verilog_file.v | param1=value1,param2=value2"></textarea>
                    <div class="help-text">Format: instance_name | verilog_file.v | param1=value1,param2=value2 (one per line)</div>
                </div>
            </div>
            
            <!-- Step 3: Top Ports -->
            <div id="step3" class="step hidden">
                <h3>🔌 Top Port Definition</h3>
                <div class="form-group">
                    <label for="topPorts">Top-Level Ports:</label>
                    <textarea id="topPorts" placeholder="direction [width] port_name"></textarea>
                    <div class="help-text">Format: direction [width] port_name (e.g., input [7:0] data_in)</div>
                </div>
            </div>
            
            <!-- Step 4: Instance to Top Mapping -->
            <div id="step4" class="step hidden">
                <h3>🔗 Instance-to-Top Mapping</h3>
                <div class="form-group">
                    <label for="instanceToTop">Instance to Top Port Mapping:</label>
                    <textarea id="instanceToTop" placeholder="instance.port[range] -> top_port[range]"></textarea>
                    <div class="help-text">Format: instance.port[range] -> top_port[range] or TIE0/TIE1/FLOAT</div>
                </div>
            </div>
            
            <!-- Step 5: Instance Connections -->
            <div id="step5" class="step hidden">
                <h3>🔄 Instance Connections</h3>
                <div class="form-group">
                    <label for="instanceConnections">Instance-to-Instance Connections:</label>
                    <textarea id="instanceConnections" placeholder="source_instance.port[range] -> target_instance.port[range]"></textarea>
                    <div class="help-text">Format: source_instance.port[range] -> target_instance.port[range]</div>
                </div>
            </div>
            
            <!-- Step 6: Generate -->
            <div id="step6" class="step hidden">
                <h3>⚡ Generate & Review</h3>
                <div class="form-group">
                    <label>Configuration Summary:</label>
                    <div id="configSummary" class="code"></div>
                </div>
                <div id="generationResult" class="result hidden"></div>
            </div>
        </div>
        
        <div class="navigation">
            <button id="prevBtn" class="prev-btn" onclick="prevStep()" disabled>← Previous</button>
            <button id="nextBtn" class="next-btn" onclick="nextStep()">Next →</button>
        </div>
    </div>

    <script>
        let currentStep = 1;
        const totalSteps = 6;
        const stepNames = [
            '', // index 0 (unused)
            'Top Module Configuration',
            'Instance Definition',
            'Top Port Definition',
            'Instance-to-Top Mapping',
            'Instance Connections',
            'Generate & Review'
        ];
        
        let configData = {
            top_module: '',
            instances: [],
            top_ports: [],
            instance_to_top: [],
            instance_connections: []
        };
        
        function updateProgress() {
            document.getElementById('currentStep').textContent = currentStep;
            document.getElementById('stepName').textContent = stepNames[currentStep];
            
            const progress = (currentStep / totalSteps) * 100;
            document.getElementById('progressBar').style.width = progress + '%';
            
            // Update buttons
            document.getElementById('prevBtn').disabled = currentStep === 1;
            const nextBtn = document.getElementById('nextBtn');
            if (currentStep === totalSteps) {
                nextBtn.textContent = 'Generate';
                nextBtn.className = 'generate-btn';
            } else {
                nextBtn.textContent = 'Next →';
                nextBtn.className = 'next-btn';
            }
        }
        
        function showStep(step) {
            // Hide all steps
            document.querySelectorAll('.step').forEach(s => s.classList.add('hidden'));
            
            // Show current step
            document.getElementById('step' + step).classList.remove('hidden');
            
            // Special handling for summary step
            if (step === 6) {
                generateSummary();
            }
        }
        
        function saveCurrentStepData() {
            switch(currentStep) {
                case 1:
                    configData.top_module = document.getElementById('topModule').value.trim();
                    break;
                case 2:
                    configData.instances = document.getElementById('instances').value.split('\\n').filter(line => line.trim());
                    break;
                case 3:
                    configData.top_ports = document.getElementById('topPorts').value.split('\\n').filter(line => line.trim());
                    break;
                case 4:
                    configData.instance_to_top = document.getElementById('instanceToTop').value.split('\\n').filter(line => line.trim());
                    break;
                case 5:
                    configData.instance_connections = document.getElementById('instanceConnections').value.split('\\n').filter(line => line.trim());
                    break;
            }
        }
        
        function loadStepData() {
            switch(currentStep) {
                case 1:
                    document.getElementById('topModule').value = configData.top_module;
                    break;
                case 2:
                    document.getElementById('instances').value = configData.instances.join('\\n');
                    break;
                case 3:
                    document.getElementById('topPorts').value = configData.top_ports.join('\\n');
                    break;
                case 4:
                    document.getElementById('instanceToTop').value = configData.instance_to_top.join('\\n');
                    break;
                case 5:
                    document.getElementById('instanceConnections').value = configData.instance_connections.join('\\n');
                    break;
            }
        }
        
        function validateCurrentStep() {
            switch(currentStep) {
                case 1:
                    if (!document.getElementById('topModule').value.trim()) {
                        alert('Top module name is required!');
                        return false;
                    }
                    break;
                case 2:
                    if (!document.getElementById('instances').value.trim()) {
                        alert('At least one instance is required!');
                        return false;
                    }
                    break;
                case 3:
                    if (!document.getElementById('topPorts').value.trim()) {
                        alert('At least one top port is required!');
                        return false;
                    }
                    break;
            }
            return true;
        }
        
        function nextStep() {
            if (!validateCurrentStep()) return;
            
            saveCurrentStepData();
            
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
                loadStepData();
                updateProgress();
            } else {
                generateVerilog();
            }
        }
        
        function prevStep() {
            if (currentStep > 1) {
                saveCurrentStepData();
                currentStep--;
                showStep(currentStep);
                loadStepData();
                updateProgress();
            }
        }
        
        function generateSummary() {
            const summary = `Top Module: ${configData.top_module}

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
        
        function generateVerilog() {
            const resultDiv = document.getElementById('generationResult');
            resultDiv.innerHTML = '<div>Generating Verilog wrapper...</div>';
            resultDiv.classList.remove('hidden');
            
            fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ config_data: configData })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    let result = '<div class="success">✅ Verilog wrapper generated successfully!</div>';
                    result += '<h4>Generated Verilog Code:</h4>';
                    result += '<div class="code">' + escapeHtml(data.verilog_code) + '</div>';
                    result += '<button onclick="downloadVerilog()">Download Verilog File</button>';
                    
                    if (data.reports && Object.keys(data.reports).length > 0) {
                        result += '<h4>Unconnected Ports Report:</h4>';
                        for (const [filename, content] of Object.entries(data.reports)) {
                            result += '<h5>' + filename + '</h5>';
                            result += '<div class="code">' + escapeHtml(content) + '</div>';
                        }
                    }
                    
                    resultDiv.innerHTML = result;
                    
                    // Store for download
                    window.generatedVerilog = data.verilog_code;
                } else {
                    resultDiv.innerHTML = '<div class="error">❌ Error: ' + data.message + '</div>';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '<div class="error">❌ Network error: ' + error.message + '</div>';
            });
        }
        
        function downloadVerilog() {
            const blob = new Blob([window.generatedVerilog], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = (configData.top_module || 'wrapper') + '.v';
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Initialize
        updateProgress();
        showStep(1);
        loadStepData();
    </script>
</body>
</html>
        """

def main():
    PORT = 8002
    
    try:
        with socketserver.TCPServer(("", PORT), VerilogWrapperWebHandler) as httpd:
            print(f"🚀 Verilog Wrapper Generator Web UI started!")
            print(f"📱 Open your web browser and go to: http://localhost:{PORT}")
            print(f"🛑 Press Ctrl+C to stop the server")
            
            def open_browser():
                time.sleep(1)
                try:
                    webbrowser.open(f'http://localhost:{PORT}')
                except:
                    pass
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()