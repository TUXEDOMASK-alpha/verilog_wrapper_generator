module final_comprehensive_test (
);

// Internal wires
    wire [7:0] w_test_inst1_bidir_port;
    wire w_test_inst1_clk;
    wire [3:0] w_test_inst1_control;
    wire [7:0] w_test_inst1_data_in;
    wire [15:0] w_test_inst1_data_out;
    wire w_test_inst1_enable;
    wire w_test_inst1_ready;
    wire w_test_inst1_ready_to_test_inst2_control_to_1;
    wire w_test_inst1_reset;
    wire [3:0] w_test_inst1_status;
    wire [3:2] w_test_inst1_status_to_test_inst2_data_in_3_2_to_1_0;
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
    wire [7:0] w_test_inst2_bidir_port;
    wire w_test_inst2_clk;
    wire [3:0] w_test_inst2_control;
    wire [7:0] w_test_inst2_data_in;
    wire [15:0] w_test_inst2_data_out;
    wire [15:0] w_test_inst2_data_out_unconnected;
    wire w_test_inst2_enable;
    wire w_test_inst2_ready;
    wire w_test_inst2_ready_unconnected;
    wire w_test_inst2_reset;
    wire [3:0] w_test_inst2_status;
    wire [3:0] w_test_inst2_status_unconnected;
    wire w_test_inst2_unused_inout1;
    wire w_test_inst2_unused_inout1_unconnected;
    wire w_test_inst2_unused_input1;
    wire w_test_inst2_unused_input1_unconnected;
    wire w_test_inst2_unused_input2;
    wire w_test_inst2_unused_input2_unconnected;
    wire w_test_inst2_unused_output1;
    wire w_test_inst2_unused_output1_unconnected;
    wire w_test_inst2_unused_output2;
    wire w_test_inst2_unused_output2_unconnected;
    wire w_test_inst2_valid;
    wire w_test_inst2_valid_unconnected;

// Tie connections
    assign w_test_inst1_enable_tied_to_1 = 1'b1;
    assign w_test_inst1_control_tied_to_0 = 4'b0000;
    assign w_test_inst2_enable_tied_to_0 = 1'b0;
    assign w_test_inst2_data_in_tied_to_1 = 8'b11111111;
    assign w_test_inst2_bidir_port_float = 8'bz;

// Partial bit connections
    assign main_data_out_high = w_test_inst1_data_out[15:8];
    assign main_data_out_low = w_test_inst1_data_out[7:0];
    assign main_status_low = w_test_inst1_status[1:0];
    assign main_bidir_lower = w_test_inst1_bidir_port[3:0];
    assign w_test_inst2_control[1] = w_test_inst1_ready;
    assign w_test_inst2_data_in[1:0] = w_test_inst1_status[3:2];

    test_module_with_many_ports test_inst1 (
        .clk(main_clk),
        .reset(main_reset),
        .data_in(main_data_in),
        .enable(w_test_inst1_enable_tied_to_1),
        .control(w_test_inst1_control_tied_to_0),
        .data_out(w_test_inst1_data_out),
        .status(w_test_inst1_status),
        .valid(main_valid),
        .ready(w_test_inst1_ready_to_test_inst2_control_to_1),
        .bidir_port(w_test_inst1_bidir_port),
        .unused_input1(w_test_inst1_unused_input1_unconnected),
        .unused_input2(w_test_inst1_unused_input2_unconnected),
        .unused_output1(w_test_inst1_unused_output1_unconnected),
        .unused_output2(w_test_inst1_unused_output2_unconnected),
        .unused_inout1(w_test_inst1_unused_inout1_unconnected)
    );

    test_module_with_many_ports test_inst2 (
        .clk(main_clk),
        .reset(main_reset),
        .data_in(w_test_inst2_data_in_tied_to_1),
        .enable(w_test_inst2_enable_tied_to_0),
        .control(w_test_inst1_ready_to_test_inst2_control_to_1),
        .data_out(w_test_inst2_data_out_unconnected),
        .status(w_test_inst2_status_unconnected),
        .valid(w_test_inst2_valid_unconnected),
        .ready(w_test_inst2_ready_unconnected),
        .bidir_port(w_test_inst2_bidir_port_float),
        .unused_input1(w_test_inst2_unused_input1_unconnected),
        .unused_input2(w_test_inst2_unused_input2_unconnected),
        .unused_output1(w_test_inst2_unused_output1_unconnected),
        .unused_output2(w_test_inst2_unused_output2_unconnected),
        .unused_inout1(w_test_inst2_unused_inout1_unconnected)
    );

endmodule