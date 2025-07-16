module wire_test_wrapper (
    input [7:0] sys_a,
    input [7:0] sys_b,
    output [8:0] sys_sum1,
    output [8:0] sys_sum2,
    input sys_clk,
    input sys_reset,
    output [3:0] sys_count
);

// Internal wires
    wire [7:0] w_adder2_a;
    wire [7:0] w_adder2_b;
    wire [8:0] w_adder2_sum;
    wire [8:0] w_adder2_sum_to_counter1_enable;
    wire w_counter1_enable;
    wire w_counter1_overflow_unconnected;

// Tie connections
    assign w_adder2_a_tied_to_0 = 1'b0;
    assign w_adder2_b_tied_to_1 = 1'b1;

// Partial bit connections
    assign sys_count[2:0][2:0] = w_counter1_count[2:0];

    simple_adder #(.WIDTH(8)) adder1 (
        .a(sys_a),
        .b(sys_b),
        .sum(sys_sum1)
    );

    simple_adder #(.WIDTH(8)) adder2 (
        .a(w_adder2_a_tied_to_0),
        .b(w_adder2_b_tied_to_1),
        .sum(w_adder2_sum_to_counter1_enable)
    );

    counter #(.WIDTH(4)) counter1 (
        .clk(sys_clk),
        .reset(sys_reset),
        .enable(w_adder2_sum_to_counter1_enable),
        .count(sys_count),
        .overflow(w_counter1_overflow_unconnected)
    );

endmodule