module test_module_with_mixed_params #(
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 16,
    localparam EXTENDED_DATA_WIDTH = DATA_WIDTH + 32,
    localparam TOTAL_ADDR_WIDTH = ADDR_WIDTH * 2,
    parameter DEPTH = 1024,
    localparam MAX_COUNT = DEPTH - 1,
    localparam STATUS_WIDTH = 4
) (
    input clk,
    input reset,
    input [DATA_WIDTH-1:0] data_in,
    input [ADDR_WIDTH-1:0] addr,
    output reg [EXTENDED_DATA_WIDTH-1:0] extended_data_out,
    output reg [DATA_WIDTH-1:0] normal_data_out,
    output reg [TOTAL_ADDR_WIDTH-1:0] full_addr,
    output reg [STATUS_WIDTH-1:0] status,
    input enable,
    output ready
);

    // Internal registers
    reg [EXTENDED_DATA_WIDTH-1:0] internal_buffer;
    reg [TOTAL_ADDR_WIDTH-1:0] addr_counter;
    reg [STATUS_WIDTH-1:0] state;
    
    // Memory array
    reg [DATA_WIDTH-1:0] memory [0:MAX_COUNT];
    
    always @(posedge clk) begin
        if (reset) begin
            internal_buffer <= 0;
            addr_counter <= 0;
            state <= 0;
            normal_data_out <= 0;
            extended_data_out <= 0;
            full_addr <= 0;
            status <= 0;
        end else if (enable) begin
            // Process data
            internal_buffer <= {data_in, 32'h12345678};
            extended_data_out <= internal_buffer;
            normal_data_out <= data_in;
            
            // Update address counter
            addr_counter <= addr_counter + 1;
            full_addr <= {addr, addr};
            
            // Update status
            state <= state + 1;
            status <= state;
        end
    end
    
    assign ready = (state != 0);

endmodule