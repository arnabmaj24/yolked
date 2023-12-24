import cv2 as cv
import numpy as np
import functions as fn

def curl(landmarks, mp_pose, counter, image, stage):
    color = (255,255,255)
    shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    angleL = fn.cosine(shoulderL, elbowL, wristL)
    angleR = fn.cosine(shoulderR, elbowR, wristR)

    if abs(angleL - angleR) > 15:
        color = (0,0,255)

    cv.putText(image, str(round(angleL, 0)), tuple(np.multiply(elbowL, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)

    cv.putText(image, str(round(angleR, 0)), tuple(np.multiply(elbowR, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)


    if angleL > 160 and angleR > 160:
        stage = "down"
    if angleL < 45 and angleR < 45 and stage == "down":
        counter += 1
        stage = "up"

    return counter, stage

def shoulderpress(landmarks, mp_pose, counter, image, stage):
    color = (255,255,255)
    shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    angleshoulderR = fn.cosine(elbowR, shoulderR, wristR)
    angleshoulderL = fn.cosine(elbowL, shoulderL, wristL)

    angleelbowL = fn.cosine(shoulderL,elbowL,wristL)
    angleelbowR = fn.cosine(shoulderR,elbowR,wristR)

    if abs(angleelbowR - angleelbowL) > 15 or abs(angleshoulderR - angleshoulderL) > 15:
        color = (0,0,255)

    if abs(elbowR[1]-elbowL[1])*480 > 25 or abs(shoulderL[1]-shoulderR[1])*480 > 25:
        color = (0, 0, 255)

    cv.putText(image, str(round(angleelbowL, 0)), tuple(np.multiply(elbowL, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)
    cv.putText(image, str(round(angleshoulderL, 0)), tuple(np.multiply(shoulderL, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)
    cv.putText(image, str(round(angleelbowR, 0)), tuple(np.multiply(elbowR, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)
    cv.putText(image, str(round(angleshoulderR, 0)), tuple(np.multiply(shoulderR, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)

    if angleshoulderL > 65 and shoulderL[1] < elbowL[1] and angleshoulderR > 65 and shoulderR[1] < elbowR[1]:
        stage = "down"
    if angleshoulderL < 15 and shoulderL[1] > elbowL[1] and stage == "down" and angleshoulderR < 15 and shoulderR[1] > elbowR[1]:
        counter += 1
        stage = "up"
    return counter, stage


def pushup(landmarks, mp_pose, counter, image, stage):
    pass

def squat(landmarks, mp_pose, counter, image, stage):
    color = (255,255,255)
    hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    footL = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
              landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
    kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    footR = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
              landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
    kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

    anglekneeR = fn.cosine(hipR, kneeR, footR)
    anglekneeL = fn.cosine(hipL, kneeL, footL)

    anglehipL = fn.cosine(kneeL, hipL, footL)
    anglehipR = fn.cosine(kneeR, hipR, footR)

    if abs(anglekneeR - anglekneeL) > 12 or abs(anglehipL - anglehipR) > 12:
        color = (0,0,255)

    if abs(kneeR[1]-kneeL[1])*480 > 20 or abs(hipL[1]-hipR[1])*480 > 20:
        color = (0,0,255)

    cv.putText(image, str(round(anglekneeR, 0)), tuple(np.multiply(kneeR, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)
    cv.putText(image, str(round(anglekneeL, 0)), tuple(np.multiply(kneeL, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)
    cv.putText(image, str(round(anglehipL, 0)), tuple(np.multiply(hipL, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)
    cv.putText(image, str(round(anglehipR, 0)), tuple(np.multiply(hipR, [640, 480]).astype(int)),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv.LINE_AA)

    if anglekneeL < 60 and anglekneeR < 60 and hipR[1] > kneeR[1] and hipL[1] > kneeL[1]:
        stage = "down"
    if anglekneeL > 160 and anglekneeR > 160 and anglehipL < 20 and anglehipR < 20 and stage == "down":
        counter +=1
        stage = "up"

    return counter, stage