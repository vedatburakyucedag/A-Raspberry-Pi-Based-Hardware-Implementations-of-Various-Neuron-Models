clc; clear;

%step size 
h = 0.001; 
N = 100000;
t(1) = 0;

% constant  
v_fs(1) = -59.9672089938647; u_fs(1) = -5.11921375684172;  a_fs = 0.1;  b_fs = 0.2;  c_fs = - 65; d_fs = 2;    I = 14; % fast spike 
v_rz(1) = -59.9672089938647; u_rz(1) = -5.11921375684172;  a_rz = 0.1;  b_rz = 0.25; c_rz = - 65; d_rz = 2;    I = 14; % rezonator 
v_tc(1) = -56.7120192753411; u_tc(1) = -9.56415562108134;  a_tc = 0.02; b_tc = 0.25; c_tc = - 65; d_tc = 0.05; I = 14; % thalamo-cortical 
v_rs(1) = -61.7920982608309; u_rs(1) = -3.39870393059430;  a_rs = 0.02; b_rs = 0.2;  c_rs = - 65; d_rs = 8;    I = 14; % regular spike
v_lt(1) = -59.0153582118010; u_lt(1) = -3.23819109280000;  a_lt = 0.02; b_lt = 0.25; c_lt = - 65; d_lt = 2;    I = 14; % low-treshold spike 
v_br(1) = -75.9863850233;    u_br(1) = 4.663766036689;     a_br = 0.02; b_br = 0.25; c_br = - 50; d_br = 4;    I_br = 20; % burst of 3 spike

[v_fs,u_fs] = function_iz_am_1n(a_fs,b_fs,c_fs,I,d_fs,t,v_fs,u_fs,h,N);
[v_rz,u_rz] = function_iz_am_1n(a_rz,b_rz,c_rz,I,d_rz,t,v_rz,u_rz,h,N);
[v_tc,u_tc] = function_iz_am_1n(a_tc,b_tc,c_tc,I,d_tc,t,v_tc,u_tc,h,N);
[v_rs,u_rs] = function_iz_am_1n(a_rs,b_rs,c_rs,I,d_rs,t,v_rs,u_rs,h,N);
[v_lt,u_lt] = function_iz_am_1n(a_lt,b_lt,c_lt,I,d_lt,t,v_lt,u_lt,h,N);
[v_br,u_br] = function_iz_am_1n(a_br,b_br,c_br,I_br,d_br,t,v_br,u_br,h,N);

save mat_iz_am_sp123456.mat v_fs v_rz v_tc v_rs v_lt v_br

figure(1); clf(1);
plot(v_rz,'k','LineWidth',1)
xlabel('Number of Samples')
ylabel('Membran Potential (mV)')
set(gca,'Fontsize',20)
grid on

