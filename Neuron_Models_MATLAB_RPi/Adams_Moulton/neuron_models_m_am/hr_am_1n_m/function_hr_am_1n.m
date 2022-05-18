function [x,y,z] = function_hr_am_1n(x,y,z,t,a,b,c,d,s,e,x0,h,N,I)

% define function handles
fx=@(t,x,y,z)   y - a*x^3 + b*x^2 + I - z;
fy=@(t,x,y)     c - d*x^2 - y;
fz=@(t,x,z)     e * ( s * ( x - x0 ) - z );

    for i=1:3

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

        x(i+1) = x(i) + h / 6 * (k1x + 2*k2x + 2*k3x + k4x);
        y(i+1) = y(i) + h / 6 * (k1y + 2*k2y + 2*k3y + k4y);
        z(i+1) = z(i) + h / 6 * (k1z + 2*k2z + 2*k3z + k4z);

    end

    for i=3:N

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
    
        x(i+1) = x(i) + h / 6 * (k1x + 2*k2x + 2*k3x + k4x);
        y(i+1) = y(i) + h / 6 * (k1y + 2*k2y + 2*k3y + k4y);
        z(i+1) = z(i) + h / 6 * (k1z + 2*k2z + 2*k3z + k4z);
    
        % adams-moulton-corrector
    
        x(i+1) = x(i) + h/24 * (9*fx(t(i+1),x(i+1),y(i+1),z(i+1)) + 19*fx(t(i),x(i),y(i),z(i)) - 5*fx(t(i-1),x(i-1),y(i-1),z(i-1)) + fx(t(i-2),x(i-2),y(i-2),z(i-2)));
        y(i+1) = y(i) + h/24 * (9*fy(t(i+1),x(i+1),y(i+1)) + 19*fy(t(i),x(i),y(i)) - 5*fy(t(i-1),x(i-1),y(i-1)) + fy(t(i-2),x(i-2),y(i-2)));
        z(i+1) = z(i) + h/24 * (9*fz(t(i+1),x(i+1),z(i+1)) + 19*fz(t(i),x(i),z(i)) - 5*fz(t(i-1),x(i-1),z(i-1)) + fz(t(i-2),x(i-2),z(i-2)));

    end
        
end

