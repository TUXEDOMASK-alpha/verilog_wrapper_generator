# Top Module Port Configuration  
# 생성할 탑 모듈의 포트를 지정합니다.
# 형식: 방향 | 포트폭 | 포트명

[TOP_PORTS]
# 방향 | 포트폭 | 포트명  
input | | clk
input | | reset
input | [DATA_WIDTH-1:0] | system_data_in
output | [DATA_WIDTH-1:0] | system_data_out