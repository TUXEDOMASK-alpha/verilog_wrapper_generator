# Configuration Files

이 디렉토리는 베릴로그 래퍼 생성기의 설정 파일들을 포함합니다.

## 파일 설명

### 1. `top_module.txt`
- **목적**: 생성할 탑 모듈의 이름을 지정
- **형식**: 
  ```
  [TOP_MODULE_NAME]
  모듈명
  ```

### 2. `instances.txt`
- **목적**: 인스턴스화할 모듈과 그 모듈의 이름 및 파라미터 지정
- **형식**: 
  ```
  [INSTANCES]
  인스턴스명 | 모듈파일경로 | 파라미터(선택사항)
  ```
- **파라미터 형식**: `PARAM1=value1,PARAM2=value2`

### 3. `top_ports.txt`
- **목적**: 생성할 탑 모듈의 포트 정의
- **형식**: 
  ```
  [TOP_PORTS]
  방향 | 포트폭 | 포트명
  ```
- **방향**: `input`, `output`, `inout`
- **포트폭**: `[7:0]`, `[31:0]` 등, 단일 비트인 경우 빈 칸

### 4. `instance_to_top.txt`
- **목적**: 인스턴스의 포트를 탑 모듈의 포트로 연결
- **형식**: 
  ```
  [INSTANCE_TO_TOP]
  인스턴스명.포트명 -> 탑포트명
  ```

### 5. `instance_connections.txt`
- **목적**: 인스턴스들 간의 연결 지정
- **형식**: 
  ```
  [INSTANCE_CONNECTIONS]
  인스턴스명.포트명 -> 인스턴스명.포트명
  ```

## 사용법

모든 설정 파일을 구성한 후:

```bash
python3 verilog_wrapper_generator.py config/ -o output.v
```

설정 파일들을 포함한 디렉토리를 인수로 전달하면 됩니다.