clc; clear;

%step size 
h = 0.01;
N = 100000;
t(1) = 0;

% constant  
a_sp1 = 0.7; b_sp1 = 0.8; c_sp1 = 5; aa_sp1 = 0;   f_sp1=1;     I_sp1=0.35;
a_sp2 = 0.7; b_sp2 = 0.8; c_sp2 = 5; aa_sp2 = 0;   f_sp2=1;     I_sp2=0.55; 
a_sp3 = 0.7; b_sp3 = 0.8; c_sp3 = 5; aa_sp3 = 0;   f_sp3=1;     I_sp3=0.75; 
a_sp4 = 0.7; b_sp4 = 0.8; c_sp4 = 5; aa_sp4 = 0.5; f_sp4=0.130; I_sp4=0;
a_sp5 = 0.7; b_sp5 = 0.8; c_sp5 = 5; aa_sp5 = 0.5; f_sp5=0.110; I_sp5=0;
a_sp6 = 0.7; b_sp6 = 0.8; c_sp6 = 5; aa_sp6 = 0.5; f_sp6=0.129; I_sp6=0;

% initial condition
v_sp1(1) = -2;      w_sp1(1) = 1.16388;
v_sp2(1) = -2;      w_sp2(1) = 1.16388;
v_sp3(1) = -2;      w_sp3(1) = 1.16388; 
v_sp4(1) = -1.6527; w_sp4(1) = -0.0476;
v_sp5(1) = 1.6418;  w_sp5(1) = -0.4184;
v_sp6(1) = -0.6135; w_sp6(1) = -0.5666;

[v_sp1, w_sp1] = function_fhn_abm_1n(a_sp1,b_sp1,c_sp1,I_sp1,h,N,t,v_sp1,w_sp1,aa_sp1,f_sp1);
[v_sp2, w_sp2] = function_fhn_abm_1n(a_sp2,b_sp2,c_sp2,I_sp2,h,N,t,v_sp2,w_sp2,aa_sp2,f_sp2);
[v_sp3, w_sp3] = function_fhn_abm_1n(a_sp3,b_sp3,c_sp3,I_sp3,h,N,t,v_sp3,w_sp3,aa_sp3,f_sp3);
[v_sp4, w_sp4] = function_fhn_abm_1n(a_sp4,b_sp4,c_sp4,I_sp4,h,N,t,v_sp4,w_sp4,aa_sp4,f_sp4);
[v_sp5, w_sp5] = function_fhn_abm_1n(a_sp5,b_sp5,c_sp5,I_sp5,h,N,t,v_sp5,w_sp5,aa_sp5,f_sp5);
[v_sp6, w_sp6] = function_fhn_abm_1n(a_sp6,b_sp6,c_sp6,I_sp6,h,N,t,v_sp6,w_sp6,aa_sp6,f_sp6);

save mat_fhn_abm_sp123456.mat v_sp1 v_sp2 v_sp3 v_sp4 v_sp5 v_sp6

figure(1); clf(1);
plot(v_sp1,'k','LineWidth',2)
xlabel('Number of Samples')
ylabel('Membran Potential (V)')
set(gca,'Fontsize',20)
grid on
    