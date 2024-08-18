---
title: Type Byte
emoji: 🐧
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 4.41.0
app_file: app.py
pinned: false
license: creativeml-openrail-m
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Create Dynamic Typed Videos with 'Type Byte'

## How Type Byte Works
Type Byte simplifies the process of turning text(words and phrases) into videos through a user-friendly interface and powerful back-end technologies. Here's a breakdown of how it works:

## 1. Composition Process
At the heart of Type Byte is the composition process. The tool combines SFX (sound effects) with text, allowing you to create a harmonious blend of visual and auditory elements. The process involves several key steps:

**Frame and Text Colors**: You start by selecting the background (frame) color and text color. This ensures that your text stands out and aligns with your brand's aesthetic.

**Text Sequence**: Type Byte animates your text, presenting it line by line or paragraph by paragraph, creating a typing effect that captures attention.

**Sound Effects**: Adding sound effects enhances the viewing experience, making your video more immersive.

## 2. Customization Options
Type Byte offers a range of customization options, ensuring that your video is tailored to your specific needs. You can choose from various:

| **Feature**               | **Description**                                                                      |
|---------------------------|--------------------------------------------------------------------------------------|
| **Text Formats**          | - **Paragraph**: Traditional text block. <br> - **Programming Style**: Code-like format with indents. |
| **Line Spacing**          | Adjust the spacing between lines for improved readability.                           |
| **Fonts**                 | A variety of fonts to match your branding.                                            |
| **Frame and Text Colors** | Multiple color options for both the background and the text.                          |
| **Typing Sound Effects**  | Different SFX to simulate various typing sounds.                                      |

Below is a visual representation of the composition process, illustrating how the different elements come together to create a typed video.



![image/gif](https://cdn-uploads.huggingface.co/production/uploads/65bb837dbfb878f46c77de4c/sAu9qEUhnkl-VcSriCK9Y.gif)



## 3. Prerequisites

Before we dive into the code, make sure you have the following installed:

- **Python 3.x**
- **Gradio**: `pip install gradio`
- **OpenCV**: `pip install opencv-python`
- **Pillow**: `pip install Pillow`
- **MoviePy**: `pip install moviepy`

moviepy.video.fx (vfx)

The module moviepy.video.fx regroups functions meant to be used with videoclip.fx().

For all other modifications, we use clip.fx and clip.fl. clip.fx is meant to make it easy to use already-written transformation functions, while clip.fl makes it easy to write new transformation functions.
  
Additionally, ensure you have a collection of fonts and sound effects ready for use in your videos. (or) to be uploaded externally.

## 4. Setting Up the Environment

To begin, let's create a Python script that sets up the Gradio interface and the necessary functions to generate the typing video.

```python
import gradio as gr
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
```

## 5. Designing the Typing Video Generator

We define a function, `create_typing_video`, that takes several inputs, such as the text to display, formatting options, font, video dimensions, and audio settings. This function will handle the creation of video frames and apply any desired effects, including sound and speed adjustments.

## 6. Customizing the Text Display

```python
def create_typing_video(code_text, format_choice, 
                        line_spacing, 
                        width_choice, 
                        height_choice, 
                        font_name="arial.ttf",
                        font_size=18, frame_rate=10, 
                        sound_choice=None, 
                        custom_audio=None, 
                        background_color="black", 
                        text_color="white", 
                        enhance_quality=False, 
                        video_speed="1.0"):
    font_path = f"font/{font_name}"
    font_size = int(font_size)
    font = ImageFont.truetype(font_path, font_size)
    
    video_frames = []
    image_width, image_height = int(width_choice), int(height_choice)
    max_width = image_width - 40  # Margin of 20 pixels on each side
    current_text = ""
```

## 7. Creating the Video Frames

We create frames one character at a time, wrapping the text as needed and adjusting the font size dynamically to fit the text within the video frame. Each frame is stored as an image and converted to a video using OpenCV.

```python
    while True:
        wrapped_lines = textwrap.wrap(code_text, width=max_width // font.getlength(' '))
        text_height = sum([font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_lines])
        
        if text_height <= image_height - 40:
            break
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)

    for char in code_text:
        current_text += char

        if format_choice == "Paragraph":
            wrapped_lines = textwrap.wrap(current_text, width=max_width // font.getlength(' '))
        else:  
            wrapped_lines = current_text.splitlines()

        image = background.copy()
        draw = ImageDraw.Draw(image)
        
        y_position = 20
        for line in wrapped_lines:
            draw.text((20, y_position), line, font=font, fill=text_color)
            line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
            y_position += line_height * line_spacing

        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_frames.append(frame)
```

## 8. Adding Audio and Enhancements

The function allows you to choose from predefined typing sounds or upload custom audio files to be looped over the video. We also include an option to enhance video quality with resizing and color correction.

```python
    if sound_choice and sound_choice != "No Sound":
        video = mp.VideoFileClip(video_filename)
        audio = mp.AudioFileClip(f"type-sounds/{sound_choice}")
        
        audio = audio.fx(mp.afx.audio_loop, duration=video.duration)
        video = video.set_audio(audio)
        video.write_videofile("typed_code_video_with_sound.mp4", codec="libx264")
        video_filename = "typed_code_video_with_sound.mp4"
    
    if custom_audio:
        video = mp.VideoFileClip(video_filename)
        audio = mp.AudioFileClip(custom_audio)
        
        audio = audio.fx(mp.afx.audio_loop, duration=video.duration)
        video = video.set_audio(audio)
        video.write_videofile("typed_code_video_with_custom_audio.mp4", codec="libx264")
        video_filename = "typed_code_video_with_custom_audio.mp4"
    
    if enhance_quality:
        video = mp.VideoFileClip(video_filename)
        video = video.fx(vfx.resize, height=720) 
        video = video.fx(vfx.colorx, 1.2)  
        video.write_videofile("enhanced_" + video_filename, codec="libx264")
        video_filename = "enhanced_" + video_filename
```

## 9. Building the Gradio Interface

With the core functionality in place, we build the Gradio interface, providing users with a simple way to interact with the app. We allow customization of text format, line spacing, font, video size, speed, and sound.

```python
iface = gr.Interface(
    fn=generate_video,
    inputs=[
        gr.Textbox(label="Enter Content", lines=10, placeholder="Enter the text to be displayed in the video..."),
        format_choice,
        line_spacing,
        width_choice,
        height_choice,
        video_speed,
        font_choice,
        font_size,
        sound_choice,
        custom_audio,
        background_color,
        text_color,
        enhance_quality,
    ],
    outputs=gr.Video(label="Typing Video"),
    title="Type Byte🐧",
    css=css,
    theme="bethecloud/storj_theme",
)
```

## 10. Conclusion

By following the steps outlined in this article, you've created a powerful and customizable typing video generator. This Gradio app allows you to create professional-quality videos with ease, perfect for showcasing your content. The flexibility of the app ensures that it can be tailored to fit various use cases, whether you're coding, writing, or creating dynamic presentations.

- *End of Article Thanks for Reading 🤗!*. 


### **Try It Out!**
| Live Demo | [Type-Byte](https://huggingface.co/spaces/prithivMLmods/TYPE-BYTE) |
| GitHub | [Type-Byte](https://github.com/PRITHIVSAKTHIUR/Type-Bytes) |
| Hugging Face | [prithivMLmods](https://huggingface.co/prithivMLmods) |
