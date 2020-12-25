%% System
AA = [1 0 -2 0 1]'; K = norm_l0(AA); p = 1; rho = norm(AA, p);

%% Measurements
N = 128; L = 512; 
X = sort(rand(N, 1) * (2*pi) - pi); Z = randn(N, 1) * .125; Y = m(X, AA) + Z;
Q = sort(rand(size(X)) * (2*pi) - pi); % "Do I feel lucky? Well, do ya, punk?" 
                                           % If not, play safe: Q = (-pi:pi/N:pi)';

subplot(5, 1, 1); plot(X, m(X, AA), 'k-', X, Y, '.'); 
title(['A system: N = ' num2str(N) ', L = ' num2str(L) ', K = ' num2str(K)]);

%% Model preparation...
% Regressors matrix
FI = cos(kron(X, 1:L));

% %% Solving LS (threefold)...
% With a textbook LS formula
warning('off', 'MATLAB:nearlySingularMatrix');
A = inv(FI' * FI) * FI' * Y; disp(showA('inv(Φ''Φ)Φ''Y => ', A, AA));
subplot(5, 1, 2); plot(X, m(X, AA), 'k-', Q, m(Q, A)); title('inv(Φ''Φ)Φ''Y');
warning('on');
% By a Matlab operator
A = FI\Y;                    disp(showA('Φ\Y => ', A, AA));
subplot(5, 1, 3); plot(X, m(X, AA), 'k-', Q, m(Q, A)); title('Φ\\Y');
% Using LS from a CVX solver
cvx_begin quiet
   cvx_solver sedumi % sdpt3 is the other one...
   
   variable A(L) 
   minimize(norm(FI * A - Y, 2)) 
cvx_end
disp(showA('arg min‖Φ*A-Y‖₂² => ', A, AA));
subplot(5, 1, 4); plot(X, m(X, AA), 'k-', Q, m(Q, A)); title('arg min‖Φ*A-Y‖₂²');

%% CVX!
cvx_begin quiet
   cvx_solver sdpt3 % 'sedumi' is the other other.

   variable A(L) 
   minimize(norm(FI * A - Y, 2)) 
   subject to 
      norm(A, p) <= rho
cvx_end
disp(showA('arg min‖Φ*A-Y‖₂² st. ‖A‖₁ <= ρ', A, AA));
subplot(5, 1, 5); plot(X, m(X, AA), 'k-', Q, m(Q, A)); title('arg min‖Φ*A-Y‖₂² st. ‖A‖₁ <= ρ');

%% Administration & beaurocracy stuff
function Y = m(X, A)
    L = length(A);
    FI = cos(kron(X, 1:L));
    Y = FI * A;
end
function L = norm_l0(A)
   L = sum(A ~= 0); 
end
function tt = showA(text, A, AA) 
   L = size(AA);
   tt = [text mat2str(A(1:L), 1) ' vs. ' mat2str(AA, 1)];
end