module multi_module_test_wrapper (
    input [15:0] sys_a,
    input [15:0] sys_b,
    output [16:0] sys_sum,
    input [7:0] sys_mult_a,
    input [7:0] sys_mult_b,
    output [15:0] sys_product,
    input sys_clk,
    input sys_reset,
    input sys_enable,
    output [3:0] sys_count,
    output sys_overflow
);

// Internal wires
    wire [15:0] w_adder_inst_a;
    wire [15:0] w_adder_inst_b;
    wire [16:0] w_adder_inst_sum;
    wire w_counter_inst_clk;
    wire [3:0] w_counter_inst_count;
    wire w_counter_inst_enable;
    wire w_counter_inst_overflow;
    wire w_counter_inst_reset;
    wire [7:0] w_mult_inst_a;
    wire [7:0] w_mult_inst_b;
    wire [15:0] w_mult_inst_product;

    simple_adder #(.WIDTH(16)) adder_inst (
        .a(sys_a),
        .b(sys_b),
        .sum(sys_sum)
    );

    simple_multiplier #(.WIDTH(8)) mult_inst (
        .a(sys_mult_a),
        .b(sys_mult_b),
        .product(sys_product)
    );

    counter #(.WIDTH(4)) counter_inst (
        .clk(sys_clk),
        .reset(sys_reset),
        .enable(sys_enable),
        .count(sys_count),
        .overflow(sys_overflow)
    );

endmodule