function [V,h,m,n] = function_hh_rkn_1n(I,C,E_Na,E_K,E_Leak,g_Na,g_K,g_Leak,t,V,h,m,n,hh,N,a,f,Vrest)

% am= (0.1*(25-V))/(exp((25-V)/10)-1);
% an = (0.01*(10-V))/(exp((10-V)/10)-1);
% ah = 0.07*exp(-V/20);
% Bm = 4*exp(-V/18); 
% Bn = 0.125*exp(-V/80);
% Bh = 1/(exp((30-V)/10)+1);

% define function handles
fV=@(t,V,h,m,n) (((I+a*sin(2*pi*f*t)) - ((g_Na * h * m^3 * (V - E_Na)) + (g_K * n^4 * (V - E_K)) + (g_Leak * (V - E_Leak)))) / C) ;
fh=@(t,V,h)     0.07*exp(-(V+Vrest)/20) * (1 - h) - 1/(exp((30-(V+Vrest))/10)+1) * h;
fm=@(t,V,m)     (0.1*(25-(V+Vrest)))/(exp((25-(V+Vrest))/10)-1) * (1 - m) - 4*exp(-(V+Vrest)/18) * m;
fn=@(t,V,n)     (0.01*(10-(V+Vrest)))/(exp((10-(V+Vrest))/10)-1) * (1 - n) - 0.125*exp(-(V+Vrest)/80) * n;

for i=1:N
    
    t(i+1) = t(i) + hh;
    
    k1V = fV(t(i)     ,V(i)          ,h(i)   ,m(i)  ,n(i));
    k1h = fh(t(i)     ,V(i)          ,h(i)               );
    k1m = fm(t(i)     ,V(i)          ,m(i)               );
    k1n = fn(t(i)     ,V(i)          ,n(i)               );
    
    k2V = fV(t(i)+hh/2 , V(i)+hh/2*k1V , h(i)+hh/2*k1h , m(i)+hh/2*k1m , n(i)+hh/2*k1n);
    k2h = fh(t(i)+hh/2 , V(i)+hh/2*k1V , h(i)+hh/2*k1h);
    k2m = fm(t(i)+hh/2 , V(i)+hh/2*k1V , m(i)+hh/2*k1m);
    k2n = fn(t(i)+hh/2 , V(i)+hh/2*k1V , n(i)+hh/2*k1n);
    
    k3V = fV(t(i)+hh/2 , V(i)+hh/2*k2V , h(i)+hh/2*k2h , m(i)+hh/2*k2m , n(i)+hh/2*k2n);
    k3h = fh(t(i)+hh/2 , V(i)+hh/2*k2V , h(i)+hh/2*k2h);
    k3m = fm(t(i)+hh/2 , V(i)+hh/2*k2V , m(i)+hh/2*k2m);
    k3n = fn(t(i)+hh/2 , V(i)+hh/2*k2V , n(i)+hh/2*k2n);
    
    k4V = fV(t(i)+hh   , V(i)+hh  *k3V , h(i)+hh  *k3h , m(i)+hh  *k3m , n(i)+hh  *k3n);
    k4h = fh(t(i)+hh   , V(i)+hh  *k3V , h(i)+hh  *k3h);
    k4m = fm(t(i)+hh   , V(i)+hh  *k3V , m(i)+hh  *k3m);
    k4n = fn(t(i)+hh   , V(i)+hh  *k3V , n(i)+hh  *k3n);
    
    k5V = fV(t(i)+hh   , V(i)+(5/32)*hh*k1V+(7/32)*hh*k2V+(13/32)*hh*k3V-(1/32)*hh*k4V, h(i)+(5/32)*hh*k1h+(7/32)*hh*k2h+(13/32)*hh*k3h-(1/32)*hh*k4h, m(i)+(5/32)*hh*k1m+(7/32)*hh*k2m+(13/32)*hh*k3m-(1/32)*hh*k4m , n(i)+(5/32)*hh*k1n+(7/32)*hh*k2n+(13/32)*hh*k3n-(1/32)*hh*k4n);
    k5h = fh(t(i)+hh   , V(i)+(5/32)*hh*k1V+(7/32)*hh*k2V+(13/32)*hh*k3V-(1/32)*hh*k4V, h(i)+(5/32)*hh*k1h+(7/32)*hh*k2h+(13/32)*hh*k3h-(1/32)*hh*k4h);
    k5m = fm(t(i)+hh   , V(i)+(5/32)*hh*k1V+(7/32)*hh*k2V+(13/32)*hh*k3V-(1/32)*hh*k4V, m(i)+(5/32)*hh*k1m+(7/32)*hh*k2m+(13/32)*hh*k3m-(1/32)*hh*k4m);
    k5n = fn(t(i)+hh   , V(i)+(5/32)*hh*k1V+(7/32)*hh*k2V+(13/32)*hh*k3V-(1/32)*hh*k4V, n(i)+(5/32)*hh*k1n+(7/32)*hh*k2n+(13/32)*hh*k3n-(1/32)*hh*k4n);
    
    V(i+1) = V(i) + hh / 6 * (k1V + 2*k2V + 2*k3V + k5V);
    h(i+1) = h(i) + hh / 6 * (k1h + 2*k2h + 2*k3h + k5h);
    m(i+1) = m(i) + hh / 6 * (k1m + 2*k2m + 2*k3m + k5m);
    n(i+1) = n(i) + hh / 6 * (k1n + 2*k2n + 2*k3n + k5n);
end

end

