module port_export_test_top (
    input   wire            clk,
    input   wire            reset,
    output  wire  [31:0]    cpu_debug_data,
    output  wire  [15:0]    cpu_debug_addr,
    output  wire            cpu_debug_valid,
    output  wire  [7:0]     uart_tx_data,
    output  wire            uart_tx_valid,
    input   wire  [7:0]     uart_rx_data,
    input   wire            uart_rx_valid
);

// Internal wires
    wire  [15:0]    w_cpu_core_addr_out_unconnected;
    wire            w_cpu_core_cache_ready_unconnected;
    wire  [31:0]    w_cpu_core_data_in_unconnected;
    wire  [31:0]    w_cpu_core_data_out_unconnected;
    wire  [15:0]    w_cpu_core_debug_addr_unconnected;
    wire  [31:0]    w_cpu_core_debug_data_unconnected;
    wire            w_cpu_core_debug_valid_unconnected;
    wire            w_cpu_core_read_enable_unconnected;
    wire  [7:0]     w_cpu_core_uart_rx_data;
    wire            w_cpu_core_uart_rx_valid;
    wire  [7:0]     w_cpu_core_uart_tx_data;
    wire  [7:0]     w_cpu_core_uart_tx_data_to_uart_module_tx_data_in;
    wire            w_cpu_core_uart_tx_valid;
    wire            w_cpu_core_uart_tx_valid_to_uart_module_tx_valid_in;
    wire            w_cpu_core_write_enable_unconnected;
    wire  [7:0]     w_uart_module_rx_data_out;
    wire  [7:0]     w_uart_module_rx_data_out_to_cpu_core_uart_rx_data;
    wire            w_uart_module_rx_valid_out;
    wire            w_uart_module_rx_valid_out_to_cpu_core_uart_rx_valid;
    wire  [7:0]     w_uart_module_tx_data_in;
    wire            w_uart_module_tx_valid_in;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu_core (
        .clk          (clk),
        .reset        (reset),
        .data_in      (w_cpu_core_data_in_unconnected),
        .data_out     (w_cpu_core_data_out_unconnected),
        .addr_out     (w_cpu_core_addr_out_unconnected),
        .read_enable  (w_cpu_core_read_enable_unconnected),
        .write_enable (w_cpu_core_write_enable_unconnected),
        .cache_ready  (w_cpu_core_cache_ready_unconnected),
        .uart_tx_data (w_cpu_core_uart_tx_data_to_uart_module_tx_data_in),
        .uart_tx_valid(w_cpu_core_uart_tx_valid_to_uart_module_tx_valid_in),
        .uart_rx_data (w_uart_module_rx_data_out_to_cpu_core_uart_rx_data),
        .uart_rx_valid(w_uart_module_rx_valid_out_to_cpu_core_uart_rx_valid),
        .debug_data   (cpu_debug_data),
        .debug_addr   (cpu_debug_addr),
        .debug_valid  (cpu_debug_valid)
    );

    uart #(.BAUD_RATE(115200)) uart_module (
        .clk         (clk),
        .reset       (reset),
        .tx_data_in  (w_cpu_core_uart_tx_data_to_uart_module_tx_data_in),
        .tx_valid_in (w_cpu_core_uart_tx_valid_to_uart_module_tx_valid_in),
        .tx_data     (uart_tx_data),
        .tx_valid    (uart_tx_valid),
        .rx_data     (uart_rx_data),
        .rx_valid    (uart_rx_valid),
        .rx_data_out (w_uart_module_rx_data_out_to_cpu_core_uart_rx_data),
        .rx_valid_out(w_uart_module_rx_valid_out_to_cpu_core_uart_rx_valid)
    );

endmodule
