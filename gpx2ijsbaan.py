# -*- coding: utf-8 -*-
import fnmatch
import gpxpy
import glob
import datetime
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import random
from scipy.fftpack import fft
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
from scipy.signal import correlate
import numpy as np

minimum_lap_time = 40

data_path = '/Users/Jouke/Downloads/schaatsnacht*.gpx'
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
    # get a list of allgpx files
    all_gpx_files = glob.glob(data_path)
    for gpx_filename1 in all_gpx_files:
        # open 1 file at the time and create a filename for the converted file in folder converted
        gpx_filename2 = gpx_filename1.replace('Downloads', 'Downloads/converted')
        gpx_filename3 = gpx_filename1.replace('Downloads', 'Downloads/converted')
        gpx_filename3 = gpx_filename3.replace('gpx', 'txt')
        print(gpx_filename1, "->", gpx_filename2)
        gpx_file1 = open(gpx_filename1, 'r')
        gpx_file2 = open(gpx_filename2, 'w')
        gpx_file3 = open(gpx_filename3, 'w')

        # Parse the gpx file
        gpx = gpxpy.parse(gpx_file1)
        lat = []
        lon = []
        alt = []
        time = []
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
        lat_n, lat_s = smooth_gps_data(lat, time)
        lon_n, lon_s = smooth_gps_data(lon, time)
        alt_n, alt_s = smooth_gps_data(alt, time)

        lat_lap_times = []
        lon_lap_times = []
        alt_lap_times = []

        lat_lap_indicator = [0] * lat_s.shape[
            0]  # Initialize the array with the minimum value to facilitate drawing both arrays in one graph
        lon_lap_indicator = [0] * lon_s.shape[
            0]  # Initialize the array with the minimum value to facilitate drawing both arrays in one graph
        alt_lap_indicator = [0] * alt_s.shape[
            0]  # Initialize the array with the minimum value to facilitate drawing both arrays in one graph

        lat_t_previous = time[0] - datetime.timedelta(seconds=minimum_lap_time)
        lon_t_previous = time[0] - datetime.timedelta(seconds=minimum_lap_time)
        alt_t_previous = time[0] - datetime.timedelta(seconds=minimum_lap_time)

        for i in range(1, lat_s.shape[
                              0] - 1):  # i runs from the 2nd untile the 1 but last element because we compare with the previous and and next point
            # Test whether this is a local minimum
            lat_t_previous = test_on_minimum(i, lat_s, time, lat_t_previous, lat_lap_times, lat_lap_indicator)
            lon_t_previous = test_on_minimum(i, lon_s, time, lon_t_previous, lon_lap_times, lon_lap_indicator)
            alt_t_previous = test_on_minimum(i, alt_s, time, alt_t_previous, alt_lap_times, alt_lap_indicator)

        print("Nr of laps lat: ", len(lat_lap_times))
        print("Nr of laps lon: ", len(lon_lap_times))
        print("Nr of laps alt: ", len(alt_lap_times))

        fig = plt.figure()
        fig.set_size_inches(30, 10)
        plt.subplot(511)
        plt.plot(lat_n[0:1000])
        plt.plot(lat_lap_indicator[0:1000], ":", lw=0.5, c="black")
        plt.subplot(512)
        plt.plot(lat_s[0:1000])
        plt.plot(lat_lap_indicator[0:1000], ":", lw=0.5, c="black")
        plt.subplot(513)
        plt.plot(lon_n[0:1000])
        plt.plot(lon_lap_indicator[0:1000], ":", lw=0.5, c="black")
        plt.subplot(514)
        plt.plot(lon_s[0:1000])
        plt.plot(lon_lap_indicator[0:1000], ":", lw=0.5, c="black")
        plt.subplot(515)
        plt.plot(lat_n)
        plt.plot(lat_lap_indicator, ":", lw=0.5, c="black")

        fft_lat = fft(lat_n)
        fig2 = plt.figure()
        fig2.set_size_inches(30, 10)
        plt.subplot(111)
        plt.plot(abs(fft_lat[0:200]))

        # Remove the first track and create a 2nd track and segment        
        gpx.tracks.remove(gpx.tracks[0])
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(gpx_segment)

        for r in range(len(lat_lap_times) - 1):
            add_rondje(r + 1, gpx_segment, lat_lap_times[r], lat_lap_times[r + 1])

        #        for point in segment.points:
        #            point.latitude = point.latitude * 1.01

        #                    point.latitude = point.latitude   * 1.000015 * random.uniform(0.999999, 1.000001) - 0.0006
        #                    point.latitude = point.latitude   * random.uniform(0.999999, 1.000001) - 0.00003
        #                    point.longitude = point.longitude * random.uniform(0.999985, 1.000015) + 0.00003
        gpx.name = "Smink.site"
        gpx.time = gpx.time + datetime.timedelta(seconds=10)
        gpx_file2.write(gpx.to_xml())
        gpx_file2.close()


def add_rondje(r, gpx_segment, t1, t2):
    print((t2 - t1).total_seconds())
    delta = (t2 - t1).total_seconds() / 50
    t = add_trackpoint(gpx_segment, 51.414833, 5.472400, t1, delta)
    t = add_trackpoint(gpx_segment, 51.414761, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.414689, 5.472409, t, delta)
    t = add_trackpoint(gpx_segment, 51.414622, 5.472449, t, delta)
    t = add_trackpoint(gpx_segment, 51.414565, 5.472518, t, delta)
    t = add_trackpoint(gpx_segment, 51.414522, 5.472610, t, delta)
    t = add_trackpoint(gpx_segment, 51.414497, 5.472718, t, delta)
    t = add_trackpoint(gpx_segment, 51.414492, 5.472833, t, delta)
    t = add_trackpoint(gpx_segment, 51.414507, 5.472945, t, delta)
    t = add_trackpoint(gpx_segment, 51.414541, 5.473046, t, delta)
    t = add_trackpoint(gpx_segment, 51.414592, 5.473127, t, delta)
    t = add_trackpoint(gpx_segment, 51.414655, 5.473182, t, delta)
    t = add_trackpoint(gpx_segment, 51.414725, 5.473206, t, delta)
    t = add_trackpoint(gpx_segment, 51.414797, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.414869, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.414941, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415013, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415085, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415156, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415228, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415300, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415372, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415444, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415516, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415588, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415660, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415732, 5.473208, t, delta)
    t = add_trackpoint(gpx_segment, 51.415804, 5.473198, t, delta)
    t = add_trackpoint(gpx_segment, 51.415871, 5.473158, t, delta)
    t = add_trackpoint(gpx_segment, 51.415928, 5.473089, t, delta)
    t = add_trackpoint(gpx_segment, 51.415971, 5.472997, t, delta)
    t = add_trackpoint(gpx_segment, 51.415996, 5.472890, t, delta)
    t = add_trackpoint(gpx_segment, 51.416001, 5.472775, t, delta)
    t = add_trackpoint(gpx_segment, 51.415986, 5.472663, t, delta)
    t = add_trackpoint(gpx_segment, 51.415952, 5.472562, t, delta)
    t = add_trackpoint(gpx_segment, 51.415901, 5.472481, t, delta)
    t = add_trackpoint(gpx_segment, 51.415838, 5.472425, t, delta)
    t = add_trackpoint(gpx_segment, 51.415768, 5.472401, t, delta)
    t = add_trackpoint(gpx_segment, 51.415696, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415624, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415552, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415480, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415408, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415336, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415264, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415192, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415120, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.415049, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.414977, 5.472400, t, delta)
    t = add_trackpoint(gpx_segment, 51.414905, 5.472400, t, delta)


def add_trackpoint(gpx_segment, lat, lon, t, delta):
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=12, time=t))
    t += datetime.timedelta(seconds=delta)
    return t


def smooth_gps_data(x, t):
    x_a = np.asarray(x)
    x_min = min(x)
    x_delta = max(x) - min(x)
    x_n = (x_a - x_min) / x_delta
    x_s = savgol_filter(x_n, 45, 5)  # deze 45 en 3 zijn maar wat gegokt
    return x_n, x_s


def test_on_minimum(i, x, t, tp, y1, y2):
    delta_t = (t[i] - tp).total_seconds()
    if (x[i] < x[i + 1]) and (x[i] < x[i - 1]) and (delta_t > minimum_lap_time):
        y1.append(t[i])
        y2[i] = 1
        tp = t[i]
    return tp


def cross_correlation_using_fft(x, y):
    f1 = fft(x)
    f2 = fft(np.flipud(y))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)


# shift &lt; 0 means that y starts 'shift' time steps before x # shift &gt; 0 means that y starts 'shift' time steps after x
def compute_shift(x, y):
    assert len(x) == len(y)
    c = cross_correlation_using_fft(x, y)
    assert len(c) == len(x)
    zero_index = int(len(x) / 2) - 1
    shift = zero_index - np.argmax(c)
    return shift


main()
