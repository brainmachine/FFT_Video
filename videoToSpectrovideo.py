import os
import multiprocessing as mp
# import numpy as np
# import ffmpeg
from video_to_fft_frames import FrameConverter
# from combine_frames import FrameSplicer

mp.set_start_method('spawn', True)

# Define input_filename, input dir and file extension.

# Windows content
inputDir = "C:\\Users\\Leo\\Documents\\FFT_Video\\input\\fixed_framerate\\"
# inputFilename = "VID_20190724_172154"
inputFilename = "VID_20190724_172154"

# Mac content
# inputDir = '/Users/alpha/Documents/FFT_Image/input/iceland_waves'
# inputFilename = 'VID_20190825_153910'


# extension = 'mp4'
extension = 'm4v'

numCores = 4


if __name__ == '__main__': 

    # Batch processing all files in inputDir

    for root, dirs, files in os.walk(inputDir, topdown=False):
        for name in files:
            # Splice the path components together
            inputPath = os.path.join(inputDir, name)
            fc = FrameConverter(input_path=inputPath, do_pickle=False)
            fc.load_video()
            fc.convert_video_to_images(fc.video) # Convert to FFT and Export frames as pngs
            fc.composite_video()




    # Single video processing version (not batch)
    '''
    # Splice the path components together
    inputPath = os.path.join(inputDir, (inputFilename+'.'+extension))

    # FrameConverter - Loads a video and converts the to 2D FFT PNGs
    fc = FrameConverter(input_path=inputPath, do_pickle=False)

    fc.load_video()

    fc.convert_video_to_images(fc.video) # Convert to FFT and Export frames as pngs

    fc.composite_video()
    '''
    # print("\n \n ------------------------------------- \n \n")
    # print("video.shape (ndarray) --> " + str(fc.video.shape))

    # Trim the video so it is divisible by 4 (for my 4 CPU cores)

    # trim = len(fc.video)%numCores # number of frames to trim off the end
    # print(len(fc.video))
    # print(trim)

    # Multiprocessing frame conversion and saving PNGs
    # 
    # framesPerSegment = len(fc.video)/numCores

    """
    segments = np.split(fc.video[:-trim], numCores, axis=0)

    jobs = []
    for index, segment in enumerate(segments):
        frameNumber = (len(fc.video)/len(segments))*index # TODO: Review
        p = mp.Process(target=fc.convert_video_to_images, args=(segment, index))
        jobs.append(p)
        p.start()

    # Block the program from continuing until we're done converting all frames
    for job in jobs:
        job.join()
    """

    """
    segmentDict = dict()
    for index, segment in enumerate(segments):
        segmentDict[index] = segment

    pool = mp.Pool(processes=numCores)
    pool.map(fc.convert_video_to_images, segmentDict)
    pool.close()
    pool.join()
    """



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