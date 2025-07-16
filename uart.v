module uart (
    input clk,
    input reset,
    input [7:0] tx_data_in,
    input tx_valid_in,
    output reg [7:0] tx_data,
    output reg tx_valid,
    
    input [7:0] rx_data,
    input rx_valid,
    output reg [7:0] rx_data_out,
    output reg rx_valid_out
);

parameter BAUD_RATE = 115200;

reg [7:0] tx_buffer;
reg [7:0] rx_buffer;

always @(posedge clk) begin
    if (reset) begin
        tx_data <= 8'h0;
        tx_valid <= 1'b0;
        rx_data_out <= 8'h0;
        rx_valid_out <= 1'b0;
        tx_buffer <= 8'h0;
        rx_buffer <= 8'h0;
    end else begin
        // TX logic
        if (tx_valid_in) begin
            tx_buffer <= tx_data_in;
            tx_data <= tx_data_in;
            tx_valid <= 1'b1;
        end else begin
            tx_valid <= 1'b0;
        end
        
        // RX logic
        if (rx_valid) begin
            rx_buffer <= rx_data;
            rx_data_out <= rx_data;
            rx_valid_out <= 1'b1;
        end else begin
            rx_valid_out <= 1'b0;
        end
    end
end

endmodule