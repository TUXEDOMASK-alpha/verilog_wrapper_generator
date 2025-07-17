[INSTANCE_CONNECTIONS]
# CPU to Cache connections
cpu_core.addr_out -> cache_ctrl.cpu_addr_in
cpu_core.data_out -> cache_ctrl.cpu_data_in
cpu_core.read_enable -> cache_ctrl.cpu_read_en
cpu_core.write_enable -> cache_ctrl.cpu_write_en
cache_ctrl.cpu_data_out -> cpu_core.data_in
cache_ctrl.cpu_ready -> cpu_core.cache_ready

# Cache to Memory connections
cache_ctrl.mem_addr_out -> main_memory.addr_in
cache_ctrl.mem_data_out -> main_memory.data_in
cache_ctrl.mem_read_en -> main_memory.read_enable
cache_ctrl.mem_write_en -> main_memory.write_enable
main_memory.data_out -> cache_ctrl.mem_data_in
main_memory.ready -> cache_ctrl.mem_ready

# CPU to UART connections
cpu_core.uart_tx_data -> uart_if.tx_data_in
cpu_core.uart_tx_valid -> uart_if.tx_valid_in
uart_if.rx_data_out -> cpu_core.uart_rx_data
uart_if.rx_valid_out -> cpu_core.uart_rx_valid

# TIE connections for unused ports
counter_inst.enable -> TIE1

# FLOAT connections for test purposes (removing adder conflicts since they're connected to top)
# Note: adder_unit.a and adder_unit.b are connected to top ports, so no FLOAT needed