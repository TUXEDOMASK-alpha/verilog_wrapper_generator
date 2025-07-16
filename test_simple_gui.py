#!/usr/bin/env python3
"""
Simple test version to debug the GUI
"""

import http.server
import socketserver
import webbrowser
import threading
import time

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_test_page()
        else:
            self.send_error(404)
    
    def serve_test_page(self):
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Debug Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; }
        .step { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        .hidden { display: none; }
        button { padding: 10px 20px; margin: 5px; cursor: pointer; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        .debug { background: #f0f0f0; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Debug Test - Step Navigation</h1>
        
        <div class="debug">
            <strong>Debug Info:</strong>
            <div>Current Step: <span id="debugStep">1</span></div>
            <div>Last Action: <span id="debugAction">Page loaded</span></div>
        </div>
        
        <div class="step" id="step1">
            <h3>Step 1: Enter Module Name</h3>
            <input type="text" id="moduleName" placeholder="Enter module name">
        </div>
        
        <div class="step hidden" id="step2">
            <h3>Step 2: Enter Instances</h3>
            <textarea id="instances" rows="5" cols="50" placeholder="Enter instances"></textarea>
        </div>
        
        <div class="step hidden" id="step3">
            <h3>Step 3: Summary</h3>
            <div id="summary"></div>
        </div>
        
        <div>
            <button onclick="debugPrev()">Previous</button>
            <button onclick="debugNext()">Next</button>
            <button onclick="debugLog()">Log Debug</button>
        </div>
    </div>

    <script>
        let currentStep = 1;
        const maxSteps = 3;
        
        function debugLog() {
            console.log('Current step:', currentStep);
            console.log('Module name:', document.getElementById('moduleName').value);
            console.log('Instances:', document.getElementById('instances').value);
            alert('Check console for debug info');
        }
        
        function updateDebugInfo(action) {
            document.getElementById('debugStep').textContent = currentStep;
            document.getElementById('debugAction').textContent = action;
            console.log('Action:', action, 'Step:', currentStep);
        }
        
        function showStep(step) {
            // Hide all steps
            for (let i = 1; i <= maxSteps; i++) {
                document.getElementById('step' + i).classList.add('hidden');
            }
            
            // Show current step
            document.getElementById('step' + step).classList.remove('hidden');
            
            updateDebugInfo('Showing step ' + step);
        }
        
        function debugNext() {
            updateDebugInfo('Next button clicked');
            
            if (currentStep < maxSteps) {
                currentStep++;
                showStep(currentStep);
                
                // Special handling for summary step
                if (currentStep === 3) {
                    const moduleName = document.getElementById('moduleName').value;
                    const instances = document.getElementById('instances').value;
                    document.getElementById('summary').innerHTML = 
                        '<strong>Module:</strong> ' + moduleName + '<br>' +
                        '<strong>Instances:</strong> ' + instances;
                }
            } else {
                alert('This is the last step!');
            }
        }
        
        function debugPrev() {
            updateDebugInfo('Previous button clicked');
            
            if (currentStep > 1) {
                currentStep--;
                showStep(currentStep);
            } else {
                alert('This is the first step!');
            }
        }
        
        // Initialize
        updateDebugInfo('Page initialized');
        showStep(1);
    </script>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode())

def main():
    PORT = 8003
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
            print(f"🔧 Debug test server started on port {PORT}")
            print(f"📱 Open: http://localhost:{PORT}")
            
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