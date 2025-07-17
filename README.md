# Verilog Wrapper Generator

이 도구는 Verilog 모듈들을 인스턴스화하고 연결하는 래퍼(wrapper) 파일을 자동으로 생성합니다.

## 주요 기능

1. **모듈 인스턴스화**: 다양한 Verilog 모듈을 인스턴스화
2. **파라미터 지원**: 복잡한 파라미터 표현식 및 의존성 해석
3. **포트 연결**: 인스턴스 간 연결 및 탑 모듈 연결
4. **포트 Export**: 인스턴스 포트를 직접 탑 모듈로 노출
5. **와이어 최적화**: 필요한 와이어만 생성
6. **에러 리포팅**: 포괄적인 에러 검출 및 리포팅
7. **코드 정렬**: 가독성 향상을 위한 완벽한 코드 정렬

## 사용법

```bash
python3 verilog_wrapper_generator.py <config_directory>
```

## 설정 파일 구조

설정 파일들은 순서대로 번호가 매겨져 있으며, 모두 `.cmd` 확장자를 사용합니다:

### 1. 01_top_module.cmd
생성할 탑 모듈의 이름을 지정합니다.

```
[TOP_MODULE_NAME]
cpu_system_top
```

### 2. 02_instances.cmd
인스턴스화할 모듈들을 지정합니다.

```
[INSTANCES]
# 인스턴스명 | 모듈파일 | [모듈명] | [파라미터]
cpu_core | cpu.v | DATA_WIDTH=32,ADDR_WIDTH=16
memory_ctrl | memory.v | memory_controller | MEM_SIZE=65536
cache_inst | cache.v | CACHE_SIZE=1024,LINE_SIZE=64

# 다중 모듈 파일에서 특정 모듈 선택
adder_inst | math_modules.v | adder | WIDTH=16
mult_inst | math_modules.v | multiplier | A_WIDTH=8,B_WIDTH=12
```

**형식**: `인스턴스명 | 모듈파일 | [모듈명] | [파라미터]`
- **모듈명**: 하나의 파일에 여러 모듈이 있을 경우 사용할 특정 모듈명 지정
- 모듈명을 생략하면 파일의 첫 번째 모듈을 사용
- **파라미터**: `KEY=VALUE` 형태로 콤마로 구분
- **복잡한 localparam 지원**: 수식 계산 (`WIDTH/2`, `A+B`) 및 조건문 (`A>16?5:4`) 처리

### 3. 03_top_ports.cmd
탑 모듈의 포트를 정의합니다.

```
[TOP_PORTS]
# 방향 | 포트폭 | 포트명
input | | sys_clk
input | | sys_reset
input | [7:0] | uart_rx_data
output | [7:0] | uart_tx_data
output | | uart_tx_valid
inout | [15:0] | external_bus
```

### 4. 04_instance_to_top.cmd
인스턴스의 포트를 탑 모듈의 포트로 연결합니다.

```
[INSTANCE_TO_TOP]
# 인스턴스명.포트명 -> 탑포트명
cpu_core.clk -> sys_clk
cpu_core.reset -> sys_reset
uart_if.rx_data -> uart_rx_data
uart_if.tx_data -> uart_tx_data

# 부분 비트 연결 지원
cpu_core.data_out[15:8] -> debug_high
cpu_core.data_out[7:0] -> debug_low
```

### 5. 05_instance_connections.cmd
인스턴스들 간의 연결을 지정합니다.

```
[INSTANCE_CONNECTIONS]
# 인스턴스명.포트명 -> 인스턴스명.포트명
cpu_core.data_out -> cache_ctrl.cpu_data_in
cpu_core.addr_out -> cache_ctrl.cpu_addr_in
cache_ctrl.cpu_data_out -> cpu_core.data_in

# 특수 연결
cpu_core.enable -> TIE1
cpu_core.unused_port -> TIE0
floating_port -> FLOAT
```

**특수 연결 타입**:
- `TIE1`: 1'b1로 연결
- `TIE0`: 1'b0로 연결  
- `FLOAT`: 연결하지 않음 (floating)

### 6. 06_instance_export_port.cmd
인스턴스의 포트를 직접 탑 모듈 포트로 노출합니다.

```
[INSTANCE_EXPORT_PORTS]
# 인스턴스명.포트명 [-> 새로운포트명]
cpu_core.debug_signal -> cpu_debug
uart_if.status
memory_ctrl.ready -> mem_ready
```

원래 포트명을 사용하려면 `->` 이후 부분을 생략합니다.

## 파라미터 지원

복잡한 파라미터 표현식을 지원합니다:

```verilog
module test_module #(
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 16,
    localparam EXTENDED_WIDTH = DATA_WIDTH + 8,
    localparam TOTAL_SIZE = ADDR_WIDTH * 2 + EXTENDED_WIDTH
)(
    // 포트 정의
);
```

## 생성된 코드 예시

```verilog
module cpu_system_top (
    input   wire            sys_clk,
    input   wire            sys_reset,
    input   wire  [7:0]     uart_rx_data,
    output  wire  [7:0]     uart_tx_data,
    output  wire            uart_tx_valid,
    inout   wire  [15:0]    external_bus
);

// Internal wires
    wire  [31:0]    w_cpu_core_data_out;
    wire  [15:0]    w_cpu_core_addr_out;
    wire            w_cache_ctrl_ready;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu_core (
        .clk     (sys_clk),
        .reset   (sys_reset),
        .data_out(w_cpu_core_data_out),
        .addr_out(w_cpu_core_addr_out)
    );

    cache #(.CACHE_SIZE(1024)) cache_ctrl (
        .clk       (sys_clk),
        .reset     (sys_reset),
        .cpu_data  (w_cpu_core_data_out),
        .cpu_addr  (w_cpu_core_addr_out),
        .ready     (w_cache_ctrl_ready)
    );

endmodule
```

## 코드 정렬 기능

생성된 코드는 완벽하게 정렬됩니다:

1. **포트 선언**: `[`의 위치와 신호 이름이 정렬
2. **와이어 선언**: `[`의 위치와 신호 이름이 정렬
3. **인스턴스 연결**: `(`의 위치가 정렬

## 에러 리포팅

다음과 같은 에러들을 검출하고 리포팅합니다:

- 존재하지 않는 모듈
- 존재하지 않는 포트
- 잘못된 포트 방향 연결 (input끼리 연결 등)
- 잘못된 TIE 연결
- 파라미터 오류

에러 리포트는 `./rpt/Error_report.list`에 저장됩니다.

## 언커넥티드 포트 리포팅

연결되지 않은 포트들은 다음 파일들에 기록됩니다:

- `./rpt/Unconnected_input.list`
- `./rpt/Unconnected_output.list`
- `./rpt/Unconnected_inout.list`

## 고급 기능

### 1. 와이어 최적화
필요한 와이어만 생성하여 불필요한 와이어 선언을 방지합니다.

### 2. 부분 비트 연결
포트의 특정 비트 범위를 연결할 수 있습니다:
```
cpu_core.data[31:16] -> memory_ctrl.high_data
cpu_core.data[15:0] -> memory_ctrl.low_data
```

### 3. 파라미터 의존성 해석
localparam이 다른 파라미터를 참조하는 경우 자동으로 해석합니다.

### 4. 모듈명 별도 지정
파일명과 모듈명이 다른 경우 별도로 지정할 수 있습니다.

## 예시 실행

```bash
# 기본 CPU 시스템 생성
python3 verilog_wrapper_generator.py ./config

# 포트 Export 기능 테스트
python3 verilog_wrapper_generator.py ./config_export_test

# 와이어 최적화 테스트
python3 verilog_wrapper_generator.py ./config_wire_test
```

## 출력 파일

- 메인 래퍼 파일: `<top_module_name>.v`
- 에러 리포트: `./rpt/Error_report.list`
- 언커넥티드 포트 리포트: `./rpt/Unconnected_*.list`

## 주의사항

1. 모든 모듈 파일은 현재 디렉토리에 있어야 합니다
2. 설정 파일들은 순서대로 처리됩니다
3. 에러가 발생하면 래퍼 파일이 생성되지 않습니다
4. 파라미터 이름은 대소문자를 구분합니다

## 문제 해결

### 자주 발생하는 에러

1. **모듈을 찾을 수 없음**: 모듈 파일 경로와 모듈명을 확인
2. **포트를 찾을 수 없음**: 포트 이름의 오타 확인
3. **파라미터 오류**: 파라미터 이름과 값의 정확성 확인
4. **연결 에러**: 포트 방향의 호환성 확인

모든 에러는 터미널에 출력되며 `./rpt/Error_report.list`에 저장됩니다.