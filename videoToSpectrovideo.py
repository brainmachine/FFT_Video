import cv2
import numpy as np
# from matplotlib import pyplot as plt
import ffmpeg
import os
import multiprocessing as mp
mp.set_start_method('spawn', True)

# TODO: BUG: Output videos are significantly shorter than the input!
# TODO: Run FFT on RGB channels separately and splice them back together. Should make nice colors that emphasize differnce.
# TODO: Idea: Stack the output PNGs like pieces of transparent paper
# TODO: Use a rolling window and look at a segment of the stack evolve. 
# TODO: This is in 3D so you can rotate around, zoom in, immerse yourself or whatever. 
# TODO: It will be a floating field of fft bins (possibly VR/UE4?)

# Define input_filename, extension and input dir. 

input_filename = 'VID_20190825_153910'
extension = 'mp4'
input_dir = "C:\\Users\\Leo\\Documents\\FFT_Video\\input\\" # TODO: Make this constant

NUM_CORES = 4

doProcess = True
doExport = True



def getFps():
    # Split the string and calculate the fps
    a, b = fileinfo['streams'][1]['avg_frame_rate'].split('/')
    a, b = float(a), float(b)
    fps = a/b
    return fps

def createExportPath():
    image_path = 'output/%s'%input_filename
    if not os.path.exists(image_path):
        os.mkdir(image_path)
        print("Created path --> %s"%image_path)

def loadVideo(pix_fmt):
    # Load the video
    # TODO: "deprecated pixel format used, make sure you did set range correctly"
    # https://stackoverflow.com/questions/23067722/swscaler-warning-deprecated-pixel-format-used

    out, _ = (
        ffmpeg
        .input(temp_dir)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True, capture_stderr=True)

    )
    # Convert to Numpy Array
    video = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, height, width, 1])
    )
    return video

def convertVideoToImages(video, offset):
    # Iterate through all the video frames and save out a PNGs
    for i, frame in enumerate(video):
        print("converting frame to fft")
        f = np.fft.fft2(frame)
        fshift = np.fft.fftshift(f)
        # TODO: Deal with divide-by-zero 
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        
        # Normalize magnitude_spectrum
        magnitude_spectrum = magnitude_spectrum/magnitude_spectrum.max()*255.0
        magnitude_spectrum.max()

        # Save the image
        outfile_path = 'output/%s/%s_fft_%s.png'% (input_filename, input_filename, str(i+offset).zfill(3))
        print(outfile_path)
        cv2.imwrite(outfile_path, magnitude_spectrum)

def processFrames(video):
    """ Process video """
    # Trim the video so it is divisible by 4 (for my 4 CPU cores)
    
    trim = len(video)%NUM_CORES # number of frames to trim off the end
    print(len(video))
    print(trim)
    # Multiprocessing frame conversion and saving PNGs
    segments = np.split(video[:-trim], 4, axis=0)
    jobs = []
    for index, segment in enumerate(segments):
        frameNumber = len(video)+len(video)*index # TODO: Reviewy
        p = mp.Process(target=convertVideoToImages, args=(segment, index))
        jobs.append(p)
        p.start()

    # Block the program from continuing until we're done converting all frames
    for job in jobs:
        job.join()

def compositeVideo():
    """ Loads all PNGs from a path and produces a video. """

    # Read the PNGs from here
    images_path = 'output/%s/*.png'%input_filename
    # Save the composite video here
    video_save_path = '%s_fft.%s'%(input_filename, extension)
    print("exporting " + video_save_path)
    (
        ffmpeg
        .input(images_path, pattern_type='glob', framerate=fps)
        .output(video_save_path, format='mp4')
        .run()
    )
    print("saved " + video_save_path)

if __name__ == '__main__': 
    # Splice the path components together5
    input_path = os.path.join(input_dir, (input_filename+'.'+extension))

    # TODO: automatically pick the right stream (if there are multiple streams)
    temp_dir = "C:\\Users\\Leo\\Documents\\FFT_Video\\input\\VID_20190707_214139.mp4"
    fileinfo = ffmpeg.probe(temp_dir)
    # fileinfo = ffmpeg.probe(input_path)
    width = fileinfo['streams'][1]['width']
    height = fileinfo['streams'][1]['height']

    fps = getFps()
    pix_fmt = fileinfo['streams'][1]['pix_fmt']
    video = np.empty(shape=[1, 1])
    if doProcess:
        # Load video file
        loadVideo(pix_fmt)
        # Create output path at output/input_file_name. 
        createExportPath()

        
        video = loadVideo(pix_fmt)

    print("\n \n ------------------------------------- \n \n")
    print("video.shape (ndarray) --> " + str(video.shape))

    if doExport:
        processFrames(video)
        compositeVideo() # Reads the processed frames from disk and exports video


    # Using NumPy
    # This saves out a good looking PNG at the end

    # img = cv2.imread('input/A-Consensus.tif', cv2.IMREAD_GRAYSCALE)
    # f = np.fft.fft2(img)
    # fshift = np.fft.fftshift(f)
    # # magnitude_spectrum = 20*np.log(np.abs(fshift))
    # magnitude_spectrum = 20*np.log(np.abs(fshift))


    # TODO: Try mapping the fshift from min() to max() making it 0-255, not the abs pipmethod (not backwards compatible)
    #magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.float32)

