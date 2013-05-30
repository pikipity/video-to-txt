function ExchangeTure=Video2Txt(VideoPath,DataPath,stepx,stepy,FrameStep)
% ExchangeTure=Video2Txt(VideoPath)
%Input: Video path
%Output: Ture or False
%Exchange every frames of the video to ASCII figures
readerobj=VideoReader(VideoPath);
vidFrames=read(readerobj);
ramp=['@@@@@@@######MMMBBHHHAAAA&&GGhh9933XXX222255SSSiiiissssrrrrrrr;;;;;;;;:::::::,,,,,,,........'];
FrameStep=fix(FrameStep);
if FrameStep<=1 || FrameStep>=get(readerobj,'NumberOfFrames')-1
    FrameStep=3;
end
for FrameNumber=1:FrameStep:get(readerobj,'NumberOfFrames')-1
    fid=fopen(strcat([DataPath,num2str(FrameNumber),'.txt']),'w');
    frame=vidFrames(:,:,:,FrameNumber);
    frame=mean(frame,3);
    stepx=fix(stepx);
    if stepx<=0
        stepx=3;
    end
    stepy=fix(stepy);
    if stepy<=0
        stepy=3;
    end
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