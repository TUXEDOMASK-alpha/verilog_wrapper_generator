// Test module with port names containing 'reg' and other keywords
module test_reg_port_names #(
    parameter WIDTH = 8
) (
    input wire clk,
    input wire reset,
    input wire [WIDTH-1:0] reg_data,
    input wire [WIDTH-1:0] wire_data,
    output reg [WIDTH-1:0] output_reg,
    output wire [WIDTH-1:0] output_wire,
    input wire reg_enable,
    input wire wire_enable,
    output reg reg_valid,
    output wire wire_valid
);

// Simple logic
always @(posedge clk) begin
    if (reset) begin
        output_reg <= 0;
        reg_valid <= 0;
    end else begin
        output_reg <= reg_data;
        reg_valid <= reg_enable;
    end
end

assign output_wire = wire_data;
assign wire_valid = wire_enable;

endmodule