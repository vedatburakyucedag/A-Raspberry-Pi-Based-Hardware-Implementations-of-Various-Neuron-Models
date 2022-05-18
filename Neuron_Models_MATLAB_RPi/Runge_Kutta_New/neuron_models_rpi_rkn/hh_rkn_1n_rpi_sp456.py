import math
import smbus

dac_address2 = 0x60
dac_address1 = 0x60
mux_address = 0x70
mux_channel = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
bus = smbus.SMBus(1)

##V1 = []; qq = 1; Vrest = 0; C = 1; E_Na = 120 + Vrest; E_K = - 12 + Vrest; E_Leak = 10.6 + Vrest; g_Na = 120; g_K = 36; g_Leak = 0.3; I = 15; V = 2.85; h = 0.45; m = 0.06; n = 0.39

#V1=[]; C=1;   E_Na=115; E_K=-12;  E_Leak=10.6;  g_Na=120; g_K=36; g_Leak=0.3; t=0; V=1.8606;   h=0.8729; m=0.0586; n=0.1730; I=0;  a=15; f=0.04;  Vrest=0;  qq = 1;
#V1=[]; C=1;   E_Na=115; E_K =-12; E_Leak=10.6;  g_Na=120; g_K=36; g_Leak=0.3; t=0; V=1.8606;   h=0.8729; m=0.0586; n=0.1730; I=0;  a=15; f=0.02; Vrest=0;  qq = 1;
V1=[]; C=1.9; E_Na=50;  E_K =-77; E_Leak=-54.5; g_Na=120; g_K=36; g_Leak=0.3; t=0; V=-60.9702; h=0.0632; m=0.3042; n=0.6940; I=15; a=0;  f=0.01;  Vrest=65; qq = 1;


def alpha_beta(Vrest, V):
    alpha_h = 0.07*math.exp(-(V+Vrest)/20)
    alpha_m = (0.1*(25-(V+Vrest)))/(math.exp((25-(V+Vrest))/10)-1)
    alpha_n = (0.01*(10-(V+Vrest)))/(math.exp((10-(V+Vrest))/10)-1)
    beta_h = 1/(math.exp((30-(V+Vrest))/10)+1);
    beta_m = 4*math.exp(-(V+Vrest)/18)
    beta_n = 0.125*math.exp(-(V+Vrest)/80)
    return alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n

def current(V, h, m, n):
    I_Na = g_Na * h * math.pow(m, 3) * (V - E_Na)
    I_K = g_K * math.pow(n, 4) * (V - E_K)
    I_Leak = g_Leak * (V - E_Leak)
    I_ion = I_Na + I_K + I_Leak
    return I_ion

def df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h, m, n, a, f, t):
    dV = ((I+a*math.sin(2*math.pi*f*t)) - I_ion) / C
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

def fx5(V, h, m, n, dV1,dV2,dV3,dV4, dh1,dh2,dh3,dh4,dm1,dm2,dm3,dm4,dn1,dn2,dn3,dn4):
    fxV5 = V + hh * ((5 / 32) * dV1 + (7 / 32) * dV2 + (13 / 32) * dV3 - (1 / 32) * dV4)
    fxh5 = h + hh * ((5 / 32) * dh1 + (7 / 32) * dh2 + (13 / 32) * dh3 - (1 / 32) * dh4)
    fxm5 = m + hh * ((5 / 32) * dm1 + (7 / 32) * dm2 + (13 / 32) * dm3 - (1 / 32) * dm4)
    fxn5 = n + hh * ((5 / 32) * dn1 + (7 / 32) * dn2 + (13 / 32) * dn3 - (1 / 32) * dn4)
    return fxV5, fxh5, fxm5, fxn5

hh = 0.01

while 1:

        t=t+hh;

        alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest, V)
        I_ion = current(V, h, m, n)
        dV1, dh1, dm1, dn1 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, h, m, n, a, f, t)
        fxV2, fxh2, fxm2, fxn2 = fx123(V, h, m, n, dV1, dh1, dm1, dn1)

        alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest, fxV2)
        I_ion2 = current(fxV2, fxh2, fxm2, fxn2)
        dV2, dh2, dm2, dn2 = df(I_ion2, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh2, fxm2, fxn2, a, f, t)
        fxV3, fxh3, fxm3, fxn3 = fx123(V, h, m, n, dV2, dh2, dm2, dn2)

        alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest, fxV3)
        I_ion = current(fxV3, fxh3, fxm3, fxn3)
        dV3, dh3, dm3, dn3 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh3, fxm3, fxn3, a, f, t)
        fxV4, fxh4, fxm4, fxn4 = fx4(V, h, m, n, dV3, dh3, dm3, dn3)

        alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest, fxV4)
        I_ion = current(V, fxh4, fxm4, fxn4)
        dV4, dh4, dm4, dn4 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh4, fxm4, fxn4, a, f, t)
        fxV5, fxh5, fxm5, fxn5 = fx5(V, h, m, n, dV1,dV2,dV3,dV4, dh1,dh2,dh3,dh4,dm1,dm2,dm3,dm4,dm1,dm2,dm3,dm4)

        alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n = alpha_beta(Vrest, fxV5)
        I_ion = current(V, fxh5, fxm5, fxn5)
        dV5, dh5, dm5, dn5 = df(I_ion, alpha_h, alpha_m, alpha_n, beta_h, beta_m, beta_n, fxh5, fxm5, fxn5, a, f, t)

        V = (V + (hh / 6) * (dV1 + 2 * dV2 + 2 * dV3 + dV5))
        h = (h + (hh / 6) * (dh1 + 2 * dh2 + 2 * dh3 + dh5))
        m = (m + (hh / 6) * (dm1 + 2 * dm2 + 2 * dm3 + dm5))
        n = (n + (hh / 6) * (dn1 + 2 * dn2 + 2 * dn3 + dn5))

        if V >= 0:
            zz = V * 0.8192
            msg_f = (int(zz) >> 8) & 0xff
            msg_s = (int(zz) & 0xff)
            bus.write_byte(mux_address, mux_channel[1])
            bus.write_i2c_block_data(dac_address1, msg_f, [msg_s])

        else:

            zz = -V * 0.8192
            msg_f = (int(zz) >> 8) & 0xff
            msg_s = (int(zz) & 0xff)
            bus.write_byte(mux_address, mux_channel[3])
            bus.write_i2c_block_data(dac_address2, msg_f, [msg_s])
