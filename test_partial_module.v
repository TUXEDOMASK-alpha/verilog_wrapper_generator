module test_partial_module (
    input clk,
    input reset,
    input [7:0] data_in,
    output reg [15:0] data_out,
    output reg [3:0] status,
    input enable,
    output ready
);

    always @(posedge clk) begin
        if (reset) begin
            data_out <= 16'h0;
            status <= 4'h0;
        end else if (enable) begin
            data_out <= {data_in, 8'h00};
            status <= data_in[3:0];
        end
    end
    
    assign ready = |data_out;

endmodule