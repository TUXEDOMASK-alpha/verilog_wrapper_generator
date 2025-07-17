[INSTANCE_CONNECTIONS]
# Test TIE0 connections - tie input ports to logic 0
cpu1.cache_ready -> TIE0
cpu1.uart_rx_valid -> TIE0

# Test TIE1 connections - tie input ports to logic 1
counter1.enable -> TIE1

# Test FLOAT connections - leave input ports floating
cpu1.data_in -> FLOAT
cpu1.uart_rx_data -> FLOAT