# Instance to Top Port Mapping
# 인스턴스의 포트를 탑 모듈의 포트로 연결합니다.
# 형식: 인스턴스명.포트명 -> 탑포트명

[INSTANCE_TO_TOP]
# Connect instance ports to top module ports
mixed_inst.clk -> clk
mixed_inst.reset -> reset
mixed_inst.i_port1 -> i_port1
mixed_inst.i_port2 -> i_port2
mixed_inst.i_port3 -> i_port3
mixed_inst.o_port1 -> o_port1
mixed_inst.o_port2 -> o_port2
mixed_inst.o_port3 -> o_port3