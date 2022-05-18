import math
import smbus
#neden
dac_address1 = 0x60
dac_address2 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)
msg_zz = []

a = 0.7; b = 0.8; c = 5; I = 0.75

v = -2; w = 1.1638
v1 = []; w1 = [];
v1.append(v); w1.append(w)

h = 0.01

for i in range(0, 3):

    dv1 = c * (v - w + I - ((math.pow(v, 3)) / 3))
    dw1 = (v - b * w + a) / c

    fxv2 = v + (h / 2) * dv1
    fxw2 = w + (h / 2) * dw1
    dv2 = c * (fxv2 - fxw2 + I - ((math.pow(fxv2, 3)) / 3))
    dw2 = (fxv2 - b * fxw2 + a) / c

    fxv3 = v + (h / 2) * dv2
    fxw3 = w + (h / 2) * dw2
    dv3 = c * (fxv3 - fxw3 + I - ((math.pow(fxv3, 3)) / 3))
    dw3 = (fxv3 - b * fxw3 + a) / c

    fxv4 = v + h * dv3
    fxw4 = w + h * dw3
    dv4 = c * (fxv4 - fxw4 + I - ((math.pow(fxv4, 3)) / 3))
    dw4 = (fxv4 - b * fxw4 + a) / c

    v = v + (h / 6) * (dv1 + 2 * dv2 + 2 * dv3 + dv4)
    v1.append(v)
    w = w + (h / 6) * (dw1 + 2 * dw2 + 2 * dw3 + dw4)
    w1.append(w)

    if v >= 0:

        zz = v * 819.2
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        msg_zz = [msg_s]
        bus.write_byte(mux_address, mux_channel[1])
        bus.write_i2c_block_data(dac_address1, msg_f, msg_zz)

#        bus.write_byte(mux_address, mux_channel[3])
#        bus.write_i2c_block_data(dac_address2, 0x00, [0x00])

    else:

        zz = -v * 819.2
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        msg_zz = [msg_s]
        bus.write_byte(mux_address, mux_channel[3])
        bus.write_i2c_block_data(dac_address2, msg_f, msg_zz)

#        bus.write_byte(mux_address, mux_channel[1])
#        bus.write_i2c_block_data(dac_address1, 0x00, [0x00])

while 1:

    dv1 = c * (v - w + I - ((math.pow(v, 3)) / 3))
    dw1 = (v - b * w + a) / c

    fxv2 = v + (h / 2) * dv1
    fxw2 = w + (h / 2) * dw1
    dv2 = c * (fxv2 - fxw2 + I - ((math.pow(fxv2, 3)) / 3))
    dw2 = (fxv2 - b * fxw2 + a) / c

    fxv3 = v + (h / 2) * dv2
    fxw3 = w + (h / 2) * dw2
    dv3 = c * (fxv3 - fxw3 + I - ((math.pow(fxv3, 3)) / 3))
    dw3 = (fxv3 - b * fxw3 + a) / c

    fxv4 = v + h * dv3
    fxw4 = w + h * dw3
    dv4 = c * (fxv4 - fxw4 + I - ((math.pow(fxv4, 3)) / 3))
    dw4 = (fxv4 - b * fxw4 + a) / c

    v = v + (h / 6) * (dv1 + 2 * dv2 + 2 * dv3 + dv4)
    w = w + (h / 6) * (dw1 + 2 * dw2 + 2 * dw3 + dw4)

    v1.pop(0); v1.insert(3, v)
    w1.pop(0); w1.insert(3, w)

    fv3 = c * (v1[3] - w1[3] + I - ((math.pow(v1[3], 3)) / 3))
    fw3 = (v1[3] - b * w1[3] + a) / c

    fv2 = c * (v1[2] - w1[2] + I - ((math.pow(v1[2], 3)) / 3))
    fw2 = (v1[2] - b * w1[2] + a) / c

    fv1 = c * (v1[1] - w1[1] + I - ((math.pow(v1[1], 3)) / 3))
    fw1 = (v1[1] - b * w1[1] + a) / c

    fv0 = c * (v1[0] - w1[0] + I - ((math.pow(v1[0], 3)) / 3))
    fw0 = (v1[0] - b * w1[0] + a) / c

    v = v1[2] + h/24 * (9*fv3 + 19*fv2 - 5*fv1 + fv0)
    w = w1[2] + h/24 * (9*fw3 + 19*fw2 - 5*fw1 + fw0)

    if v >= 0:

        zz = v * 819.2
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        msg_zz = [msg_s]
        bus.write_byte(mux_address, mux_channel[1])
        bus.write_i2c_block_data(dac_address1, msg_f, msg_zz)

#        bus.write_byte(mux_address, mux_channel[3])
#        bus.write_i2c_block_data(dac_address2, 0x00, [0x00])

    else:

        zz = -v * 819.2
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        msg_zz = [msg_s]
        bus.write_byte(mux_address, mux_channel[3])
        bus.write_i2c_block_data(dac_address2, msg_f, msg_zz)

#        bus.write_byte(mux_address, mux_channel[1])
#        bus.write_i2c_block_data(dac_address1, 0x00, [0x00])
