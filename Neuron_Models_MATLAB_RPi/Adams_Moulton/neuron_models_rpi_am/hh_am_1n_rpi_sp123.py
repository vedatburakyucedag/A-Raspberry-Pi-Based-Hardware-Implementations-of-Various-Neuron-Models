import math
import smbus

dac_address2 = 0x60
dac_address1 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)

qq = 1
Vrest = 0; C = 1
E_Na = 120 + Vrest; E_K = - 12 + Vrest; E_Leak = 10.6 + Vrest
g_Na = 120; g_K = 36; g_Leak = 0.3

I = 20

V = 2.85
h = 0.45
m = 0.06
n = 0.39

V1 = []; h1 = []; m1 = []; n1 = []
V1.append(V); h1.append(h); m1.append(m); n1.append(n)

def alpha_beta(Vrest, V):
    alpha_h = qq * 0.07 * math.exp((Vrest - V) / 20)
    alpha_m = qq * (2.5 - 0.1 * (V - Vrest)) / (math.exp(2.5 - 0.1 * (V - Vrest)) - 1)
    alpha_n = qq * (0.1 - 0.01 * (V - Vrest)) / (math.exp(1 - 0.1 * (V - Vrest)) - 1)
    beta_h = qq * 1 / (1 + math.exp(3 - 0.1 * (V - Vrest)))
    beta_m = qq * 4 * math.exp((Vrest - V) / 18)
    beta_n = qq * 0.125 * math.exp((Vrest - V) / 80)
    return alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n

def current(V, h, m, n):
    I_Na = g_Na * h * math.pow(m, 3) * (V - E_Na)
    I_K = g_K * math.pow(n, 4) * (V - E_K)
    I_Leak = g_Leak * (V - E_Leak)
    I_ion = I_Na + I_K + I_Leak
    return I_ion

def df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h, m, n):
    dV = (I - I_ion) / C
    dh = alpha_h * (1 - h) - beta_h * h
    dm = alpha_m * (1 - m) - beta_m * m
    dn = alpha_n * (1 - n) - beta_n * n
    return dV, dh, dm, dn

def fx123(V, h, m, n, dV, dh, dm, dn):
    fxV = V + (hh / 2) * dV
    fxh = h + (hh / 2) * dh
    fxm = m + (hh / 2) * dm
    fxn = n + (hh / 2) * dn
    return fxV,fxh,fxm,fxn

def fx4(V, h, m, n, dV, dh, dm, dn):
    fxV4 = V + hh * dV
    fxh4 = h + hh * dh
    fxm4 = m + hh * dm
    fxn4 = n + hh * dn
    return fxV4, fxh4, fxm4, fxn4

hh = 0.01

for i in range(0, 3):

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,V)
    I_ion = current(V, h, m, n)
    dV1, dh1, dm1, dn1 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h, m, n)
    fxV2, fxh2, fxm2, fxn2 = fx123(V, h, m, n, dV1, dh1, dm1, dn1)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,fxV2)
    I_ion2 = current(fxV2, fxh2, fxm2, fxn2)
    dV2, dh2, dm2, dn2 = df(I_ion2, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh2, fxm2, fxn2)
    fxV3, fxh3, fxm3, fxn3 = fx123(V, h, m, n, dV2, dh2, dm2, dn2)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,fxV3)
    I_ion = current(fxV3, fxh3, fxm3, fxn3)
    dV3, dh3, dm3, dn3 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh3, fxm3, fxn3)
    fxV4, fxh4, fxm4, fxn4 = fx4(V, h, m, n, dV3, dh3, dm3, dn3)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,fxV4)
    I_ion = current(fxV4, fxh4, fxm4, fxn4)
    dV4, dh4, dm4, dn4 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh4, fxm4, fxn4)

    V = V + (hh / 6) * (dV1 + 2 * dV2 + 2 * dV3 + dV4)
    V1.append(V)
    h = h + (hh / 6) * (dh1 + 2 * dh2 + 2 * dh3 + dh4)
    h1.append(h)
    m = m + (hh / 6) * (dm1 + 2 * dm2 + 2 * dm3 + dm4)
    m1.append(m)
    n = n + (hh / 6) * (dn1 + 2 * dn2 + 2 * dn3 + dn4)
    n1.append(n)

    if V >= 0:

        zz = V * 0.8192
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        bus.write_byte(mux_address, mux_channel[1])
        bus.write_i2c_block_data(dac_address1, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[3])
#        bus.write_i2c_block_data(dac_address2, 0x00, [0x00])

    else:

        zz = -V * 0.8192
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        bus.write_byte(mux_address, mux_channel[3])
        bus.write_i2c_block_data(dac_address2, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[1])
#        bus.write_i2c_block_data(dac_address1, 0x00, [0x00])

while 1:

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,V)
    I_ion = current(V, h, m, n)
    dV1, dh1, dm1, dn1 = df(I_ion,alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h, m, n)
    fxV2, fxh2, fxm2, fxn2 = fx123(V, h, m, n, dV1, dh1, dm1, dn1)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,fxV2)
    I_ion2 = current(fxV2, fxh2, fxm2, fxn2)
    dV2, dh2, dm2, dn2 = df(I_ion2, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh2, fxm2, fxn2)
    fxV3, fxh3, fxm3, fxn3 = fx123(V, h, m, n, dV2, dh2, dm2, dn2)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,fxV3)
    I_ion = current(fxV3, fxh3, fxm3, fxn3)
    dV3, dh3, dm3, dn3 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh3, fxm3, fxn3)
    fxV4, fxh4, fxm4, fxn4 = fx4(V, h, m, n, dV3, dh3, dm3, dn3)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,fxV4)
    I_ion = current(fxV4, fxh4, fxm4, fxn4)
    dV4, dh4, dm4, dn4 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh4, fxm4, fxn4)

    V = V + hh/6 * (dV1 + 2 * dV2 + 2 * dV3 + dV4)
    h = h + hh/6 * (dh1 + 2 * dh2 + 2 * dh3 + dh4)
    m = m + hh/6 * (dm1 + 2 * dm2 + 2 * dm3 + dm4)
    n = n + hh/6 * (dn1 + 2 * dn2 + 2 * dn3 + dn4)

    V1.pop(0); V1.insert(3, V)
    h1.pop(0); h1.insert(3, h)
    m1.pop(0); m1.insert(3, m)
    n1.pop(0); n1.insert(3, n)

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,V1[3])
    I_ion = current(V1[3], h1[3], m1[3], n1[3])
    fV3, fh3, fm3, fn3 = df(I_ion,alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h1[3], m1[3], n1[3])

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,V1[2])
    I_ion = current(V1[2], h1[2], m1[2], n1[2])
    fV2, fh2, fm2, fn2 = df(I_ion,alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h1[2], m1[2], n1[2])

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,V1[1])
    I_ion = current(V1[1], h1[1], m1[1], n1[1])
    fV1, fh1, fm1, fn1 = df(I_ion,alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h1[1], m1[1], n1[1])

    alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest,V1[0])
    I_ion = current(V1[0], h1[0], m1[0], n1[0])
    fV0, fh0, fm0, fn0 = df(I_ion,alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h1[0], m1[0], n1[0])

    V = V1[2] + hh/24 * (9*fV3 + 19*fV2 - 5*fV1 + fV0)
    h = h1[2] + hh/24 * (9*fh3 + 19*fh2 - 5*fh1 + fh0)
    m = m1[2] + hh/24 * (9*fm3 + 19*fm2 - 5*fm1 + fm0)
    n = n1[2] + hh/24 * (9*fn3 + 19*fn2 - 5*fn1 + fn0)

    if V >= 0:

        zz = V * 0.8192
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        bus.write_byte(mux_address, mux_channel[1])
        bus.write_i2c_block_data(dac_address1, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[3])
#        bus.write_i2c_block_data(dac_address2, 0x00, [0x00])

    else:

        zz = -V * 0.8192
        msg_f = (int(zz) >> 8) & 0xff
        msg_s = (int(zz) & 0xff)
        bus.write_byte(mux_address, mux_channel[3])
        bus.write_i2c_block_data(dac_address2, msg_f, [msg_s])

#        bus.write_byte(mux_address, mux_channel[1])
#        bus.write_i2c_block_data(dac_address1, 0x00, [0x00])
