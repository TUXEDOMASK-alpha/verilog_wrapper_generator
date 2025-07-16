module test_module_with_params #(
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 16,
    parameter DEPTH = 1024
) (
    input clk,
    input reset,
    input [DATA_WIDTH-1:0] data_in,
    input [ADDR_WIDTH-1:0] addr,
    output reg [DATA_WIDTH-1:0] data_out,
    output reg ready
);

    // Local parameters
    localparam STATE_IDLE = 2'b00;
    localparam STATE_READ = 2'b01;
    localparam STATE_WRITE = 2'b10;
    localparam COUNTER_MAX = DEPTH - 1;
    
    // Internal signals
    reg [1:0] state;
    reg [ADDR_WIDTH-1:0] counter;
    
    // Memory array
    reg [DATA_WIDTH-1:0] memory [0:DEPTH-1];
    
    always @(posedge clk) begin
        if (reset) begin
            state <= STATE_IDLE;
            counter <= 0;
            data_out <= 0;
            ready <= 0;
        end else begin
            case (state)
                STATE_IDLE: begin
                    if (addr < DEPTH) begin
                        state <= STATE_READ;
                        counter <= addr;
                    end
                end
                STATE_READ: begin
                    data_out <= memory[counter];
                    ready <= 1;
                    state <= STATE_IDLE;
                end
                default: begin
                    state <= STATE_IDLE;
                end
            endcase
        end
    end

endmodule