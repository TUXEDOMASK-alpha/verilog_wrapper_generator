# Instance to Instance Connections
# 인스턴스들 간의 연결을 지정합니다.
# 형식: 인스턴스명.포트명 -> 인스턴스명.포트명

[INSTANCE_CONNECTIONS]
# CPU와 캐시 연결
cpu_core.data_out -> cache_ctrl.cpu_data_in
cpu_core.addr_out -> cache_ctrl.cpu_addr_in
cpu_core.read_enable -> cache_ctrl.cpu_read_en
cpu_core.write_enable -> cache_ctrl.cpu_write_en
cache_ctrl.cpu_data_out -> cpu_core.data_in
cache_ctrl.cpu_ready -> cpu_core.cache_ready

# 캐시와 메모리 연결
cache_ctrl.mem_data_out -> main_memory.data_in
cache_ctrl.mem_addr_out -> main_memory.addr_in
cache_ctrl.mem_read_en -> main_memory.read_enable
cache_ctrl.mem_write_en -> main_memory.write_enable
main_memory.data_out -> cache_ctrl.mem_data_in
main_memory.ready -> cache_ctrl.mem_ready

# CPU와 UART 연결 (디버그/통신용)
cpu_core.uart_tx_data -> uart_if.tx_data_in
cpu_core.uart_tx_valid -> uart_if.tx_valid_in
uart_if.rx_data_out -> cpu_core.uart_rx_data
uart_if.rx_valid_out -> cpu_core.uart_rx_valid