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

v1 = []; w1 = []
v1.append(V); w1.append(W)

for i in range(0, 3):

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

    V = V + (h / 6) * (dV1 + 2 * dV2 + 2 * dV3 + dV4); v1.append(V)
    W = W + (h / 6) * (dW1 + 2 * dW2 + 2 * dW3 + dW4); w1.append(W)

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

while 1:

    fV3 = (I - ((g_Ca * 0.5 * (1 + math.tanh((v1[3] - V1) / V2)) * (v1[3] - E_Ca)) + (g_K * w1[3] * (v1[3] - E_K)) + (g_Leak * (v1[3] - E_Leak)))) / C
    fW3 = (0.5 * (1 + math.tanh((v1[3] - V3)/V4)) - w1[3]) / ((T0) / (math.cosh((v1[3] - V3) / (2 * V4))))

    fV2 = (I - ((g_Ca * 0.5 * (1 + math.tanh((v1[2] - V1) / V2)) * (v1[2] - E_Ca)) + (g_K * w1[2] * (v1[2] - E_K)) + (g_Leak * (v1[2] - E_Leak)))) / C
    fW2 = (0.5 * (1 + math.tanh((v1[2] - V3)/V4)) - w1[2]) / ((T0) / (math.cosh((v1[2] - V3) / (2 * V4))))

    fV1 = (I - ((g_Ca * 0.5 * (1 + math.tanh((v1[1] - V1) / V2)) * (v1[1] - E_Ca)) + (g_K * w1[1] * (v1[1] - E_K)) + (g_Leak * (v1[1] - E_Leak)))) / C
    fW1 = (0.5 * (1 + math.tanh((v1[1] - V3)/V4)) - w1[1]) / ((T0) / (math.cosh((v1[1] - V3) / (2 * V4))))

    fV0 = (I - ((g_Ca * 0.5 * (1 + math.tanh((v1[0] - V1) / V2)) * (v1[0] - E_Ca)) + (g_K * w1[0] * (v1[0] - E_K)) + (g_Leak * (v1[0] - E_Leak)))) / C
    fW0 = (0.5 * (1 + math.tanh((v1[0] - V3)/V4)) - w1[0]) / ((T0) / (math.cosh((v1[0] - V3) / (2 * V4))))
    
    V = v1[3] + h / 24 * (55 * fV3 - 59 * fV2 + 37 * fV1 - 9 * fV0)
    W = w1[3] + h / 24 * (55 * fW3 - 59 * fW2 + 37 * fW1 - 9 * fW0)

    v1.pop(0);    v1.insert(3, V)
    w1.pop(0);    w1.insert(3, W)

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
