// Test module with edge cases in port names
module test_edge_cases (
    input wire clk,
    input reg reset,
    input wire [7:0] reg_data,
    input reg [7:0] wire_data,
    output reg [7:0] output_reg,
    output wire [7:0] output_wire,
    input reg_enable,
    input wire_enable,
    output reg_valid,
    output wire_valid,
    input [7:0] input_reg,
    input [7:0] input_wire,
    output [7:0] output_reg_data,
    output [7:0] output_wire_data
);

// Simple assignments
assign output_wire = wire_data;
assign wire_valid = wire_enable;
assign output_wire_data = input_wire;

always @(posedge clk) begin
    if (reset) begin
        output_reg <= 0;
        reg_valid <= 0;
        output_reg_data <= 0;
    end else begin
        output_reg <= reg_data;
        reg_valid <= reg_enable;
        output_reg_data <= input_reg;
    end
end

endmodule