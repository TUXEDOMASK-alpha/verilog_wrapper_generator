module cpu_system_top (
    input   wire            sys_clk,
    input   wire            sys_reset,
    input   wire  [7:0]     uart_rx_data,
    output  wire  [7:0]     uart_tx_data,
    output  wire            uart_tx_valid,
    input   wire            uart_rx_valid,
    output  wire  [31:0]    debug_data,
    output  wire  [15:0]    debug_addr,
    output  wire            debug_valid,
    inout   wire  [15:0]    external_bus
);

// Internal wires
    wire  [15:0]    w_cache_ctrl_cpu_addr_in;
    wire  [31:0]    w_cache_ctrl_cpu_data_in;
    wire  [31:0]    w_cache_ctrl_cpu_data_out;
    wire  [31:0]    w_cache_ctrl_cpu_data_out_to_cpu_core_data_in;
    wire            w_cache_ctrl_cpu_read_en;
    wire            w_cache_ctrl_cpu_ready;
    wire            w_cache_ctrl_cpu_ready_to_cpu_core_cache_ready;
    wire            w_cache_ctrl_cpu_write_en;
    wire  [15:0]    w_cache_ctrl_mem_addr_out;
    wire  [15:0]    w_cache_ctrl_mem_addr_out_to_main_memory_addr_in;
    wire  [31:0]    w_cache_ctrl_mem_data_in;
    wire  [31:0]    w_cache_ctrl_mem_data_out;
    wire  [31:0]    w_cache_ctrl_mem_data_out_to_main_memory_data_in;
    wire            w_cache_ctrl_mem_read_en;
    wire            w_cache_ctrl_mem_read_en_to_main_memory_read_enable;
    wire            w_cache_ctrl_mem_ready;
    wire            w_cache_ctrl_mem_write_en;
    wire            w_cache_ctrl_mem_write_en_to_main_memory_write_enable;
    wire  [15:0]    w_cpu_core_addr_out;
    wire  [15:0]    w_cpu_core_addr_out_to_cache_ctrl_cpu_addr_in;
    wire            w_cpu_core_cache_ready;
    wire  [31:0]    w_cpu_core_data_in;
    wire  [31:0]    w_cpu_core_data_out;
    wire  [31:0]    w_cpu_core_data_out_to_cache_ctrl_cpu_data_in;
    wire            w_cpu_core_read_enable;
    wire            w_cpu_core_read_enable_to_cache_ctrl_cpu_read_en;
    wire  [7:0]     w_cpu_core_uart_rx_data;
    wire            w_cpu_core_uart_rx_valid;
    wire  [7:0]     w_cpu_core_uart_tx_data;
    wire  [7:0]     w_cpu_core_uart_tx_data_to_uart_if_tx_data_in;
    wire            w_cpu_core_uart_tx_valid;
    wire            w_cpu_core_uart_tx_valid_to_uart_if_tx_valid_in;
    wire            w_cpu_core_write_enable;
    wire            w_cpu_core_write_enable_to_cache_ctrl_cpu_write_en;
    wire  [15:0]    w_main_memory_addr_in;
    wire  [31:0]    w_main_memory_data_in;
    wire  [31:0]    w_main_memory_data_out;
    wire  [31:0]    w_main_memory_data_out_to_cache_ctrl_mem_data_in;
    wire            w_main_memory_read_enable;
    wire            w_main_memory_ready;
    wire            w_main_memory_ready_to_cache_ctrl_mem_ready;
    wire            w_main_memory_write_enable;
    wire  [7:0]     w_uart_if_rx_data_out;
    wire  [7:0]     w_uart_if_rx_data_out_to_cpu_core_uart_rx_data;
    wire            w_uart_if_rx_valid_out;
    wire            w_uart_if_rx_valid_out_to_cpu_core_uart_rx_valid;
    wire  [7:0]     w_uart_if_tx_data_in;
    wire            w_uart_if_tx_valid_in;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu_core (
        .clk          (sys_clk),
        .reset        (sys_reset),
        .data_in      (w_cache_ctrl_cpu_data_out_to_cpu_core_data_in),
        .data_out     (w_cpu_core_data_out_to_cache_ctrl_cpu_data_in),
        .addr_out     (w_cpu_core_addr_out_to_cache_ctrl_cpu_addr_in),
        .read_enable  (w_cpu_core_read_enable_to_cache_ctrl_cpu_read_en),
        .write_enable (w_cpu_core_write_enable_to_cache_ctrl_cpu_write_en),
        .cache_ready  (w_cache_ctrl_cpu_ready_to_cpu_core_cache_ready),
        .uart_tx_data (w_cpu_core_uart_tx_data_to_uart_if_tx_data_in),
        .uart_tx_valid(w_cpu_core_uart_tx_valid_to_uart_if_tx_valid_in),
        .uart_rx_data (w_uart_if_rx_data_out_to_cpu_core_uart_rx_data),
        .uart_rx_valid(w_uart_if_rx_valid_out_to_cpu_core_uart_rx_valid),
        .debug_data   (debug_data),
        .debug_addr   (debug_addr),
        .debug_valid  (debug_valid)
    );

    memory #(.MEM_SIZE(65536)) main_memory (
        .clk         (sys_clk),
        .reset       (sys_reset),
        .data_in     (w_cache_ctrl_mem_data_out_to_main_memory_data_in),
        .addr_in     (w_cache_ctrl_mem_addr_out_to_main_memory_addr_in),
        .read_enable (w_cache_ctrl_mem_read_en_to_main_memory_read_enable),
        .write_enable(w_cache_ctrl_mem_write_en_to_main_memory_write_enable),
        .data_out    (w_main_memory_data_out_to_cache_ctrl_mem_data_in),
        .ready       (w_main_memory_ready_to_cache_ctrl_mem_ready),
        .external_bus(external_bus)
    );

    cache #(.CACHE_SIZE(1024), .LINE_SIZE(64)) cache_ctrl (
        .clk         (sys_clk),
        .reset       (sys_reset),
        .cpu_data_in (w_cpu_core_data_out_to_cache_ctrl_cpu_data_in),
        .cpu_addr_in (w_cpu_core_addr_out_to_cache_ctrl_cpu_addr_in),
        .cpu_read_en (w_cpu_core_read_enable_to_cache_ctrl_cpu_read_en),
        .cpu_write_en(w_cpu_core_write_enable_to_cache_ctrl_cpu_write_en),
        .cpu_data_out(w_cache_ctrl_cpu_data_out_to_cpu_core_data_in),
        .cpu_ready   (w_cache_ctrl_cpu_ready_to_cpu_core_cache_ready),
        .mem_data_out(w_cache_ctrl_mem_data_out_to_main_memory_data_in),
        .mem_addr_out(w_cache_ctrl_mem_addr_out_to_main_memory_addr_in),
        .mem_read_en (w_cache_ctrl_mem_read_en_to_main_memory_read_enable),
        .mem_write_en(w_cache_ctrl_mem_write_en_to_main_memory_write_enable),
        .mem_data_in (w_main_memory_data_out_to_cache_ctrl_mem_data_in),
        .mem_ready   (w_main_memory_ready_to_cache_ctrl_mem_ready)
    );

    uart #(.BAUD_RATE(115200)) uart_if (
        .clk         (sys_clk),
        .reset       (sys_reset),
        .tx_data_in  (w_cpu_core_uart_tx_data_to_uart_if_tx_data_in),
        .tx_valid_in (w_cpu_core_uart_tx_valid_to_uart_if_tx_valid_in),
        .tx_data     (uart_tx_data),
        .tx_valid    (uart_tx_valid),
        .rx_data     (uart_rx_data),
        .rx_valid    (uart_rx_valid),
        .rx_data_out (w_uart_if_rx_data_out_to_cpu_core_uart_rx_data),
        .rx_valid_out(w_uart_if_rx_valid_out_to_cpu_core_uart_rx_valid)
    );

endmodule
