[INSTANCE_CONNECTIONS]
cpu1.data_out -> cpu2.data_out
cpu1.invalid_port -> cpu2.invalid_port
cpu1.cache_ready -> TIE2
cpu1.uart_tx_data -> FLOAT