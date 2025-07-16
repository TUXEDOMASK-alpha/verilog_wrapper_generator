// File containing multiple modules for testing

module simple_adder #(
    parameter WIDTH = 8
) (
    input [WIDTH-1:0] a,
    input [WIDTH-1:0] b,
    output [WIDTH:0] sum
);
    assign sum = a + b;
endmodule

module simple_multiplier #(
    parameter WIDTH = 8
) (
    input [WIDTH-1:0] a,
    input [WIDTH-1:0] b,
    output [2*WIDTH-1:0] product
);
    assign product = a * b;
endmodule

module counter #(
    parameter WIDTH = 8,
    localparam MAX_COUNT = 255
) (
    input clk,
    input reset,
    input enable,
    output reg [WIDTH-1:0] count,
    output reg overflow
);
    always @(posedge clk) begin
        if (reset) begin
            count <= 0;
            overflow <= 0;
        end else if (enable) begin
            if (count == MAX_COUNT) begin
                count <= 0;
                overflow <= 1;
            end else begin
                count <= count + 1;
                overflow <= 0;
            end
        end
    end
endmodule