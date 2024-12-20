import cv2

def get_image_quality(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to read the image at {image_path}")
        return None

    # Check if the OpenCV library was built with progressive JPEG support
    build_info = cv2.getBuildInformation()
    if "JPEG" in build_info and "PROGRESSIVE" in build_info:
        progressive_support = True
    else:
        progressive_support = False
        print("OpenCV was not built with JPEG support.")

    # Check image resolution
    height, width, _ = img.shape
    if height <= 140:
        resolution_quality = "140p or lower"
    elif height <= 240:
        resolution_quality = "240p"
    elif height <= 360:
        resolution_quality = "360p"
    elif height <= 480:
        resolution_quality = "480p"
    elif height <= 720:
        resolution_quality = "720p"
    elif height <= 1080:
        resolution_quality = "1080p"
    else:
        resolution_quality = "Higher than 1080p"

    return progressive_support, resolution_quality

# Example usage
image_path = 'C:/Users/LENOVO/Desktop/Smart_Attendence_System/datafolder/Sandeep_Chaudhary/sandeepChaudhary_1.png'
progressive_support, resolution_quality = get_image_quality(image_path)

print(f"Progressive JPEG support: {progressive_support}")
print(f"Resolution quality: {resolution_quality}")


