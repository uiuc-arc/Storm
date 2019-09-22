import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
import torch.distributions.constraints as constraints
from pyro.infer import SVI
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
from pyro.contrib.autoguide import *
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
nyear=40
nyear=torch.tensor(nyear)
C= np.array([[27, 25, 25, 16, 22, 32, 14, 7, 24, 25, 23, 31, 14, 37, 36, 37, 34, 28, 44, 49, 58, 58, 83, 66, 127, 104, 101, 133, 89, 130, 173, 143, 142, 112, 97, 186, 118, 159, 211, 103, 33, 26, 35, 27, 15, 18, 32, 24, 23, 36, 24, 41, 24, 30, 42, 45, 49, 52, 43, 57, 70, 82, 76, 84, 129, 99, 132, 133, 105, 134, 188, 178, 147, 149, 112, 197, 131, 196, 232, 105, 67, 61, 36, 47, 27, 34, 27, 29, 33, 58, 55, 59, 48, 65, 73, 63, 77, 76, 92, 106], [134, 103, 106, 156, 232, 171, 216, 194, 183, 240, 340, 298, 277, 231, 176, 350, 225, 337, 375, 179, 28, 37, 26, 21, 32, 27, 33, 14, 25, 32, 26, 32, 24, 26, 52, 54, 39, 54, 39, 62, 71, 66, 69, 99, 151, 114, 116, 121, 127, 151, 226, 204, 177, 178, 107, 205, 137, 214, 246, 107, 32, 38, 37, 27, 23, 18, 19, 16, 25, 25, 31, 37, 28, 42, 47, 32, 43, 54, 54, 63, 84, 66, 95, 89, 151, 93, 129, 122, 115, 136, 220, 164, 170, 170, 111, 237, 146, 217, 236, 122], [42, 56, 45, 29, 47, 39, 37, 31, 42, 55, 46, 66, 46, 73, 68, 82, 89, 82, 90, 88, 119, 117, 139, 154, 259, 150, 220, 227, 214, 238, 367, 314, 287, 246, 173, 378, 203, 331, 378, 206, 19, 38, 39, 24, 24, 27, 30, 23, 34, 39, 40, 50, 32, 48, 59, 35, 59, 67, 58, 57, 81, 79, 92, 112, 162, 133, 149, 169, 157, 167, 228, 206, 184, 181, 117, 256, 153, 246, 275, 139, 22, 26, 16, 30, 20, 13, 15, 10, 19, 26, 21, 22, 22, 25, 28, 32, 29, 37, 36, 33], [52, 50, 55, 57, 104, 59, 78, 91, 85, 102, 173, 138, 120, 115, 75, 140, 75, 121, 172, 88, 24, 22, 20, 19, 15, 26, 22, 11, 25, 31, 18, 26, 21, 39, 40, 45, 39, 37, 36, 37, 51, 54, 65, 81, 124, 87, 99, 119, 81, 118, 167, 151, 157, 127, 96, 177, 99, 166, 179, 90, 20, 26, 25, 18, 23, 22, 22, 12, 26, 26, 33, 39, 22, 33, 30, 42, 64, 41, 49, 52, 77, 57, 79, 63, 144, 63, 115, 99, 118, 114, 184, 151, 141, 141, 72, 175, 116, 176, 192, 103], [49, 47, 40, 39, 31, 45, 37, 25, 36, 52, 47, 50, 43, 40, 74, 70, 63, 62, 66, 84, 108, 103, 128, 153, 217, 117, 180, 192, 178, 216, 305, 269, 241, 237, 182, 325, 175, 280, 360, 186, 32, 33, 37, 24, 21, 29, 25, 24, 21, 35, 27, 52, 37, 51, 44, 55, 62, 61, 54, 58, 81, 85, 98, 109, 164, 122, 144, 153, 130, 174, 234, 206, 201, 182, 123, 229, 156, 190, 247, 133, 35, 35, 30, 34, 29, 35, 38, 25, 31, 26, 35, 48, 24, 53, 51, 58, 58, 52, 55, 68], [81, 71, 94, 108, 178, 94, 136, 167, 129, 158, 214, 207, 187, 186, 154, 251, 143, 213, 281, 139, 28, 26, 34, 16, 36, 20, 28, 22, 26, 42, 31, 36, 22, 41, 43, 38, 54, 50, 51, 71, 78, 66, 93, 104, 145, 111, 131, 154, 114, 138, 243, 209, 194, 150, 117, 231, 148, 214, 217, 126, 31, 25, 24, 31, 20, 20, 31, 15, 22, 34, 23, 28, 26, 34, 33, 40, 49, 33, 44, 35, 59, 55, 56, 78, 112, 88, 100, 94, 101, 136, 194, 177, 176, 154, 119, 199, 129, 182, 199, 76], [46, 63, 50, 47, 32, 45, 35, 28, 47, 50, 51, 59, 50, 61, 81, 73, 90, 66, 96, 85, 131, 111, 133, 187, 239, 186, 238, 241, 200, 241, 371, 339, 289, 289, 171, 393, 242, 334, 410, 189, 33, 28, 27, 30, 23, 29, 26, 29, 36, 39, 37, 42, 31, 60, 58, 57, 66, 56, 53, 63, 88, 79, 76, 108, 157, 126, 159, 185, 138, 173, 248, 212, 203, 199, 145, 249, 133, 234, 265, 123, 15, 20, 11, 10, 11, 8, 10, 11, 16, 17, 18, 16, 10, 22, 25, 32, 20, 30, 27, 23], [40, 35, 26, 45, 105, 60, 67, 73, 58, 86, 115, 102, 88, 92, 79, 121, 78, 122, 122, 65, 44, 48, 36, 36, 21, 38, 37, 26, 33, 56, 28, 38, 30, 50, 49, 44, 76, 59, 64, 64, 95, 72, 107, 106, 187, 131, 166, 185, 137, 157, 259, 220, 220, 198, 167, 283, 156, 222, 299, 135, 19, 27, 20, 17, 20, 15, 19, 16, 22, 22, 15, 35, 22, 22, 36, 35, 50, 44, 42, 52, 70, 49, 73, 73, 119, 74, 113, 110, 121, 128, 178, 149, 142, 162, 113, 204, 107, 170, 200, 95], [22, 22, 22, 14, 13, 16, 24, 14, 12, 24, 16, 29, 15, 26, 29, 36, 36, 29, 31, 47, 54, 45, 64, 69, 112, 73, 98, 90, 79, 99, 163, 117, 141, 106, 76, 157, 102, 136, 152, 75, 29, 36, 22, 27, 26, 21, 18, 33, 29, 37, 14, 44, 20, 43, 45, 54, 44, 49, 54, 43, 58, 63, 75, 81, 141, 103, 128, 123, 94, 145, 211, 161, 134, 131, 119, 192, 147, 175, 210, 98, 12, 15, 18, 19, 12, 16, 14, 11, 22, 23, 23, 35, 20, 33, 37, 38, 39, 42, 30, 34], [53, 48, 63, 72, 108, 61, 105, 103, 99, 109, 170, 144, 134, 123, 84, 152, 96, 156, 173, 83, 20, 24, 26, 18, 17, 20, 28, 10, 21, 37, 23, 31, 22, 25, 41, 35, 38, 32, 43, 47, 50, 57, 65, 86, 110, 86, 96, 90, 87, 105, 175, 139, 128, 168, 96, 190, 117, 149, 198, 95, 20, 24, 23, 16, 22, 15, 24, 16, 20, 26, 30, 44, 19, 33, 33, 53, 45, 41, 50, 51, 59, 54, 53, 70, 146, 83, 118, 120, 85, 132, 173, 156, 149, 128, 76, 165, 109, 148, 189, 108], [16, 16, 18, 17, 16, 8, 13, 15, 10, 19, 25, 23, 6, 17, 27, 27, 32, 35, 31, 24, 41, 49, 45, 64, 74, 64, 75, 70, 64, 92, 134, 108, 114, 103, 69, 141, 83, 111, 162, 68, 41, 40, 33, 28, 31, 37, 15, 19, 38, 43, 46, 52, 34, 58, 46, 52, 57, 65, 64, 84, 100, 92, 115, 111, 192, 143, 176, 179, 140, 181, 284, 240, 220, 188, 153, 272, 182, 228, 303, 146, 31, 28, 18, 19, 26, 30, 30, 17, 26, 29, 41, 45, 31, 32, 59, 47, 54, 56, 60, 64], [76, 62, 85, 99, 158, 114, 140, 159, 120, 150, 239, 186, 179, 178, 122, 227, 114, 197, 254, 129, 15, 16, 22, 28, 27, 18, 20, 12, 19, 29, 25, 28, 18, 34, 33, 43, 35, 37, 26, 32, 47, 47, 47, 54, 112, 88, 106, 97, 79, 106, 157, 123, 128, 106, 81, 163, 88, 131, 187, 81, 47, 41, 39, 34, 31, 34, 36, 24, 27, 48, 32, 39, 35, 47, 73, 74, 85, 75, 73, 70, 114, 91, 118, 135, 194, 157, 211, 209, 185, 230, 318, 255, 255, 229, 183, 343, 191, 277, 372, 179], [33, 40, 44, 18, 27, 40, 23, 20, 27, 35, 31, 36, 38, 52, 60, 50, 47, 61, 55, 56, 96, 80, 82, 110, 185, 106, 123, 151, 139, 147, 242, 189, 211, 189, 152, 244, 146, 213, 266, 140, 23, 31, 25, 22, 25, 24, 21, 20, 26, 43, 32, 40, 25, 31, 34, 38, 49, 40, 55, 50, 67, 54, 46, 81, 125, 101, 121, 117, 96, 137, 181, 168, 153, 151, 100, 205, 122, 183, 212, 101, 43, 39, 36, 43, 21, 43, 29, 21, 39, 45, 34, 49, 30, 45, 67, 55, 74, 68, 68, 57], [105, 84, 92, 129, 175, 132, 160, 164, 133, 193, 288, 253, 243, 218, 151, 291, 161, 259, 344, 159, 40, 40, 41, 39, 18, 36, 27, 36, 46, 51, 39, 67, 38, 40, 65, 54, 61, 63, 66, 70, 94, 101, 104, 121, 196, 140, 170, 168, 157, 190, 280, 246, 232, 205, 149, 289, 164, 273, 313, 154, 28, 39, 45, 28, 33, 26, 31, 27, 34, 51, 45, 45, 32, 54, 44, 64, 67, 52, 56, 54, 103, 76, 93, 119, 212, 122, 165, 192, 156, 193, 242, 224, 201, 192, 164, 265, 187, 237, 324, 166], [35, 35, 30, 45, 17, 46, 24, 21, 40, 34, 24, 37, 45, 41, 67, 70, 69, 55, 58, 73, 90, 74, 102, 102, 176, 149, 145, 174, 144, 171, 265, 211, 188, 165, 136, 274, 158, 229, 294, 148, 28, 38, 35, 32, 31, 38, 32, 21, 45, 36, 40, 43, 33, 50, 49, 58, 52, 57, 63, 60, 96, 83, 98, 85, 172, 143, 153, 143, 154, 149, 269, 159, 193, 200, 121, 259, 182, 223, 288, 122, 23, 32, 34, 22, 17, 23, 27, 21, 36, 35, 29, 30, 21, 33, 47, 49, 53, 43, 56, 58], [86, 70, 77, 95, 151, 102, 125, 135, 130, 155, 215, 182, 170, 140, 110, 221, 122, 220, 216, 103, 28, 33, 20, 25, 15, 30, 19, 10, 16, 35, 28, 31, 23, 30, 43, 36, 51, 53, 45, 51, 66, 64, 74, 85, 150, 81, 133, 132, 88, 134, 199, 139, 170, 153, 98, 194, 145, 150, 220, 120, 19, 29, 23, 21, 25, 19, 16, 13, 24, 26, 15, 29, 26, 25, 42, 41, 47, 47, 44, 50, 56, 58, 73, 74, 133, 81, 113, 135, 96, 150, 187, 164, 154, 135, 95, 213, 130, 168, 233, 104], [21, 24, 24, 25, 17, 29, 23, 16, 14, 18, 25, 34, 22, 32, 37, 36, 43, 32, 41, 68, 72, 57, 57, 73, 135, 84, 98, 115, 84, 121, 166, 149, 132, 127, 95, 154, 108, 164, 185, 91, 27, 35, 28, 29, 18, 30, 24, 22, 21, 39, 23, 39, 22, 33, 41, 53, 46, 38, 53, 51, 91, 54, 81, 97, 134, 85, 110, 128, 115, 148, 230, 146, 158, 139, 109, 229, 120, 192, 209, 98, 16, 19, 17, 9, 12, 23, 17, 16, 20, 24, 18, 23, 14, 33, 28, 31, 28, 35, 36, 34], [56, 51, 46, 55, 106, 68, 80, 82, 84, 107, 150, 115, 107, 108, 62, 141, 82, 126, 151, 76, 52, 48, 48, 57, 52, 47, 49, 42, 38, 83, 56, 73, 57, 61, 86, 75, 99, 89, 81, 94, 135, 142, 146, 190, 282, 202, 228, 274, 227, 280, 424, 331, 303, 318, 238, 433, 233, 397, 450, 227, 47, 48, 39, 31, 34, 39, 26, 27, 39, 48, 43, 68, 44, 51, 60, 72, 72, 69, 79, 69, 94, 110, 121, 129, 223, 153, 207, 186, 184, 233, 308, 268, 281, 241, 168, 329, 194, 255, 350, 175], [29, 26, 13, 19, 18, 13, 14, 15, 22, 17, 21, 28, 15, 23, 31, 27, 36, 21, 41, 35, 44, 44, 55, 54, 88, 78, 80, 88, 84, 91, 136, 118, 127, 112, 86, 147, 91, 141, 178, 71, 18, 27, 29, 13, 20, 23, 29, 20, 22, 25, 23, 33, 23, 30, 46, 51, 40, 44, 54, 45, 63, 63, 68, 84, 115, 79, 101, 102, 104, 140, 201, 171, 149, 168, 87, 181, 111, 166, 229, 96, 25, 25, 33, 29, 18, 20, 16, 17, 20, 31, 22, 41, 21, 41, 44, 37, 46, 32, 48, 43], [79, 72, 64, 97, 138, 90, 107, 125, 105, 121, 195, 167, 166, 164, 96, 191, 108, 202, 187, 90, 40, 35, 23, 33, 28, 39, 19, 30, 20, 44, 34, 47, 32, 48, 58, 48, 47, 66, 58, 59, 100, 69, 91, 126, 187, 139, 163, 181, 150, 200, 269, 247, 214, 194, 159, 271, 131, 263, 289, 138, 27, 37, 26, 28, 24, 28, 20, 16, 23, 31, 21, 49, 15, 44, 41, 51, 58, 54, 45, 43, 81, 69, 72, 72, 157, 109, 124, 141, 116, 155, 198, 200, 135, 160, 100, 222, 143, 171, 231, 111], [26, 41, 27, 32, 29, 38, 30, 19, 24, 31, 33, 39, 23, 36, 43, 52, 58, 55, 46, 54, 83, 72, 86, 100, 167, 109, 147, 141, 124, 138, 231, 203, 193, 168, 127, 221, 133, 200, 243, 118, 22, 27, 32, 29, 27, 32, 14, 30, 30, 36, 25, 33, 28, 34, 47, 45, 46, 46, 38, 34, 73, 68, 73, 87, 141, 95, 125, 122, 130, 151, 232, 171, 167, 145, 91, 234, 123, 197, 218, 131, 32, 35, 27, 29, 25, 34, 27, 18, 25, 32, 33, 36, 27, 40, 58, 50, 44, 45, 49, 47], [88, 63, 79, 80, 142, 75, 126, 144, 127, 150, 227, 180, 194, 180, 115, 226, 124, 194, 244, 108, 44, 46, 35, 35, 41, 39, 31, 26, 46, 55, 56, 71, 43, 57, 74, 68, 80, 66, 74, 78, 108, 89, 103, 146, 235, 155, 178, 200, 193, 220, 331, 277, 282, 226, 175, 316, 184, 272, 358, 171, 14, 26, 16, 37, 19, 25, 14, 19, 36, 38, 19, 32, 21, 42, 45, 49, 41, 36, 47, 52, 78, 59, 90, 80, 142, 93, 120, 126, 109, 139, 178, 164, 171, 174, 112, 198, 113, 158, 212, 114], [33, 46, 43, 46, 44, 41, 34, 30, 41, 57, 54, 54, 34, 49, 67, 79, 90, 71, 64, 109, 118, 119, 120, 157, 222, 148, 211, 205, 178, 224, 325, 265, 272, 270, 194, 355, 226, 338, 317, 184, 25, 14, 22, 15, 13, 20, 15, 14, 16, 19, 17, 31, 17, 27, 31, 33, 39, 29, 33, 45, 42, 43, 48, 57, 92, 70, 89, 89, 76, 96, 157, 99, 107, 89, 72, 137, 76, 125, 130, 74, 31, 42, 38, 29, 24, 46, 25, 28, 41, 35, 34, 46, 39, 30, 64, 49, 68, 53, 69, 74], [100, 76, 80, 118, 163, 129, 151, 155, 156, 170, 282, 223, 197, 194, 157, 271, 151, 247, 261, 138, 18, 34, 24, 27, 26, 23, 27, 18, 31, 41, 20, 36, 26, 39, 51, 54, 61, 55, 42, 56, 70, 50, 72, 95, 138, 111, 138, 146, 115, 148, 226, 179, 172, 166, 105, 246, 144, 206, 235, 126, 28, 26, 35, 24, 29, 25, 31, 23, 29, 43, 27, 44, 33, 41, 45, 40, 54, 58, 53, 68, 76, 63, 84, 104, 163, 107, 115, 143, 133, 156, 254, 203, 198, 139, 123, 263, 129, 199, 278, 115], [27, 34, 32, 28, 23, 28, 18, 21, 24, 39, 31, 33, 24, 48, 52, 50, 44, 50, 46, 54, 85, 74, 86, 123, 169, 101, 140, 149, 143, 168, 226, 176, 192, 185, 139, 230, 132, 220, 294, 124, 15, 25, 18, 27, 27, 20, 32, 20, 26, 42, 22, 31, 21, 35, 33, 37, 51, 39, 47, 44, 63, 63, 67, 73, 128, 79, 101, 104, 104, 122, 191, 140, 153, 142, 106, 219, 122, 171, 230, 104, 28, 35, 25, 27, 19, 25, 21, 15, 36, 34, 37, 34, 22, 42, 48, 45, 66, 38, 51, 53], [60, 61, 82, 88, 110, 70, 116, 131, 117, 133, 219, 177, 172, 142, 98, 207, 121, 179, 205, 104, 21, 29, 24, 12, 15, 18, 14, 18, 22, 32, 21, 22, 26, 31, 37, 43, 33, 34, 30, 42, 51, 53, 65, 65, 94, 64, 92, 99, 103, 122, 162, 127, 132, 122, 96, 161, 81, 153, 171, 84, 20, 29, 26, 20, 19, 16, 18, 11, 23, 27, 23, 33, 23, 26, 34, 25, 47, 27, 34, 42, 52, 45, 58, 66, 113, 62, 96, 98, 93, 115, 164, 144, 131, 115, 86, 163, 112, 153, 173, 88], [28, 37, 31, 26, 23, 19, 33, 20, 31, 36, 28, 35, 24, 44, 56, 62, 61, 44, 58, 59, 76, 74, 88, 98, 170, 97, 152, 138, 117, 144, 241, 205, 182, 163, 125, 227, 140, 194, 243, 120, 33, 41, 27, 30, 34, 28, 29, 26, 37, 31, 32, 39, 32, 34, 43, 57, 70, 66, 37, 74, 81, 55, 83, 107, 170, 115, 145, 155, 140, 164, 272, 209, 184, 200, 142, 258, 168, 210, 246, 131, 31, 35, 34, 22, 25, 34, 28, 19, 19, 29, 26, 36, 27, 39, 47, 56, 38, 47, 47, 47], [69, 65, 88, 93, 129, 96, 152, 124, 105, 142, 202, 205, 191, 150, 118, 243, 129, 233, 265, 124, 25, 42, 22, 33, 30, 39, 33, 32, 33, 42, 37, 54, 36, 43, 53, 56, 64, 50, 80, 70, 89, 87, 110, 109, 215, 125, 169, 177, 143, 218, 296, 210, 233, 223, 146, 270, 164, 231, 308, 138, 45, 55, 42, 40, 51, 49, 40, 28, 53, 80, 49, 66, 40, 87, 74, 100, 84, 90, 77, 96, 161, 121, 138, 181, 263, 192, 260, 249, 226, 279, 402, 333, 360, 321, 225, 407, 240, 313, 440, 227], [24, 28, 30, 19, 13, 14, 22, 15, 23, 30, 23, 48, 23, 19, 37, 48, 51, 27, 40, 45, 71, 61, 61, 71, 144, 71, 110, 114, 107, 124, 175, 165, 161, 146, 100, 186, 119, 174, 211, 108, 11, 10, 10, 16, 13, 14, 14, 6, 11, 18, 16, 22, 18, 20, 22, 20, 20, 22, 21, 25, 47, 32, 38, 48, 63, 46, 66, 72, 59, 80, 112, 93, 98, 82, 59, 109, 64, 106, 114, 60, 32, 41, 35, 36, 33, 44, 29, 17, 32, 53, 35, 41, 44, 52, 37, 72, 68, 56, 60, 69], [104, 83, 91, 114, 215, 125, 181, 189, 161, 179, 262, 242, 242, 219, 168, 320, 157, 273, 335, 150, 24, 29, 14, 27, 17, 30, 31, 18, 23, 25, 27, 33, 20, 20, 30, 41, 38, 43, 38, 55, 48, 36, 63, 63, 122, 86, 85, 100, 88, 124, 173, 149, 133, 133, 102, 184, 113, 149, 194, 82, 23, 26, 23, 21, 13, 23, 23, 21, 22, 34, 23, 33, 16, 30, 38, 41, 37, 41, 42, 37, 53, 53, 59, 74, 144, 72, 92, 113, 85, 119, 173, 164, 138, 110, 115, 214, 102, 160, 181, 105], [39, 44, 46, 36, 34, 39, 31, 24, 35, 48, 33, 47, 37, 50, 59, 63, 62, 69, 75, 60, 110, 93, 102, 115, 184, 139, 167, 171, 160, 199, 306, 246, 228, 229, 165, 308, 155, 279, 322, 146, 30, 33, 22, 32, 24, 20, 23, 15, 27, 19, 24, 40, 19, 35, 36, 35, 40, 44, 50, 60, 75, 64, 76, 72, 150, 103, 107, 109, 114, 145, 203, 170, 163, 143, 114, 228, 119, 176, 222, 100, 20, 25, 16, 11, 14, 22, 13, 9, 24, 35, 17, 19, 18, 23, 39, 35, 37, 36, 46, 30], [49, 53, 67, 75, 96, 66, 86, 85, 99, 90, 155, 100, 117, 97, 77, 146, 87, 144, 173, 101, 27, 26, 22, 35, 37, 35, 25, 24, 28, 46, 42, 33, 16, 42, 43, 64, 56, 75, 41, 48, 87, 66, 75, 114, 158, 108, 151, 140, 119, 138, 216, 185, 176, 187, 119, 252, 160, 216, 274, 103, 35, 41, 27, 23, 23, 24, 18, 19, 14, 45, 26, 40, 28, 39, 44, 46, 51, 44, 41, 59, 56, 61, 89, 92, 137, 96, 125, 135, 111, 152, 212, 152, 161, 148, 113, 228, 137, 183, 209, 100], [31, 26, 26, 22, 24, 23, 25, 23, 24, 34, 32, 40, 20, 40, 63, 53, 49, 51, 60, 51, 75, 62, 79, 97, 151, 96, 158, 132, 113, 153, 228, 192, 166, 166, 107, 198, 119, 188, 233, 101, 26, 33, 25, 40, 30, 31, 21, 22, 33, 33, 37, 45, 35, 36, 46, 55, 66, 57, 51, 57, 82, 69, 83, 109, 179, 107, 150, 139, 132, 154, 227, 222, 165, 199, 136, 259, 152, 224, 225, 130, 29, 30, 28, 16, 13, 22, 20, 16, 30, 40, 23, 30, 25, 41, 34, 42, 46, 47, 43, 52], [54, 55, 81, 82, 128, 85, 111, 112, 97, 125, 190, 171, 143, 149, 108, 197, 113, 184, 204, 104, 25, 47, 29, 38, 27, 38, 30, 21, 27, 37, 33, 61, 33, 43, 57, 45, 66, 62, 56, 61, 89, 83, 118, 116, 206, 113, 137, 142, 142, 194, 249, 242, 223, 201, 149, 272, 179, 239, 302, 127, 24, 30, 18, 30, 23, 23, 18, 16, 30, 32, 34, 33, 29, 27, 59, 59, 54, 46, 54, 45, 80, 60, 74, 76, 149, 96, 140, 120, 111, 152, 199, 168, 173, 149, 122, 215, 121, 158, 225, 108], [32, 37, 31, 33, 21, 28, 29, 22, 28, 36, 26, 42, 46, 42, 72, 52, 72, 47, 51, 63, 70, 68, 66, 108, 187, 84, 133, 145, 111, 154, 241, 186, 180, 181, 139, 261, 146, 243, 265, 130, 41, 36, 39, 33, 31, 35, 41, 34, 39, 52, 41, 59, 38, 57, 69, 68, 76, 66, 78, 70, 96, 81, 103, 140, 194, 173, 176, 162, 154, 197, 298, 222, 235, 247, 150, 294, 183, 244, 342, 182, 25, 36, 34, 38, 22, 35, 28, 25, 24, 42, 35, 35, 34, 34, 49, 57, 62, 56, 56, 43], [79, 71, 79, 96, 153, 112, 144, 162, 127, 171, 232, 224, 199, 151, 143, 273, 163, 222, 272, 114, 24, 32, 25, 29, 19, 28, 20, 20, 18, 31, 21, 29, 21, 43, 48, 39, 48, 45, 48, 45, 66, 55, 72, 76, 144, 91, 118, 135, 119, 128, 175, 149, 165, 129, 117, 199, 108, 155, 239, 102, 37, 40, 34, 30, 26, 38, 34, 26, 39, 59, 32, 41, 40, 64, 72, 78, 78, 69, 76, 69, 104, 90, 119, 115, 218, 125, 176, 197, 171, 223, 309, 240, 231, 221, 163, 324, 196, 264, 319, 168], [34, 45, 26, 40, 26, 29, 26, 32, 38, 42, 53, 45, 43, 49, 81, 59, 53, 73, 94, 76, 105, 75, 105, 136, 200, 132, 166, 180, 159, 179, 278, 254, 236, 206, 148, 277, 161, 255, 318, 158, 29, 31, 26, 34, 19, 33, 33, 25, 30, 47, 26, 52, 30, 52, 57, 56, 54, 63, 53, 61, 78, 67, 91, 110, 201, 99, 140, 167, 142, 198, 277, 193, 209, 183, 142, 268, 144, 238, 294, 140, 28, 36, 33, 23, 21, 25, 23, 27, 24, 32, 26, 38, 33, 44, 56, 66, 54, 58, 63, 67], [104, 73, 85, 100, 176, 117, 142, 150, 137, 140, 235, 182, 210, 176, 119, 235, 128, 228, 265, 123, 27, 20, 20, 23, 16, 19, 24, 21, 29, 29, 19, 27, 20, 35, 31, 45, 42, 39, 38, 38, 56, 48, 86, 83, 123, 85, 112, 105, 116, 115, 178, 145, 165, 126, 98, 163, 116, 150, 178, 91, 32, 48, 38, 40, 32, 42, 39, 34, 48, 48, 32, 63, 36, 61, 72, 78, 85, 60, 83, 77, 127, 112, 118, 134, 208, 142, 189, 190, 176, 225, 316, 259, 263, 229, 183, 319, 212, 288, 346, 159], [32, 15, 24, 14, 21, 20, 19, 16, 20, 18, 19, 37, 22, 35, 34, 35, 46, 40, 42, 42, 46, 52, 74, 79, 118, 85, 91, 121, 100, 123, 199, 121, 141, 122, 108, 189, 100, 166, 172, 110, 53, 68, 49, 44, 37, 54, 56, 48, 58, 59, 57, 73, 47, 74, 84, 86, 92, 89, 98, 102, 139, 139, 141, 187, 306, 223, 239, 253, 200, 301, 433, 295, 290, 298, 241, 378, 252, 382, 493, 208, 41, 44, 38, 45, 43, 49, 43, 25, 47, 66, 40, 65, 52, 64, 71, 60, 75, 79, 81, 79], [107, 124, 120, 140, 219, 156, 201, 220, 198, 269, 328, 316, 272, 236, 180, 344, 228, 328, 383, 188, 27, 27, 31, 22, 23, 24, 16, 20, 29, 34, 25, 29, 21, 28, 41, 53, 54, 40, 37, 57, 67, 52, 64, 90, 144, 98, 139, 124, 114, 143, 198, 166, 165, 152, 85, 215, 126, 174, 223, 106, 21, 17, 28, 13, 17, 18, 16, 18, 20, 36, 19, 35, 17, 26, 32, 37, 40, 36, 40, 34, 41, 55, 60, 72, 119, 78, 92, 96, 82, 103, 136, 122, 126, 138, 85, 171, 101, 154, 180, 82]], dtype=np.float32)
C=torch.tensor(C)
nsite=100
nsite=torch.tensor(nsite)
year= np.array([-0.95, -0.9, -0.85, -0.8, -0.75, -0.7, -0.65, -0.6, -0.55, -0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], dtype=np.float32).reshape(40,1)
year=torch.tensor(year)
def model(nyear,C,nsite,year):
    year_squared = torch.zeros([amb(nyear)])
    year_cubed = torch.zeros([amb(nyear)])
    year_squared=year*year
    year_cubed=year*year*year
    sd_year = pyro.sample('sd_year'.format(''), dist.Normal(torch.tensor(1234.0)*torch.ones([amb(1)]),torch.tensor(1234.0)*torch.ones([amb(1)])))
    sd_alpha = pyro.sample('sd_alpha'.format(''), dist.Normal(torch.tensor(1234.0)*torch.ones([amb(1)]),torch.tensor(1234.0)*torch.ones([amb(1)])))
    mu = pyro.sample('mu'.format(''), dist.Normal(torch.tensor(0.0)*torch.ones([amb(1)]),torch.tensor(10.0)*torch.ones([amb(1)])))
    with pyro.iarange('alpha_range_'.format('')):
        alpha = pyro.sample('alpha'.format(''), dist.Normal(mu*torch.ones([amb(nsite)]),sd_alpha*torch.ones([amb(nsite)])))
    with pyro.iarange('beta_range_'.format(''), 3):
        beta = pyro.sample('beta'.format(''), dist.Normal(torch.tensor(0.0)*torch.ones([amb(3)]),torch.tensor(10.0)*torch.ones([amb(3)])))
    with pyro.iarange('eps_range_'.format(''), nyear):
        eps = pyro.sample('eps'.format(''), dist.Normal(torch.tensor(0.0)*torch.ones([amb(nyear)]),sd_year*torch.ones([amb(nyear)])))
    log_lambdax = torch.zeros([amb(nyear),amb( nsite)])
    for i in range(1, nyear+1):
        log_lambdax[i-1]=alpha+beta[1-1]*year[i-1]+beta[2-1]*year_squared[i-1]+beta[3-1]*year_cubed[i-1]+eps[i-1]
    for i in range(1, nyear+1):
        pyro.sample('obs_{0}_100'.format(i), torch.distributions.Poisson(torch.exp(log_lambdax[i-1])), obs=C[i-1])
    
def guide(nyear,C,nsite,year):
    arg_1 = pyro.param('arg_1', torch.ones((amb(1))))
    arg_2 = pyro.param('arg_2', torch.ones((amb(1))), constraint=constraints.positive)
    sd_year = pyro.sample('sd_year'.format(''), dist.Normal(arg_1,arg_2))
    arg_3 = pyro.param('arg_3', torch.ones((amb(1))))
    arg_4 = pyro.param('arg_4', torch.ones((amb(1))), constraint=constraints.positive)
    sd_alpha = pyro.sample('sd_alpha'.format(''), dist.Normal(arg_3,arg_4))
    arg_5 = pyro.param('arg_5', torch.ones((amb(1))), constraint=constraints.positive)
    arg_6 = pyro.param('arg_6', torch.ones((amb(1))), constraint=constraints.positive)
    mu = pyro.sample('mu'.format(''), dist.Gamma(arg_5,arg_6))
    arg_7 = pyro.param('arg_7', torch.ones((amb(nsite))))
    arg_8 = pyro.param('arg_8', torch.ones((amb(nsite))), constraint=constraints.positive)
    with pyro.iarange('alpha_prange'):
        alpha = pyro.sample('alpha'.format(''), dist.Normal(arg_7,arg_8))
    arg_9 = pyro.param('arg_9', torch.ones((amb(3))))
    arg_10 = pyro.param('arg_10', torch.ones((amb(3))), constraint=constraints.positive)
    with pyro.iarange('beta_prange'):
        beta = pyro.sample('beta'.format(''), dist.Normal(arg_9,arg_10))
    arg_11 = pyro.param('arg_11', torch.ones((amb(nyear))), constraint=constraints.positive)
    arg_12 = pyro.param('arg_12', torch.ones((amb(nyear))), constraint=constraints.positive)
    with pyro.iarange('eps_prange'):
        eps = pyro.sample('eps'.format(''), dist.Gamma(arg_11,arg_12))
    for i in range(1, nyear+1):
        pass
    for i in range(1, nyear+1):
        pass

    pass
optim = Adam({'lr': 0.05})
svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')
for i in range(4000):
    loss = svi.step(nyear,C,nsite,year)
    if ((i % 1000) == 0):
        print(loss)
for name in pyro.get_param_store().get_all_param_names():
    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))
print('sd_year_mean', np.array2string(dist.Normal(pyro.param('arg_1'), pyro.param('arg_2')).mean.detach().numpy(), separator=','))
print('eps_mean', np.array2string(dist.Gamma(pyro.param('arg_11'), pyro.param('arg_12')).mean.detach().numpy(), separator=','))
print('mu_mean', np.array2string(dist.Gamma(pyro.param('arg_5'), pyro.param('arg_6')).mean.detach().numpy(), separator=','))
print('beta_mean', np.array2string(dist.Normal(pyro.param('arg_9'), pyro.param('arg_10')).mean.detach().numpy(), separator=','))
print('alpha_mean', np.array2string(dist.Normal(pyro.param('arg_7'), pyro.param('arg_8')).mean.detach().numpy(), separator=','))
print('sd_alpha_mean', np.array2string(dist.Normal(pyro.param('arg_3'), pyro.param('arg_4')).mean.detach().numpy(), separator=','))