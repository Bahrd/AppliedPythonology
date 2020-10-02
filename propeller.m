%% Preliminaries...
close all;

blades = 4; rpm = pi/47; alpha = 0.0:pi*0.01:2*pi;

%% Initial drawing...
rho = sin(blades*alpha + rpm);
polarplot(alpha, rho, 'r');

%% Animation...
% Horizontal scanning (vertical one is an exercise for a reader... ;))
h = getframe(gcf); frame = h.cdata;
for m = 2:1:size(h.cdata, 1)
    rho = sin(blades*alpha + m*rpm);
    polarplot(alpha, rho, 'r');
    h = getframe(gcf); frame(m, :, :) = h.cdata(m, :, :);
end
%% Demonstration!
imshow(frame);