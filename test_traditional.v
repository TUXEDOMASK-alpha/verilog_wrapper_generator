module test_traditional (
    clk,
    reset,
    data_in,
    data_out,
    valid,
    bidir
);

    input clk;
    input reset;
    input [7:0] data_in;
    output [15:0] data_out;
    output valid;
    inout [3:0] bidir;
    
    reg [15:0] data_out;
    wire valid;

    always @(posedge clk) begin
        if (reset) begin
            data_out <= 16'h0;
        end else begin
            data_out <= {data_in, 8'h00};
        end
    end
    
    assign valid = |data_out;

endmodule