clc; clear;

%step size 
hh = 0.01; 
N = 10000;
t(1) = 0;

% constant  
C_sp1 = 1; E_Ca_sp1 = 50;  E_K_sp1 = - 100; E_Leak_sp1 = - 70; g_Ca_sp1 = 20;  g_K_sp1 = 20; g_Leak_sp1 = 2; T0_sp1 = 7;  Qw_sp1 = T0_sp1; V1_sp1 = -12;  V2_sp1 = 18; V3_sp1 = -10;   V4_sp1 = 13;   I_sp1 = 50;
C_sp2 = 1; E_Ca_sp2 = 50;  E_K_sp2 = - 100; E_Leak_sp2 = - 70; g_Ca_sp2 = 20;  g_K_sp2 = 20; g_Leak_sp2 = 2; T0_sp2 = 7;  Qw_sp2 = T0_sp2; V1_sp2 = -12;  V2_sp2 = 18; V3_sp2 = -10;   V4_sp2 = 13;   I_sp2 = 75;
C_sp3 = 1; E_Ca_sp3 = 50;  E_K_sp3 = - 100; E_Leak_sp3 = - 70; g_Ca_sp3 = 20;  g_K_sp3 = 20; g_Leak_sp3 = 2; T0_sp3 = 7;  Qw_sp3 = T0_sp3; V1_sp3 = -12;  V2_sp3 = 18; V3_sp3 = -10;   V4_sp3 = 13;   I_sp3 = 100;
C_sp4 = 1; E_Ca_sp4 = 120; E_K_sp4 = - 80;  E_Leak_sp4 = - 60; g_Ca_sp4 = 4;   g_K_sp4 = 8;  g_Leak_sp4 = 2; T0_sp4 = 15; Qw_sp4 = T0_sp4; V1_sp4 = -1.2; V2_sp4 = 18; V3_sp4 = 14.95; V4_sp4 = 17.4; I_sp4 = 54;
C_sp5 = 1; E_Ca_sp5 = 120; E_K_sp5 = - 80;  E_Leak_sp5 = - 60; g_Ca_sp5 = 4;   g_K_sp5 = 8;  g_Leak_sp5 = 2; T0_sp5 = 15; Qw_sp5 = T0_sp5; V1_sp5 = -1.2; V2_sp5 = 18; V3_sp5 = 12;    V4_sp5 = 17.4; I_sp5 = 40;
C_sp6 = 1; E_Ca_sp6 = 120; E_K_sp6 = - 84;  E_Leak_sp6 = - 60; g_Ca_sp6 = 4.4; g_K_sp6 = 8;  g_Leak_sp6 = 2; T0_sp6 = 5;  Qw_sp6 = T0_sp6; V1_sp6 = -1.2; V2_sp6 = 18; V3_sp6 = 2;     V4_sp6 = 30;   I_sp6 = 120;

%initial conditions
V_sp1(1) = -12.7743548965288; W_sp1(1) = 0.376576642801617;
V_sp2(1) = -12.7743548965288; W_sp2(1) = 0.376576642801617;
V_sp3(1) = -12.7743548965288; W_sp3(1) = 0.376576642801617;
V_sp4(1) = -32.6940;          W_sp4(1) = 0.0294;
V_sp5(1) = -32.6940;          W_sp5(1) = 0.0294;
V_sp6(1) = -46.6906;          W_sp6(1) = 0.3221;

[V_sp1,W_sp1] = function_ml_am_1n(E_Ca_sp1,E_K_sp1,E_Leak_sp1,g_Ca_sp1,g_K_sp1,g_Leak_sp1,V1_sp1,V2_sp1,V3_sp1,V4_sp1,T0_sp1,I_sp1,hh,N,t,V_sp1,W_sp1,C_sp1);
[V_sp2,W_sp2] = function_ml_am_1n(E_Ca_sp2,E_K_sp2,E_Leak_sp2,g_Ca_sp2,g_K_sp2,g_Leak_sp2,V1_sp2,V2_sp2,V3_sp2,V4_sp2,T0_sp2,I_sp2,hh,N,t,V_sp2,W_sp2,C_sp2);
[V_sp3,W_sp3] = function_ml_am_1n(E_Ca_sp3,E_K_sp3,E_Leak_sp3,g_Ca_sp3,g_K_sp3,g_Leak_sp3,V1_sp3,V2_sp3,V3_sp3,V4_sp3,T0_sp3,I_sp3,hh,N,t,V_sp3,W_sp3,C_sp3);
[V_sp4,W_sp4] = function_ml_am_1n(E_Ca_sp4,E_K_sp4,E_Leak_sp4,g_Ca_sp4,g_K_sp4,g_Leak_sp4,V1_sp4,V2_sp4,V3_sp4,V4_sp4,T0_sp4,I_sp4,hh,N,t,V_sp4,W_sp4,C_sp4);
[V_sp5,W_sp5] = function_ml_am_1n(E_Ca_sp5,E_K_sp5,E_Leak_sp5,g_Ca_sp5,g_K_sp5,g_Leak_sp5,V1_sp5,V2_sp5,V3_sp5,V4_sp5,T0_sp5,I_sp5,hh,N,t,V_sp5,W_sp5,C_sp5);
[V_sp6,W_sp6] = function_ml_am_1n(E_Ca_sp6,E_K_sp6,E_Leak_sp6,g_Ca_sp6,g_K_sp6,g_Leak_sp6,V1_sp6,V2_sp6,V3_sp6,V4_sp6,T0_sp6,I_sp6,hh,N,t,V_sp6,W_sp6,C_sp6);

save mat_ml_am_sp123456.mat V_sp1 V_sp2 V_sp3 V_sp4 V_sp5 V_sp6

figure(1); clf(1);
plot(V_sp6,'k','LineWidth',2)
xlabel('Number of Samples')
ylabel('Membran Potential (mV)')
set(gca,'Fontsize',30)
grid on
