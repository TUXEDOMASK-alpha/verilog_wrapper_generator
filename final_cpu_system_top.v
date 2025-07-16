module enhanced_cpu_system (
    input system_clock,
    input system_reset,
    input [7:0] uart_receive_data,
    output [7:0] uart_transmit_data,
    output uart_transmit_valid,
    input uart_receive_valid,
    output [31:0] cpu_debug_information,
    output [15:0] cpu_debug_address,
    output cpu_debug_enable,
    inout [15:0] memory_external_interface
);

// Internal wires
    wire w_cache_ctrl_clk;
    wire [15:0] w_cache_ctrl_cpu_addr_in;
    wire [31:0] w_cache_ctrl_cpu_data_in;
    wire [31:0] w_cache_ctrl_cpu_data_out;
    wire [31:0] w_cache_ctrl_cpu_data_out_to_cpu_core_data_in;
    wire w_cache_ctrl_cpu_read_en;
    wire w_cache_ctrl_cpu_ready;
    wire w_cache_ctrl_cpu_ready_to_cpu_core_cache_ready;
    wire w_cache_ctrl_cpu_write_en;
    wire [15:0] w_cache_ctrl_mem_addr_out;
    wire [15:0] w_cache_ctrl_mem_addr_out_to_main_memory_addr_in;
    wire [31:0] w_cache_ctrl_mem_data_in;
    wire [31:0] w_cache_ctrl_mem_data_out;
    wire [31:0] w_cache_ctrl_mem_data_out_to_main_memory_data_in;
    wire w_cache_ctrl_mem_read_en;
    wire w_cache_ctrl_mem_read_en_to_main_memory_read_enable;
    wire w_cache_ctrl_mem_ready;
    wire w_cache_ctrl_mem_write_en;
    wire w_cache_ctrl_mem_write_en_to_main_memory_write_enable;
    wire w_cache_ctrl_reset;
    wire [15:0] w_cpu_core_addr_out;
    wire [15:0] w_cpu_core_addr_out_to_cache_ctrl_cpu_addr_in;
    wire w_cpu_core_cache_ready;
    wire w_cpu_core_clk;
    wire [31:0] w_cpu_core_data_in;
    wire [31:0] w_cpu_core_data_out;
    wire [31:0] w_cpu_core_data_out_to_cache_ctrl_cpu_data_in;
    wire [15:0] w_cpu_core_debug_addr;
    wire [31:0] w_cpu_core_debug_data;
    wire w_cpu_core_debug_valid;
    wire w_cpu_core_read_enable;
    wire w_cpu_core_read_enable_to_cache_ctrl_cpu_read_en;
    wire w_cpu_core_reset;
    wire [7:0] w_cpu_core_uart_rx_data;
    wire w_cpu_core_uart_rx_valid;
    wire [7:0] w_cpu_core_uart_tx_data;
    wire [7:0] w_cpu_core_uart_tx_data_to_uart_if_tx_data_in;
    wire w_cpu_core_uart_tx_valid;
    wire w_cpu_core_uart_tx_valid_to_uart_if_tx_valid_in;
    wire w_cpu_core_write_enable;
    wire w_cpu_core_write_enable_to_cache_ctrl_cpu_write_en;
    wire [15:0] w_main_memory_addr_in;
    wire w_main_memory_clk;
    wire [31:0] w_main_memory_data_in;
    wire [31:0] w_main_memory_data_out;
    wire [31:0] w_main_memory_data_out_to_cache_ctrl_mem_data_in;
    wire [15:0] w_main_memory_external_bus;
    wire w_main_memory_read_enable;
    wire w_main_memory_ready;
    wire w_main_memory_ready_to_cache_ctrl_mem_ready;
    wire w_main_memory_reset;
    wire w_main_memory_write_enable;
    wire w_uart_if_clk;
    wire w_uart_if_reset;
    wire [7:0] w_uart_if_rx_data;
    wire [7:0] w_uart_if_rx_data_out;
    wire [7:0] w_uart_if_rx_data_out_to_cpu_core_uart_rx_data;
    wire w_uart_if_rx_valid;
    wire w_uart_if_rx_valid_out;
    wire w_uart_if_rx_valid_out_to_cpu_core_uart_rx_valid;
    wire [7:0] w_uart_if_tx_data;
    wire [7:0] w_uart_if_tx_data_in;
    wire w_uart_if_tx_valid;
    wire w_uart_if_tx_valid_in;

    cpu #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) cpu_core (
        .clk(system_clock),
        .reset(system_reset),
        .data_in(w_cache_ctrl_cpu_data_out_to_cpu_core_data_in),
        .data_out(w_cpu_core_data_out_to_cache_ctrl_cpu_data_in),
        .addr_out(w_cpu_core_addr_out_to_cache_ctrl_cpu_addr_in),
        .read_enable(w_cpu_core_read_enable_to_cache_ctrl_cpu_read_en),
        .write_enable(w_cpu_core_write_enable_to_cache_ctrl_cpu_write_en),
        .cache_ready(w_cache_ctrl_cpu_ready_to_cpu_core_cache_ready),
        .uart_tx_data(w_cpu_core_uart_tx_data_to_uart_if_tx_data_in),
        .uart_tx_valid(w_cpu_core_uart_tx_valid_to_uart_if_tx_valid_in),
        .uart_rx_data(w_uart_if_rx_data_out_to_cpu_core_uart_rx_data),
        .uart_rx_valid(w_uart_if_rx_valid_out_to_cpu_core_uart_rx_valid),
        .debug_data(cpu_debug_information),
        .debug_addr(cpu_debug_address),
        .debug_valid(cpu_debug_enable)
    );

    memory #(.MEM_SIZE(65536)) main_memory (
        .clk(system_clock),
        .reset(system_reset),
        .data_in(w_cache_ctrl_mem_data_out_to_main_memory_data_in),
        .addr_in(w_cache_ctrl_mem_addr_out_to_main_memory_addr_in),
        .read_enable(w_cache_ctrl_mem_read_en_to_main_memory_read_enable),
        .write_enable(w_cache_ctrl_mem_write_en_to_main_memory_write_enable),
        .data_out(w_main_memory_data_out_to_cache_ctrl_mem_data_in),
        .ready(w_main_memory_ready_to_cache_ctrl_mem_ready),
        .external_bus(memory_external_interface)
    );

    cache #(.CACHE_SIZE(1024), .LINE_SIZE(64)) cache_ctrl (
        .clk(system_clock),
        .reset(system_reset),
        .cpu_data_in(w_cpu_core_data_out_to_cache_ctrl_cpu_data_in),
        .cpu_addr_in(w_cpu_core_addr_out_to_cache_ctrl_cpu_addr_in),
        .cpu_read_en(w_cpu_core_read_enable_to_cache_ctrl_cpu_read_en),
        .cpu_write_en(w_cpu_core_write_enable_to_cache_ctrl_cpu_write_en),
        .cpu_data_out(w_cache_ctrl_cpu_data_out_to_cpu_core_data_in),
        .cpu_ready(w_cache_ctrl_cpu_ready_to_cpu_core_cache_ready),
        .mem_data_out(w_cache_ctrl_mem_data_out_to_main_memory_data_in),
        .mem_addr_out(w_cache_ctrl_mem_addr_out_to_main_memory_addr_in),
        .mem_read_en(w_cache_ctrl_mem_read_en_to_main_memory_read_enable),
        .mem_write_en(w_cache_ctrl_mem_write_en_to_main_memory_write_enable),
        .mem_data_in(w_main_memory_data_out_to_cache_ctrl_mem_data_in),
        .mem_ready(w_main_memory_ready_to_cache_ctrl_mem_ready)
    );

    uart #(.BAUD_RATE(115200)) uart_if (
        .clk(system_clock),
        .reset(system_reset),
        .tx_data_in(w_cpu_core_uart_tx_data_to_uart_if_tx_data_in),
        .tx_valid_in(w_cpu_core_uart_tx_valid_to_uart_if_tx_valid_in),
        .tx_data(uart_transmit_data),
        .tx_valid(uart_transmit_valid),
        .rx_data(uart_receive_data),
        .rx_valid(uart_receive_valid),
        .rx_data_out(w_uart_if_rx_data_out_to_cpu_core_uart_rx_data),
        .rx_valid_out(w_uart_if_rx_valid_out_to_cpu_core_uart_rx_valid)
    );

endmodule