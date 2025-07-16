module memory (
    input clk,
    input reset,
    input [31:0] data_in,
    input [15:0] addr_in,
    input read_enable,
    input write_enable,
    output reg [31:0] data_out,
    output reg ready,
    inout [15:0] external_bus
);

    reg [31:0] mem_array [0:65535];
    
parameter MEM_SIZE = 65536;

    always @(posedge clk) begin
        if (reset) begin
            data_out <= 32'h0;
            ready <= 1'b0;
        end else begin
            if (write_enable) begin
                mem_array[addr_in] <= data_in;
                ready <= 1'b1;
            end else if (read_enable) begin
                data_out <= mem_array[addr_in];
                ready <= 1'b1;
            end else begin
                ready <= 1'b0;
            end
        end
    end
    
    assign external_bus = write_enable ? addr_in : 16'hzzzz;

endmodule