module param_test_top (
    input   wire            clk,
    input   wire            reset,
    input   wire  [7:0]     data_a,
    input   wire  [7:0]     data_b,
    output  wire  [8:0]     sum_out,
    output  wire  [15:0]    mem_data_out,
    output  wire  [31:0]    cpu_debug
);

// Internal wires
    wire  [15:0]    w_cpu_unit_addr_out_unconnected;
    wire            w_cpu_unit_cache_ready_unconnected;
    wire  [31:0]    w_cpu_unit_data_in_unconnected;
    wire  [31:0]    w_cpu_unit_data_out_unconnected;
    wire  [15:0]    w_cpu_unit_debug_addr_unconnected;
    wire            w_cpu_unit_debug_valid_unconnected;
    wire            w_cpu_unit_read_enable_unconnected;
    wire  [7:0]     w_cpu_unit_uart_rx_data_unconnected;
    wire            w_cpu_unit_uart_rx_valid_unconnected;
    wire  [7:0]     w_cpu_unit_uart_tx_data_unconnected;
    wire            w_cpu_unit_uart_tx_valid_unconnected;
    wire            w_cpu_unit_write_enable_unconnected;
    wire  [15:0]    w_main_mem_addr_in_unconnected;
    wire  [31:0]    w_main_mem_data_in_unconnected;
    wire  [15:0]    w_main_mem_external_bus_unconnected;
    wire            w_main_mem_read_enable_unconnected;
    wire            w_main_mem_ready_unconnected;
    wire            w_main_mem_write_enable_unconnected;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu_unit (
        .clk          (clk),
        .reset        (reset),
        .data_in      (w_cpu_unit_data_in_unconnected),
        .data_out     (w_cpu_unit_data_out_unconnected),
        .addr_out     (w_cpu_unit_addr_out_unconnected),
        .read_enable  (w_cpu_unit_read_enable_unconnected),
        .write_enable (w_cpu_unit_write_enable_unconnected),
        .cache_ready  (w_cpu_unit_cache_ready_unconnected),
        .uart_tx_data (w_cpu_unit_uart_tx_data_unconnected),
        .uart_tx_valid(w_cpu_unit_uart_tx_valid_unconnected),
        .uart_rx_data (w_cpu_unit_uart_rx_data_unconnected),
        .uart_rx_valid(w_cpu_unit_uart_rx_valid_unconnected),
        .debug_data   (cpu_debug),
        .debug_addr   (w_cpu_unit_debug_addr_unconnected),
        .debug_valid  (w_cpu_unit_debug_valid_unconnected)
    );

    memory #(.MEM_SIZE(1024*64)) main_mem (
        .clk         (clk),
        .reset       (reset),
        .data_in     (w_main_mem_data_in_unconnected),
        .addr_in     (w_main_mem_addr_in_unconnected),
        .read_enable (w_main_mem_read_enable_unconnected),
        .write_enable(w_main_mem_write_enable_unconnected),
        .data_out    (mem_data_out),
        .ready       (w_main_mem_ready_unconnected),
        .external_bus(w_main_mem_external_bus_unconnected)
    );

    simple_adder #(.WIDTH(8)) adder_8bit (
        .a  (data_a),
        .b  (data_b),
        .sum(sum_out)
    );

endmodule
