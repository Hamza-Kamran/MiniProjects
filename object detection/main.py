import cv2
import cv2 as cv


first_frame = None
vid = cv2.VideoCapture(0)

while True:

    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)


    if first_frame is None:
        first_frame = gray
        continue

    #find abs difference between this gray and first frame
    diff = cv2.absdiff(first_frame, gray)

    #use abs diff and threshold to make it look cleaner
    threshold = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    #find contours to line detected object

    (cnts, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)


    cv2.imshow("Video", gray)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", threshold)
    cv2.imshow("Rect", frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break


vid.release()