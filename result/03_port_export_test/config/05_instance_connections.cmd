[INSTANCE_CONNECTIONS]
cpu_core.uart_tx_data -> uart_module.tx_data_in
cpu_core.uart_tx_valid -> uart_module.tx_valid_in
uart_module.rx_data_out -> cpu_core.uart_rx_data
uart_module.rx_valid_out -> cpu_core.uart_rx_valid