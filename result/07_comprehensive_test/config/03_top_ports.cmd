[TOP_PORTS]
input | | sys_clk
input | | sys_reset
input | [7:0] | uart_rx_data
output | [7:0] | uart_tx_data
output | | uart_tx_valid
input | | uart_rx_valid
output | [31:0] | debug_data
output | [15:0] | debug_addr
output | | debug_valid
inout | [15:0] | external_bus
input | [7:0] | adder_input_a
input | [7:0] | adder_input_b
output | [8:0] | adder_result
output | [15:0] | counter_output