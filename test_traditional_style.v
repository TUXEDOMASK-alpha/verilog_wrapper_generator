// Test traditional style port declaration
module test_traditional_style (
    clk,
    reset,
    reg_data,
    wire_data,
    output_reg,
    output_wire,
    reg_enable,
    wire_enable
);

input wire clk;
input wire reset;
input wire [7:0] reg_data;
input wire [7:0] wire_data;
output reg [7:0] output_reg;
output wire [7:0] output_wire;
input reg_enable;
input wire_enable;

// Simple logic
assign output_wire = wire_data;

always @(posedge clk) begin
    if (reset) begin
        output_reg <= 0;
    end else begin
        output_reg <= reg_data;
    end
end

endmodule