
A = imresize(imread('images\Lampart.jpg'), [512 512]);
A = rgb2gray(A); 

wn = 'bior4.4';  % bior1.1 == Haar wavelets; bior2.2 == Le Gal (5/3); bior4.4 == CDF (9/7) 
dwtmode('per');

% % One for a show...
% imshow(A);
% [cA, cV, cH, cD] = dwt2(A, wn);
% imshow([nrmd(cA), nrmd(cH); nrmd(cV), nrmd(cD)])
% pause;
% 
% A = idwt2(cA, cV, cH, cD, wn);
% imshow(A, [])
% pause;

% % ... or for computations!
L = 8; [B, C] = wavedec2(A, L, wn); %L = 1, ... log_2(N)
    T = 64; B(abs(B) < T) = 0; 
    %B = QQ(B, -6);
    BB = B ~= 0; BB = sum(BB(:));
A = waverec2(B, C, wn);

imshow(A, []); title([string(round(100*BB/numel(A), 2))+'% of non-zeros']); 


function AA = nrmd(A)
    AA = abs(A/max(abs(A(:))));
end