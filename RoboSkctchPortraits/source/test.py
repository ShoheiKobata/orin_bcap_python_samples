import cv2
import time


# check
def check_camera_connection():
    """
    Check the connection between the camera numbers and the computer. 

    """
    true_camera_is = []  

    # check the camera number from 0 to 9
    for camera_number in range(0, 10):
        cap = cv2.VideoCapture(camera_number)
        ret, frame = cap.read()

        if ret is True:
            true_camera_is.append(camera_number)
            print("port number", camera_number, "Find!")

        else:
            print("port number", camera_number,"None")
    print("Connected camera", len(true_camera_is))


# 画像を表示させて実際に確かめるコード
def check_camera_connection_display(save_flag=False):
    """
    Display the image and check the camera number 

    """
    true_camera_is = [] 

    for camera_number in range(0, 5):
        #  for windows -> cv2.CAP_DSHOW
        cap = cv2.VideoCapture(camera_number,cv2.CAP_DSHOW)
        # other
        # cap = cv2.VideoCapture(camera_number)

        ret, frame = cap.read()

        if ret is True:
            start = time.time()

            while True:
                elasped_time = time.time() - start
                ret2, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if elasped_time > 3.0:
                    if save_flag :
                        # save data file
                        save_data_name = f'N_{camera_number}.png'
                        cv2.imwrite(save_data_name, gray)

                    break

                cv2.imshow(f'Camera Number: {camera_number}',gray)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


            cap.release()
            cv2.destroyAllWindows()

            true_camera_is.append(camera_number)
            print("port number", camera_number, "Find!")

        else:
            print("port number", camera_number,"None")

    print(f"Number of connected camera: {len(true_camera_is)}")

if __name__ == '__main__':
    # check_camera_connection()
    check_camera_connection_display(save_flag=False)
