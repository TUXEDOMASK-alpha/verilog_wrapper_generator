// Test module with various Verilog keywords in port names
module test_keyword_ports (
    input wire clk,
    input wire reset,
    
    // Basic keywords that might be confused
    input wire input_data,
    output wire output_data,
    inout wire inout_signal,
    
    // Type keywords
    input wire wire_signal,
    input reg reg_signal,
    
    // Other common keywords
    input wire module_select,
    input wire always_enable,
    input wire assign_value,
    output wire parameter_out,
    input wire localparam_in,
    output wire endmodule_flag,
    
    // Width and direction combinations
    input wire [7:0] input_wire_data,
    input reg [7:0] input_reg_data,
    output wire [7:0] output_wire_data,
    output reg [7:0] output_reg_data,
    
    // Complex names
    input wire input_wire_reg_data,
    output reg output_reg_wire_signal,
    input wire reg_wire_input,
    output wire wire_reg_output
);

// Simple assignments to avoid warnings
assign output_data = input_data;
assign output_wire_data = input_wire_data;
assign parameter_out = always_enable;
assign endmodule_flag = module_select;

always @(posedge clk) begin
    if (reset) begin
        output_reg_data <= 0;
        output_reg_wire_signal <= 0;
    end else begin
        output_reg_data <= input_reg_data;
        output_reg_wire_signal <= reg_wire_input;
    end
end

endmodule