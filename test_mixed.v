module test_mixed (
    clk,
    reset,
    data_in,
    addr_in,
    data_out,
    addr_out,
    valid,
    ready
);

    input clk, reset;
    input [7:0] data_in, addr_in;
    output [15:0] data_out;
    output [7:0] addr_out;
    output valid, ready;
    
    reg [15:0] data_out;
    reg [7:0] addr_out;

    always @(posedge clk) begin
        if (reset) begin
            data_out <= 16'h0;
            addr_out <= 8'h0;
        end else begin
            data_out <= {data_in, 8'h00};
            addr_out <= addr_in;
        end
    end
    
    assign valid = |data_out;
    assign ready = |addr_out;

endmodule