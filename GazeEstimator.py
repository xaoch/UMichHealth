import cv2
import numpy as np
import math
import os
import json

# Get a list of all the files in the directory
directory = "D:\\Data\\UMichHealth\\HCAJ18\\postures_1\\"
files = os.listdir(directory)

def get_angle(keypoints,frame):
    size=[720,1280]
    nose_x = keypoints[0*3]
    nose_y = keypoints[0*3+1]
    leye_x = keypoints[16*3]
    leye_y = keypoints[16*3+1]
    reye_x = keypoints[15*3]
    reye_y = keypoints[15*3+1]
    lear_x = keypoints[18*3]
    lear_y = keypoints[18*3+1]
    rear_x = keypoints[17*3]
    rear_y = keypoints[17*3+1]
    lmouth_x = keypoints[9*3]
    lmouth_y = keypoints[9*3+1]
    rmouth_x = keypoints[10*3]
    rmouth_y = keypoints[10*3+1]
    img_size = size

    leyePresent=True
    reyePresent=True
    learPresent=True
    rearPresent=True
    if leye_x==0:
        leyePresent=False
    if reye_x==0:
        reyePresent=False
    if lear_x==0:
        learPresent=False
    if rear_x==0:
        rearPresent=False

    # 3D model points.
    image_points=[]
    model_points=[]
    image_points.append((nose_x,nose_y))
    model_points.append((0.0, 0.0, 0.0))
    if leyePresent:
        image_points.append((leye_x, leye_y))
        model_points.append((-225.0, 170.0, -135.0))
    if reyePresent:
        image_points.append((reye_x, reye_y))
        model_points.append((225.0, 170.0, -135.0))
    if learPresent:
        image_points.append((lear_x, lear_y))
        model_points.append((-250, 100, -200))
    if rearPresent:
        image_points.append((rear_x, rear_y))
        model_points.append((250, 100, -200))
    image_points = np.array(image_points)
    model_points = np.array(model_points)
    # Camera internals
    focal_length = img_size[1]
    center = (img_size[1] / 2, img_size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )
    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,\
                                                                  image_points,\
                                                                  camera_matrix,\
                                                                  dist_coeffs,\
                                                                  flags=cv2.SOLVEPNP_SQPNP)

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                     translation_vector, camera_matrix, dist_coeffs)

    for p in image_points:
        cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

    cv2.line(frame, p1, p2, (255, 0, 0), 2)
    # calculate rotation angles
    theta = cv2.norm(rotation_vector)
    # transformed to quaterniond
    w = np.cos(theta / 2)
    x = np.sin(theta / 2) * rotation_vector[0] / theta
    y = np.sin(theta / 2) * rotation_vector[1] / theta
    z = np.sin(theta / 2) * rotation_vector[2] / theta
    # quaterniondToEulerAngle
    ysqr = y * y
    xsqr = x * x
    zsqr = z * z
    # pitch (x-axis rotation)
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (xsqr + ysqr)
    pitch = math.atan2(t0, t1)
    pitch = pitch * 180 / math.pi
    # yaw (y-axis rotation)
    t2 = 2.0 * (w * y - z * x)
    t2 = 1.0 if t2 > 1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    yaw = math.asin(t2)
    yaw = yaw * 180 / math.pi
    # roll (z-axis rotation)
    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (ysqr + zsqr)
    roll = math.atan2(t3, t4)
    roll = roll * 180 / math.pi
    if roll > 90:
        roll = (roll - 180) % 180
    if roll < -90:
        roll = (roll + 180) % 180
    angle_dict = {"pitch": pitch,\
                          "yaw":   yaw,\
                          "roll":  roll}
    return angle_dict

# Read the contents of each file and process it
for file in files:
    with open(os.path.join(directory, file), 'r') as f:
        #HCAJ18_1_000000000000_keypoints
        base_name, file_extension = os.path.splitext(file)
        parts = base_name.split('_')
        frame = int(parts[-2])
        openpose_data = json.load(f)
        if frame==1000:
            break
        persons=openpose_data["people"]
        personNumber=0
        for person in persons:
            personNumber=personNumber+1
            rotation=None
            # try:
            rotation=get_angle(person['pose_keypoints_2d'],frame)
            #except:
            #    rotation=None
            print(frame,personNumber,rotation)
        # Process the data here (e.g. extract keypoints, etc.)

