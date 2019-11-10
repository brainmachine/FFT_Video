import numpy as np

class FrameSplicer:

    def __init__():
        pass

    def process_frames(self, video):
        """ Process video """
        # Trim the video so it is divisible by 4 (for my 4 CPU cores)
        
        trim = len(video)%NUM_CORES # number of frames to trim off the end
        print(len(video))
        print(trim)
        # Multiprocessing frame conversion and saving PNGs
        segments = np.split(video[:-trim], 4, axis=0)
        jobs = []
        for index, segment in enumerate(segments):
            frameNumber = len(video)+len(video)*index # TODO: Review
            p = mp.Process(target=convertVideoToImages, args=(segment, index))
            jobs.append(p)
            p.start()

        # Block the program from continuing until we're done converting all frames
        for job in jobs:
            job.join()

    def composite_video(self):
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