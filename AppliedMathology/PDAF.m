%% Filters' shapes:
   % rectangular, triangular, squared (Epanechnikov's) and cubic (Keys') interpolation functions
   totem = @(x) (abs(x) < 1/2);
   tipi =  @(x) (abs(x) < 1)  .*                                                      (1 - abs(x));
   wgwm =  @(x) (abs(x) < 1)  .*                                (3/4 * (1 - x.^2));
   Keys =  @(x)                  (abs(x) < 1) .* (  4/3 * abs(x.^3) - 7/3 * x.^2                  +    1) + ...
                (abs(x) >= 1) .* (abs(x) < 2) .* (-7/12 * abs(x.^3) +   3 * x.^2 - 59/12 * abs(x) + 15/6) + ...
                (abs(x) >= 2) .* (abs(x) < 3) .* ( 1/12 * abs(x.^3) - 2/3 * x.^2 + 21/12 * abs(x) -  3/2);
   Keysq = @(x) Keys(x) .* Keys(x);

   fltr = eval('Keysq');
  
%% Apertures & blurring
bokeh = -256:8:256;
 
for bkh = bokeh
    S = imread('images\Leopard.jpg'); S = imresize(S, .5);
    % Separable (product) filters generation
    w  = 2;
    V  = fltr(linspace(-w, w, abs(bkh) + 3));
    HL = fltr(linspace(-w, 0, abs(bkh/2) + 3)); HR = fltr(linspace( 0, w, abs(bkh/2) + 3));  
    L = V' * HL; R = V' * HR;
    % Filter normalization
    L = L/sum(L(:)); R = R/sum(R(:));  %surf(L); surf(R);    
    % Swapping left and right apertures
    if(bkh < 0)
        P = L; L = R; R = P;
    end

    IL = imfilter(S, L, 'replicate');
         subplot(2, 3, 1); imshow(IL); pause(0.05);
    IR = imfilter(S, R, 'replicate');
         subplot(2, 3, 3); imshow(IR); pause(0.05);
    % subplot(2, 1, 1);imshow(IL/2 + IR/2); pause(0.05);
    % B&W PD AF
    IL = rgb2gray(IL); IR = rgb2gray(IR); 
         subplot(2, 3, 2); plot(1:512, IL(512, :), 1:512, IR(512, :))
         subplot(2, 3, [4 5 6]); 
         crosscorr(double(IL(512, :)), double(IR(512, :)), 'NumLags', 128);
         pause(0.025);
end

%% TO DO
% Fancy to implement an RGB AF in Matlab?