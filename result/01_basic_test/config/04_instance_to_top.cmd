# Instance to Top Port Mapping
# 인스턴스의 포트를 탑 모듈의 포트로 연결합니다.
# 형식: 인스턴스명.포트명 -> 탑포트명

[INSTANCE_TO_TOP]
# 클록과 리셋 연결
cpu_core.clk -> sys_clk
cpu_core.reset -> sys_reset
main_memory.clk -> sys_clk
main_memory.reset -> sys_reset
cache_ctrl.clk -> sys_clk
cache_ctrl.reset -> sys_reset
uart_if.clk -> sys_clk
uart_if.reset -> sys_reset

# UART 인터페이스 연결
uart_if.rx_data -> uart_rx_data
uart_if.tx_data -> uart_tx_data
uart_if.tx_valid -> uart_tx_valid
uart_if.rx_valid -> uart_rx_valid

# 디버그 포트 연결
cpu_core.debug_data -> debug_data
cpu_core.debug_addr -> debug_addr
cpu_core.debug_valid -> debug_valid

# 외부 버스 연결
main_memory.external_bus -> external_bus