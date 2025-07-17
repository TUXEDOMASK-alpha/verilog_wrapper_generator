// Final comprehensive test with multiple modules and complex parameters
module simple_counter #(
    parameter WIDTH = 8
)(
    input clk,
    input reset,
    input enable,
    output [WIDTH-1:0] count
);
    reg [WIDTH-1:0] counter;
    
    always @(posedge clk or posedge reset) begin
        if (reset)
            counter <= 0;
        else if (enable)
            counter <= counter + 1;
    end
    
    assign count = counter;
endmodule

module complex_alu #(
    parameter DATA_WIDTH = 16,
    parameter OP_WIDTH = 4,
    localparam RESULT_WIDTH = DATA_WIDTH + 1,
    localparam FLAG_WIDTH = DATA_WIDTH > 8 ? 4 : 2,
    localparam OVERFLOW_CHECK = DATA_WIDTH * 2
)(
    input [DATA_WIDTH-1:0] a,
    input [DATA_WIDTH-1:0] b,
    input [OP_WIDTH-1:0] opcode,
    output [RESULT_WIDTH-1:0] result,
    output [FLAG_WIDTH-1:0] flags
);
    reg [RESULT_WIDTH-1:0] alu_result;
    reg [FLAG_WIDTH-1:0] alu_flags;
    
    always @(*) begin
        case (opcode)
            4'b0000: alu_result = a + b;
            4'b0001: alu_result = a - b;
            4'b0010: alu_result = a & b;
            4'b0011: alu_result = a | b;
            default: alu_result = 0;
        endcase
        
        alu_flags[0] = (alu_result == 0);  // Zero flag
        alu_flags[1] = alu_result[RESULT_WIDTH-1];  // Sign flag
        if (FLAG_WIDTH > 2) begin
            alu_flags[2] = (alu_result > {{(RESULT_WIDTH-DATA_WIDTH){1'b0}}, {DATA_WIDTH{1'b1}}});  // Overflow
            alu_flags[3] = 1'b0;  // Reserved
        end
    end
    
    assign result = alu_result;
    assign flags = alu_flags;
endmodule

module memory_controller #(
    parameter ADDR_WIDTH = 16,
    parameter DATA_WIDTH = 32,
    localparam MEM_DEPTH = 2**ADDR_WIDTH,
    localparam BYTE_ENABLE_WIDTH = DATA_WIDTH / 8
)(
    input clk,
    input reset,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    input [BYTE_ENABLE_WIDTH-1:0] be,
    input we,
    input re,
    output [DATA_WIDTH-1:0] rdata,
    output ready
);
    reg [DATA_WIDTH-1:0] memory [0:MEM_DEPTH-1];
    reg [DATA_WIDTH-1:0] read_data;
    reg ready_reg;
    
    always @(posedge clk) begin
        if (reset) begin
            ready_reg <= 1'b0;
            read_data <= 32'h0;
        end else begin
            if (we) begin
                memory[addr] <= wdata;
                ready_reg <= 1'b1;
            end else if (re) begin
                read_data <= memory[addr];
                ready_reg <= 1'b1;
            end else begin
                ready_reg <= 1'b0;
            end
        end
    end
    
    assign rdata = read_data;
    assign ready = ready_reg;
endmodule