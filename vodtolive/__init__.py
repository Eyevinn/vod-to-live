import m3u8


class HLSVod:
    def __init__(self, hlsManifestUri):
        self.hlsManifestUri = hlsManifestUri
        self.m3u8_obj = m3u8.load(self.hlsManifestUri)
        self.segments = {}

        print "Is master playlist?"
        print self.m3u8_obj.is_variant
        print("\n")

        #print "HLSVOD Object:"
        #print self.m3u8_obj

        print "Target duration:"
        print self.m3u8_obj.target_duration
        print("\n")

        print "BASE URI:"
        print self.m3u8_obj.base_uri
        print("\n")

        for playlist in self.m3u8_obj.playlists:
            pth = self.m3u8_obj.base_uri + playlist.uri
            print "PLAYLIST URI: "
            print pth
            print("\n")
            print "Stream Info:"
            print playlist.stream_info
            print("\n")
            #print "Media:"
            #print playlist.media
            m3u8_playlist = m3u8.load(pth)
            for segment in m3u8_playlist.segments:
                key = str(playlist.stream_info.bandwidth)
                if not key in self.segments:
                    self.segments[key] = []
                self.segments[key].append(segment)
                #print "KEYS: "
                #print self.segments.keys()
                #print "Length: "
                #print len(self.segments)

        self.index = 0

    def list_playlists(self):
        print self.m3u8_obj.playlists


    def list_bitrates(self):
        res = []
    #for key in self.segments.keys()
    #	res.append(key)
    #return res
    
    def next(self):
        self.index += 1
    #print(self.index)
    
    def get_segment(self, bitrate):
        res = ""

        res += self.m3u8_obj.base_uri + self.segments[bitrate] [self.index].uri    + "\n"
        res += self.m3u8_obj.base_uri + self.segments[bitrate] [self.index+1].uri  + "\n"
            
        return res

    def dump(self):
        print self.segments
    
    def write_to_textfile(self):
        newMasterPlaylistFile = 'masterplaylistfile.m3u8'
        x = open(newMasterPlaylistFile,'w')
        x.write("#EXTM3U")
        x.write("\n")  
        
        counter = 0
        for playlist in self.m3u8_obj.playlists:
            #Create master playlist textfile

            x.write("#EXT-X-STREAM-INF:")
            x.write("AVERAGE-BANDWIDTH=" + str(playlist.stream_info.average_bandwidth) +",") 
            x.write("BANDWIDTH=" + str(playlist.stream_info.bandwidth) +",")
            x.write("CODECS=" + format(playlist.stream_info.codecs) +",") 
            x.write("RESOLUTION=" + format(playlist.stream_info.resolution))
            x.write("\n")
            x.write(self.m3u8_obj.base_uri + playlist.uri)
            x.write("\n")


            #For each Media playlist, create media playlist files 
            newFileName = 'playlistfile-'+str(counter)+'.m3u8'
            outfile = open(newFileName,'w')
            pth = self.m3u8_obj.base_uri + playlist.uri
            m3u8_playlist = m3u8.load(pth)
            outfile.write("#EXTM3U")
            outfile.write("\n")
            for segment in m3u8_playlist.segments:
                #print ("KEY: ")
                #print segment.base_uri
                #print segment.uri
                #print segment.duration
                #print type(segment)
                #print(segment)
                #outfile.write(pth)
                #segmentString = str(segment)
                outfile.write("#EXTINF:")
                outfile.write(str(segment.duration) +",")
                outfile.write("\n")
                outfile.write(segment.base_uri + segment.uri)
                #outfile.write(format(segment))
                outfile.write("\n")
            outfile.write("#EXT-X-ENDLIST")
            outfile.close()
            counter+=1
        x.close()
