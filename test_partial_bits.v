module test_partial_bits (
);

// Internal wires
    wire [7:0] w_test_inst1_bidir_port;
    wire [7:0] w_test_inst1_bidir_port_unconnected;
    wire w_test_inst1_clk;
    wire [3:0] w_test_inst1_control;
    wire [3:0] w_test_inst1_control_unconnected;
    wire [7:0] w_test_inst1_data_in;
    wire [15:0] w_test_inst1_data_out;
    wire w_test_inst1_enable;
    wire w_test_inst1_enable_unconnected;
    wire w_test_inst1_ready;
    wire w_test_inst1_ready_unconnected;
    wire w_test_inst1_reset;
    wire [3:0] w_test_inst1_status;
    wire w_test_inst1_unused_inout1;
    wire w_test_inst1_unused_inout1_unconnected;
    wire w_test_inst1_unused_input1;
    wire w_test_inst1_unused_input1_unconnected;
    wire w_test_inst1_unused_input2;
    wire w_test_inst1_unused_input2_unconnected;
    wire w_test_inst1_unused_output1;
    wire w_test_inst1_unused_output1_unconnected;
    wire w_test_inst1_unused_output2;
    wire w_test_inst1_unused_output2_unconnected;
    wire w_test_inst1_valid;
    wire w_test_inst1_valid_unconnected;

// Partial bit connections
    assign output_data_high = w_test_inst1_data_out[15:8];
    assign output_data_low = w_test_inst1_data_out[7:0];
    assign status_low_bits = w_test_inst1_status[1:0];

    test_module_with_many_ports test_inst1 (
        .clk(sys_clk),
        .reset(sys_reset),
        .data_in(input_data),
        .enable(w_test_inst1_enable_unconnected),
        .control(w_test_inst1_control_unconnected),
        .data_out(w_test_inst1_data_out),
        .status(w_test_inst1_status),
        .valid(w_test_inst1_valid_unconnected),
        .ready(w_test_inst1_ready_unconnected),
        .bidir_port(w_test_inst1_bidir_port_unconnected),
        .unused_input1(w_test_inst1_unused_input1_unconnected),
        .unused_input2(w_test_inst1_unused_input2_unconnected),
        .unused_output1(w_test_inst1_unused_output1_unconnected),
        .unused_output2(w_test_inst1_unused_output2_unconnected),
        .unused_inout1(w_test_inst1_unused_inout1_unconnected)
    );

endmodule