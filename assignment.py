import glm
import numpy as np
import cv2 as cv2
block_size = 1.0
active_voxels = []
rotMatList = []
tvecList = []

class CamData:
    mtx = None
    dist = None
    rvec = None
    tvec = None
    rotMat = None
    pos = None



def LoadData():
    cam_1 = CamData()
    cam_2 = CamData()
    # Load previously saved camera data
    with np.load('calibrations/intrinsic_cam1.npz') as X:
        cam_1.mtx, cam_1.dist = [X[i] for i in ('mtx','dist')]
    with np.load('calibrations/extrinsic_cam1.npz') as X:
        cam_1.pos, cam_1.rvec, cam_1.tvec, cam_1.rotMat = [X[i] for i in ('pos', 'rvec', 'tvec', 'rotMat')]

    with np.load('calibrations/intrinsic_cam2.npz') as X:
        cam_2.mtx, cam_2.dist = [X[i] for i in ('mtx','dist')]
    with np.load('calibrations/extrinsic_cam2.npz') as X:
        cam_2.pos, cam_2.rvec, cam_2.tvec, cam_2.rotMat = [X[i] for i in ('pos', 'rvec', 'tvec', 'rotMat')]




    rotMatList.append(cam_1.rotMat)
    rotMatList.append(cam_2.rotMat)
    rotMatList.append(cam_2.rotMat)
    rotMatList.append(cam_2.rotMat)

    tvecList.append(cam_1.tvec)
    tvecList.append(cam_2.tvec)
    tvecList.append(cam_2.tvec)
    tvecList.append(cam_2.tvec)
    return cam_1, cam_2



a, b = LoadData()

def generate_grid(width, depth):
    # Generates the floor grid locations
    # You don't need to edit this function
    data = []
    for x in range(width):
        for z in range(depth):
            data.append([x*block_size - width/2, -block_size, z*block_size - depth/2])
    return data


def set_voxel_positions(width, height, depth):
    print("Current active voxels: ", len(active_voxels))
    # Generates random voxel locations
    # TODO: You need to calculate proper voxel arrays instead of random ones.
    data = []
    for elem in active_voxels:
        data.append([elem[0] * block_size - width / 2, elem[1] * block_size, elem[2] * block_size - depth / 2])
    # for x in range(width):
    #     for y in range(height):
    #         for z in range(depth):
    #             if random.randint(0, 1000) < 5:
    #                 data.append([x*block_size - width/2, y*block_size, z*block_size - depth/2])

    return data


def get_cam_positions():
    # Generates dummy camera locations at the 4 corners of the room
    # TODO: You need to input the estimated locations of the 4 cameras in the world coordinates.
    return np.array([[1479.83871125, 3780.60917984, -829.51554058],
                    [302.73434419, 3159.49229733,-590.67064462]])/50


def get_cam_rotation_matrices():
    global a, b
    # Generates dummy camera rotation matrices, looking down 45 degrees towards the center of the room
    # TODO: You need to input the estimated camera rotation matrices (4x4) of the 4 cameras in the world coordinates.
    cam_angles = [[0, 45, -45], [0, 135, -45], [0, 225, -45], [0, 315, -45]]
    cam_rotations = []

    # cam_rotations = [glm.mat4(1), glm.mat4(1), glm.mat4(1), glm.mat4(1)]
    for rotmtx in rotMatList:
        mat = glm.mat4(
            [[rotmtx[0][0], rotmtx[0][1], rotmtx[0][2], 0],
            [rotmtx[1][0], rotmtx[1][1], rotmtx[1][2], 0],
            [rotmtx[2][0], rotmtx[2][1], rotmtx[2][2], 0],
            [0, 0, 0, 1]])
        rot_mat = glm.rotate(mat, glm.radians(90), (0, 1, 1))
        cam_rotations.append(rot_mat)

    cam_angles = tvecList

    for c in range(len(cam_rotations)):
        cam_rotations[c] = glm.rotate(cam_rotations[c], cam_angles[c][0] * np.pi / 180, [1, 0, 0])
        cam_rotations[c] = glm.rotate(cam_rotations[c], cam_angles[c][1] * np.pi / 180, [0, 1, 0])
        cam_rotations[c] = glm.rotate(cam_rotations[c], cam_angles[c][2] * np.pi / 180, [0, 0, 1])
    return cam_rotations


# Load the static first frame of each bg-subtracted video
cframe_c1 = cv2.imread('subtracted/cam_1/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)
cframe_c2 = cv2.imread('subtracted/cam_2/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)
cframe_c3 = cv2.imread('subtracted/cam_3/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)
cframe_c4 = cv2.imread('subtracted/cam_4/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)

def is_in_foreground(table_element, frame_num):
    #print(table_element)
    pos = table_element[0]
    c_1 = table_element[1].astype('int')
    c_2 = table_element[2].astype('int')

    # Check pixel value of each camera coords
    val_c1 = cframe_c1[c_1[1], c_1[0]]
    val_c2 =cframe_c1[c_2[1], c_2[0]]
    if val_c2 != 0 and val_c1 != 0:
        return True
    else:
        return False

def construct_table():
    global active_voxels
    global a, b

    table = []
    for x in range(-1000, 1000, 10):
        for y in range(0, 1000, 10):
            for z in range(-1000, 1000, 10):
                voxel_coords = np.float32([x,y,z])
                imgpts_a, jac = cv2.projectPoints(voxel_coords, a.rvec, a.tvec, a.mtx, a.dist)
                imgpts_b, jac = cv2.projectPoints(voxel_coords, b.rvec, b.tvec, b.mtx, b.dist)
                table.append([(x, y, z), imgpts_a.ravel(), imgpts_b.ravel()])

    print("Constructed table!")
    return table

table = construct_table()

for elem in table:
    if(is_in_foreground(elem, 0)):
        active_voxels.append(elem[0])
