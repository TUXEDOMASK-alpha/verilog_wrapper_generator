module mixed_param_test_wrapper (
    input sys_clk,
    input sys_reset,
    input [15:0] sys_data_in,
    input [11:0] sys_addr,
    output [47:0] sys_extended_data_out,
    output [15:0] sys_normal_data_out,
    output [23:0] sys_full_addr,
    output [3:0] sys_status,
    input sys_enable,
    output sys_ready
);

// Internal wires
    wire [11:0] w_mixed_param_inst_addr;
    wire w_mixed_param_inst_clk;
    wire [15:0] w_mixed_param_inst_data_in;
    wire w_mixed_param_inst_enable;
    wire [47:0] w_mixed_param_inst_extended_data_out;
    wire [23:0] w_mixed_param_inst_full_addr;
    wire [15:0] w_mixed_param_inst_normal_data_out;
    wire w_mixed_param_inst_ready;
    wire w_mixed_param_inst_reset;
    wire [3:0] w_mixed_param_inst_status;

    test_module_with_mixed_params #(.DATA_WIDTH(16), .ADDR_WIDTH(12), .DEPTH(512)) mixed_param_inst (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(sys_data_in),
        .addr(sys_addr),
        .extended_data_out(sys_extended_data_out),
        .normal_data_out(sys_normal_data_out),
        .full_addr(sys_full_addr),
        .status(sys_status),
        .enable(sys_enable),
        .ready(sys_ready)
    );

endmodule