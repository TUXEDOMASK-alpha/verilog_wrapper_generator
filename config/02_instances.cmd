# Instance Configuration
# 인스턴스화할 모듈과 그 모듈의 이름 및 파라미터를 지정합니다.
# 형식: 인스턴스명 | 모듈파일경로 | 파라미터(선택사항)

[INSTANCES]
# 인스턴스명 | 모듈파일 | 모듈명(선택) | 파라미터(선택)
cpu_inst | cpu_module.v | cpu_module | DATA_WIDTH=32,ADDR_WIDTH=16
mem_inst | memory_module.v | memory_module | DATA_WIDTH=32,ADDR_WIDTH=16