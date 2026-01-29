%% Filters' shapes:
   % rectangular, triangular, squared (Epanechnikov's) and cubic (Keys') interpolation functions
   totem = @(x) (abs(x) < 1/2);
   tipi =  @(x) (abs(x) < 1)  .*                                                      (1 - abs(x));
   wgwm =  @(x) (abs(x) < 1)  .*                                (3/4 * (1 - x.^2));
   Keys =  @(x)                  (abs(x) < 1) .* (  4/3 * abs(x.^3) - 7/3 * x.^2                  +    1) + ...
                (abs(x) >= 1) .* (abs(x) < 2) .* (-7/12 * abs(x.^3) +   3 * x.^2 - 59/12 * abs(x) + 15/6) + ...
                (abs(x) >= 2) .* (abs(x) < 3) .* ( 1/12 * abs(x.^3) - 2/3 * x.^2 + 21/12 * abs(x) -  3/2);

   fltr = eval('tipi');
   
bokeh = -256:8:256;
var_focus = []; grdnt_focus = []; edge_focus = [];
 
%% Image generation
for bkh = bokeh
    S = imread('images\Leopard.jpg'); 
    S = imresize(S, .5);
    w = 2;
    L = fltr(linspace(-w, w, abs(bkh) + 3)') * fltr(linspace(-w, w, abs(bkh) + 3));
    L = L/sum(L(:)); % surf(L);

    I = imfilter(S, L, 'replicate');
    subplot(3, 3, [1 2; 4 5]); imshow(I); title('Image');
    I = rgb2gray(I);
    I = I + 64 * uint8(randn(size(I),'like', double(I)));

    %% variance 
    focus_function = var(double(I(:)));
    var_focus = [var_focus, focus_function];
    %% other candidates
    % edge
    name = 'Roberts';% 'Prewitt' | 'Roberts' | 'log' | 'zerocross' | 'Canny' | 'approxcanny'
    e = edge(I, name); focus_function = sum(e(:)); 
    edge_focus = [edge_focus, focus_function];
    subplot(3, 3, 7); imshow(e); title('Edge');
    pause(0.001);
    % gradient
    grdnt = imgradient(I, name); focus_function = sum(grdnt(:));
    subplot(3, 3, 8); imshow(grdnt, [min(grdnt(:)) max(grdnt(:))]); title('Gradient');
    pause(0.001);    
    grdnt_focus = [grdnt_focus, focus_function];
    
    subplot(3, 3, 3); plot(log10(var_focus)); title('Variance AF');
    subplot(3, 3, 6); plot(log10(edge_focus)); title('Edge AF');
    subplot(3, 3, 9); plot(log10(grdnt_focus)); title('Gradient AF');
                                 
    pause(0.001);
end