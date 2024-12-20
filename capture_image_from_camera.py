# import cv2
# import os
# import datetime
# from api_base import MongoClient,db

# def capture_data(inp_fileName_id,folderName):
#     while True:
#         cam_port = 0
        
# # Open a connection to the camera
#         cam = cv2.VideoCapture(cam_port)

# # Check if the camera opened successfully
#         if cam.isOpened():
#             print(f"Camera opened successfully at index {cam_port}")
#             break
#         else:
#             print(f"Error: Unable to open camera at index {cam_port}")

# # Reading the input using the camera
#     # inp = input('Enter person name: ')
#     inp_fileName_id = str(inp_fileName_id)
#     folderName = str(folderName)
# # Create a folder named  if it doesn't exist
#     folder_path = os.path.join(os.getcwd(),'datafolder',folderName)
#     os.makedirs(folder_path, exist_ok=True)

# # image count
#     image_count = 1

#     while True:
# # Capture a single frame
#         ret, image = cam.read()

# # Check if the frame was captured successfully
#         if not ret:
#             print("Error: Unable to capture frame from the camera")
#             break

# # Display the frame
#         cv2.imshow(inp_fileName_id, image)

# #for Capture image if 'a' or 'A' and q key is pressed for quit
#         key = cv2.waitKey(1)
#         if key & 0xFF == ord('q'):
#             print("Exiting camera")
#             break
#         elif key & 0xFF == ord('a') or key & 0xFF == ord('A'):
# # Save the image in the 'shobhit' folder with a manually entered unique identifier
#             file_path = os.path.join(folder_path, f"{inp_fileName_id}_{image_count}.png")
#             cv2.imwrite(file_path, image)
#             print(f"Image {image_count} taken and saved ")
#             db.image_data.insert_one({
#                 'name_id': inp_fileName_id,
#                 'folder_name': folderName,
#                 'file_path': file_path,
#                 'timestamp': datetime.datetime.now()
#             })
#             image_count += 1

# # Release the camera and close all OpenCV windows
#     camrel=cam.release()
#     if camrel:
#         return camrel
#     cv2.destroyAllWindows()







import cv2
import os
import datetime
from api_base import MongoClient, db

def capture_data(inp_fileName_id, folderName):
    cam_port = 0

    # Open a connection to the camera
    cam = cv2.VideoCapture(cam_port)

    # Check if the camera opened successfully
    if not cam.isOpened():
        print(f"Error: Unable to open camera at index {cam_port}")
        return

    print(f"Camera opened successfully at index {cam_port}")

    try:
        # Reading the input using the camera
        inp_fileName_id = str(inp_fileName_id)
        folderName = str(folderName)

        # Create a folder named if it doesn't exist
        folder_path = os.path.join(os.getcwd(), 'datafolder', folderName)
        os.makedirs(folder_path, exist_ok=True)

        # image count
        image_count = 1

        while True:
            # Capture a single frame
            ret, image = cam.read()

            # Check if the frame was captured successfully
            if not ret:
                print("Error: Unable to capture frame from the camera")
                break

            # Display the frame
            cv2.imshow(inp_fileName_id, image)

            # for Capture image if 'a' or 'A' and q key is pressed for quit
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                print("Exiting camera")
                break
            elif key & 0xFF == ord('a') or key & 0xFF == ord('A'):
                # Save the image in the 'shobhit' folder with a manually entered unique identifier
                file_path = os.path.join(folder_path, f"{inp_fileName_id}_{image_count}.png")
                cv2.imwrite(file_path, image)
                print(f"Image {image_count} taken and saved ")
                db.image_data.insert_one({
                    'name_id': inp_fileName_id,
                    'folder_name': folderName,
                    'file_path': file_path,
                    'timestamp': datetime.datetime.now()
                })
                image_count += 1

        cam.release()
        print("Camera released successfully")

    finally:
        cv2.destroyAllWindows()

# Example usage:
# capture_data("example_id", "example_folder")

    

