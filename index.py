import os
from instabot import Bot
from PIL import Image
import schedule
import time
 

# Prepare the image for Instagram
def prepare_image(input_path, output_path, target_size=(1080, 1080)):
    img = Image.open(input_path)
    width, height = img.size
    aspect_ratio = width / height

    # Crop to fit aspect ratio
    if aspect_ratio > 1:  # Landscape
        new_width = height * target_size[0] / target_size[1]
        left = (width - new_width) / 2
        right = left + new_width
        img = img.crop((left, 0, right, height))
    elif aspect_ratio < 1:  # Portrait
        new_height = width * target_size[1] / target_size[0]
        top = (height - new_height) / 2
        bottom = top + new_height
        img = img.crop((0, top, width, bottom))

    # Resize the image
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    img.save(output_path)


# Post an image on Instagram
def post_to_instagram(image_path, caption, username, password):
    """
    Logs into Instagram and posts the provided image with a caption.
    """
    resized_image = "resized_" + image_path

    # Prepare the image
    prepare_image(image_path, resized_image)

    # Clean up any existing .REMOVE_ME file (from Instabot uploads)
    remove_me_file = resized_image + ".REMOVE_ME"
    if os.path.exists(remove_me_file):
        os.remove(remove_me_file)

    # Initialize the bot
    bot = Bot()
    bot.login(username=username, password=password, use_cookie=False)

    # Upload the photo
    success = bot.upload_photo(resized_image, caption=caption)

    # Clean up after posting
    if success and os.path.exists(remove_me_file):
        os.remove(remove_me_file)


# Function to schedule a single post
def schedule_post(image_path, caption, post_time, username, password):
    
    print(f"Scheduled post: {image_path} with caption: '{caption}' at {post_time}")
    schedule.every().day.at(post_time).do(post_to_instagram, image_path, caption, username, password)

# Main function for scheduling multiple posts
def main():
    # Your Instagram credentials


    # List of posts to schedule (image file paths and captions)   
    posts = [
        {"image": "v1_txt2img_0.jpg", "caption": "dd", "time": input("Enter time")},
        #{"image": "img2.jpeg", "caption": "Post 2 - Good morning!", "time": "12:15"},
    ]

    # Schedule all posts
    for post in posts:
        schedule_post(post["image"], post["caption"], post["time"], USERNAME, PASSWORD)

    # Keep the script running to handle scheduled posts
    print("Instagram bot is running and waiting to post...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
