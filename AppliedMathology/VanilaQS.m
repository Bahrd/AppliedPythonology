%% QuQuRickU
clear psi;
%% A simple implementation of a basic Grover's quantum search algorithm
% Number of qubits
Q = 10; 

% Declarations and definitions...
NoS = 2^Q;                                               % A database size
n = randi(NoS);                                          % A location of a marked state |n> 
                                                         % is randomly selected
psi = @(n, NoS) [zeros(n - 1, 1); 1; zeros(NoS - n, 1)]; % The shortcut to a state constructor... 
R =   @(n, NoS) eye(NoS) - 2*psi(n, NoS)*(psi(n, NoS)'); % ... and to a sign flipper R(n) = I - 2|n><n|

H = hadamard(NoS)/sqrt(NoS);                             % A normalized Hadamard matrix
Rn = R(n, NoS); R1 = R(1, NoS);                          % Flippers
G = -Rn * H * R1 * H;                                    % The Grover operator matrix

%% Uno, due, tre... 
q = floor(pi*sqrt(NoS)/4);                               % NUmber of Grover operator iterations

% An iterative (more 'quantum implementable') version... 
% (forgive the lack of the 1st/2n/third distinction please! ;)
O = psi(1, NoS);
phi = Rn * H * O;                                        % Initial step (inverting a phase of the marked state)
for i = 1:q
    phi = G * phi;                                       % Step-by-step amplitude amplification 
    sprintf('After %dth iteration P(No = %d) = %0.3g', i, n, phi(n)^2)
end
% or its 'en bloc genre'...
phi = (G^q) * Rn * H * O;       
sprintf('P(No = %d) = %0.3g', n, phi(n)^2)