function gaussianblur(ImgName, sz)
    Img=imread(ImgName);
    %Read the Image file
    I = double(Img);
    %Design the Gaussian Kernel using 3d gaussian function
    %Standard Deviation to measure the width and height of kernel
    sigma = ceil(sz/2);
    [x,y]=meshgrid(-sz:sz,-sz:sz);
    width = size(x,1)-1;
    height = size(y,1)-1;
    Equation = -(x.^2+y.^2)/(2*sigma*sigma);
    Kernel= (exp(Equation)/(2*pi*sigma*sigma));
    
    %Initialize the matrix/3darray to manipulate rgb values of image
    imar=I;
        %Pad the vector with zeros to ensure the blurring does not go
        %outside the image causing error
        I = padarray(I,[sz sz]);
        %Convolution of the kernel, gaussian function applied to every
        %pixel in image of the face
        for i = 1:size(I,1)-width
            for j = 1:size(I,2)-height
                p=i+width;
                q=j+height;
                temp1 = I(i:p,j:q,1).*Kernel;
                temp2 = I(i:p,j:q,2).*Kernel;
                temp3 = I(i:p,j:q,3).*Kernel;
                imar(i,j,1)=sum(temp1(:));
                imar(i,j,2)=sum(temp2(:));
                imar(i,j,3)=sum(temp3(:));
            end
        end
    %Blurred image of face after Gaussian blur has been applied is saved
    %into temp folder to be pasted into original image.
    out = uint8(imar);
    imwrite(out,'./temp/face.jpg','jpg')
end



    
