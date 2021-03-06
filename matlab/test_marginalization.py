# -*- coding: utf-8 -*-
import marginalization as mg
import numpy as np
import matplotlib.pyplot as pp
def marginalize_pose_test():
    """
    Test function for testing the marginalize_pose function.
    """
    # create a temporary hessian
    hessian = np.arange(400).reshape(20, 20)
    num_poses = 4
    pose_size = 3
    num_lm = 8
    lm_size = 1
    pose_id = 1
    lm_ids = np.array([0, 1, 2])
    mg.marginalize_pose(hessian, num_poses, pose_size, num_lm, lm_size,
                        pose_id, lm_ids)

def marginalize_pose_csv_test(pose_size, lm_ids):
    proj_pose_size = 6;
    u = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/u_orig.txt", delimiter=",", autostrip=True)
    w = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/w_orig.txt", delimiter=",", autostrip=True)

    v = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/v_orig.txt", delimiter=",", autostrip=True)
    
    v_marg = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/v.txt", delimiter=",", autostrip=True)
    
    vi_marg = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/vinv.txt", delimiter=",", autostrip=True)
    
    w_marg = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/w.txt", delimiter=",", autostrip=True)
    
    wvwt = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/wvwt.txt", delimiter=",", autostrip=True)    
    
    # since w is always operating on 6 pose elements, we must pad it
    # horizontally, if the pose size is larger than 6.
    if pose_size != proj_pose_size:
        w_padded = np.zeros([u.shape[0], w.shape[1]])
        c = np.array([range(i, i + proj_pose_size)
                     for i in range(0, u.shape[0])
                     if i % pose_size == 0]).flatten()
        w_padded[c , :] = w
    else:
        w_padded = w
    
    #marginalize any zero diagonals
    zero_idx = np.where( np.diag(u) == 0 )[0];
    u[zero_idx, zero_idx] = 1
    
    # construct the hessian
    hessian = np.r_[np.c_[u, w_padded], np.c_[w_padded.T, v]]
    # the total number of poses in the hessian
    num_poses = u.shape[0] / pose_size
    # the pose id of the pose to be marginalized
    pose_id = 0
    # we must now obtain the id of any landmark that was seen in this pos
    if lm_ids.shape[0] == 0:
        lm_ids = w_padded[pose_id * pose_size + 3, :].nonzero()[0]
        
    prior = mg.marginalize_pose(hessian, num_poses, pose_size, w.shape[1], 1 ,
                                pose_id, lm_ids)
    diff = wvwt - prior[0:wvwt.shape[0], 0:wvwt.shape[1]]
    
    
    pass

# run the test
# marginalize_pose_csv_test(9);
lm_ids = np.genfromtxt("/Users/nimski/Code/Build/rslam/Applications/"
        "rslam-desktop/lm_ids.txt", delimiter=",", autostrip=True)
marginalize_pose_csv_test(6, lm_ids.astype(int));