function gaussianblur(ImgName, sz)
    Img=imread(ImgName);
    %Read an Image
    I = double(Img);
    %Design the Gaussian Kernel
    %Standard Deviation
    sigma = ceil(sz/2);
    [x,y]=meshgrid(-sz:sz,-sz:sz);
    width = size(x,1)-1;
    height = size(y,1)-1;
    Equation = -(x.^2+y.^2)/(2*sigma*sigma);
    Kernel= (exp(Equation)/(2*pi*sigma*sigma));
    
    %Initialize
    imar=I;
        %Pad the vector with zeros
        I = padarray(I,[sz sz]);
        %Convolution
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
    %Image without Noise after Gaussian blur
    out = uint8(imar);
    imwrite(out,'/Users/antonzhulkovskiy/Desktop/NEA/temp/face.jpg','jpg')
end



    
