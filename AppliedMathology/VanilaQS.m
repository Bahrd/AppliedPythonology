%% QuQuRickU
clear psi;
%% A simple implementation of a basic Grover's quantum search algorithm
% Number of qubits
Q = 7; NoS = 2^Q; 
% A location n of a marked state |n> is randomly selected here
n = randi(NoS);
% The shortcuts to a state constructor... 
psi = @(n, NoS) [zeros(n - 1, 1); 1; zeros(NoS - n, 1)];
% ... and to a sign flipper R(n) = I - 2|n><n|
R = @(n) eye(NoS) - 2*psi(n, NoS)*(psi(n, NoS)');

% A normalized Hadamard matrix
H = hadamard(NoS)/sqrt(NoS);
% Grover operator matrix
G = -R(n) * H * R(1) * H;

%% Uno, due, tre... 
% NUmber of Grover operator iterations
q = floor(pi*sqrt(NoS)/4);

% An iterative (more 'quantum implementable') version... 
% (forgive the lack of the 1st/2n/third distinction please! ;)
O = psi(1, NoS);
phi = R(n) * H * O;                     % Initial step (inverting a phase of the marked state)
for i = 1:q
    phi = G * phi;                      % Step-by-step amplitude amplification 
    sprintf('After %dth iteration P(No = %d) = %0.3g', i, n, phi(n)^2)
end
% or its 'en bloc genre'...
phi = (G^q) * R(n) * H * O;       
sprintf('P(No = %d) = %0.3g', n, phi(n)^2)