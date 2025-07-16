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

    test_partial_module test_inst1 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(input_data),
        .data_out(output_data_high),
        .status(status_low),
        .enable(TIE1),
        .ready(system_ready)
    );

    test_partial_module test_inst2 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(TIE0),
        .data_out(test_inst2_data_out),
        .status(test_inst2_status),
        .enable(TIE0),
        .ready(1'bz)
    );

endmodule