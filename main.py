import os
import requests
import time
from moviepy.editor import VideoFileClip, clips_array, vfx, afx

'''
8f54df74a2msh3d57fd3abbb3ecap1e26ddjsn64030ce3ffea     a6a96ce2c6msh6d4b38cfe13e2e0p13000ejsnebf04e73a91a    0feb57de3cmsh371a78fd6f179e3p1c9fd9jsn088702af67e5
https://tiktok-video-feature-summary.p.rapidapi.com/    tiktok-video-feature-summary.p.rapidapi.com   
https://tiktok-download-video1.p.rapidapi.com/getVideo    tiktok-download-video1.p.rapidapi.com     
https://tiktok-download5.p.rapidapi.com/getVideo       tiktok-download5.p.rapidapi.com 
'''


# Set up the API information
url = "https://tiktok-download-video1.p.rapidapi.com/getVideo"     
headers = {
    "X-RapidAPI-Key": "0feb57de3cmsh371a78fd6f179e3p1c9fd9jsn088702af67e5",   
    "X-RapidAPI-Host": "tiktok-download-video1.p.rapidapi.com",      
}
    
# Get the current working directory
current_directory = os.getcwd()

# Create the output folder if it doesn't exist
output_folder = os.path.join(current_directory, "do gia dung videos")
os.makedirs(output_folder, exist_ok=True)

# Read video links from links_dgd.txt
links_path = os.path.join(current_directory, "links_dgd.txt")
with open(links_path, "r") as file:
    video_links = file.read().splitlines()

for i, video_link in enumerate(video_links):
    # Get video information
    info_querystring = {"url": video_link, "hd": "1"}
    info_response = requests.get(url, headers=headers, params=info_querystring)
    
    # Check if the request was successful (status code 200)
    if info_response.status_code == 200:
        try:
            content = info_response.json()
            # Check if 'data' key is present in the response
            if 'data' in content:
                link = content['data'].get('play')
                if link:                    # Download the video
                    video_response = requests.get(link)
                    
                    # Check if the video download was successful
                    if video_response.status_code == 200:
                        video_filename = f"video_{i}.mp4"
                        video_path = os.path.join(output_folder, video_filename)
                        
                        with open(video_path, 'wb') as video_file:
                            video_file.write(video_response.content)
                            # Edit the video
                            clip = VideoFileClip(video_path, audio=False)
                            edited_clip = (
                            clip.fx(vfx.speedx, 1.1)
                            .fx(vfx.mirror_x)
                            .fx(afx.audio_fadeout, 2)
                            )

                            # Save the edited video
                            edited_filename = f"do gia dung {i}.mp4"
                            edited_path = os.path.join(output_folder, edited_filename)
                            edited_clip.write_videofile(edited_path, codec="libx264", audio_codec="aac")

                            # Close the clips
                            clip.close()
                            edited_clip.close()

                            # Delete the original video
                        os.remove(video_path)
                        
                        print(f"Video {i} downloaded successfully.")
                    else:
                        print(f"Failed to download video {i}. Status code: {video_response.status_code}")
                else:
                    print("The 'play' key is not present in the response.")
            else:
                print("The 'data' key is not present in the response.")
        except Exception as e:
            print(f"An error occurred: {e}")
            # Continue to the next iteration of the loop
            continue
    else:
        print(f"Failed to fetch video information. Status code: {info_response.status_code}")

'''
# Download, edit, and delete original videos
for i, video_link in enumerate(video_links):
    # Download the video
    querystring = {"url": video_link, "hd": "1"}
    response = requests.get(url, headers=headers, params=querystring)
    content = response.json()
    link = content['data']['play']
    response = requests.get(link)
    video_filename = f"video_{i}.mp4"
    video_path = os.path.join(output_folder, video_filename)

    with open(video_path, "wb") as video_file:
        video_file.write(response.content)

    # Edit the video
    clip = VideoFileClip(video_path, audio=False)
    edited_clip = (
        clip.fx(vfx.speedx, 1.1)
        .fx(vfx.mirror_x)
        .fx(afx.audio_fadeout, 2)
    )

    # Save the edited video
    edited_filename = f"do gia dung {i}.mp4"
    edited_path = os.path.join(output_folder, edited_filename)
    edited_clip.write_videofile(edited_path, codec="libx264", audio_codec="aac")

    # Close the clips
    clip.close()
    edited_clip.close()

    # Delete the original video
    os.remove(video_path)

print("Videos downloaded, edited, and original files deleted successfully.")'''
