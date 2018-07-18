
import numpy as np
import cv2
import copy

def main():
    cap = cv2.VideoCapture('testvid.mp4')
    # pip install opencv-contrib-python
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    first_iteration_indicator = 1
    while(cap.isOpened()):      
        if (first_iteration_indicator == 1):
            ret, frame = cap.read()
            first_frame = copy.deepcopy(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape[:2]
            accum_image = np.zeros((height, width), np.uint8)
            first_iteration_indicator = 0
        else:
            ret, frame = cap.read()  # read a frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fgmask = fgbg.apply(gray) 

            thresh = 2
            maxValue = 2
            ret, th1 = cv2.threshold(fgmask, thresh, maxValue, cv2.THRESH_BINARY)

            accum_image = cv2.add(accum_image, th1)

        color_image = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
        result = cv2.add(color_image, frame)
        cv2.imshow('frame1', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # apply a color map
    # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
    color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)

    # overlay the color mapped image to the first frame
    result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

    # save the final overlay image
    cv2.imwrite('heatmap.jpg', result_overlay)

    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()