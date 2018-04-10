clc;
clear;
path_groundtruth_image = 'C:/YL_course/CSCE 633/project/code/results/groundtruth';
path_dehazed_image = 'C:/YL_course/CSCE 633/project/code/results/dehaze_aodnet';

% get the file name of two images to be compared
listing = dir(path_dehazed_image);  %list all dehazing output
num_dehazed_image = length(listing) -2; % exclue . and .. returned by dir command
total_psnr = 0;
total_ssim = 0;
measure_array = struct([]);
idx = 1;  %idx for measure array 

for i = 1: 5 %num_dehazed_image    
    if(listing(i).isdir == 0)
        dehazed_image = listing(i).name;
        image_idx = strtok(dehazed_image,'_');
        filename_groundtruth_image = fullfile(path_groundtruth_image,strcat(image_idx,'.png'));
        filename_dehazed_image = fullfile(path_dehazed_image,dehazed_image);
        groundtruth_image=imread(filename_groundtruth_image);
        dehazed_iamge=imread(filename_dehazed_image);
        
        % compute PSNR
        image_psnr = 0;
        for channel = 1:3
            x = groundtruth_image(:,:,channel);
            y = dehazed_iamge(:,:,channel);
            channel_psnr = psnr(x,y);
            image_psnr = image_psnr + channel_psnr;
        end
        
        % compute the SSIM
        image_ssim = ssim(dehazed_iamge, groundtruth_image);
        
        field1 = 'name';
        value1 = listing(i).name;
        field2 = 'PSNR';
        value2 = image_psnr/3;
        field3 = 'SSIM';
        value3 = image_ssim;
        st = struct(field1,value1,field2,value2,field3,value3);
        if(idx == 1)    
            measure_array = st;
        else    
            measure_array(idx) = st;
        end
        idx = idx +1;       
        
        total_psnr = total_psnr + image_psnr/3;
        total_ssim = total_ssim + image_ssim;
    end
end

save('result_per_image.mat','measure_array');
avg_psnr_dataset = total_psnr/num_dehazed_image
avg_ssim_dataset = total_ssim/num_dehazed_image

