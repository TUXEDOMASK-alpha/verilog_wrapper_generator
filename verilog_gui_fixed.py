#!/usr/bin/env python3
"""
Fixed Verilog Wrapper Generator Web GUI
"""

import http.server
import socketserver
import json
import os
import tempfile
import shutil
import webbrowser
import threading
import time
from verilog_wrapper_generator import WrapperGenerator

# Global session data
session_data = {
    'current_step': 1,
    'config_data': {
        'top_module': '',
        'instances': [],
        'top_ports': [],
        'instance_to_top': [],
        'instance_connections': []
    }
}

class FixedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/api/generate':
            self.handle_generate()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Verilog Wrapper Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; color: #333; }
        .progress { margin-bottom: 30px; }
        .progress-bar { width: 100%; height: 20px; background: #ddd; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: #4CAF50; transition: width 0.3s; }
        .step-info { margin-top: 10px; font-weight: bold; color: #666; }
        .step { margin-bottom: 20px; }
        .step.hidden { display: none; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #333; }
        input, textarea { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px; }
        input:focus, textarea:focus { outline: none; border-color: #4CAF50; }
        textarea { height: 120px; font-family: monospace; resize: vertical; }
        .help { margin-top: 8px; font-size: 14px; color: #666; }
        .navigation { display: flex; justify-content: space-between; margin-top: 30px; }
        button { padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
        .btn-prev { background: #666; color: white; }
        .btn-next { background: #4CAF50; color: white; }
        .btn-generate { background: #2196F3; color: white; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        button:hover:not(:disabled) { opacity: 0.8; }
        .result { margin-top: 20px; padding: 20px; background: #f9f9f9; border-radius: 5px; }
        .code { background: #f0f0f0; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: monospace; white-space: pre-wrap; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
        .download-btn { margin-top: 15px; padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Verilog Wrapper Generator</h1>
            <p>Create Verilog wrapper files step by step</p>
        </div>
        
        <div class="progress">
            <div class="progress-bar">
                <div id="progressFill" class="progress-fill"></div>
            </div>
            <div class="step-info">
                Step <span id="stepNumber">1</span> of 6: <span id="stepName">Top Module Configuration</span>
            </div>
        </div>
        
        <div class="steps">
            <div id="step1" class="step">
                <h3>Step 1: Top Module Configuration</h3>
                <div class="form-group">
                    <label for="topModule">Top Module Name:</label>
                    <input type="text" id="topModule" placeholder="e.g., cpu_system_wrapper">
                    <div class="help">Enter the name for your top-level wrapper module</div>
                </div>
            </div>
            
            <div id="step2" class="step hidden">
                <h3>Step 2: Instance Definition</h3>
                <div class="form-group">
                    <label for="instances">Instance Definitions:</label>
                    <textarea id="instances" placeholder="instance_name | verilog_file.v | param1=value1,param2=value2"></textarea>
                    <div class="help">Format: instance_name | verilog_file.v | param1=value1,param2=value2 (one per line)</div>
                </div>
            </div>
            
            <div id="step3" class="step hidden">
                <h3>Step 3: Top Port Definition</h3>
                <div class="form-group">
                    <label for="topPorts">Top-Level Ports:</label>
                    <textarea id="topPorts" placeholder="direction [width] port_name"></textarea>
                    <div class="help">Format: direction [width] port_name (e.g., input [7:0] data_in)</div>
                </div>
            </div>
            
            <div id="step4" class="step hidden">
                <h3>Step 4: Instance-to-Top Mapping</h3>
                <div class="form-group">
                    <label for="instanceToTop">Instance to Top Port Mapping:</label>
                    <textarea id="instanceToTop" placeholder="instance.port[range] -> top_port[range]"></textarea>
                    <div class="help">Format: instance.port[range] -> top_port[range] or TIE0/TIE1/FLOAT</div>
                </div>
            </div>
            
            <div id="step5" class="step hidden">
                <h3>Step 5: Instance Connections</h3>
                <div class="form-group">
                    <label for="instanceConnections">Instance-to-Instance Connections:</label>
                    <textarea id="instanceConnections" placeholder="source_instance.port[range] -> target_instance.port[range]"></textarea>
                    <div class="help">Format: source_instance.port[range] -> target_instance.port[range]</div>
                </div>
            </div>
            
            <div id="step6" class="step hidden">
                <h3>Step 6: Generate & Review</h3>
                <div class="form-group">
                    <label>Configuration Summary:</label>
                    <div id="configSummary" class="code"></div>
                </div>
                <div id="generationResult" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div class="navigation">
            <button id="prevBtn" class="btn-prev" onclick="goToPreviousStep()">← Previous</button>
            <button id="nextBtn" class="btn-next" onclick="goToNextStep()">Next →</button>
        </div>
    </div>

    <script>
        let currentStep = 1;
        const totalSteps = 6;
        const stepNames = [
            '', // index 0
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
        
        let generatedCode = '';
        
        function updateDisplay() {
            // Update progress
            const progress = (currentStep / totalSteps) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
            
            // Update step info
            document.getElementById('stepNumber').textContent = currentStep;
            document.getElementById('stepName').textContent = stepNames[currentStep];
            
            // Update buttons
            document.getElementById('prevBtn').disabled = currentStep === 1;
            
            const nextBtn = document.getElementById('nextBtn');
            if (currentStep === totalSteps) {
                nextBtn.textContent = 'Generate';
                nextBtn.className = 'btn-generate';
            } else {
                nextBtn.textContent = 'Next →';
                nextBtn.className = 'btn-next';
            }
            
            // Show/hide steps
            for (let i = 1; i <= totalSteps; i++) {
                const stepElement = document.getElementById('step' + i);
                if (i === currentStep) {
                    stepElement.classList.remove('hidden');
                } else {
                    stepElement.classList.add('hidden');
                }
            }
            
            // Handle special cases
            if (currentStep === 6) {
                generateSummary();
            }
        }
        
        function saveCurrentStep() {
            switch(currentStep) {
                case 1:
                    configData.top_module = document.getElementById('topModule').value.trim();
                    break;
                case 2:
                    const instancesText = document.getElementById('instances').value;
                    configData.instances = instancesText.split('\\n').filter(line => line.trim());
                    break;
                case 3:
                    const portsText = document.getElementById('topPorts').value;
                    configData.top_ports = portsText.split('\\n').filter(line => line.trim());
                    break;
                case 4:
                    const mappingText = document.getElementById('instanceToTop').value;
                    configData.instance_to_top = mappingText.split('\\n').filter(line => line.trim());
                    break;
                case 5:
                    const connectionsText = document.getElementById('instanceConnections').value;
                    configData.instance_connections = connectionsText.split('\\n').filter(line => line.trim());
                    break;
            }
        }
        
        function loadCurrentStep() {
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
                    if (!configData.top_module) {
                        alert('Please enter a top module name');
                        return false;
                    }
                    break;
                case 2:
                    if (configData.instances.length === 0) {
                        alert('Please define at least one instance');
                        return false;
                    }
                    break;
                case 3:
                    if (configData.top_ports.length === 0) {
                        alert('Please define at least one top port');
                        return false;
                    }
                    break;
            }
            return true;
        }
        
        function goToNextStep() {
            console.log('Next button clicked, current step:', currentStep);
            
            saveCurrentStep();
            
            if (!validateCurrentStep()) {
                return;
            }
            
            if (currentStep < totalSteps) {
                currentStep++;
                updateDisplay();
                loadCurrentStep();
            } else {
                // Generate Verilog
                generateVerilog();
            }
        }
        
        function goToPreviousStep() {
            console.log('Previous button clicked, current step:', currentStep);
            
            if (currentStep > 1) {
                saveCurrentStep();
                currentStep--;
                updateDisplay();
                loadCurrentStep();
            }
        }
        
        function generateSummary() {
            let summary = 'Top Module: ' + configData.top_module + '\\n\\n';
            
            summary += 'Instances (' + configData.instances.length + '):\\n';
            configData.instances.forEach((inst, i) => {
                summary += '  ' + (i + 1) + '. ' + inst + '\\n';
            });
            
            summary += '\\nTop Ports (' + configData.top_ports.length + '):\\n';
            configData.top_ports.forEach((port, i) => {
                summary += '  ' + (i + 1) + '. ' + port + '\\n';
            });
            
            summary += '\\nInstance-to-Top Mappings (' + configData.instance_to_top.length + '):\\n';
            configData.instance_to_top.forEach((mapping, i) => {
                summary += '  ' + (i + 1) + '. ' + mapping + '\\n';
            });
            
            summary += '\\nInstance Connections (' + configData.instance_connections.length + '):\\n';
            configData.instance_connections.forEach((conn, i) => {
                summary += '  ' + (i + 1) + '. ' + conn + '\\n';
            });
            
            document.getElementById('configSummary').textContent = summary;
        }
        
        function generateVerilog() {
            const resultDiv = document.getElementById('generationResult');
            resultDiv.innerHTML = '<div>Generating Verilog wrapper...</div>';
            resultDiv.style.display = 'block';
            
            fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    config_data: configData
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    generatedCode = data.verilog_code;
                    
                    let result = '<div class="success">✅ Verilog wrapper generated successfully!</div>';
                    result += '<h4>Generated Verilog Code:</h4>';
                    result += '<div class="code">' + escapeHtml(data.verilog_code) + '</div>';
                    result += '<button class="download-btn" onclick="downloadVerilog()">Download Verilog File</button>';
                    
                    if (data.reports && Object.keys(data.reports).length > 0) {
                        result += '<h4>Unconnected Ports Report:</h4>';
                        for (const [filename, content] of Object.entries(data.reports)) {
                            result += '<h5>' + filename + '</h5>';
                            result += '<div class="code">' + escapeHtml(content) + '</div>';
                        }
                    }
                    
                    resultDiv.innerHTML = result;
                } else {
                    resultDiv.innerHTML = '<div class="error">❌ Error: ' + data.message + '</div>';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '<div class="error">❌ Network error: ' + error.message + '</div>';
            });
        }
        
        function downloadVerilog() {
            const blob = new Blob([generatedCode], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = (configData.top_module || 'wrapper') + '.v';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Initialize
        updateDisplay();
        loadCurrentStep();
    </script>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_generate(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            result = self.generate_verilog(data.get('config_data', {}))
            self.send_json_response(result)
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
            f.write("# Instances\\n\\n[INSTANCES]\\n")
            for instance in config_data.get('instances', []):
                if instance.strip():
                    f.write(f"{instance}\\n")
                    
        # Top ports
        with open(os.path.join(config_dir, 'top_ports.txt'), 'w') as f:
            f.write("# Top Ports\\n\\n[TOP_PORTS]\\n")
            for port in config_data.get('top_ports', []):
                if port.strip():
                    f.write(f"{port}\\n")
                    
        # Instance to top mapping
        with open(os.path.join(config_dir, 'instance_to_top.txt'), 'w') as f:
            f.write("# Instance to Top Mapping\\n\\n[INSTANCE_TO_TOP]\\n")
            for mapping in config_data.get('instance_to_top', []):
                if mapping.strip():
                    f.write(f"{mapping}\\n")
                    
        # Instance connections
        with open(os.path.join(config_dir, 'instance_connections.txt'), 'w') as f:
            f.write("# Instance Connections\\n\\n[INSTANCE_CONNECTIONS]\\n")
            for connection in config_data.get('instance_connections', []):
                if connection.strip():
                    f.write(f"{connection}\\n")
    
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

def main():
    PORT = 8004
    
    try:
        with socketserver.TCPServer(("", PORT), FixedHandler) as httpd:
            print(f"🚀 Fixed Verilog GUI started on port {PORT}")
            print(f"📱 Open: http://localhost:{PORT}")
            print("🔧 This version has debugging enabled")
            
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
        print("\\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()