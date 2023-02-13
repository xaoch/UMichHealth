import tensorflow as tf
import tensorflow_hub as hub

import cv2
import numpy as np
import math

# Optional if you are using a GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']


def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]

        if (c1 > confidence_threshold) & (c2 > confidence_threshold):
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)


EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

colors= [(255, 0, 0),
         (0, 255, 0),
         (0, 0, 255),
         (255, 0, 255),
         (255, 255, 0),
         (0, 255, 255)]

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0, 255, 0), -1)

def drawBox(frame, box, confidence_threshold, personNumber):
    y, x, c = frame.shape


    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    start_point = (int(box[1]*x),int(box[0]*y))

    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    end_point = (int(box[3]*x),int(box[2]*y))

    # Blue color in BGR
    color = colors[personNumber]

    # Line thickness of 2 px
    thickness = 2
    print(start_point)
    print(end_point)
    cv2.rectangle(frame, start_point,end_point,color,thickness)

def getRotation(image_points,frame,personNumber):
    print("Image Points: ",image_points)
    size = frame.shape
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (-225.0, 170.0, -135.0),  # Left eye left corner
        (225.0, 170.0, -135.0),  # Right eye right corner
        (-250, 100, -200),  # Left ear
        (250,100,-200),     # Rigth ear
    ])

    # Camera internals

    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                  dist_coeffs, flags=cv2.SOLVEPNP_EPNP)

    # Show Image
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 3000.0)]), rotation_vector,
                                                     translation_vector, camera_matrix, dist_coeffs)

    for p in image_points:
        cv2.circle(frame[0], (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

    try:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        vertical_angle = int(math.degrees(math.atan(m)))
    except:
        vertical_angle = 0

    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (50, 50*(personNumber+1))

    # fontScale
    fontScale = 1

    # Blue color in BGR
    color = colors[personNumber]

    # Line thickness of 2 px
    thickness = 2

    # Using cv2.putText() method

    cv2.line(frame, p1, p2, color, 2)

    # Display image
    #cv2.imshow("Output", image)
    #cv2.waitKey(0)


    rvec_matrix = cv2.Rodrigues(rotation_vector)[0]
    proj_matrix = np.hstack((rvec_matrix, translation_vector))
    eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]

    pitch = eulerAngles[0]
    yaw = eulerAngles[1]
    roll = eulerAngles[2]
    #pitch = self.fixAngles(pitch)
    #roll = self.fixAngles(roll)
    angleText="Y:"+"{:.0f}".format(yaw[0])+",P:"+"{:.0f}".format(pitch[0])+",R:"+"{:.0f}".format(roll[0])+",2D:"+str(vertical_angle)
    cv2.putText(frame, angleText, org, font, fontScale, color, thickness, cv2.LINE_AA)

    return (pitch, yaw, roll)

def getGaze(frame,person,confidence_threshold,personNumber):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(person, [y, x, 1]))

    nose_x = shaped[0][1]
    nose_y = shaped[0][0]
    leye_x = shaped[1][1]
    leye_y = shaped[1][0]
    reye_x = shaped[2][1]
    reye_y = shaped[2][0]
    lear_x = shaped[3][1]
    lear_y = shaped[3][0]
    rear_x = shaped[4][1]
    rear_y = shaped[4][0]

    image_points = np.array([
        (nose_x, nose_y),  # Nose tip
        (leye_x, leye_y),  # Left eye left corner
        (reye_x, reye_y),  # Right eye right corner
        (lear_x, lear_y),  # Left ear
        (rear_x, rear_y),  # Rigth ear
    ], dtype="double")

    (pitch, yaw, roll) = getRotation(image_points, frame,personNumber)
    print(pitch,yaw,roll)


def loop_through_people(frame,keypoints, boundingBoxes, edges, confidence_threshold):
    personIndex=-1
    size=frame.shape
    personNumber=-1
    for person in keypoints:
        personIndex=personIndex+1
        confidencePerson=boundingBoxes[personIndex][4]
        if confidencePerson>0.2:
            personNumber=personNumber+1
            print("person: "+str(personIndex))
            getGaze(frame,person,confidence_threshold,personNumber)
            drawBox(frame,boundingBoxes[personIndex],confidence_threshold,personNumber)
            #draw_connections(frame, person, edges, confidence_threshold)
            #draw_keypoints(frame, person, confidence_threshold)


cap = cv2.VideoCapture("D:\\Data\\UMichHealth\\HCAJ18\\HCAJ18_1.mp4")
frameNumber=0
while cap.isOpened():
    ret, frame = cap.read()
    frameNumber=frameNumber+1
    if (frameNumber%15==0):
        print(frameNumber)
        # Resize image
        img = tf.image.resize_with_pad(tf.expand_dims(frame, axis=0), 352, 640)
        input_img = tf.cast(img, dtype=tf.int32)

        # Detection section
        results = movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))
        boundingBoxes = results['output_0'].numpy()[:, :, -5:].reshape((6,5))



        # Render keypoints
        loop_through_people(frame, keypoints_with_scores, boundingBoxes, EDGES, 0.2)

        cv2.imshow('Movenet Multipose', frame)
        cv2.waitKey(0)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()