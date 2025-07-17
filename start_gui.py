#!/usr/bin/env python3
"""
Verilog Wrapper Generator Web GUI Launcher
Simple launcher script with dependency checking
"""

import sys
import subprocess
import importlib
import webbrowser
import time
import threading

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask']
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is not installed")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip3 install {' '.join(missing_packages)} --break-system-packages")
        return False
    
    return True

def open_browser_delayed(url, delay=3):
    """Open browser after a delay"""
    def open_browser():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 Opened browser at {url}")
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print(f"Please manually open: {url}")
    
    thread = threading.Thread(target=open_browser)
    thread.daemon = True
    thread.start()

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🔧 Verilog Wrapper Generator - Web GUI")
    print("=" * 60)
    
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n2. Starting Flask server...")
    try:
        # Open browser after 3 seconds
        url = "http://localhost:5001"
        open_browser_delayed(url)
        
        # Start the Flask application
        from verilog_gui_app import app
        print(f"\n🚀 Server starting at {url}")
        print("📝 Use the web interface to create and manage Verilog wrapper configurations")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 60)
        
        app.run(debug=False, host='0.0.0.0', port=5001)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()