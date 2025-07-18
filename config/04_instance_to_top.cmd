# Instance to Top Port Mapping
# 인스턴스의 포트를 탑 모듈의 포트로 연결합니다.
# 형식: 인스턴스명.포트명 -> 탑포트명

[INSTANCE_TO_TOP]
# Connect instance ports to top module ports
cpu_inst.clk -> clk
cpu_inst.reset -> reset
cpu_inst.data_in -> system_data_in
mem_inst.clk -> clk
mem_inst.reset -> reset
mem_inst.data_out -> system_data_out