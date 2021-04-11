%% QuQuRickU
%% A simple implementation of a basic Grover's quantum search algorithm
% Number of qubits
Q = 5; NoS = 2^Q; 
% A location n of a marked state is randomly selected here
n = randi(NoS);
% A shortcut to a flipper
R = @(n) fR(n, NoS);
%Hadamard matrix
H = hadamard(NoS)/sqrt(NoS);
%Grover operator matrix
G = -R(n)*H*R(1)*H;

%% Uno, due, tre...
phi_0 = zeros(NoS, 1); phi_0(1) = 1;
phi = R(n)*H*phi_0;                 % Initial step (inverting a phase of the marked state)
for i = 1:floor(pi*sqrt(NoS)/4)
    phi = G*phi;                    % Step-by-step amplitude amplification 
    sprintf('%dth iteration yields %d with prob. %0.3g', i, n, phi(n)^2)
end
% or in an 'en bloc!' version...
phi = R(n)*H*phi_0;
q = floor(pi*sqrt(NoS)/4);
phi = (G^q)*phi;              
sprintf('%dth power of G yields %d with prob. %0.3g', q, n, phi(n)^2)

%% Flipper (aka 'amplitude sign flipping operator')
% Flipping the sign of the ampitude of the state |n> operator
% (which happens to be a mean after Walsh-Hadamard transform when |0>)
function r = fR(n, NoS)
    psi = zeros(NoS, 1); psi(n) = 1;
    r = eye(NoS) - 2*psi*(psi');
end
