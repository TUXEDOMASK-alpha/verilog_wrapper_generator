# Top Module Port Configuration  
# 생성할 탑 모듈의 포트를 지정합니다.
# 형식: 방향 | 포트폭 | 포트명

[TOP_PORTS]
# 방향 | 포트폭 | 포트명
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