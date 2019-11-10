"""
Load a video, convert each frame to a 2D Spectrogram and export image
Run this first, then use combine_frames.py to create a video.
"""
import os
import multiprocessing as mp
import cv2
import numpy as np
import ffmpeg
import pickle

mp.set_start_method('spawn', True)

class FrameConverter:
    """ Convert video to 2D DFT frames """

    def __init__(self, input_path, do_pickle=False):
        self.input_path = input_path

        self.do_pickle = do_pickle
        self.pickle_path = None
        self._set_pickle_path()

        self.fileinfo = ffmpeg.probe(input_path)
        self.fps = self._get_fps
        self.width, self.height = self._get_size()
        self.num_chans = 1 # RGB, TODO: Handle monochrome and RGBA videos

        
        self.pix_fmt = self._get_pix_fmt()

        self.video = self._load_video()
        self.export_path = None

        self._create_export_path()


    def _set_pickle_path(self):
        _, self.pickle_path = os.path.split(self.input_path)
        self.pickle_path, _ = os.path.splitext(self.pickle_path)
        self.pickle_path = 'pickled_np_arrays/' + self.pickle_path + '.pickle'

    def _get_size(self):
        """ Find the width and height of the video. """
        # TODO: Automatically pick the right stream
        width = self.fileinfo['streams'][1]['width']
        height = self.fileinfo['streams'][1]['height']

        return [width, height]

    def _get_pix_fmt(self):
        return self.fileinfo['streams'][1]['pix_fmt']

    def _get_fps(self):
        """ Find the FPS of the video, some magic involved...
        Maybe there's a better way to do this. """
        # Split the string and calculate the fps
        a, b = self.fileinfo['streams'][1]['avg_frame_rate'].split('/')
        a, b = float(a), float(b)
        fps = a/b
        return fps

    def _create_export_path(self):
        """ Create an export folder if it doesn't exist already. """
        _, file_name = os.path.split(self.input_path)

        # drop the extension
        file_name, _ = os.path.splitext(file_name)
        self.export_path = 'output/%s'%file_name
        if not os.path.exists(self.export_path):
            os.mkdir(self.export_path)
            print("Created path --> %s"%self.input_path)


    def _load_video(self):
        # Load the video
        # TODO: "deprecated pixel format used, make sure you did set range correctly"
        # https://stackoverflow.com/questions/23067722/swscaler-warning-deprecated-pixel-format-used
        print('Loading video file...')
        if self.do_pickle:
            print('Attempting to load pickled video')

            # video = pickle.load(open( picklePath))
            try:
                pickle_in = open(self.pickle_path, "rb")
                video = pickle.load(pickle_in)
                print('Loaded pickled video numpy array.')
                return video
            except FileNotFoundError:
                print('Pickle file not found')
                pass

            
        
        out, _ = (
            ffmpeg
            .input(self.input_path)
            .output('pipe:', format='rawvideo', pix_fmt='gray')
            # .run(capture_stdout=True, capture_stderr=True)
            .run(capture_stdout=True)

        )
        # Convert to Numpy Array
        np_video = (
            np
            .frombuffer(out, np.uint8)
            .reshape([-1, self.height, self.width, self.num_chans])
        )
        
        if self.do_pickle:
            pickle_out = open(self.pickle_path, "wb")
            pickle.dump(np_video, pickle_out)
            pickle_out.close()


        return np_video

    def convert_video_to_images(self, video, offset=0):
        """ Iterate through all the video frames and export as PNGs.
            We pass in a video segment + the frame offset so we can support multiprocessing.
        """

        for index, frame in enumerate(video):
            print("converting frame to fft")
            frame = np.fft.fft2(frame)
            fshift = np.fft.fftshift(frame)
            # TODO: Deal with divide-by-zero
            magnitude_spectrum = 20*np.log(np.abs(fshift))

            # Normalize magnitude_spectrum
            magnitude_spectrum = magnitude_spectrum/magnitude_spectrum.max()*255.0
            print("max spectrum" + str(magnitude_spectrum.max()))

            # Save the image
            _, filename = os.path.split(self.input_path)
            filename, _ = os.path.splitext(filename)
            outfile_path = 'output/%s/%s_fft_%s.png'% (filename, filename, str(index+offset).zfill(3))
            print(outfile_path)
            cv2.imwrite(outfile_path, magnitude_spectrum)
    
    def composite_video(self):
        """ Loads all PNGs from a path and produces a video. """

        _, input_filename = os.path.split(self.input_path)
        input_filename, extension = os.path.splitext(input_filename)
        # Read the PNGs from here
        images_path = 'output/%s/*.png'%input_filename
        # Save the composite video here
        video_save_path = '%s_fft%s'%(input_filename, extension)
        print("exporting " + video_save_path)
        (
            ffmpeg
            .input(images_path, pattern_type='glob', framerate=60)
            .output(video_save_path, format='mp4')
            .run()
        )
        print("saved " + video_save_path)
