import m3u8

class HLSVod:
    def __init__(self, hlsManifestUri):
        self.hlsManifestUri = hlsManifestUri
        self.m3u8_obj = m3u8.load(self.hlsManifestUri)
        self.segments = {}

        #print "Is master playlist?"
        #print self.m3u8_obj.is_variant
        #print("\n")

        #print "HLSVOD Object:"
        #print self.m3u8_obj

        #print "Target duration:"
        #print self.m3u8_obj.target_duration
        #print("\n")

        #print "BASE URI:"
        #print self.m3u8_obj.base_uri
        #print("\n")

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

    def get_live_master_manifest(self):
        master_manifest_string = ""
        master_manifest_string += "#EXTM3U" + "\n"
        counter = 0

        for playlist in self.m3u8_obj.playlists:
            master_manifest_string += "#EXT-X-STREAM-INF:" + "AVERAGE-BANDWIDTH=" + str(playlist.stream_info.average_bandwidth) + "," + "BANDWIDTH=" + str(playlist.stream_info.bandwidth) + "," + "CODECS=" + '"' + playlist.stream_info.codecs + '"'
            newFileName = str(playlist.stream_info.bandwidth)
            if playlist.stream_info.resolution != None:
                master_manifest_string += ",RESOLUTION="
                resolution = ""
                for res in playlist.stream_info.resolution:
                    resolution += str(res)
                    master_manifest_string += str(res)
                    if res != playlist.stream_info.resolution[-1]:
                        master_manifest_string += "x"
                        resolution += "x"
                    #newFileName = resolution +'.m3u8'
            else:
                newFileName = "audio"
            #newFileName = str(playlist.stream_info.bandwidth) +str(counter)+'.m3u8'
            master_manifest_string += "\n" + newFileName + ".m3u8" + "\n"
            counter += 1

        #print ("Return manifest as a single string!")
        return master_manifest_string

    def get_live_media_manifest(self, bitrate):
        media_manifest_string = ""
        media_manifest_string += "#EXTM3U" + "\n"
        media_manifest_string += "#EXT-X-VERSION:3" + "\n"
        media_manifest_string += "#EXT-X-TARGETDURATION:4" + "\n"
        media_manifest_string += "#EXT-X-MEDIA-SEQUENCE:0" + "\n"
        media_manifest_string += "#EXT-X-PLAYLIST-TYPE:EVENT" + "\n"

        for segment in self.segments[bitrate]:
            media_manifest_string += "#EXTINF:" + str(segment.duration)  + "\n" + segment.base_uri + segment.uri + "\n"
            
        return media_manifest_string
    
    '''
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
            #print("CODEC TYPE")
            #print(type(playlist.stream_info.codecs))
            #print(playlist.stream_info.codecs)
            #print("RESOLUTION")
            #print(type(playlist.stream_info.resolution))
            #print(playlist.stream_info.resolution)
            x.write("CODECS=" + '"' + playlist.stream_info.codecs + '"')
            if playlist.stream_info.resolution != None:
                x.write(",")
                x.write("RESOLUTION=")
                for res in playlist.stream_info.resolution:
                    x.write(str(res))
                    if res != playlist.stream_info.resolution[-1]:
                        x.write("x")
            x.write("\n")
            #x.write(self.m3u8_obj.base_uri + playlist.uri)
            #x.write("\n")

            #EXT tags
            ext_x_media_sequence = 0
            ext_x_target_duration = 4
            ext_x_version = 3
            ext_x_playlist_type = "EVENT"

            #For each Media playlist, create media playlist files 
            newFileName = 'playlistfile-'+str(counter)+'.m3u8'
            y = open(newFileName,'w')
            pth = self.m3u8_obj.base_uri + playlist.uri
            #x.write(self.m3u8_obj.base_uri)
            x.write(newFileName)
            x.write("\n")
            m3u8_playlist = m3u8.load(pth)
            y.write("#EXTM3U" + "\n")
            y.write("#EXT-X-VERSION:" + str(ext_x_version) + "\n")
            y.write("#EXT-X-TARGETDURATION:" + str(ext_x_target_duration) + "\n")
            y.write("#EXT-X-MEDIA-SEQUENCE:" + str(ext_x_media_sequence) + "\n")
            y.write("#EXT-X-PLAYLIST-TYPE:" + ext_x_playlist_type + "\n")
            for segment in m3u8_playlist.segments:
                #print ("KEY: ")
                #print segment.base_uri
                #print segment.uri
                #print segment.duration
                #print type(segment)
                #print(segment)
                #y.write(pth)
                #segmentString = str(segment)
                y.write("#EXTINF:")
                y.write(str(segment.duration) +",")
                y.write("\n")
                y.write(segment.base_uri + segment.uri)
                #y.write(format(segment))
                y.write("\n")

            if ext_x_playlist_type != "EVENT":
                y.write("#EXT-X-ENDLIST")

            y.close()
            counter+=1
        x.close()
    '''
