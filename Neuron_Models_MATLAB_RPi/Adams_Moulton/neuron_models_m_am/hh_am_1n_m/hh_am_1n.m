clc; clear;

% step size 
hh = 0.01;
N = 100000;
t(1) = 0;

% constant  
I_sp1 = 10; C_sp1 = 1; E_Na_sp1 = 120; E_K_sp1 = - 12; E_Leak_sp1 = 10.6;  g_Na_sp1 = 120; g_K_sp1 = 36; g_Leak_sp1 = 0.3; a_sp1 = 0;  f_sp1 = 0;    Vrest_sp1 = 0;      
I_sp2 = 15; C_sp2 = 1; E_Na_sp2 = 120; E_K_sp2 = - 12; E_Leak_sp2 = 10.6;  g_Na_sp2 = 120; g_K_sp2 = 36; g_Leak_sp2 = 0.3; a_sp2 = 0;  f_sp2 = 0;    Vrest_sp2 = 0;         
I_sp3 = 20; C_sp3 = 1; E_Na_sp3 = 120; E_K_sp3 = - 12; E_Leak_sp3 = 10.6;  g_Na_sp3 = 120; g_K_sp3 = 36; g_Leak_sp3 = 0.3; a_sp3 = 0;  f_sp3 = 0;    Vrest_sp3 = 0;
I_sp4 = 15; C_sp4 = 1; E_Na_sp4 = 50;  E_K_sp4 = - 77; E_Leak_sp4 = -54.5; g_Na_sp4 = 120; g_K_sp4 = 36; g_Leak_sp4 = 0.3; a_sp4 = 0;  f_sp4 = 0;    Vrest_sp4 = 65;
I_sp5 = 0;  C_sp5 = 1; E_Na_sp5 = 115; E_K_sp5 = - 12; E_Leak_sp5 = 10.6;  g_Na_sp5 = 120; g_K_sp5 = 36; g_Leak_sp5 = 0.3; a_sp5 = 15; f_sp5 = 0.02; Vrest_sp5 = 0;
I_sp6 = 0;  C_sp6 = 1; E_Na_sp6 = 115; E_K_sp6 = -12;  E_Leak_sp6 = 10.6;  g_Na_sp6 = 120; g_K_sp6 = 36; g_Leak_sp6 = 0.3; a_sp6 = 15; f_sp6 = 0.04; Vrest_sp6 = 0;

% initial conditions
V_sp1(1) = 2.85;     h_sp1(1) = 0.45;   m_sp1(1) = 0.06;   n_sp1(1) = 0.39;
V_sp2(1) = 2.85;     h_sp2(1) = 0.45;   m_sp2(1) = 0.06;   n_sp2(1) = 0.39;
V_sp3(1) = 2.85;     h_sp3(1) = 0.45;   m_sp3(1) = 0.06;   n_sp3(1) = 0.39;
V_sp4(1) = -60.9702; h_sp4(1) = 0.0632; m_sp4(1) = 0.3042; n_sp4(1) = 0.6940;
V_sp5(1) = 1.8606;   h_sp5(1) = 0.8729; m_sp5(1) = 0.0586; n_sp5(1) = 0.1730;
V_sp6(1) = 1.8606;   h_sp6(1) = 0.8729; m_sp6(1) = 0.0586; n_sp6(1) = 0.1730;

[V_sp1,h_sp1,m_sp1,n_sp1] = function_hh_am_1n(I_sp1,C_sp1,E_Na_sp1,E_K_sp1,E_Leak_sp1,g_Na_sp1,g_K_sp1,g_Leak_sp1,t,V_sp1,h_sp1,m_sp1,n_sp1,hh,N,a_sp1,f_sp1,Vrest_sp1);
[V_sp2,h_sp2,m_sp2,n_sp2] = function_hh_am_1n(I_sp2,C_sp2,E_Na_sp2,E_K_sp2,E_Leak_sp2,g_Na_sp2,g_K_sp2,g_Leak_sp2,t,V_sp2,h_sp2,m_sp2,n_sp2,hh,N,a_sp2,f_sp2,Vrest_sp2);
[V_sp3,h_sp3,m_sp3,n_sp3] = function_hh_am_1n(I_sp3,C_sp3,E_Na_sp3,E_K_sp3,E_Leak_sp3,g_Na_sp3,g_K_sp3,g_Leak_sp3,t,V_sp3,h_sp3,m_sp3,n_sp3,hh,N,a_sp3,f_sp3,Vrest_sp3);
[V_sp4,h_sp4,m_sp4,n_sp4] = function_hh_am_1n(I_sp4,C_sp4,E_Na_sp4,E_K_sp4,E_Leak_sp4,g_Na_sp4,g_K_sp4,g_Leak_sp4,t,V_sp4,h_sp4,m_sp4,n_sp4,hh,N,a_sp4,f_sp4,Vrest_sp4);
[V_sp5,h_sp5,m_sp5,n_sp5] = function_hh_am_1n(I_sp5,C_sp5,E_Na_sp5,E_K_sp5,E_Leak_sp5,g_Na_sp5,g_K_sp5,g_Leak_sp5,t,V_sp5,h_sp5,m_sp5,n_sp5,hh,N,a_sp5,f_sp5,Vrest_sp5);
[V_sp6,h_sp6,m_sp6,n_sp6] = function_hh_am_1n(I_sp6,C_sp6,E_Na_sp6,E_K_sp6,E_Leak_sp6,g_Na_sp6,g_K_sp6,g_Leak_sp6,t,V_sp6,h_sp6,m_sp6,n_sp6,hh,N,a_sp6,f_sp6,Vrest_sp6);

save mat_hh_am_sp123456.mat V_sp1 V_sp2 V_sp3 V_sp4 V_sp5 V_sp6
 
figure(1); clf(1);
plot(V_sp4,'k','LineWidth',2)
xlabel('Number of Samples')
ylabel('Membran Potential (mV)')
set(gca,'Fontsize',20)
grid on
