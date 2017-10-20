from vodtolive import HLSVod
import threading

def main():

    vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')

    def create_live_master_playlist_file(mastermanifeststring):
        newMasterPlaylistFile = 'masterplaylistfile.m3u8'
        x = open(newMasterPlaylistFile,'w')
        x.write(mastermanifeststring)
        x.close()

    def create_live_media_playlist_file(mediamanifeststring, bandwidth):
        newMediaPlaylistFile = str(bandwidth) + '.m3u8'
        x = open(newMediaPlaylistFile,'w')
        x.write(mediamanifeststring)
        x.close()   

    mastermanifeststring = vod.get_live_master_manifest()

    for playlist in vod.m3u8_obj.playlists:
        bandwidth = str(playlist.stream_info.bandwidth)
        mediamanifeststring = vod.get_live_media_manifest(bandwidth)
        print("########## MEDIA PLAYLIST STARTS ##########")
        print(mediamanifeststring)
        print("########## MEDIA PLAYLIST ENDS ##########")
        print("\n")
        resolution = ""
        if playlist.stream_info.resolution != None:
            for res in playlist.stream_info.resolution:
                resolution += str(res)
                if res != playlist.stream_info.resolution[-1]:
                    resolution += "x"
        else:
            resolution = "audio"
        create_live_media_playlist_file(mediamanifeststring, playlist.stream_info.bandwidth)

    print("########## MASTER MANIFEST STARTS ##########")
    print vod.get_live_master_manifest()
    print("########## MASTER MANIFEST ENDS ##########")

    create_live_master_playlist_file(mastermanifeststring)

    #print("GET SEGMENTS: ")
    #print vod.get_segment('808400')
    #vod.next()
        
    '''def timerFunction():
        timer = threading.Timer(3.0, timerFunction)
        #if playIsActive == True:
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
                #     print x
                #print vod.get_segment(str(x))
                segments = vod.get_segment(str(x))
                print segments
            #text_file.write(segments)
        vod.next()
        
        #else:
        #timer.cancel()
    timerFunction()
    '''

if __name__ == '__main__':
    try:
        main()
    except Exception, err:
        raise
