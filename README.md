# Hidden Sector
## The World as Waveform

## The Group Conversation
#### How the conversation shaped the work
- Symmetry 
- Hidden sector
- Consciousness 

As a group we engaged with a variety of topics, including symmetry, consciousness, magic and the hidden sector. Early on, it became rather evident that we all had a different understanding of words and concepts and finding points of contact between art and physics was one of the more challenging and rewarding parts of the process. 
Early on we discussed ideas of symmetry (and symmetry-breaking) in physics - a concept that is both interesting and relatable to visual thinkers. These conversations had a great impact on my work and the choices I made while producing it. 

- [image] (yin/yang - or other symmetry)
    
From a personal standpoint I am creating this work at a time where my environment is changing quite considerably as I depart to Iceland after spending 8 years in Vancouver. 
When I moved to Vancouver in 2011 I was overwhelmed by how the environment was different than anything I had experienced before. One of the major differences I noticed was that the ocean seemed to have a different 'personality'. The Pacific Ocean seemed much calmer (and perhaps, more mystical) than the untame and unpredictable Atlantic Ocean. Staring at the ocean waves in English Bay I felt like I was speaking with a consciousness I hadn't met before - and I was fascinated. While in Iceland, I didn't give the ocean much thought - I didn't feel like it had a particular personality. It was just the ocean, and the ocean is quite scary. It wasn't until I experienced the Pacific that I realized that this was not the same ocean at all. 

At one point, while meditating by the Pacific Ocean, I had the feeling that the ocean itself was really standing still, it's surface was merely shifting due waves passing through it. This is a feeling I wanted to capture in my work. Seeing ocean waves not as a chaotic shifting surface but as a separate set of waves of different frequencies and amplitudes moduliting a field of stillness. For instance, a wave with a low frequency creates larger waves and higher frequencies create smaller waves. Blending these together creates a large wave with smaller ripples. In a way, I am trying to separate the wave itself from the medium it passes through. The medium of water simultaneously fascilitates the motion of the wave and reveals the shape of the wave. 

#### Consciousness and Magical Thinking
Art and physics may seem like entirely different fields with their own ways of thinking, but on a human level I think the practicioners in both fields are seeking knowledge about how the world works and how we fit into that picture. 

## What I have generated for the project (how many pieces)
I have produced a computer program that converts videos to animated 2D Fourier Tranform plots. I am using this program to convert videos of ocean waves to animated plots that show how the frequency and amplitude of the waves change over time.
The first step in creating the animation was to process a still image and convert it to a 2D Fourier Transform. I was doing this around the same time as scientists involved with the Event Horizon Telescope network produced the first image of a black hole, so I thought it would be an excellent subject matter for an initial test. I wanted to see if the aesthetics - and the *feeling* - of the image was preserved in the process.

<br> </br>
![M87*, Messier 87](https://cdn.eso.org/images/screen/eso1907a.jpg "Credit:
EHT Collaboration")
*M87**, *Messier 87*. Credit:
EHT Collaboration
<br> </br>
![M87*, Messier 87](output/A-Consensus_full_res_fft_lvls_cntrst_curve_low_res.png "2D Fourier Transform of the M87*, Messier 87 image.")
2D Fourier Transform of the M87*, Messier 87 image.


Personally, I was very excited to see the first image of a black hole. It's a massive stellar entity with a gravitational field that light cannot escape. As to the image itself, there is something intruiging about the assymetry of the glowing halo around the object. It feels both unexpected and familiar at the same time. 

Looking at both images, I was happy to discover that the *feeling* I get from looking at both images is the same. This supports my belief that there might be something about the specific composition of frequencies in our visual field that creates an impression in our vision (and ultimately our consciousness) and can make us feel a certain way. The emotional effects of relative compositions of frequencies (and amplitude) are well known in music. We know that certain frequencies, only relative to certain other ones, can create a specific emotional response. Composers and musicians take advantage of this when writing music. A simple example of this is chord composition. A major chord feels happy and uplifting and a minor chord can make you sad. As we generally accept this with sound, it makes sense to me that the same principles apply to light (or any other medium).

Before starting to convert images of ocean waves, I wanted to have a better understanding of how simple geometry is transformed into the frequency domain. For this puspose I used an image of the ceiling at the Waterfront station, downtown Vancouver. 

!["Waterfront station ceiling."](input/waterfront_ceiling_low_res.jpg "Waterfront station ceiling.")
Waterfront station ceiling.
!["Waterfront station ceiling Fourier Transform."](output/waterfron_ceiling_fft_levels_low_res.png)




## Technical requirements and space needed

See TECHNICAL_REQUIREMENTS.md



# Video installation possibilities, notes. 
Possible video formats: 
- Single channel
    - Alternate source-video and FFT-video playback
    - OR blend the videos 
        - blending arc: source_only (1 cycle) -> fade to fft (1 cycle) -> fft_only (1 cycle) -> swap video+fft-source and repeat cycle
    - OR composite videos (source: left, fft: right)

- Dual channel:
    - Videos play synchronously on 2 projectors, side-by-side on the same wall
    - Audio is played on 2 channels, speakers mounted on left and right








