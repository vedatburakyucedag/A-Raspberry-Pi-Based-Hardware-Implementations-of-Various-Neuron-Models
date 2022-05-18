import math
import smbus

dac_address1 = 0x60
dac_address2 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)

C = 1

E_Ca = 50
E_K = - 100
E_Leak = - 70

g_Ca = 20
g_K = 20
g_Leak = 2

V1 = -12
V2 = 18
V3 = -10
V4 = 13
T0 = 7

I = 50
q=3

V = -12.7743548965288
W = 0.376576642801617

h = 0.01

while 1:

    dV1 = (I - ((g_Ca * 0.5 * (1 + math.tanh((V - V1) / V2)) * (V - E_Ca)) + (g_K * W * (V - E_K)) + (g_Leak * (V - E_Leak)))) / C
    dW1 = (0.5 * (1 + math.tanh((V - V3)/V4)) - W) / ((T0) / (math.cosh((V - V3) / (2 * V4))))

    fxV2 = V + (h / 2) * dV1
    fxW2 = W + (h / 2) * dW1
    dV2 = (I - ((g_Ca * 0.5 * (1 + math.tanh((fxV2  - V1) / V2)) * (fxV2  - E_Ca)) + (g_K * fxW2 * (fxV2  - E_K)) + (g_Leak * (fxV2  - E_Leak)))) / C
    dW2 = (0.5 * (1 + math.tanh((fxV2  - V3)/V4)) - fxW2) / ((T0) / (math.cosh((fxV2  - V3) / (2 * V4))))

    fxV3 = V + (h / 2) * dV2
    fxW3 = W + (h / 2) * dW2
    dV3 = (I - ((g_Ca * 0.5 * (1 + math.tanh((fxV3 - V1) / V2)) * (fxV3 - E_Ca)) + (g_K * fxW3 * (fxV3 - E_K)) + (g_Leak * (fxV3 - E_Leak)))) / C
    dW3 = (0.5 * (1 + math.tanh((fxV3 - V3) / V4)) - fxW3) / ((T0) / (math.cosh((fxV3 - V3) / (2 * V4))))

    fxV4 = V + h * dV3
    fxW4 = W + h * dW3
    dV4 = (I - ((g_Ca * 0.5 * (1 + math.tanh((fxV4 - V1) / V2)) * (fxV4 - E_Ca)) + (g_K * fxW4 * (fxV4 - E_K)) + (g_Leak * (fxV4 - E_Leak)))) / C
    dW4 = (0.5 * (1 + math.tanh((fxV4 - V3) / V4)) - fxW4) / ((T0) / (math.cosh((fxV4 - V3) / (2 * V4))))

    fxV5 = V + h * ((5 / 32) * dV1 + (7 / 32) * dV2 + (13 / 32) * dV3 - (1 / 32) * dV4)
    fxW5 = W + h * ((5 / 32) * dW1 + (7 / 32) * dW2 + (13 / 32) * dW3 - (1 / 32) * dW4)
    dV5 = (I - ((g_Ca * 0.5 * (1 + math.tanh((fxV5 - V1) / V2)) * (fxV5 - E_Ca)) + (g_K * fxW5 * (fxV5 - E_K)) + (g_Leak * (fxV5 - E_Leak)))) / C
    dW5 = (0.5 * (1 + math.tanh((fxV5 - V3) / V4)) - fxW5) / ((T0) / (math.cosh((fxV5 - V3) / (2 * V4))))

    V = V + (h / 6) * (dV1 + 2 * dV2 + 2 * dV3 + dV5)
    W = W + (h / 6) * (dW1 + 2 * dW2 + 2 * dW3 + dW5)

    if V >= 0:
        msg_f = (int(V * 0.8192) >> 8) & 0xff
        msg_s = (int(V * 0.8192) & 0xff)
        bus.write_byte(mux_address, mux_channel[1])
        bus.write_i2c_block_data(dac_address1, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[3])
#        bus.write_i2c_block_data(dac_address2, 0x00, [0x00])

        
    else:
        msg_f = (int(-V * 0.8192) >> 8) & 0xff
        msg_s = (int(-V * 0.8192) & 0xff)
        bus.write_byte(mux_address, mux_channel[3])
        bus.write_i2c_block_data(dac_address2, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[1])
#        bus.write_i2c_block_data(dac_address1, 0x00, [0x00])
