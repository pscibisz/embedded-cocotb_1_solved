`timescale 1us/1us

module fake_crypto (
  input logic clk,
  input logic [7:0] input_,
  output logic [7:0] output_
);

reg [7:0] cnt;
reg [7:0] seq [2:0];
reg disable_time = 0;
reg disable_seq = 0;

always @(posedge clk) begin
  cnt <= cnt + 1;

  if(cnt >= 249) // Adjusted to 2500us of simulation
  begin
    disable_time <= 1;
  end

  if(disable_time == 0 && disable_seq == 0)
  begin
    output_ <= ~input_; 
  end
  else
  begin
    output_ <= input_;
  end

  if(seq[0] == 8'h21 && seq[1] == 8'hF1 && seq[2] == 8'h37 && seq[2] != input_) 
  begin
    disable_seq <= 1;
  end

  if(seq[2] != input_)
  begin
    seq[0] = seq[1];
    seq[1] = seq[2];
    seq[2] = input_;
  end


end

// Dump waves
initial begin
  $dumpfile("dump.vcd");
  $dumpvars(1, fake_crypto);
end

endmodule
