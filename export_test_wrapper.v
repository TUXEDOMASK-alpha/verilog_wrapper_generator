module export_test_wrapper (
    input [7:0] sys_a,
    input [7:0] sys_b,
    output [8:0] sum,
    input ext_clk,
    input ext_reset,
    input ext_enable,
    output [3:0] ext_count,
    output ext_overflow
);

// Internal wires
    wire [8:0] w_adder1_sum_unconnected;
    wire w_counter1_clk_unconnected;
    wire [3:0] w_counter1_count_unconnected;
    wire w_counter1_enable_unconnected;
    wire w_counter1_overflow_unconnected;
    wire w_counter1_reset_unconnected;

    simple_adder #(.WIDTH(8)) adder1 (
        .a(sys_a),
        .b(sys_b),
        .sum(sum)
    );

    counter #(.WIDTH(4)) counter1 (
        .clk(ext_clk),
        .reset(ext_reset),
        .enable(ext_enable),
        .count(ext_count),
        .overflow(ext_overflow)
    );

endmodule