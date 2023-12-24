import cv2 as cv
import mediapipe as mp
import workouts as wk
from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.python.solutions.drawing_utils import DrawingSpec
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles


excluded_landmarks = [
    PoseLandmark.LEFT_EYE,
    PoseLandmark.RIGHT_EYE,
    PoseLandmark.LEFT_EYE_INNER,
    PoseLandmark.RIGHT_EYE_INNER,
    PoseLandmark.LEFT_EAR,
    PoseLandmark.RIGHT_EAR,
    PoseLandmark.LEFT_EYE_OUTER,
    PoseLandmark.RIGHT_EYE_OUTER,
    PoseLandmark.NOSE,
    PoseLandmark.MOUTH_LEFT,
    PoseLandmark.MOUTH_RIGHT ]

custom_style = mp_drawing_styles.get_default_pose_landmarks_style()
custom_connections = list(mp_pose.POSE_CONNECTIONS)
for landmark in excluded_landmarks:
    # we change the way the excluded landmarks are drawn
    custom_style[landmark] = DrawingSpec(color=(255,255,0), thickness=None)
    # we remove all connections which contain these landmarks
    custom_connections = [connection_tuple for connection_tuple in custom_connections
                            if landmark.value not in connection_tuple]

counter = 0
stage = "up"
workout = 0
cap = cv.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image.flags.writeable = False

        # results = pose.process(image)

        results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))


        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        try:

            landmarks = results.pose_landmarks.landmark
            if workout == 1:
                counter, stage = wk.curl(landmarks,mp_pose,counter, image, stage)
            elif workout == 2:
                counter, stage = wk.shoulderpress(landmarks,mp_pose,counter, image, stage)
            elif workout == 3:
                counter, stage = wk.squat(landmarks, mp_pose, counter, image, stage)

        except:
            pass


        cv.rectangle(image, (0,0), (100,50), (255,255,255), -1)
        cv.putText(image, "REPS:", (20,20),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv.LINE_AA)
        cv.putText(image, str(counter), (20, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv.LINE_AA)

        cv.rectangle(image, (440, 0), (640, 70), (255, 255, 255), -1)
        curlcol = shoulderpresscol = squatcol = (0,0,0)
        if workout == 1:
            curlcol = (0,255,0)
        elif workout == 2:
            shoulderpresscol = (0,255,0)
        elif workout == 3:
            squatcol = (0,255,0)

        cv.putText(image, "1. Barbell Curl", (460, 20),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, curlcol, 2, cv.LINE_AA)
        cv.putText(image, "2. Shoulder Press", (460, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, shoulderpresscol, 2, cv.LINE_AA)
        cv.putText(image, "3. Squat", (460, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, squatcol, 2, cv.LINE_AA)


        mp_drawing.draw_landmarks(image, results.pose_landmarks, connections = custom_connections,
            landmark_drawing_spec=custom_style
                                    # mp_drawing.DrawingSpec(color=(245,118,66), thickness=2, circle_radius=4),
                                    # mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv.imshow('Mediapipe Feed', image)
        k = cv.waitKey(10) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('r'):
            counter = 0
        elif k == ord('0'):
            workout = 0
            counter = 0
        elif k == ord('1'):
            workout = 1
            counter = 0
        elif k == ord('2'):
            workout = 2
            counter = 0
        elif k == ord('3'):
            workout = 3
            counter = 0

cap.release()
cv.destroyAllWindows()

