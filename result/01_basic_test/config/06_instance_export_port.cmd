# Instance Port Export Configuration
# 인스턴스의 포트를 직접 탑 모듈 포트로 노출시킵니다.
# 형식: 인스턴스명.포트명 [-> 새로운포트명]
# 새로운 포트명을 지정하지 않으면 원래 포트명을 사용합니다.

[INSTANCE_EXPORT_PORTS]
# 예시: 인스턴스의 포트를 직접 탑 모듈로 노출
# cpu_core.debug_signal -> cpu_debug
# uart_if.status