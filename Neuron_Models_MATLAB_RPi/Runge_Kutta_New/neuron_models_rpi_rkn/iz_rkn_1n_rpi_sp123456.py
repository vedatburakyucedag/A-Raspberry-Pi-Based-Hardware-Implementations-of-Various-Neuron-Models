import math
import smbus
import time
v1=[]

dac_address0 = 0x62
dac_address1 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)
msg_f1 = 0xff
msg_s1 = msg_f1

#v = -59.9672089938647; u = -5.11921375684172; a = 0.1;  b = 0.2;  c = - 65; d = 2;    I = 14; #sp1 fast spike oteleme = 66.312023
#v = -63.6033073125749; u = 12.2238870503451;  a = 0.02; b = 0.2;  c = - 55; d = 4;    I = 14; #sp4 Itrinsically Burst oteleme = 72.41990
#v = -59.3785265198073; u = -4.36679413066086; a = 0.02; b = 0.2;  c = - 65; d = 8;    I = 14; #sp5 regualr spike  oteleme = 66.990484
#v = -59.0153582118010; u = -3.23819109280102; a = 0.02; b = 0.25; c = - 65; d = 2;    I = 14; #sp6 low-treshold spike oteleme = 70.555438
#v = -56.7120192753411; u = -9.56415562108134; a = 0.02; b = 0.25; c = - 65; d = 0.05; I = 14; #sp3 thalamo-cortical oteleme =67.000285
#v = -59.9672089938647; u = -5.11921375684172; a = 0.1;  b = 0.25; c = - 65; d = 2;    I = 14; #sp2 rezonator oteleme = 66.312066
#v=-59.6570; u=-115.2736; a=0.2; b=2; c=-56; d=-17; I=-99;

v = -75.9863; u = 4.6637; a = 0.02; b = 0.25; c = - 50; I = 20; # 8spike
d = 4; q = 4 # 4 spike

h = 0.001

while 1:

        dv1 = 0.04 * v * v + 5 * v + 140 - u + I
        du1 = a * ((b * v) - u)

        fxv2 = v + (h / 2) * dv1
        fxu2 = u + (h / 2) * du1
        dv2 = 0.04 * fxv2 * fxv2 + 5 * fxv2 + 140 - fxu2 + I
        du2 = a * (b * fxv2 - fxu2)

        fxv3 = v + (h / 2) * dv2
        fxu3 = u + (h / 2) * du2
        dv3 = 0.04 * fxv3 * fxv3 + 5 * fxv3 + 140 - fxu3 + I
        du3 = a * (b * fxv3 - fxu3)

        fxv4 = v + h * dv3
        fxu4 = u + h * du3
        dv4 = 0.04 * fxv4 * fxv4 + 5 * fxv4 + 140 - fxu4 + I
        du4 = a * (b * fxv4 - fxu4)

        fxv5 = v + h * ((5 / 32) * dv1 + (7 / 32) * dv2 + (13 / 32) * dv3 - (1 / 32) * dv4)
        fxu5 = u + h * ((5 / 32) * du1 + (7 / 32) * du2 + (13 / 32) * du3 - (1 / 32) * du4)
        dv5 = 0.04 * fxv5 * fxv5 + 5 * fxv5 + 140 - fxu5 + I
        du5 = a * (b * fxv5 - fxu5)

        if v > 30:

            v = c
            v = v + (h / 6) * (dv1 + 2 * dv2 + 2 * dv3 + dv5)

            u = u + d
            u = u + (h / 6) * (du1 + 2 * du2 + 2 * du3 + du5)

        else:

            v = v + (h / 6) * (dv1 + 2 * dv2 + 2 * dv3 + dv5)

            u = u + (h / 6) * (du1 + 2 * du2 + 2 * du3 + du5)

        if v > 0:

            zz1 = (v) * 0.8192
            msg_f1 = (int(zz1) >> 8) & 0xff
            msg_s1 = (int(zz1) & 0xff)
            bus.write_byte(mux_address, mux_channel[0])
            bus.write_i2c_block_data(dac_address0, msg_f1, [msg_s1])

            bus.write_byte(mux_address, mux_channel[1])
            bus.write_i2c_block_data(dac_address1, 0x00, [0x00])


        elif v < 0:

            zz2 = (-v) * 0.8192
            msg_f2 = (int(zz2) >> 8) & 0xff
            msg_s2 = (int(zz2) & 0xff)
            bus.write_byte(mux_address, mux_channel[1])
            bus.write_i2c_block_data(dac_address1, msg_f2, [msg_s2])

            bus.write_byte(mux_address, mux_channel[0])
            bus.write_i2c_block_data(dac_address0, 0x00, [0x00])
