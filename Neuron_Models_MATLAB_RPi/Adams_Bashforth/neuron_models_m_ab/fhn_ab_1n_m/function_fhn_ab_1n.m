function [v, w] = function_fhn_ab_1n(a,b,c,I,h,N,t,v,w,aa,f)
   
% define function handles
fv=@(t,v,w)  c * (v - w + I - (v^3) / 3) + (aa/(2*pi*f))*cos(2*pi*f*t);
fw=@(t,v,w)  (v - b*w + a)/c;

    for i=1:3

        t(i+1) = t(i) + h;

        k1v = fv(t(i)     ,v(i)          ,w(i)          );
        k1w = fw(t(i)     ,v(i)          ,w(i)          );

        k2v = fv(t(i)+h/2 , v(i)+h/2*k1v , w(i)+h/2*k1w );
        k2w = fw(t(i)+h/2 , v(i)+h/2*k1v , w(i)+h/2*k1w );

        k3v = fv(t(i)+h/2 , v(i)+h/2*k2v , w(i)+h/2*k2w );
        k3w = fw(t(i)+h/2 , v(i)+h/2*k2v , w(i)+h/2*k2w );

        k4v = fv(t(i)+h   , v(i)+h  *k3v , w(i)+h  *k3w );
        k4w = fw(t(i)+h   , v(i)+h  *k3v , w(i)+h  *k3w );

        v(i+1) = v(i) + h/6 * (k1v + 2*k2v + 2*k3v + k4v);
        w(i+1) = w(i) + h/6 * (k1w + 2*k2w + 2*k3w + k4w);

    end

    % adams-boshforth

    for i=4:N

        t(i+1) = t(i) + h;
    
        v(i+1) = v(i) + h/24 * (55*fv(t(i),v(i),w(i)) - 59*fv(t(i-1),v(i-1),w(i-1)) + 37*fv(t(i-2),v(i-2),w(i-2)) - 9*fv(t(i-3),v(i-3),w(i-3)));
        w(i+1) = w(i) + h/24 * (55*fw(t(i),v(i),w(i)) - 59*fw(t(i-1),v(i-1),w(i-1)) + 37*fw(t(i-2),v(i-2),w(i-2)) - 9*fw(t(i-3),v(i-3),w(i-3)));
    
    end
    
end

