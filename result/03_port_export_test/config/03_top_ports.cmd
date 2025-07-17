[TOP_PORTS]
input | | clk
input | | reset
output | [31:0] | cpu_debug_data
output | [15:0] | cpu_debug_addr
output | | cpu_debug_valid
output | [7:0] | uart_tx_data
output | | uart_tx_valid
input | [7:0] | uart_rx_data
input | | uart_rx_valid