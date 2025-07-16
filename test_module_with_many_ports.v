module test_module_with_many_ports (
    input clk,
    input reset,
    input [7:0] data_in,
    input enable,
    input [3:0] control,
    output reg [15:0] data_out,
    output reg [3:0] status,
    output reg valid,
    output reg ready,
    inout [7:0] bidir_port,
    input unused_input1,
    input unused_input2,
    output unused_output1,
    output unused_output2,
    inout unused_inout1
);

    always @(posedge clk) begin
        if (reset) begin
            data_out <= 16'h0;
            status <= 4'h0;
            valid <= 1'b0;
            ready <= 1'b0;
        end else if (enable) begin
            data_out <= {data_in, 8'h00};
            status <= control;
            valid <= 1'b1;
            ready <= 1'b1;
        end
    end

endmodule