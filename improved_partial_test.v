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
    wire [15:0] test_inst1_data_out;
    wire [3:0] test_inst1_status;
    wire [7:0] test_inst2_data_in;
    wire [15:0] test_inst2_data_out;
    wire test_inst2_ready;
    wire [3:0] test_inst2_status;

// Tie connections
    assign test_inst2_ready = 1'bz;
    assign test_inst1_enable = 1'b1;
    assign test_inst2_enable = 1'b0;
    assign test_inst2_data_in = 1'b0;

// Partial bit connections
    assign output_data_high = test_inst1_data_out[15:8];
    assign output_data_low = test_inst1_data_out[7:0];
    assign status_low = test_inst1_status[1:0];
    assign test_inst2_data_in[1:0] = test_inst1_status[3:2];

    test_partial_module test_inst1 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(input_data),
        .data_out(test_inst1_data_out),
        .status(test_inst1_status),
        .enable(test_inst1_enable),
        .ready(system_ready)
    );

    test_partial_module test_inst2 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(test_inst2_data_in),
        .data_out(test_inst2_data_out),
        .status(test_inst2_status),
        .enable(test_inst2_enable),
        .ready(test_inst2_ready)
    );

endmodule