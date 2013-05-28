function ExchangeTure=Video2Txt(VideoPath)
% ExchangeTure=Video2Txt(VideoPath)
%Input: Video path
%Output: Ture or False
%Exchange every frames of the video to ASCII figures
readerobj=VideoReader(VideoPath);
vidFrames=read(readerobj);
ramp=['@@@@@@@######MMMBBHHHAAAA&&GGhh9933XXX222255SSSiiiissssrrrrrrr;;;;;;;;:::::::,,,,,,,........'];
for FrameNumber=1:3:get(readerobj,'NumberOfFrames')-1
    fid=fopen(strcat([num2str(FrameNumber),'.txt']),'w');
    frame=vidFrames(:,:,:,FrameNumber);
    frame=mean(frame,3);
    stepx=3;
    stepy=3;
    sizx=fix(size(frame,2)/stepx);
    sizy=fix(size(frame,1)/stepy);
    lumin=zeros(sizy,sizx);
    for j=1:stepy
        for k=1:stepx
            lumin=lumin+frame(j:stepy:(sizy-1)*stepy+j,k:stepx:(sizx-1)*stepx+k);
        end
    end
    str=ramp(fix(lumin/(stepx*stepy)/256*length(ramp))+1);
    for h=1:sizy
        fwrite(fid,[str(h,:),13,10]);
    end
    fclose(fid);
end
ExchangeTure=1;