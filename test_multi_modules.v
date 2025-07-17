// Test file with multiple modules and complex parameters
module adder #(
    parameter WIDTH = 8,
    localparam RESULT_WIDTH = WIDTH + 1
)(
    input  [WIDTH-1:0] a,
    input  [WIDTH-1:0] b,
    output [RESULT_WIDTH-1:0] sum
);
    assign sum = a + b;
endmodule

module multiplier #(
    parameter A_WIDTH = 8,
    parameter B_WIDTH = 8,
    localparam PRODUCT_WIDTH = A_WIDTH + B_WIDTH,
    localparam OVERFLOW_BIT = PRODUCT_WIDTH > 16 ? 1 : 0
)(
    input  [A_WIDTH-1:0] a,
    input  [B_WIDTH-1:0] b,
    output [PRODUCT_WIDTH-1:0] product,
    output overflow
);
    assign product = a * b;
    assign overflow = OVERFLOW_BIT;
endmodule

module divider #(
    parameter WIDTH = 16,
    localparam QUOTIENT_WIDTH = WIDTH,
    localparam REMAINDER_WIDTH = WIDTH/2
)(
    input  [WIDTH-1:0] dividend,
    input  [WIDTH-1:0] divisor,
    output [QUOTIENT_WIDTH-1:0] quotient,
    output [REMAINDER_WIDTH-1:0] remainder
);
    assign quotient = dividend / divisor;
    assign remainder = dividend % divisor;
endmodule