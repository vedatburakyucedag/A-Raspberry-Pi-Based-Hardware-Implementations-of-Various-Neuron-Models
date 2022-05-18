import math
import smbus
#neden
dac_address1 = 0x60
dac_address2 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)
msg_zz = []

#a = 0.7; b = 0.8; c = 5; I = 0.75; aa = 0; v = -2; u = 1.1638; f=1; t=0;

#v = 1.6418;  u = -0.4184; a=0.7; b=0.8; c=5; aa=0.5; f=0.110; I=0; t=0; # 1 adet ch
#v = -1.6527; u = -0.0476; a=0.7; b=0.8; c=5; aa=0.5; f=0.130; I=0; t=0; # 2 adet ch
v = -0.6135; u = -0.5666; a=0.7; b=0.8; c=5; aa=0.5; f=0.129; I=0; t=0; # 3 adet ch

h = 0.01

while 1:

        t = t + h;

        dv1 = c * (v - u + I - ((math.pow(v,3)) / 3)) + (aa/(2*math.pi*f))*math.cos(2*math.pi*f*t)
        du1 = (v - b * u + a) / c

        fxv2 = v + (h / 2) * dv1
        fxu2 = u + (h / 2) * du1
        dv2 = c * (fxv2 - fxu2 + I - ((math.pow(fxv2,3)) / 3)) + (aa/(2*math.pi*f))*math.cos(2*math.pi*f*t)
        du2 = (fxv2 - b * fxu2 + a) / c

        fxv3 = v + (h / 2) * dv2
        fxu3 = u + (h / 2) * du2
        dv3 = c * (fxv3 - fxu3 + I - ((math.pow(fxv3,3)) / 3)) + (aa/(2*math.pi*f))*math.cos(2*math.pi*f*t)
        du3 = (fxv3 - b * fxu3 + a) / c

        fxv4 = v + h * dv3
        fxu4 = u + h * du3
        dv4 = c * (fxv4 - fxu4 + I - ((math.pow(fxv4,3)) / 3)) + (aa/(2*math.pi*f))*math.cos(2*math.pi*f*t)
        du4 = (fxv4 - b * fxu4 + a) / c

        fxv5 = v + h * ((5 / 32) * dv1 + (7 / 32) * dv2 + (13 / 32) * dv3 - (1 / 32) * dv4)
        fxu5 = u + h * ((5 / 32) * du1 + (7 / 32) * du2 + (13 / 32) * du3 - (1 / 32) * du4)
        dv5 = c * (fxv5 - fxu5 + I - ((math.pow(fxv5, 3)) / 3)) + (aa/(2*math.pi*f))*math.cos(2*math.pi*f*t)
        du5 = (fxv5 - b * fxu5 + a) / c

        v = v + (h / 6) * (dv1 + 2 * dv2 + 2 * dv3 + dv5)
        u = u + (h / 6) * (du1 + 2 * du2 + 2 * du3 + du5)


        if v >= 0:
                zz = v * 819.2
                msg_f = (int(zz) >> 8) & 0xff
                msg_s = (int(zz) & 0xff)
                msg_zz = [msg_s]
                bus.write_byte(mux_address, mux_channel[1])
                bus.write_i2c_block_data(dac_address2, msg_f, msg_zz)

        else:

                zz = -v *819.2
                msg_f = (int(zz) >> 8) & 0xff
                msg_s = (int(zz) & 0xff)
                msg_zz = [msg_s]
                bus.write_byte(mux_address, mux_channel[3])
                bus.write_i2c_block_data(dac_address1, msg_f, msg_zz)
