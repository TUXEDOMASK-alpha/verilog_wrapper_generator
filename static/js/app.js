/**
 * Verilog Wrapper Generator Web GUI
 * JavaScript Application Logic
 */

class VerilogGUI {
    constructor() {
        this.editors = {};
        this.currentConfig = {};
        this.isLoading = false;
        
        this.init();
    }

    init() {
        this.setupEditors();
        this.setupEventListeners();
        this.loadConfiguration();
        this.updateStatus('Ready', 'secondary');
    }

    setupEditors() {
        const editorConfigs = [
            { id: 'topModuleEditor', key: 'top_module' },
            { id: 'instancesEditor', key: 'instances' },
            { id: 'topPortsEditor', key: 'top_ports' },
            { id: 'portMappingEditor', key: 'instance_to_top' },
            { id: 'connectionsEditor', key: 'instance_connections' },
            { id: 'exportPortsEditor', key: 'instance_export_ports' }
        ];

        editorConfigs.forEach(config => {
            const textarea = document.getElementById(config.id);
            if (textarea) {
                // Add auto-resize functionality
                this.setupAutoResize(textarea);
                
                // Add change listener
                textarea.addEventListener('input', () => {
                    this.currentConfig[config.key] = textarea.value;
                    this.debounceValidation();
                });
                
                this.editors[config.key] = textarea;
            }
        });

        // Setup wrapper preview
        const wrapperPreview = document.getElementById('wrapperPreview');
        if (wrapperPreview) {
            this.editors.preview = wrapperPreview;
        }
    }

    setupAutoResize(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.max(this.scrollHeight, 200) + 'px';
        });
    }

    setupEventListeners() {
        // Navigation buttons
        document.getElementById('loadConfigBtn')?.addEventListener('click', () => {
            this.loadConfiguration();
        });

        document.getElementById('saveConfigBtn')?.addEventListener('click', () => {
            this.saveConfiguration();
        });

        document.getElementById('generateBtn')?.addEventListener('click', () => {
            this.generateWrapper();
        });

        document.getElementById('validateBtn')?.addEventListener('click', () => {
            this.validateConfiguration();
        });

        document.getElementById('downloadBtn')?.addEventListener('click', () => {
            this.downloadWrapper();
        });

        // Tab switching
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (event) => {
                this.onTabSwitch(event.target.getAttribute('data-bs-target'));
            });
        });
    }

    onTabSwitch(targetTab) {
        // Focus on the corresponding editor when tab is switched
        const editorMap = {
            '#top-module': 'topModuleEditor',
            '#instances': 'instancesEditor', 
            '#top-ports': 'topPortsEditor',
            '#port-mapping': 'portMappingEditor',
            '#connections': 'connectionsEditor',
            '#export-ports': 'exportPortsEditor'
        };

        const editorId = editorMap[targetTab];
        if (editorId) {
            setTimeout(() => {
                document.getElementById(editorId)?.focus();
            }, 100);
        }
    }

    debounceValidation() {
        clearTimeout(this.validationTimeout);
        this.validationTimeout = setTimeout(() => {
            this.validateConfiguration();
        }, 1000);
    }

    async loadConfiguration() {
        try {
            this.setLoading(true);
            this.updateStatus('Loading configuration...', 'secondary', true);

            const response = await fetch('/api/config/load');
            const data = await response.json();

            if (data.success) {
                this.currentConfig = data.config;
                this.updateEditors();
                this.updateStatus('Configuration loaded', 'success');
            } else {
                throw new Error(data.error || 'Failed to load configuration');
            }
        } catch (error) {
            console.error('Error loading configuration:', error);
            this.updateStatus('Error loading configuration', 'danger');
            this.showNotification('Error loading configuration: ' + error.message, 'danger');
        } finally {
            this.setLoading(false);
        }
    }

    async saveConfiguration() {
        try {
            this.setLoading(true);
            this.updateStatus('Saving configuration...', 'secondary', true);

            const response = await fetch('/api/config/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentConfig)
            });

            const data = await response.json();

            if (data.success) {
                this.updateStatus('Configuration saved', 'success');
                this.showNotification('Configuration saved successfully', 'success');
            } else {
                throw new Error(data.error || 'Failed to save configuration');
            }
        } catch (error) {
            console.error('Error saving configuration:', error);
            this.updateStatus('Error saving configuration', 'danger');
            this.showNotification('Error saving configuration: ' + error.message, 'danger');
        } finally {
            this.setLoading(false);
        }
    }

    async generateWrapper() {
        try {
            this.setLoading(true);
            this.updateStatus('Generating wrapper...', 'secondary', true);

            const response = await fetch('/api/wrapper/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentConfig)
            });

            const data = await response.json();

            if (data.success) {
                this.editors.preview.value = data.wrapper_code;
                this.updateStatus('Wrapper generated successfully', 'success');
                
                // Enable download button
                document.getElementById('downloadBtn').disabled = false;

                // Show error report if any
                if (data.error_report && data.error_report.trim()) {
                    this.showErrorReport(data.error_report);
                } else {
                    this.hideErrorReport();
                }
            } else {
                throw new Error(data.error || 'Failed to generate wrapper');
            }
        } catch (error) {
            console.error('Error generating wrapper:', error);
            this.updateStatus('Error generating wrapper', 'danger');
            this.showNotification('Error generating wrapper: ' + error.message, 'danger');
        } finally {
            this.setLoading(false);
        }
    }

    async validateConfiguration() {
        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentConfig)
            });

            const data = await response.json();

            if (data.success) {
                if (data.valid) {
                    this.updateStatus('Configuration valid', 'success');
                    this.hideErrorReport();
                } else {
                    this.updateStatus('Configuration has issues', 'warning');
                    if (data.errors.length > 0 || data.warnings.length > 0) {
                        const report = [
                            ...data.errors.map(err => `ERROR: ${err}`),
                            ...data.warnings.map(warn => `WARNING: ${warn}`)
                        ].join('\n');
                        this.showErrorReport(report);
                    }
                }
            }
        } catch (error) {
            console.error('Error validating configuration:', error);
            this.updateStatus('Validation error', 'danger');
        }
    }

    downloadWrapper() {
        const wrapperCode = this.editors.preview.value;
        if (!wrapperCode.trim()) {
            this.showNotification('No wrapper code to download', 'warning');
            return;
        }

        const blob = new Blob([wrapperCode], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'wrapper.v';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showNotification('Wrapper code downloaded', 'success');
    }

    updateEditors() {
        Object.keys(this.currentConfig).forEach(key => {
            if (this.editors[key]) {
                this.editors[key].value = this.currentConfig[key];
                // Trigger auto-resize
                if (this.editors[key].dispatchEvent) {
                    this.editors[key].dispatchEvent(new Event('input'));
                }
            }
        });
    }

    updateStatus(message, type, loading = false) {
        const statusIcon = document.getElementById('statusIcon');
        const statusText = document.getElementById('statusText');

        if (statusIcon && statusText) {
            statusIcon.innerHTML = loading ? 
                '<i class="fas fa-spinner fa-spin text-primary"></i>' :
                `<i class="fas fa-circle text-${type}"></i>`;
            statusText.textContent = message;
            
            // Add status transition class
            statusIcon.classList.add('status-transition');
            statusText.classList.add('status-transition');
        }
    }

    showErrorReport(report) {
        const errorPanel = document.getElementById('errorPanel');
        const errorContent = document.getElementById('errorContent');
        
        if (errorPanel && errorContent) {
            errorContent.textContent = report;
            errorPanel.style.display = 'block';
        }
    }

    hideErrorReport() {
        const errorPanel = document.getElementById('errorPanel');
        if (errorPanel) {
            errorPanel.style.display = 'none';
        }
    }

    showNotification(message, type) {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    setLoading(loading) {
        this.isLoading = loading;
        const loadingModal = document.getElementById('loadingModal');
        const modal = bootstrap.Modal.getOrCreateInstance(loadingModal);
        
        if (loading) {
            modal.show();
        } else {
            modal.hide();
        }
        
        // Disable/enable buttons
        const buttons = ['loadConfigBtn', 'saveConfigBtn', 'generateBtn', 'validateBtn'];
        buttons.forEach(btnId => {
            const btn = document.getElementById(btnId);
            if (btn) {
                btn.disabled = loading;
                if (loading) {
                    btn.classList.add('btn-loading');
                } else {
                    btn.classList.remove('btn-loading');
                }
            }
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.verilogGUI = new VerilogGUI();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+S or Cmd+S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            window.verilogGUI.saveConfiguration();
        }
        
        // Ctrl+Enter or Cmd+Enter to generate
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            window.verilogGUI.generateWrapper();
        }
    });
    
    // Add window beforeunload handler
    window.addEventListener('beforeunload', function(e) {
        // Could add unsaved changes detection here
    });
    
    console.log('Verilog Wrapper Generator Web GUI initialized');
});