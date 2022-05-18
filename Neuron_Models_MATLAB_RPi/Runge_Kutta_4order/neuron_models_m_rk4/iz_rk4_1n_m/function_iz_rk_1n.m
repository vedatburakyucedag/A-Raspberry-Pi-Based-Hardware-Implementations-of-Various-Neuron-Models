function [v,u] = function_iz_rk_1n(a,b,c,I,d,t,v,u,h,N)

% define function handles
fv=@(t,v,u)   0.04*v^2 + 5*v + 140 - u + I;
fu=@(t,v,u)   a*(b*v - u);

    %update loop
    for i=1:N

        t(i+1) = t(i) + h;

        k1v = fv(t(i)     ,v(i)          ,u(i)          );
        k1u = fu(t(i)     ,v(i)          ,u(i)          );

        k2v = fv(t(i)+h/2 , v(i)+h/2*k1v , u(i)+h/2*k1u );
        k2u = fu(t(i)+h/2 , v(i)+h/2*k1v , u(i)+h/2*k1u );

        k3v = fv(t(i)+h/2 , v(i)+h/2*k2v , u(i)+h/2*k2u );
        k3u = fu(t(i)+h/2 , v(i)+h/2*k2v , u(i)+h/2*k2u );

        k4v = fv(t(i)+h   , v(i)+h  *k3v , u(i)+h  *k3u );
        k4u = fu(t(i)+h   , v(i)+h  *k3v , u(i)+h  *k3u );

        if v(i)>=30

            v(i) = c;
            v(i+1) = v(i) + h/6 * (k1v + 2*k2v + 2*k3v + k4v);

            u(i) = u(i) + d;
            u(i+1) = u(i) + h/6 * (k1u + 2*k2u + 2*k3u + k4u);
            
        else

            v(i+1) = v(i) + h/6 * (k1v + 2*k2v + 2*k3v + k4v);
            u(i+1) = u(i) + h/6 * (k1u + 2*k2u + 2*k3u + k4u);

    end

end

