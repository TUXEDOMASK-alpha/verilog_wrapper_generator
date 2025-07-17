# Verilog Wrapper Generator - Web GUI 가이드

## 📋 개요

Verilog Wrapper Generator의 웹 기반 GUI 인터페이스입니다. 브라우저에서 configuration 파일을 편집하고 실시간으로 wrapper 코드를 생성할 수 있습니다.

## 🚀 시작하기

### 1. 실행 방법

```bash
# 간단한 실행 (자동으로 브라우저 열림)
python3 start_gui.py

# 또는 직접 Flask 서버 실행
python3 verilog_gui_app.py
```

### 2. 브라우저에서 접속

```
http://localhost:5001
```

## 🎯 주요 기능

### 📝 Configuration 편집

**6개의 탭으로 구성된 설정 편집기:**

1. **Top Module** - 탑 모듈 이름 및 파라미터 설정
2. **Instances** - 인스턴스화할 모듈들 정의
3. **Top Ports** - 탑 모듈 포트 정의
4. **Port Mapping** - 인스턴스 포트를 탑 포트로 연결
5. **Connections** - 인스턴스들 간의 연결 정의
6. **Export Ports** - 인스턴스 포트를 직접 탑 모듈로 노출

### 🔄 실시간 기능

- **자동 검증**: 입력 시 자동으로 설정 검증
- **실시간 미리보기**: wrapper 코드 즉시 확인
- **에러 리포팅**: 설정 오류 및 경고 표시

### 💾 파일 관리

- **Load Config**: 기존 config 파일들 불러오기
- **Save Config**: 현재 설정을 파일로 저장
- **Download Wrapper**: 생성된 wrapper 코드 다운로드

## 📖 사용 방법

### 1. 새 프로젝트 시작

1. **Load Config** 버튼 클릭하여 기본 템플릿 로드
2. **Top Module** 탭에서 모듈 이름과 파라미터 설정
3. **Instances** 탭에서 사용할 모듈들 정의

### 2. 설정 편집

각 탭에서 다음 형식으로 설정:

#### Top Module 예시:
```
[TOP_MODULE_NAME]
my_wrapper

[TOP_MODULE_PARAMETERS]
DATA_WIDTH = 32
ADDR_WIDTH = 16
```

#### Instances 예시:
```
[INSTANCES]
cpu_core | cpu.v | DATA_WIDTH=32
memory | memory.v | memory_controller | MEM_SIZE=65536
```

#### Top Ports 예시:
```
[TOP_PORTS]
input | | clk
input | | reset
input | [DATA_WIDTH-1:0] | data_in
output | [DATA_WIDTH-1:0] | data_out
```

### 3. Wrapper 생성

1. 모든 설정 완료 후 **Generate Wrapper** 버튼 클릭
2. 오른쪽 미리보기 패널에서 생성된 코드 확인
3. **Download** 버튼으로 wrapper 파일 다운로드

## ⌨️ 키보드 단축키

- **Ctrl+S (또는 Cmd+S)**: 설정 저장
- **Ctrl+Enter (또는 Cmd+Enter)**: Wrapper 생성

## 🎨 UI 구성

### 왼쪽 패널 (Configuration Editor)
- 탭 기반 설정 편집기
- 문법 하이라이팅 지원
- 자동 크기 조절

### 오른쪽 패널 (Live Preview)
- 실시간 상태 표시
- 생성된 wrapper 코드 미리보기
- 에러/경고 표시

## 🔧 고급 기능

### 실시간 검증
- 입력 중 자동으로 설정 검증
- 오타 및 형식 오류 즉시 감지
- 경고 및 에러 메시지 표시

### 템플릿 시스템
- 각 설정 파일별 기본 템플릿 제공
- 주석과 예시 포함
- 초보자도 쉽게 시작 가능

### 에러 리포팅
- 상세한 에러 메시지
- 라인별 오류 위치 표시
- 수정 제안 포함

## 🐛 문제 해결

### 서버가 시작되지 않는 경우
```bash
# Flask 설치 확인
python3 -c "import flask; print('Flask installed')"

# 포트 충돌 확인
lsof -i :5001
```

### 브라우저에서 접속되지 않는 경우
1. 방화벽 설정 확인
2. `127.0.0.1:5001` 또는 `localhost:5001` 시도
3. 다른 브라우저로 테스트

### 설정 파일이 저장되지 않는 경우
1. `./config` 디렉토리 권한 확인
2. 디스크 공간 확인
3. 브라우저 콘솔에서 JavaScript 에러 확인

## 📁 파일 구조

```
Script_Lab/
├── verilog_gui_app.py      # Flask 서버
├── start_gui.py            # GUI 런처
├── templates/
│   └── index.html          # 메인 HTML 템플릿
├── static/
│   ├── css/style.css       # 스타일시트
│   └── js/app.js          # JavaScript 로직
└── config/                 # 설정 파일 저장 위치
    ├── 01_top_module.cmd
    ├── 02_instances.cmd
    ├── 03_top_ports.cmd
    ├── 04_instance_to_top.cmd
    ├── 05_instance_connections.cmd
    └── 06_instance_export_port.cmd
```

## 🔄 기존 CLI와의 차이점

| 기능 | CLI | Web GUI |
|------|-----|---------|
| 설정 편집 | 텍스트 에디터 필요 | 브라우저에서 직접 편집 |
| 실시간 미리보기 | 없음 | 즉시 확인 가능 |
| 에러 검증 | 생성 시에만 | 입력 중 실시간 검증 |
| 사용성 | 명령어 숙지 필요 | 직관적인 GUI |
| 이식성 | 로컬 실행만 | 웹 브라우저만 있으면 가능 |

## 💡 팁과 요령

1. **템플릿 활용**: 각 탭의 기본 템플릿을 참고하여 형식 학습
2. **실시간 검증**: 입력 후 잠시 기다리면 자동 검증됨
3. **에러 확인**: 오른쪽 하단 에러 패널에서 상세 정보 확인
4. **키보드 단축키**: Ctrl+S로 빠른 저장, Ctrl+Enter로 즉시 생성
5. **미리보기 활용**: wrapper 코드를 미리 확인하여 예상 결과 검토

---

**🎉 Verilog Wrapper Generator Web GUI로 더 쉽고 빠르게 wrapper를 생성하세요!**