%% walsh hadamard discrete cosine wavelet image thresholding
function whdcwt

    %% Some helpful functions
    function AA = nrmd(A)
        AA = A/max(abs(A(:)));
    end
    function AA = trhd(A, T)
        A(abs(A) < T) = 0;
        AA = A;
    end
    %% An image 
    A = imresize(imread('images\Lampart.jpg'), [512 512]);
    A = rgb2gray(A); % ?All I see turns to brown? - to gray, in fact (for simplicity)

    %% GUI Slider
    f = gcf; 
    c = uicontrol(f, 'Style', 'slider');
        c.Value = 0.0;
        c.Callback = @sliderMovement;
        warning('off'); 
            imshow(A, []); 
        warning('on');
    %% A GUI slider handler with the transforms
    function sliderMovement(src, ~)
        transform = 'DCT'; 
        
        switch(transform)
        %% Discrete cosine transform
        case 'DCT' 
            % (Forward) Transform
            B = dct2(double(A)); 
            
            % Thresholding
            B(abs(B) < src.Value * 256) = 0; BB = B ~= 0;
            
            % Visualisation
            warning('off');
               subplot(1, 2, 1); imshow(log(abs(B)), []); title('Cosine Transform');
            warning('on');
            
            % Inverse transform
            B = idct2(B);
        end
        %% Show the result!
        BB = sum(BB(:));
        warning('off');
            subplot(1, 2, 2); 
            imshow(B, []);
            title(['Non-zeros = ' string(round(100*BB/numel(A), 2)) '%']); % prod(size(A))
        warning('on');
    end
end