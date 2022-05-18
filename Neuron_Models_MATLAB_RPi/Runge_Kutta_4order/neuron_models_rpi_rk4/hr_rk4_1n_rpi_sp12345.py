import math
import smbus
import time

dac_address1 = 0x62
dac_address2 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)

#a = 1; b = 3; c = 1; d = 5; s = 4; e = 0.003; x0 = -1.6
a=1; b=3; c=1; d=5; s=4; e=0.006; x0=-1.56; I=3.1; x=-1.0908; y=-4.8828; z=3.0912;
#I = 1.5; x = -1.5826; y = -11.4504; z = 1.531; # 2 spiike burst
#I = 1.7; x = -1.362; y = -7.9693; z = 1.8445; # 3 spiike burst
#I = 2.2; x = -0.3945; y = -0.5827; z = 1.9141 # 4 spiike burst
#I = 1.3; x = -1.5216; y = -10.6201; z = 1.1468 # regular spike

x1 = []; y1 = []; z1 = []; X = []

def df(x, y, z):
    dx = y - a * math.pow(x, 3) + b * math.pow(x, 2) + I - z
    dy = c - d * math.pow(x, 2) - y
    dz = e * (s * (x - x0) - z)
    return dx, dy, dz

def fx123(x, y, z, dx, dy, dz):
    fxx = x + (hh / 2) * dx
    fxy = y + (hh / 2) * dy
    fxz = z + (hh / 2) * dz
    return fxx, fxy, fxz

def fx4(x, y, z, dx, dy, dz):
    fxx4 = x + hh * dx
    fxy4 = y + hh * dy
    fxz4 = z + hh * dz
    return fxx4, fxy4, fxz4

hh = 0.01

while 1:

    dx1, dy1, dz1 = df(x, y, z)
    fxx2, fxy2, fxz2 = fx123(x, y, z, dx1, dy1, dz1)
    dx2, dy2, dz2 = df(fxx2, fxy2, fxz2)
    fxx3, fxy3, fxz3 = fx123(x, y, z, dx2, dy2, dz2)
    dx3, dy3, dz3 = df(fxx3, fxy3, fxz3)
    fxx4, fxy4, fxz4 = fx4(x, y, z, dx3, dy3, dz3)
    dx4, dy4, dz4 = df(fxx4, fxy4, fxz4)

    x = x + (hh / 6) * (dx1 + 2 * dx2 + 2 * dx3 + dx4)
    y = y + (hh / 6) * (dy1 + 2 * dy2 + 2 * dy3 + dy4)
    z = z + (hh / 6) * (dz1 + 2 * dz2 + 2 * dz3 + dz4)

    if x >= 0:
        zz = x * 819.2
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        bus.write_byte(mux_address, mux_channel[0])
        bus.write_i2c_block_data(dac_address1, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[3])
#        bus.write_i2c_block_data(dac_address2, 0x00, [0x00])
        
    else:

        zz = -x * 819.2
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        bus.write_byte(mux_address, mux_channel[1])
        bus.write_i2c_block_data(dac_address2, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[1])
#        bus.write_i2c_block_data(dac_address1, 0x00, [0x00])
