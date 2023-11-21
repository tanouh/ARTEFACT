import cv2
# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50, 
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100, 
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000
}