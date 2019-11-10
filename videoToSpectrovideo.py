import os
import multiprocessing as mp
import numpy as np
import ffmpeg
from video_to_fft_frames import FrameConverter
from combine_frames import FrameSplicer

mp.set_start_method('spawn', True)

# TODO: BUG: Output videos are significantly shorter than the input!
# TODO: Run FFT on RGB channels separately and splice them back together. Should make nice colors that emphasize differnce.
# TODO: Idea: Stack the output PNGs like pieces of transparent paper
# TODO: Use a rolling window and look at a segment of the stack evolve. 
# TODO: This is in 3D so you can rotate around, zoom in, immerse yourself or whatever. 
# TODO: It will be a floating field of fft bins (possibly VR/UE4?)

# Define input_filename, input dir and file extension.
# inputDir = "C:\\Users\\Leo\\Documents\\FFT_Video\\input\\"
inputDir = '/Users/alpha/Documents/FFT_Image'
inputFilename = 'VID_20190825_153910'
extension = 'mp4'

numCores = 2
 

if __name__ == '__main__': 
    # Splice the path components together5
    inputPath = os.path.join(inputDir, (inputFilename+'.'+extension))

    # FrameConverter
    fc = FrameConverter(inputPath)

        
    print("\n \n ------------------------------------- \n \n")
    print("video.shape (ndarray) --> " + str(video.shape))

    # Trim the video so it is divisible by 4 (for my 4 CPU cores)
        
    trim = len(fc.video)%numCores # number of frames to trim off the end
    print(len(fc.video))
    print(trim)

    # Multiprocessing frame conversion and saving PNGs
    segments = np.split(fc.video[:-trim], 4, axis=0)
    jobs = []
    for index, segment in enumerate(segments):
        frameNumber = len(fc.video)+len(fc.video)*index # TODO: Review
        p = mp.Process(target=fc.convert_video_to_images, args=(segment, index))
        jobs.append(p)
        p.start()

    # Block the program from continuing until we're done converting all frames
    for job in jobs:
        job.join()

    # Using NumPy
    # This saves out a good looking PNG at the end

    # img = cv2.imread('input/A-Consensus.tif', cv2.IMREAD_GRAYSCALE)
    # f = np.fft.fft2(img)
    # fshift = np.fft.fftshift(f)
    # # magnitude_spectrum = 20*np.log(np.abs(fshift))
    # magnitude_spectrum = 20*np.log(np.abs(fshift))


    # TODO: Try mapping the fshift from min() to max() making it 0-255, not the abs pipmethod (not backwards compatible)
    #magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.float32)



# TODO: BUG: Output videos are significantly git shorter than the input!
# TODO: Run FFT on RGB channels separately and splice them back together. Should make nice colors that emphasize differnce.
# TODO: Idea: Stack the output PNGs like pieces of transparent paper
# TODO: Use a rolling window and look at a segment of the stack evolve. 
# TODO: This is in 3D so you can rotate around, zoom in, immerse yourself or whatever. 
# TODO: It will be a floating field of fft bins (possibly VR/UE4?)