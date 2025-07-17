[INSTANCES]
cpu_core | cpu.v | cpu | DATA_WIDTH=32, ADDR_WIDTH=16
main_memory | memory.v | memory | MEM_SIZE=65536
cache_ctrl | cache.v | cache | CACHE_SIZE=1024, LINE_SIZE=64
uart_if | uart.v | uart | BAUD_RATE=115200
adder_unit | simple_adder.v | simple_adder | WIDTH=8
counter_inst | counter.v | counter | WIDTH=16