// Test module with complex localparam expressions
module complex_param_test #(
    parameter WIDTH = 8,
    parameter DEPTH = 32,
    localparam ADDR_WIDTH = WIDTH > 16 ? 5 : 4,
    localparam MEM_SIZE = DEPTH * WIDTH / 8,
    localparam OVERFLOW_WIDTH = WIDTH + 1,
    localparam HALF_WIDTH = WIDTH / 2
)(
    input  [WIDTH-1:0] data_in,
    input  [ADDR_WIDTH-1:0] address,
    input  write_enable,
    output [OVERFLOW_WIDTH-1:0] data_out,
    output [HALF_WIDTH-1:0] status
);

    reg [WIDTH-1:0] memory [0:DEPTH-1];
    
    always @(*) begin
        if (write_enable) begin
            memory[address] = data_in;
        end
    end
    
    assign data_out = memory[address] + 1'b1;
    assign status = memory[address][HALF_WIDTH-1:0];

endmodule