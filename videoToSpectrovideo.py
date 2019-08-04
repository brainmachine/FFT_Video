import cv2
import numpy as np
# from matplotlib import pyplot as plt
import ffmpeg
import os
import multiprocessing as mp
mp.set_start_method('spawn', True)

# TODO: Idea: Stack the output PNGs like pieces of transparent paper
# TODO: Use a rolling window and look at a segment of the stack evolve. 
# TODO: This is in 3D so you can rotate around, zoom in, immerse yourself or whatever. 
# TODO: It will be a floating field of fft bins (possibly VR/UE4?)

# Define input_filename, extension and input dir. 
input_filename = 'aegissida'
extension = 'mp4'
input_dir = 'input' # TODO: Make this constant

def convertVideoToImages(video, offset):
    # Iterate through all the video frames and save out a PNGs
    for i, frame in enumerate(video):
        print("converting frame to fft")
        f = np.fft.fft2(frame)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        
        # Normalize magnitude_spectrum
        magnitude_spectrum = magnitude_spectrum/magnitude_spectrum.max()*255.0
        magnitude_spectrum.max()

        # Save the image
        outfile_path = 'output/%s/%s_fft_%s.png'% (input_filename, input_filename, str(i+offset).zfill(3))
        print(outfile_path)
        cv2.imwrite(outfile_path, magnitude_spectrum)



if __name__ == '__main__': 
    # Splice the path components together5
    input_path = os.path.join(input_dir, (input_filename+'.'+extension))

    # TODO: populate these with ffprobe
    # TODO: automatically pick the right stream (if there are multiple streams)
    fileinfo = ffmpeg.probe(input_path)
    width = fileinfo['streams'][1]['width']
    height = fileinfo['streams'][1]['height']

    # duration = float(fileinfo['format']['duration'])
    # num_frames = int(fileinfo['format']['size'])
    # fps = num_frames/duration

    # Split the string and calculate the fps
    a, b = fileinfo['streams'][1]['avg_frame_rate'].split('/')
    a, b = float(a), float(b)
    fps = a/b

    # Create output path at output/input_file_name. 
    # This is where we save all the processed FFT PNGs 
    # before we composite them into a new video. 
    image_path = 'output/%s'%input_filename
    if not os.path.exists(image_path):
        os.mkdir(image_path)
        print("Created path --> %s"%image_path)

    # Load the video
    out, _ = (
        ffmpeg
        .input(input_path)
        .output('pipe:', format='rawvideo', pix_fmt='gray')
        .run(capture_stdout=True)
    )
    # Convert to Numpy Array
    video = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, height, width, 1])
    )

    print("\n \n ------------------------------------- \n \n")
    print("video.shape (ndarray) --> " + str(video.shape))


    # Trim the video so it is divisible by 4 (for my 4 CPU cores)
    NUM_CORES = 4
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

    # Single core version of video conversion
    # convertVideoToImages(video, 0)


    # Composite the frames into a video

    # Read the PNGs from here
    input_path = 'output/%s/*.png'%input_filename

    # Save the composite video here
    output_path = '%s_fft.%s'%(input_filename, extension)
    print("exporting " + output_path)
    (
        ffmpeg
        .input(input_path, pattern_type='glob', framerate=fps)
        .output(output_path)
        .run()
    )
    print("saved " + output_path)
    # Using NumPy
    # This saves out a good looking PNG at the end

    # img = cv2.imread('input/A-Consensus.tif', cv2.IMREAD_GRAYSCALE)
    # f = np.fft.fft2(img)
    # fshift = np.fft.fftshift(f)
    # # magnitude_spectrum = 20*np.log(np.abs(fshift))
    # magnitude_spectrum = 20*np.log(np.abs(fshift))


    # TODO: Try mapping the fshift from min() to max() making it 0-255, not the abs pipmethod (not backwards compatible)
    #magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.float32)

