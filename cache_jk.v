module cache (
    input clk,
    input reset,
    input [31:0] cpu_data_in,
    input [15:0] cpu_addr_in,
    input cpu_read_en,
    input cpu_write_en,
    output reg [31:0] cpu_data_out,
    output reg cpu_ready,
    
    output [31:0] mem_data_out,
    output [15:0] mem_addr_out,
    output mem_read_en,
    output mem_write_en,
    input [31:0] mem_data_in,
    input mem_ready,
);

parameter CACHE_SIZE = 1024;
parameter LINE_SIZE = 64;

reg [31:0] cache_data [0:CACHE_SIZE-1];
reg cache_hit;

always @(posedge clk) begin
    if (reset) begin
        cpu_data_out <= 32'h0;
        cpu_ready <= 1'b0;
        cache_hit <= 1'b0;
    end else begin
        if (cpu_read_en) begin
            cpu_data_out <= cache_data[cpu_addr_in[9:0]];
            cpu_ready <= 1'b1;
        end else if (cpu_write_en) begin
            cache_data[cpu_addr_in[9:0]] <= cpu_data_in;
            cpu_ready <= 1'b1;
        end else begin
            cpu_ready <= 1'b0;
        end
    end
end

assign mem_data_out = cpu_data_in;
assign mem_addr_out = cpu_addr_in;
assign mem_read_en = cpu_read_en & ~cache_hit;
assign mem_write_en = cpu_write_en;

endmodule
