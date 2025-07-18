# Top Module Port Configuration  
# 생성할 탑 모듈의 포트를 지정합니다.
# 형식: 방향 | 포트폭 | 포트명

[TOP_PORTS]
# 방향 | 포트폭 | 포트명  
input | | clk
input | | reset
input | [L-1:0] | i_port1
input | [M-1:0] | i_port2
input | [N-1:0] | i_port3
output | [L-1:0] | o_port1
output | [M-1:0] | o_port2
output | [P-1:0] | o_port3