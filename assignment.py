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
    cam_3 = CamData()
    cam_4 = CamData()

    # Load previously saved camera data
    with np.load('calibrations/intrinsic_cam1.npz') as X:
        cam_1.mtx, cam_1.dist = [X[i] for i in ('mtx','dist')]
    with np.load('calibrations/extrinsic_cam1.npz') as X:
        cam_1.pos, cam_1.rvec, cam_1.tvec, cam_1.rotMat = [X[i] for i in ('pos', 'rvec', 'tvec', 'rotMat')]

    with np.load('calibrations/intrinsic_cam2.npz') as X:
        cam_2.mtx, cam_2.dist = [X[i] for i in ('mtx','dist')]
    with np.load('calibrations/extrinsic_cam2.npz') as X:
        cam_2.pos, cam_2.rvec, cam_2.tvec, cam_2.rotMat = [X[i] for i in ('pos', 'rvec', 'tvec', 'rotMat')]

    with np.load('calibrations/intrinsic_cam3.npz') as X:
        cam_3.mtx, cam_3.dist = [X[i] for i in ('mtx','dist')]
    with np.load('calibrations/extrinsic_cam3.npz') as X:
        cam_3.pos, cam_3.rvec, cam_3.tvec, cam_3.rotMat = [X[i] for i in ('pos', 'rvec', 'tvec', 'rotMat')]

    with np.load('calibrations/intrinsic_cam4.npz') as X:
        cam_4.mtx, cam_4.dist = [X[i] for i in ('mtx','dist')]
    with np.load('calibrations/extrinsic_cam4.npz') as X:
        cam_4.pos, cam_4.rvec, cam_4.tvec, cam_4.rotMat = [X[i] for i in ('pos', 'rvec', 'tvec', 'rotMat')]

    intrinsic_mtx_1 = np.array([[488.788, 0, 332.71],
                       [0, 491.286, 229.215],
                       [0, 0, 1]])
    intrinsic_mtx_2 = np.array([[494.5, 0, 336.71],
                       [0, 497, 226],
                       [0, 0, 1]])
    intrinsic_mtx_3 = np.array([[493.77, 0, 322.71],
                       [0, 492, 246],
                       [0, 0, 1]])

    intrinsic_mtx_4 = np.array([[499.77, 0, 341.71],
                       [0, 500, 248.240],
                       [0, 0, 1]])
    print(cam_1.mtx)
    print(cam_2.mtx)
    #print(cam_3.pos)
    print(cam_3.mtx)
    #print(cam_4.pos)
    print(cam_4.mtx)
    # print(cam_2.pos)
    # print(cam_3.pos)
    # print(cam_4.pos)

    rotMatList.append(cam_1.rotMat)
    rotMatList.append(cam_2.rotMat)
    rotMatList.append(cam_3.rotMat)
    rotMatList.append(cam_4.rotMat)

    tvecList.append(cam_1.tvec)
    tvecList.append(cam_2.tvec)
    tvecList.append(cam_3.tvec)
    tvecList.append(cam_4.tvec)

    return cam_1, cam_2, cam_3, cam_4



a, b, c, d = LoadData()

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
    return np.array([[3873.60303505, 4503.18403609, -1841.59617025]])/50
                    # [377.5391725, 5427.07309437, -2010.04293555],
                    # [-5165.18212503, 117.33270127, -2751.96824027],
                    # [-5089.74642322, 6064.01821336, -2774.71874731]])/50


def get_cam_rotation_matrices():
    global a, b
    # Generates dummy camera rotation matrices, looking down 45 degrees towards the center of the room
    # TODO: You need to input the estimated camera rotation matrices (4x4) of the 4 cameras in the world coordinates.
    cam_rotations = []
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
cv2.imshow('img', cframe_c1)
cv2.waitKey()
# cframe_c2 = cv2.imread('subtracted/cam_2/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)
# cframe_c3 = cv2.imread('subtracted/cam_3/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)
# cframe_c4 = cv2.imread('subtracted/cam_4/subtr_frame_0.jpg', cv2.IMREAD_GRAYSCALE)

def is_in_foreground(table_element):
    pos = table_element[0]

    c_1 = table_element[1].astype('int')
    # c_2 = table_element[2].astype('int')
    # c_3 = table_element[3].astype('int')
    # c_4 = table_element[4].astype('int')

    # Check pixel value of each camera coords
    val_c1 = cframe_c1[c_1[1], c_1[0]]
    print(val_c1)
    # val_c2 = cframe_c2[c_2[1], c_2[0]]
    # val_c3 = cframe_c3[c_3[1], c_3[0]]
    # val_c4 = cframe_c4[c_4[1], c_4[0]]
    if val_c1 == 0:# and val_c2 ==0 and val_c3 == 0 and val_c4 == 0:
        return True
    else:
        return False

def construct_table():
    global active_voxels
    global a, b

    table = []
    for x in range(-64, 512, 8):
        for z in range(-64, 512, 8):
            for y in range(0, 128, 8):
                voxel_coords = np.float32([x,z,y])
                #active_voxels.append(voxel_coords)

                imgpts_a, jac = cv2.projectPoints(voxel_coords, a.rvec, a.tvec, a.mtx, a.dist)
                # imgpts_b, jac = cv2.projectPoints(voxel_coords, b.rvec, b.tvec, b.mtx, b.dist)
                # imgpts_c, jac = cv2.projectPoints(voxel_coords, c.rvec, c.tvec, c.mtx, c.dist)
                # imgpts_d, jac = cv2.projectPoints(voxel_coords, d.rvec, d.tvec, d.mtx, d.dist)
                table.append([(x, y, z), imgpts_a.ravel()])#, imgpts_b.ravel(), imgpts_c.ravel(), imgpts_d.ravel()])
    print("Constructed table!")
    return table

table = construct_table()

for elem in table:
    if(is_in_foreground(elem)):
         active_voxels.append(elem[0])
