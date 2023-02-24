import glm
import random
import numpy as np

block_size = 1.0

def construct_tree(width, height, depth):
    table = []
    for x in range(width):
        for y in range(height):
            for z in range(depth):
                project_1 = (1, 2)
                project_2 = (4, 2)
                project_3 = (6, 4)
                project_4 = (2, 9)
                table.append([(x, y, z), project_1, project_2, project_3, project_4])
    # print(len(table))
    # print(len(table[0]))
    # print(table[0])
    return table


table = construct_tree(10, 10, 10)
active_voxels = []
active_voxels.append([80, 0, 8])
active_voxels.append([25, 0, 60])

for i, elem in enumerate(table):  # For every voxel
    if (i < 10):
        print(table[i])


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
