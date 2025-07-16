module cpu_system_top (
    input sys_clk,
    input sys_reset,
    input [7:0] uart_rx_data,
    output [7:0] uart_tx_data,
    output uart_tx_valid,
    input uart_rx_valid,
    output [31:0] debug_data,
    output [15:0] debug_addr,
    output debug_valid,
    inout [15:0] external_bus
);

// Internal wires
    wire [15:0] cache_ctrl_cpu_addr_in;
    wire [31:0] cache_ctrl_cpu_data_in;
    wire [31:0] cache_ctrl_cpu_data_out;
    wire cache_ctrl_cpu_read_en;
    wire cache_ctrl_cpu_ready;
    wire cache_ctrl_cpu_write_en;
    wire [15:0] cache_ctrl_mem_addr_out;
    wire [31:0] cache_ctrl_mem_data_in;
    wire [31:0] cache_ctrl_mem_data_out;
    wire cache_ctrl_mem_read_en;
    wire cache_ctrl_mem_ready;
    wire cache_ctrl_mem_write_en;
    wire [15:0] cpu_core_addr_out;
    wire cpu_core_cache_ready;
    wire [31:0] cpu_core_data_in;
    wire [31:0] cpu_core_data_out;
    wire cpu_core_read_enable;
    wire [7:0] cpu_core_uart_rx_data;
    wire cpu_core_uart_rx_valid;
    wire [7:0] cpu_core_uart_tx_data;
    wire cpu_core_uart_tx_valid;
    wire cpu_core_write_enable;
    wire [15:0] main_memory_addr_in;
    wire [31:0] main_memory_data_in;
    wire [31:0] main_memory_data_out;
    wire main_memory_read_enable;
    wire main_memory_ready;
    wire main_memory_write_enable;
    wire [7:0] uart_if_rx_data_out;
    wire uart_if_rx_valid_out;
    wire [7:0] uart_if_tx_data_in;
    wire uart_if_tx_valid_in;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu_core (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(cache_ctrl_cpu_data_out),
        .data_out(cache_ctrl_cpu_data_in),
        .addr_out(cache_ctrl_cpu_addr_in),
        .read_enable(cache_ctrl_cpu_read_en),
        .write_enable(cache_ctrl_cpu_write_en),
        .cache_ready(cache_ctrl_cpu_ready),
        .uart_tx_data(uart_if_tx_data_in),
        .uart_tx_valid(uart_if_tx_valid_in),
        .uart_rx_data(uart_if_rx_data_out),
        .uart_rx_valid(uart_if_rx_valid_out),
        .debug_data(debug_data),
        .debug_addr(debug_addr),
        .debug_valid(debug_valid)
    );

    memory #(.MEM_SIZE(65536)) main_memory (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(cache_ctrl_mem_data_out),
        .addr_in(cache_ctrl_mem_addr_out),
        .read_enable(cache_ctrl_mem_read_en),
        .write_enable(cache_ctrl_mem_write_en),
        .data_out(cache_ctrl_mem_data_in),
        .ready(cache_ctrl_mem_ready),
        .external_bus(external_bus)
    );

    cache #(.CACHE_SIZE(1024), .LINE_SIZE(64)) cache_ctrl (
        .clk(sys_clk),
        .reset(sys_reset),
        .cpu_data_in(cpu_core_data_out),
        .cpu_addr_in(cpu_core_addr_out),
        .cpu_read_en(cpu_core_read_enable),
        .cpu_write_en(cpu_core_write_enable),
        .cpu_data_out(cpu_core_data_in),
        .cpu_ready(cpu_core_cache_ready),
        .mem_data_out(main_memory_data_in),
        .mem_addr_out(main_memory_addr_in),
        .mem_read_en(main_memory_read_enable),
        .mem_write_en(main_memory_write_enable),
        .mem_data_in(main_memory_data_out),
        .mem_ready(main_memory_ready)
    );

    uart #(.BAUD_RATE(115200)) uart_if (
        .clk(sys_clk),
        .reset(sys_reset),
        .tx_data_in(cpu_core_uart_tx_data),
        .tx_valid_in(cpu_core_uart_tx_valid),
        .tx_data(uart_tx_data),
        .tx_valid(uart_tx_valid),
        .rx_data(uart_rx_data),
        .rx_valid(uart_rx_valid),
        .rx_data_out(cpu_core_uart_rx_data),
        .rx_valid_out(cpu_core_uart_rx_valid)
    );

endmodule