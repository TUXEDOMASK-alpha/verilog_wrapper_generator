# Instance to Instance Connections
# 인스턴스들 간의 연결을 지정합니다.
# 형식: 인스턴스명.포트명 -> 인스턴스명.포트명

[INSTANCE_CONNECTIONS]
# CPU to Memory connections
cpu_inst.addr_out -> mem_inst.addr_in
cpu_inst.data_out -> mem_inst.data_in
cpu_inst.mem_enable -> mem_inst.mem_enable
cpu_inst.mem_write -> mem_inst.mem_write