# -*- coding: utf-8 -*-
import fnmatch
import gpxpy
import glob
import datetime
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import random

data_path = '/Users/Jouke/Downloads/*lekker*.gpx'

#   <trkpt lat="51.5033710" lon="5.3644590">
#    <ele>-12.2</ele>
#    <time>2017-11-19T07:27:58Z</time>
#    <extensions>
#     <gpxtpx:TrackPointExtension>
#      <gpxtpx:atemp>21</gpxtpx:atemp>
#      <gpxtpx:hr>94</gpxtpx:hr>
#      <gpxtpx:cad>51</gpxtpx:cad>
#     </gpxtpx:TrackPointExtension>
#    </extensions>
#   </trkpt>

def main():
    #get a list of allgpx files
    all_gpx_files = glob.glob(data_path)
    for gpx_filename1 in all_gpx_files:
        # open 1 file at the time and create a filename for the converted file in folder converted
        gpx_filename2 =  gpx_filename1.replace('Downloads', 'Downloads/converted')
        print (gpx_filename1, "->", gpx_filename2)
        gpx_file1 = open(gpx_filename1, 'r')
        gpx_file2 = open(gpx_filename2, 'w')
    
        # Parse the gpx file
        gpx = gpxpy.parse(gpx_file1)
        lat = []
        lon = []
        alt = []
        time = []
        rondes = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    alt.append(point.elevation)
                    time.append(point.time)
#                    hr.append(point.extensions['TrackPointExtension']['hr'])
#                    p  = point.extensions
#                    for i in p:
#                        print(i, p[i])
#                   print (p['TrackPointExtension']['hr'])
                    rondes.append(0)
        lat_s = savgol_filter(lat, 45, 5) # deze 45 en 3 zijn maar wat gegokt
        rondetijden = []
        print("max min =", max(lat_s), min(lat_s))
        rondes[0] = min(lat_s)
        rondes[lat_s.shape[0]-1] = min(lat_s)
        
        t_vorige = time[0]
        for i in range(1,lat_s.shape[0] - 1):
            if ((lat_s[i] < lat_s[i+1]) and (lat_s[i] < lat_s[i-1]) and (time[i] - t_vorige).total_seconds() > 40):
                rondetijden.append(time[i])
                rondes[i] = max(lat_s)
                t_vorige = time[i]
            else: 
                rondes[i] = min(lat_s)
        # Remove the first track and create a 2nd track and segment        
        gpx.tracks.remove(gpx.tracks[0])
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(gpx_segment)

        for r in range (0,len(rondetijden)-1):
            add_rondje(r+1, gpx_segment,rondetijden[r],rondetijden[r+1])
 
#        for point in segment.points:
#            point.latitude = point.latitude * 1.01
       
        fig = plt.figure()
        fig.set_size_inches(30,10)
        plt.subplot(211)
        plt.plot(lat)
        plt.subplot(212)
        plt.plot(lat_s)
        plt.plot(rondes, ":", lw=0.5, c="black")
        
#                    point.latitude = point.latitude   * 1.000015 * random.uniform(0.999999, 1.000001) - 0.0006      
#                    point.latitude = point.latitude   * random.uniform(0.999999, 1.000001) - 0.00003     
#                    point.longitude = point.longitude * random.uniform(0.999985, 1.000015) + 0.00003     
        gpx.name = "Smink.site"
        gpx.time = gpx.time + datetime.timedelta(seconds=10)
        gpx_file2.write(gpx.to_xml())
        gpx_file2.close()
     
def add_rondje(r, gpx_segment, t1, t2):
    delta = (t2-t1).total_seconds() / 50
#    print ("rondetijd ", r, ":\t", (t2-t1).total_seconds())
    print ( (t2-t1).total_seconds())
    t = t1
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414833, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414761, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414689, 5.472409, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414622, 5.472449, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414565, 5.472518, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414522, 5.47261, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414497, 5.472718, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414492, 5.472833, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414507, 5.472945, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414541, 5.473046, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414592, 5.473127, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414655, 5.473182, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414725, 5.473206, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414797, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414869, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414941, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415013, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415085, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415156, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415228, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.4153, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415372, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415444, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415516, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415588, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.41566, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415732, 5.473208, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415804, 5.473198, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415871, 5.473158, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415928, 5.473089, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415971, 5.472997, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415996, 5.47289, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.416001, 5.472775, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415986, 5.472663, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415952, 5.472562, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415901, 5.472481, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415838, 5.472425, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415768, 5.472401, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415696, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415624, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415552, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.41548, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415408, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415336, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415264, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415192, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.41512, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.415049, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414977, 5.4724, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(51.414905, 5.4724, elevation=12, time=t))

main()

