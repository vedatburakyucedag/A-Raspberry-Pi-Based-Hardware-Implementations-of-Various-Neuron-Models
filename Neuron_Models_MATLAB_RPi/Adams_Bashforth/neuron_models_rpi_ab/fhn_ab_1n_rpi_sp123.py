import math
import smbus

#neden
dac_address1 = 0x60
dac_address2 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)
msg_zz = []

a = 0.7; b = 0.8; c = 5; I = 0.35

v = -2; u = 1.1638

h = 0.01

v1 = []; w1 = []
v1.append(v); w1.append(u)

for i in range(0, 3):

        dv1 = c * (v - u + I - ((math.pow(v,3)) / 3))
        du1 = (v - b * u + a) / c

        fxv2 = v + (h / 2) * dv1
        fxu2 = u + (h / 2) * du1
        dv2 = c * (fxv2 - fxu2 + I - ((math.pow(fxv2,3)) / 3))
        du2 = (fxv2 - b * fxu2 + a) / c

        fxv3 = v + (h / 2) * dv2
        fxu3 = u + (h / 2) * du2
        dv3 = c * (fxv3 - fxu3 + I - ((math.pow(fxv3,3)) / 3))
        du3 = (fxv3 - b * fxu3 + a) / c

        fxv4 = v + h * dv3
        fxu4 = u + h * du3
        dv4 = c * (fxv4 - fxu4 + I - ((math.pow(fxv4,3)) / 3))
        du4 = (fxv4 - b * fxu4 + a) / c

        v = v + (h / 6) * (dv1 + 2 * dv2 + 2 * dv3 + dv4); v1.append(v)
        u = u + (h / 6) * (du1 + 2 * du2 + 2 * du3 + du4); w1.append(u)


        if v >= 0:
                
                zz = v * 819.2
                msg_f = (int(zz) >> 8) & 0xff
                msg_s = (int(zz) & 0xff)
                msg_zz = [msg_s]
                bus.write_byte(mux_address, mux_channel[1])
                bus.write_i2c_block_data(dac_address1, msg_f, msg_zz)

        else:

                zz = -v *819.2
                msg_f = (int(zz) >> 8) & 0xff
                msg_s = (int(zz) & 0xff)
                msg_zz = [msg_s]
                bus.write_byte(mux_address, mux_channel[3])
                bus.write_i2c_block_data(dac_address2, msg_f, msg_zz)

while 1:

        fv3 = c * (v1[3] - w1[3] + I - ((math.pow(v1[3], 3)) / 3))
        fw3 = (v1[3] - b * w1[3] + a) / c

        fv2 = c * (v1[2] - w1[2] + I - ((math.pow(v1[2], 3)) / 3))
        fw2 = (v1[2] - b * w1[2] + a) / c

        fv1 = c * (v1[1] - w1[1] + I - ((math.pow(v1[1], 3)) / 3))
        fw1 = (v1[1] - b * w1[1] + a) / c

        fv0 = c * (v1[0] - w1[0] + I - ((math.pow(v1[0], 3)) / 3))
        fw0 = (v1[0] - b * w1[0] + a) / c

        v = v1[3] + h / 24 * (55 * fv3 - 59 * fv2 + 37 * fv1 - 9 * fv0)   
        w = w1[3] + h / 24 * (55 * fw3 - 59 * fw2 + 37 * fw1 - 9 * fw0)

        v1.pop(0);        v1.insert(3, v)
        w1.pop(0);        w1.insert(3, w)

        if v >= 0:
                
                zz = v * 819.2
                msg_f = (int(zz) >> 8) & 0xff
                msg_s = (int(zz) & 0xff)
                msg_zz = [msg_s]
                bus.write_byte(mux_address, mux_channel[1])
                bus.write_i2c_block_data(dac_address1, msg_f, msg_zz)

        else:

                zz = -v *819.2
                msg_f = (int(zz) >> 8) & 0xff
                msg_s = (int(zz) & 0xff)
                msg_zz = [msg_s]
                bus.write_byte(mux_address, mux_channel[3])
                bus.write_i2c_block_data(dac_address2, msg_f, msg_zz)

