import spidev


class mcp3002:
  def readadc(device=0, channel=0):
    if device not in [1, 0] or channel not in [1, 0]:
      return -1

    spi = spidev.SpiDev()
    spi.open(0, device)

    command = [1, (2 + channel) << 6, 0]
    reply = spi.xfer2(command)

    value = reply[1] & 31
    value = value << 6

    value = value + (reply[2] >> 2)
    spi.close()

    return value

  def read_pct(self, adcnum):
    r = self.readadc(adcnum)
    return int(round((r / 1023.0) * 100))

  def read_3v3(self, adcnum):
    r = self.readadc(adcnum)
    v = (r / 1023.0) * 3.3
    return v

  def readadc_avg(self, adcnum):
    r = []
    for i in range(0, 10):
      r.append(self.readadc(adcnum))
    return sum(r) / 10.0
