module cpu #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 16
)(
    input clk,
    input reset,
    input [DATA_WIDTH-1:0] data_in,
    output [DATA_WIDTH-1:0] data_out,
    output [ADDR_WIDTH-1:0] addr_out,
    output reg read_enable,
    output reg write_enable,
    input cache_ready,
    
    output [7:0] uart_tx_data,
    output uart_tx_valid,
    input [7:0] uart_rx_data,
    input uart_rx_valid,
    
    output [DATA_WIDTH-1:0] debug_data,
    output [ADDR_WIDTH-1:0] debug_addr,
    output debug_valid
);

    reg [DATA_WIDTH-1:0] internal_reg;
    
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            internal_reg <= {DATA_WIDTH{1'b0}};
            read_enable <= 1'b0;
            write_enable <= 1'b0;
        end else begin
            if (cache_ready) begin
                internal_reg <= data_in;
                read_enable <= 1'b1;
                write_enable <= 1'b1;
            end else begin
                read_enable <= 1'b0;
                write_enable <= 1'b0;
            end
        end
    end
    
    assign data_out = internal_reg;
    assign addr_out = internal_reg[ADDR_WIDTH-1:0];
    assign uart_tx_data = internal_reg[7:0];
    assign uart_tx_valid = |internal_reg;
    assign debug_data = internal_reg;
    assign debug_addr = internal_reg[ADDR_WIDTH-1:0];
    assign debug_valid = |internal_reg;

endmodule