# Instance Configuration
# 인스턴스화할 모듈과 그 모듈의 이름 및 파라미터를 지정합니다.
# 형식: 인스턴스명 | 모듈파일경로 | 파라미터(선택사항)

[INSTANCES]
# 인스턴스명 | 모듈파일 | 파라미터
cpu_core | cpu.v | DATA_WIDTH=32,ADDR_WIDTH=16
main_memory | memory.v | MEM_SIZE=65536
cache_ctrl | cache.v | CACHE_SIZE=1024,LINE_SIZE=64
uart_if | uart.v | BAUD_RATE=115200