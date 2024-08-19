import gradio as gr
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
import moviepy.editor as mp
import moviepy.video.fx.all as vfx

css = """
#col-container {
    margin: 0 auto;
    max-width: 290px;
}
"""

def create_typing_video(code_text, format_choice, line_spacing, width_choice, height_choice, font_name="arial.ttf", font_size=18, frame_rate=10, sound_choice=None, custom_audio=None, background_color="black", text_color="white", enhance_quality=False, video_speed="1.0"):
    font_path = f"font/{font_name}"
    
    # Convert font_size to integer
    font_size = int(font_size)
    font = ImageFont.truetype(font_path, font_size)
    
    video_frames = []
    
    # Setup initial parameters
    image_width, image_height = int(width_choice), int(height_choice)
    max_width = image_width - 40  # Margin of 20 pixels on each side
    current_text = ""
    
    # Create the background
    background = Image.new("RGB", (image_width, image_height), color=background_color)
    
    # Calculate the maximum width and adjust font size if necessary
    while True:
        wrapped_lines = textwrap.wrap(code_text, width=max_width // font.getlength(' '))
        text_height = sum([font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_lines])
        
        if text_height <= image_height - 40:
            break
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
    
    # Generate frames for the typing effect
    for char in code_text:
        current_text += char

        if format_choice == "Paragraph":
            wrapped_lines = textwrap.wrap(current_text, width=max_width // font.getlength(' '))
        else:  # Programming
            wrapped_lines = current_text.splitlines()

        # Copy the background image for each frame
        image = background.copy()
        draw = ImageDraw.Draw(image)
        
        y_position = 20
        for line in wrapped_lines:
            draw.text((20, y_position), line, font=font, fill=text_color)
            line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
            y_position += line_height * line_spacing

        # Convert to numpy array for OpenCV
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_frames.append(frame)
    
    # Create a video writer
    video_filename = "typed_code_video.mp4"
    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (image_width, image_height))
    
    for frame in video_frames:
        out.write(frame)
    out.release()

    # Adjust video speed
    speed_factor = {
        "1x": 1.0,
        "1.25x": 1.25,
        "1.5x": 1.5,
        "1.75x": 1.75,
        "2x": 2.0
    }.get(video_speed, 1.0)  # Default to 1.0 if video_speed is not found in the dictionary
    
    video = mp.VideoFileClip(video_filename).fx(vfx.speedx, factor=speed_factor)
    video.write_videofile("speed_adjusted_video.mp4", codec="libx264")
    video_filename = "speed_adjusted_video.mp4"

    # Add sound if a sound choice is selected
    if sound_choice and sound_choice != "No Sound":
        video = mp.VideoFileClip(video_filename)
        audio = mp.AudioFileClip(f"type-sounds/{sound_choice}")
        
        # Loop the audio to match the duration of the video
        audio = audio.fx(mp.afx.audio_loop, duration=video.duration)
        video = video.set_audio(audio)
        video.write_videofile("typed_code_video_with_sound.mp4", codec="libx264")
        video_filename = "typed_code_video_with_sound.mp4"
    
    # Add custom audio if provided
    if custom_audio:
        video = mp.VideoFileClip(video_filename)
        audio = mp.AudioFileClip(custom_audio)
        
        # Loop the custom audio to match the duration of the video
        audio = audio.fx(mp.afx.audio_loop, duration=video.duration)
        video = video.set_audio(audio)
        video.write_videofile("typed_code_video_with_custom_audio.mp4", codec="libx264")
        video_filename = "typed_code_video_with_custom_audio.mp4"
    
    # Apply video quality enhancement if enabled
    if enhance_quality:
        video = mp.VideoFileClip(video_filename)
        video = video.fx(vfx.resize, height=720)  # Resize video to enhance quality
        video = video.fx(vfx.colorx, 1.2)  # Increase contrast
        video.write_videofile("enhanced_" + video_filename, codec="libx264")
        video_filename = "enhanced_" + video_filename
    
    return video_filename
    
def generate_video(code_text, format_choice, line_spacing, width_choice, height_choice, font_choice, font_size, sound_choice, custom_audio, background_color, text_color, enhance_quality, video_speed):
    return create_typing_video(code_text, format_choice, line_spacing, width_choice, height_choice, font_name=font_choice, font_size=font_size, sound_choice=sound_choice, custom_audio=custom_audio, background_color=background_color, text_color=text_color, enhance_quality=enhance_quality, video_speed=video_speed)

# Create Gradio interface
format_choice = gr.Dropdown(
    choices=["Paragraph", "Programming"],
    value="Paragraph",
    label="Text Format"
)

line_spacing = gr.Dropdown(
    choices=[1.0, 1.15, 1.5, 2.0, 2.5, 3.0],
    value=1.5,
    label="Line Spacing"
)

font_choice = gr.Dropdown(
    choices=[
        "DejaVuMathTeXGyre.ttf", 
        "FiraCode-Medium.ttf", 
        "InputMono-Light.ttf",
        "JetBrainsMono-Thin.ttf", 
        "ProggyCrossed Regular Mac.ttf", 
        "SourceCodePro-Black.ttf", 
        "arial.ttf", 
        "calibri.ttf", 
        "mukta-malar-extralight.ttf", 
        "noto-sans-arabic-medium.ttf", 
        "times new roman.ttf",
        "ANGSA.ttf",
        "Book-Antiqua.ttf",
        "CONSOLA.TTF",
        "COOPBL.TTF",
        "Rockwell-Bold.ttf",
        "Candara Light.TTF",
        "Carlito-Regular.ttf Carlito-Regular.ttf",
        "Castellar.ttf",
        "Courier New.ttf",
        "LSANS.TTF",
        "Lucida Bright Regular.ttf",
        "TRTempusSansITC.ttf",
        "Verdana.ttf",
        "bell-mt.ttf",
        "eras-itc-light.ttf",
        "fonnts.com-aptos-light.ttf",
        "georgia.ttf",
        "segoeuithis.ttf",
        "youyuan.TTF",
        "TfPonetoneExpanded-7BJZA.ttf",
    ],
    value="SourceCodePro-Black.ttf",
    label="Currently, it is recommended to use the default font."
)

font_size = gr.Dropdown(
    choices=["16", "18", "20", "22", "24"],
    value="18",
    label="Font Size"
)

width_choice = gr.Dropdown(
    choices=["400","800", "1024", "1280", "1920"],
    value="800",
    label="Video Width"
)

height_choice = gr.Dropdown(
    choices=["400", "720", "1080", "1440", "2160"],
    value="400",
    label="Video Height"
)

sound_choice = gr.Dropdown(
    choices=["No Sound",
             "Mediumspeed Typing.mp3", 
             "Speed Typing.mp3",
             "Bass Typing.mp3",
             "Bay Typing.mp3",
             "Crack Typing.mp3",
             "Deep Sence Typing.mp3",
             "Flacking Typing.mp3",
             "Flaw Typing.mp3",
             "Focused Typing.mp3",
             "K55 Typing.mp3",
             "Laptop Typing.mp3",
             "NDC Typing.mp3",
             "RedMECH Typing.mp3",
             "Smooth Typing.mp3",
             "Stop Tpying.mp3",
            ],
    value="No Sound",
    label="Typing Sound"
)
custom_audio = gr.File(
    label="Upload Custom Audio SFX🔊",
    type="filepath"
)

background_color = gr.Dropdown(
    choices=["black", "white", "darkblue", "orange", "green"],
    value="black",
    label="Background Color"
)

text_color = gr.Dropdown(
    choices=["black", "white", "darkblue", "orange", "green"],
    value="white",
    label="Text Color"
)

enhance_quality = gr.Checkbox(
    label="Enhance Video Quality"
)

video_speed = gr.Dropdown(
    choices=["1x", "1.25x", "1.5x", "1.75x", "2x"],
    value="1x",
    label="Video Speed"
)

iface = gr.Interface(
    fn=generate_video,
    inputs=[
        gr.Textbox(label="Enter Content", lines=10, placeholder="Enter the text to be displayed in the video..."),
        format_choice,
        line_spacing,
        width_choice,
        height_choice,
        font_choice,
        font_size,
        sound_choice,
        custom_audio,
        background_color,
        text_color,
        enhance_quality,
        video_speed
    ],
    
    outputs=gr.Video(label="Typing Video"),
    title="Type Bytes🐧",
    css=css,
    theme="bethecloud/storj_theme",
)

if __name__ == "__main__": 
    iface.launch(share=True)
