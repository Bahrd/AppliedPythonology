%% QuQuRickU
%% A simple implementation of a basic Grover's quantum search algorithm
% Number of qubits
Q = 3; NoS = 2^Q; 
% A location n of a marked state is randomly selected here
n = randi(NoS);
% A shortcut to a flipper
R = @(n) fR(n, NoS);
%Hadamard matrix
H = hadamard(NoS)/sqrt(NoS);
%Grover operator matrix
G = -R(n) * H * R(1) * H;

%% Uno, due, tre... 
phi_0 = zeros(NoS, 1); phi_0(1) = 1;
% NUmber of Grover operator iteration
q = floor(pi*sqrt(NoS)/4);

% An iterative (more 'quantum implementable') version... 
% (forgive the lack of the 1st/2n/third distinction please! ;)
phi = R(n) * H * phi_0;                   % Initial step (inverting a phase of the marked state)
for i = 1:q
    phi = G * phi;                        % Step-by-step amplitude amplification 
    sprintf('After %dth iteration P(No = %d) = %0.3g', i, n, phi(n)^2)
end
% or its 'en bloc genre'...
phi = (G^q) * R(n) * H * phi_0;       
sprintf('P(No = %d) = %0.3g', n, phi(n)^2)

%% Flipper (aka 'amplitude sign flipping operator')
% Flipping the sign of the ampitude of the state |n> operator
% (which happens to be a mean at |0> after Walsh-Hadamard transform)
function r = fR(n, NoS)
    psi = zeros(NoS, 1); psi(n) = 1;
    r = eye(NoS) - 2*psi*(psi');
end
