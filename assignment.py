import glm
import random
import numpy as np
import cv2 as cv2
block_size = 1.0

def construct_table(width, height, depth):
    table = []
    for x in range(width):
        for y in range(height):
            for z in range(depth):
                project_1 = (320, 420)
                project_2 = (122, 44)
                project_3 = (12, 7)
                project_4 = (12, 12)
                table.append([(x, y, z), project_1, project_2, project_3, project_4])
    return table


def generate_grid(width, depth):
    # Generates the floor grid locations
    # You don't need to edit this function
    data = []
    for x in range(width):
        for z in range(depth):
            data.append([x*block_size - width/2, -block_size, z*block_size - depth/2])
    return data


def set_voxel_positions(width, height, depth):
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
    return [[-64 * block_size, 64 * block_size, 63 * block_size],
            [63 * block_size, 64 * block_size, 63 * block_size],
            [63 * block_size, 64 * block_size, -64 * block_size],
            [-64 * block_size, 64 * block_size, -64 * block_size]]


def get_cam_rotation_matrices():
    # Generates dummy camera rotation matrices, looking down 45 degrees towards the center of the room
    # TODO: You need to input the estimated camera rotation matrices (4x4) of the 4 cameras in the world coordinates.
    cam_angles = [[0, 45, -45], [0, 135, -45], [0, 225, -45], [0, 315, -45]]
    cam_rotations = [glm.mat4(1), glm.mat4(1), glm.mat4(1), glm.mat4(1)]
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

# Check if in foreground for each of the four views (cameras)
def is_in_foreground(table_element, frame_num):
    pos = table_element[0]
    c_1 = table_element[1]
    c_2 = table_element[2]
    c_3 = table_element[3]
    c_4 = table_element[4]

    print(cframe_c1[c_1])
    print(cframe_c2[c_2])
    print(cframe_c3[c_3])
    print(cframe_c4[c_4])

table = construct_table(10, 10, 10)
is_in_foreground(table[0], 0)


# active_voxels = []
# active_voxels.append([80, 0, 8])
# active_voxels.append([25, 0, 60])
