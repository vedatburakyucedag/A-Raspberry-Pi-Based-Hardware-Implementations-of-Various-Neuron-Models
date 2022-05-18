clc; clear;

%step size 
h = 0.01; 
N = 100000;
t(1) = 0;

% constant  
a_sp1 = 1; b_sp1 = 3; c_sp1 = 1; d_sp1 = 5; s_sp1 = 4; e_sp1 = 0.003; x0_sp1 = -1.6; 
a_sp2 = 1; b_sp2 = 3; c_sp2 = 1; d_sp2 = 5; s_sp2 = 4; e_sp2 = 0.003; x0_sp2 = -1.6; 
a_sp3 = 1; b_sp3 = 3; c_sp3 = 1; d_sp3 = 5; s_sp3 = 4; e_sp3 = 0.003; x0_sp3 = -1.6; 
a_sp4 = 1; b_sp4 = 3; c_sp4 = 1; d_sp4 = 5; s_sp4 = 4; e_sp4 = 0.003; x0_sp4 = -1.6; 
a_sp5 = 1; b_sp5 = 3; c_sp5 = 1; d_sp5 = 5; s_sp5 = 4; e_sp5 = 0.006; x0_sp5 = -1.56; 

I_sp1 = 1.3; x_sp1(1) = -1.5216; y_sp1(1) = -10.6201; z_sp1(1) = 1.1468; % regular spike
I_sp2 = 1.5; x_sp2(1) = -1.5826; y_sp2(1) = -11.4504; z_sp2(1) = 1.531;  % burst of 2 spike
I_sp3 = 1.7; x_sp3(1) = -1.362;  y_sp3(1) = -7.9693;  z_sp3(1) = 1.8445; % burst of 3 spike
I_sp4 = 2.2; x_sp4(1) = -0.3945; y_sp4(1) = -0.5827;  z_sp4(1) = 1.9141; % burst of 4 spike
I_sp5 = 3.1; x_sp5(1) = -1.0908; y_sp5(1) = -4.8828;  z_sp5(1) = 3.0912; % chaotic

[x_sp1,y_sp1,z_sp1] = function_hr_am_1n(x_sp1,y_sp1,z_sp1,t,a_sp1,b_sp1,c_sp1,d_sp1,s_sp1,e_sp1,x0_sp1,h,N,I_sp1);
[x_sp2,y_sp2,z_sp2] = function_hr_am_1n(x_sp2,y_sp2,z_sp2,t,a_sp2,b_sp2,c_sp2,d_sp2,s_sp2,e_sp2,x0_sp2,h,N,I_sp2);
[x_sp3,y_sp3,z_sp3] = function_hr_am_1n(x_sp3,y_sp3,z_sp3,t,a_sp3,b_sp3,c_sp3,d_sp3,s_sp3,e_sp3,x0_sp3,h,N,I_sp3);
[x_sp4,y_sp4,z_sp4] = function_hr_am_1n(x_sp4,y_sp4,z_sp4,t,a_sp4,b_sp4,c_sp4,d_sp4,s_sp4,e_sp4,x0_sp4,h,N,I_sp4);
[x_sp5,y_sp5,z_sp5] = function_hr_am_1n(x_sp5,y_sp5,z_sp5,t,a_sp5,b_sp5,c_sp5,d_sp5,s_sp5,e_sp5,x0_sp5,h,N,I_sp5);

save mat_hr_am_sp12345.mat x_sp1 x_sp2 x_sp3 x_sp4 x_sp5

figure(1); clf(1); 
plot(x_sp5,'k','LineWidth',2)
xlabel('Number of Samples')
ylabel('Membran Potential (V)')
set(gca,'Fontsize',20)
grid on