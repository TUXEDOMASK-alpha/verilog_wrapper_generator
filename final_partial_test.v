module partial_test_system (
    input sys_clk,
    input sys_reset,
    input [7:0] input_data,
    output [7:0] output_data_high,
    output [7:0] output_data_low,
    output [1:0] status_low,
    output system_ready
);

// Internal wires
    wire [15:0] w_test_inst1_data_out_unconnected;
    wire [3:2] w_test_inst1_status_to_test_inst2_data_in_3_2_to_1_0;
    wire [3:0] w_test_inst1_status_unconnected;
    wire [15:0] w_test_inst2_data_out_unconnected;
    wire w_test_inst2_ready_unconnected;
    wire [3:0] w_test_inst2_status_unconnected;

// Tie connections
    assign w_test_inst2_ready = 1'bz;
    assign w_test_inst1_enable = 1'b1;
    assign w_test_inst2_enable = 1'b0;
    assign w_test_inst2_data_in = 1'b0;

// Partial bit connections
    assign output_data_high = w_test_inst1_data_out[15:8];
    assign output_data_low = w_test_inst1_data_out[7:0];
    assign status_low = w_test_inst1_status[1:0];
    assign w_test_inst2_data_in[1:0] = w_test_inst1_status[3:2];

    test_partial_module test_inst1 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(input_data),
        .data_out(w_test_inst1_data_out),
        .status(w_test_inst1_status),
        .enable(w_test_inst1_enable),
        .ready(system_ready)
    );

    test_partial_module test_inst2 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(w_test_inst2_data_in),
        .data_out(w_test_inst2_data_out_unconnected),
        .status(w_test_inst2_status_unconnected),
        .enable(w_test_inst2_enable),
        .ready(w_test_inst2_ready)
    );

endmodule