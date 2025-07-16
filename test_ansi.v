module test_ansi (
    input clk,
    input reset,
    input [7:0] data_in,
    output reg [15:0] data_out,
    output wire valid,
    inout [3:0] bidir
);

    always @(posedge clk) begin
        if (reset) begin
            data_out <= 16'h0;
        end else begin
            data_out <= {data_in, 8'h00};
        end
    end
    
    assign valid = |data_out;

endmodule