# Instance to Top Port Mapping
# 인스턴스의 포트를 탑 모듈의 포트로 연결합니다.
# 형식: 인스턴스명.포트명 -> 탑포트명

[INSTANCE_TO_TOP]
# Connect instance ports to top module ports
test_inst.clk -> clk
test_inst.reset -> reset
test_inst.data_in -> data_in
test_inst.addr -> addr
test_inst.data_out -> data_out
test_inst.valid -> valid