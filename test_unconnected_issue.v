module test_module (
    input clk,
    input reset,
    input enable,
    input [7:0] data_in,
    output [7:0] data_out,
    output valid,
    output [3:0] debug,
    input unused_input,
    output unused_output
);
    assign data_out = data_in;
    assign valid = enable;
    assign debug = 4'b0000;
    assign unused_output = 1'b0;
endmodule