%% QuQuRickU
% A simple implementation of a basic Grover's quantum search algorithm

% Number of qubits
Q = 6; NoS = 2^Q; 
% A marked state |n>...
n = randi(NoS);

%% Preparations
phi_n = zeros(NoS, 1); phi_n(n) = 1;

% Reflection w.r.t. |n>
R = eye(NoS) - 2*phi_n*(phi_n');

% Initial state |0...0>
phi_0 = zeros(NoS, 1); phi_0(1) = 1;
% Reflection w.r.t. |0>
I = eye(NoS) - 2*phi_0*(phi_0');
%Hadamard matrix
H = hadamard(NoS)/sqrt(NoS);
%Grover operator matrix
G = -R*H*I*H;


%% Uno, due, tre...
fi = R*H*phi_0;             % Initial step (inverting a phase of the marked state)
for i = 1:floor(pi*sqrt(NoS)/4)
    fi = G*fi;              % Step-by-step amplitude amplification 
    sprintf('%dth iteration yields %d with prob. %0.3g', i, n, fi(n)^2)
end

% or...
fi = R*H*phi_0;             % Initial step (inverting a phase of the marked state)
q = floor(pi*sqrt(NoS)/4);
fi = (G^q)*fi;              % En bloc amplitude amplification
sprintf('%dth power of G yields %d with prob. %0.3g', q, n, fi(n)^2)
