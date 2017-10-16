from vodtolive import HLSVod
import threading

def main():
    
    vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')
    #vod = HLSVod('http://184.72.239.149/vod/smil:BigBuckBunny.smil/playlist.m3u8')
    #vod.dump()
    #print "LIST PLAYLISTS"
    #vod.list_playlists()
    #print('HLS START')
    
    #text_file = open("text_file.txt", "w")
        
    #playIsActive = True
    vod.write_to_textfile("test/")
    print("GET SEGMENTS: ")
    print vod.get_segment('808400')
    vod.next()
        
    '''def timerFunction():
        timer = threading.Timer(3.0, timerFunction)
        if playIsActive == True:
        timer.start()
        #print vod.get_segment('18830456')
        
        for bw in vod.m3u8_obj.playlists:
        bandwidths = []
        bw = bw.stream_info.bandwidth
        bandwidths.append(bw)
        #print("Bandwidth")
        #print bw
        for x in bandwidths:
        print "2 SEGMENTS with bandwidth " + str(x)
        #print x
        #print vod.get_segment(str(x))
        segments = vod.get_segment(str(x))
        print segments
        #text_file.write(segments)
        vod.next()
        
        else:
        timer.cancel()
        timerFunction()
        '''

if __name__ == '__main__':
    try:
        main()
    except Exception, err:
        raise
