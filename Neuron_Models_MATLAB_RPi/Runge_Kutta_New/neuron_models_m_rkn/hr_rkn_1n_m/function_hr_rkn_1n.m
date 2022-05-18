function [x,y,z] = function_hr_rkn_1n(x,y,z,t,a,b,c,d,s,e,x0,h,N,I)

% define function handles
fx=@(t,x,y,z)   y - a*x^3 + b*x^2 + I - z;
fy=@(t,x,y)     c - d*x^2 - y;
fz=@(t,x,z)     e * ( s * ( x - x0 ) - z );

    for i=1:N

        t(i+1) = t(i) + h;

        k1x = fx(t(i)     ,x(i)          ,y(i)          ,z(i));
        k1y = fy(t(i)     ,x(i)          ,y(i)               );
        k1z = fz(t(i)     ,x(i)                         ,z(i));

        k2x = fx(t(i)+h/2 , x(i)+h/2*k1x , y(i)+h/2*k1y , z(i)+h/2*k1z);
        k2y = fy(t(i)+h/2 , x(i)+h/2*k1x , y(i)+h/2*k1y);
        k2z = fz(t(i)+h/2 , x(i)+h/2*k1x , z(i)+h/2*k1z);

        k3x = fx(t(i)+h/2 , x(i)+h/2*k2x , y(i)+h/2*k2y , z(i)+h/2*k2z);
        k3y = fy(t(i)+h/2 , x(i)+h/2*k2x , y(i)+h/2*k2y);
        k3z = fz(t(i)+h/2 , x(i)+h/2*k2x , z(i)+h/2*k2z);

        k4x = fx(t(i)+h   , x(i)+h*k3x   , y(i)+h*k3y   , z(i)+h*k3z);
        k4y = fy(t(i)+h   , x(i)+h*k3x   , y(i)+h*k3y);
        k4z = fz(t(i)+h   , x(i)+h*k3x   , z(i)+h*k3z);

        k5x = fx(t(i)+(3/4)*h , x(i)+(5/32)*h*k1x+(7/32)*h*k2x+(13/32)*h*k3x-(1/32)*h*k4x , y(i)+(5/32)*h*k1y+(7/32)*h*k2y+(13/32)*h*k3y-(1/32)*h*k4y , z(i)+(5/32)*h*k1z+(7/32)*h*k2z+(13/32)*h*k3z-(1/32)*h*k4z);
        k5y = fy(t(i)+(3/4)*h , x(i)+(5/32)*h*k1x+(7/32)*h*k2x+(13/32)*h*k3x-(1/32)*h*k4x , y(i)+(5/32)*h*k1y+(7/32)*h*k2y+(13/32)*h*k3y-(1/32)*h*k4y );
        k5z = fz(t(i)+(3/4)*h , x(i)+(5/32)*h*k1x+(7/32)*h*k2x+(13/32)*h*k3x-(1/32)*h*k4x , z(i)+(5/32)*h*k1z+(7/32)*h*k2z+(13/32)*h*k3z-(1/32)*h*k4z);

        x(i+1) = x(i) + h / 6 * (k1x + 2*k2x + 2*k3x + k5x);
        y(i+1) = y(i) + h / 6 * (k1y + 2*k2y + 2*k3y + k5y);
        z(i+1) = z(i) + h / 6 * (k1z + 2*k2z + 2*k3z + k5z);
    end

end

