module tie_connections_test (
    input   wire            clk,
    input   wire            reset,
    output  wire  [31:0]    cpu_debug_data,
    output  wire  [7:0]     counter_value
);

// Internal wires
    wire            w_counter1_enable;
    wire            w_counter1_overflow_unconnected;
    wire  [15:0]    w_cpu1_addr_out_unconnected;
    wire            w_cpu1_cache_ready;
    wire  [31:0]    w_cpu1_data_in;
    wire  [31:0]    w_cpu1_data_out_unconnected;
    wire  [15:0]    w_cpu1_debug_addr_unconnected;
    wire            w_cpu1_debug_valid_unconnected;
    wire            w_cpu1_read_enable_unconnected;
    wire  [7:0]     w_cpu1_uart_rx_data;
    wire            w_cpu1_uart_rx_valid;
    wire  [7:0]     w_cpu1_uart_tx_data_unconnected;
    wire            w_cpu1_uart_tx_valid_unconnected;
    wire            w_cpu1_write_enable_unconnected;

// Tie connections
    assign w_cpu1_cache_ready_tied_to_0 = 1'b0;
    assign w_cpu1_uart_rx_valid_tied_to_0 = 1'b0;
    assign w_counter1_enable_tied_to_1 = 1'b1;
    assign w_cpu1_data_in_float = 1'bz;
    assign w_cpu1_uart_rx_data_float = 1'bz;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu1 (
        .clk          (clk),
        .reset        (reset),
        .data_in      (w_cpu1_data_in_float),
        .data_out     (w_cpu1_data_out_unconnected),
        .addr_out     (w_cpu1_addr_out_unconnected),
        .read_enable  (w_cpu1_read_enable_unconnected),
        .write_enable (w_cpu1_write_enable_unconnected),
        .cache_ready  (w_cpu1_cache_ready_tied_to_0),
        .uart_tx_data (w_cpu1_uart_tx_data_unconnected),
        .uart_tx_valid(w_cpu1_uart_tx_valid_unconnected),
        .uart_rx_data (w_cpu1_uart_rx_data_float),
        .uart_rx_valid(w_cpu1_uart_rx_valid_tied_to_0),
        .debug_data   (cpu_debug_data),
        .debug_addr   (w_cpu1_debug_addr_unconnected),
        .debug_valid  (w_cpu1_debug_valid_unconnected)
    );

    counter #(.WIDTH(8)) counter1 (
        .clk     (clk),
        .reset   (reset),
        .enable  (w_counter1_enable_tied_to_1),
        .count   (counter_value),
        .overflow(w_counter1_overflow_unconnected)
    );

endmodule
