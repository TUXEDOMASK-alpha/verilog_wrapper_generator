module param_test_wrapper (
);

// Internal wires
    wire [11:0] w_param_inst_addr;
    wire w_param_inst_clk;
    wire [15:0] w_param_inst_data_in;
    wire [15:0] w_param_inst_data_out;
    wire w_param_inst_ready;
    wire w_param_inst_reset;

    test_module_with_params #(.DATA_WIDTH(16), .ADDR_WIDTH(12), .DEPTH(512)) param_inst (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(sys_data_in),
        .addr(sys_addr),
        .data_out(sys_data_out),
        .ready(sys_ready)
    );

endmodule