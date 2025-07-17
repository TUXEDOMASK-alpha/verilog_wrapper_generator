module counter #(
    parameter WIDTH = 4
)(
    input  wire              clk,
    input  wire              reset,
    input  wire              enable,
    output reg  [WIDTH-1:0]  count,
    output wire              overflow
);

always @(posedge clk) begin
    if (reset) begin
        count <= 0;
    end else if (enable) begin
        count <= count + 1;
    end
end

assign overflow = (count == {WIDTH{1'b1}}) && enable;

endmodule