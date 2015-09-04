# -*- coding: utf-8 -*-
"""
test_childreader.py: unit tester for child_reader.py

Created on Fri Aug 28 16:22:30 2015

@author: gtucker
"""

from child_reader import ChildRun
import numpy as np
from numpy.testing import assert_array_equal


def test_child_reader():
    """Tests creating a ChildReader object and reading data"""
    
    # Instantiate a child run
    cr = ChildRun('tests/testchildrun')
    
    # Read the first time step
    cr.read_next_timeslice()

    # Test data from .nodes file
    assert cr.current_time==0.0, 'time error'
    assert cr.number_of_nodes==9, 'num nodes should be 9'
    assert cr.number_of_edges==34, 'num edges should be 34'
    assert cr.number_of_triangles==9, 'num tri should be 9'

    # Test data from .nodes file
    assert_array_equal(np.round(cr.x, decimals=1), \
                       np.array([480.8, 0.0, 0.0, 0.0, 500.0, 1000.0, 1000.0, \
                       1000.0, 500.0]))
    assert_array_equal(np.round(cr.y, decimals=1), \
                       np.array([523.5, 0.0, 500.0, 1000.0, 1000.0, 1000.0, 0.0, \
                       500.0, 0.0]))
    assert_array_equal(cr.edg_at_node, np.array([0, 12, 1, 3, 5, 7, 28, 9, 11], \
                       dtype=int))
    assert_array_equal(cr.bnd, np.array([0, 1, 1, 1, 1, 1, 1, 1, 2], dtype=int))
    
    # Test data from .area file
    assert_array_equal(np.round(cr.drainage_area, decimals=1), \
                       np.array([249753.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                       
    # Test data from .net file
    assert_array_equal(cr.drains_to, np.array([8, -1, -1, -1, -1, -1, -1, -1, -1]))
                       
     # Test data from .q (discharge) file
    assert_array_equal(np.round(cr.q, decimals=1), np.zeros(9))
                       
     # Test data from .slp (slope) file
    assert_array_equal(np.round(cr.slope, decimals=3), np.zeros(9))
                       
     # Test data from .tau (shear stress) file
    assert_array_equal(np.round(cr.tau, decimals=1), np.zeros(9))
                       
    # Test data from .varea (Voronoi cell area) file
    assert_array_equal(np.round(cr.voronoi_area, decimals=1), \
                       np.array([249753.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                       
     # Test data from .z (elevation) file
    assert_array_equal(np.round(cr.z, decimals=1), np.zeros(9))
                       
    # Test data from .edges file
    assert_array_equal(cr.edge_tail, np.array([0, 2, 0, 3, 0, 4, 0, 5, 0, 7, \
                                               0, 8, 1, 2, 1, 8, 2, 3, 2, 8, \
                                               3, 4, 3, 5, 4, 5, 5, 7, 6, 7, \
                                               6, 8, 7, 8], dtype=int))
    assert_array_equal(cr.edge_head, np.array([2, 0, 3, 0, 4, 0, 5, 0, 7, 0, \
                                               8, 0, 2, 1, 8, 1, 3, 2, 8, 2, \
                                               4, 3, 5, 3, 5, 4, 7, 5, 7, 6, \
                                               8, 6, 8, 7], dtype=int))
    assert_array_equal(cr.ccw_edge, np.array([10, 16,  0, 20,  2, 24,  4, 26,  6, 32, \
                                               8, 19, 14, 18, 12, 31, 13,  3,  1, 15, \
                                              22,  5, 17, 25, 21,  7, 23,  9, 30, 27, \
                                              28, 33, 29, 11], dtype=int))
                                              
    # Test data from .tri file
    assert_array_equal(cr.tri_vertex, np.array([[0, 2, 8],
                                                [0, 3, 2],
                                                [0, 4, 3],
                                                [0, 5, 4],
                                                [0, 7, 5],
                                                [0, 8, 7],
                                                [1, 8, 2],
                                                [3, 4, 5],
                                                [6, 7, 8]], dtype=int))
                                             
    # Test data from .tri file
    assert_array_equal(cr.tri_edge, np.array([[ 6,  5,  1],
                                              [-1,  0,  2],
                                              [ 7,  1,  3],
                                              [ 7,  2,  4],
                                              [-1,  3,  5],
                                              [ 8,  4,  0],
                                              [ 0, -1, -1],
                                              [ 3, -1,  2],
                                              [ 5, -1, -1]], dtype=int))
                                             
    # Test data from .tri file
    assert_array_equal(cr.tri_tri,  np.array([[10,  1, 19],
                                              [ 0,  3, 16],
                                              [ 2,  5, 20],
                                              [ 4,  7, 24],
                                              [ 6,  9, 26],
                                              [ 8, 11, 32],
                                              [12, 15, 18],
                                              [22, 21, 25],
                                              [30, 29, 33]], dtype=int))

    # Read the first time step
    cr.read_next_timeslice()

    # Test data from .nodes file
    assert cr.current_time==1.0, 'time error'
    assert cr.number_of_nodes==9, 'num nodes should be 9'
    assert cr.number_of_edges==34, 'num edges should be 34'
    assert cr.number_of_triangles==9, 'num tri should be 9'
                                             
    # Now try again with values

    # Test data from .nodes file
    assert_array_equal(np.round(cr.x, decimals=1), \
                       np.array([480.8, 0.0, 0.0, 0.0, 500.0, 1000.0, 1000.0, \
                       1000.0, 500.0]))
    assert_array_equal(np.round(cr.y, decimals=1), \
                       np.array([523.5, 0.0, 500.0, 1000.0, 1000.0, 1000.0, 0.0, \
                       500.0, 0.0]))
    assert_array_equal(cr.edg_at_node, np.array([0, 12, 1, 3, 5, 7, 28, 9, 11], \
                       dtype=int))
    assert_array_equal(cr.bnd, np.array([0, 1, 1, 1, 1, 1, 1, 1, 2], dtype=int))
    
    # Test data from .area file
    assert_array_equal(np.round(cr.drainage_area, decimals=1), \
                       np.array([249753.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                       
    # Test data from .net file
    assert_array_equal(cr.drains_to, np.array([8, -1, -1, -1, -1, -1, -1, -1, -1]))
                       
     # Test data from .q (discharge) file
    assert_array_equal(np.round(cr.q, decimals=1), np.zeros(9))
                       
     # Test data from .slp (slope) file
    assert_array_equal(np.round(cr.slope, decimals=3),  \
                       np.array([0.002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                       
     # Test data from .tau (shear stress) file
    assert_array_equal(np.round(cr.tau, decimals=1), np.zeros(9))
                       
    # Test data from .varea (Voronoi cell area) file
    assert_array_equal(np.round(cr.voronoi_area, decimals=1), \
                       np.array([249753.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                       
     # Test data from .z (elevation) file: now increased by 1 at interior node
    assert_array_equal(np.round(cr.z, decimals=1), \
                       np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                       
    # Test data from .edges file
    assert_array_equal(cr.edge_tail, np.array([0, 2, 0, 3, 0, 4, 0, 5, 0, 7, \
                                               0, 8, 1, 2, 1, 8, 2, 3, 2, 8, \
                                               3, 4, 3, 5, 4, 5, 5, 7, 6, 7, \
                                               6, 8, 7, 8], dtype=int))
    assert_array_equal(cr.edge_head, np.array([2, 0, 3, 0, 4, 0, 5, 0, 7, 0, \
                                               8, 0, 2, 1, 8, 1, 3, 2, 8, 2, \
                                               4, 3, 5, 3, 5, 4, 7, 5, 7, 6, \
                                               8, 6, 8, 7], dtype=int))
    assert_array_equal(cr.ccw_edge, np.array([10, 16,  0, 20,  2, 24,  4, 26,  6, 32, \
                                               8, 19, 14, 18, 12, 31, 13,  3,  1, 15, \
                                              22,  5, 17, 25, 21,  7, 23,  9, 30, 27, \
                                              28, 33, 29, 11], dtype=int))
                                              
    # Test data from .tri file
    assert_array_equal(cr.tri_vertex, np.array([[0, 2, 8],
                                                [0, 3, 2],
                                                [0, 4, 3],
                                                [0, 5, 4],
                                                [0, 7, 5],
                                                [0, 8, 7],
                                                [1, 8, 2],
                                                [3, 4, 5],
                                                [6, 7, 8]], dtype=int))
                                             
    # Test data from .tri file
    assert_array_equal(cr.tri_edge, np.array([[ 6,  5,  1],
                                              [-1,  0,  2],
                                              [ 7,  1,  3],
                                              [ 7,  2,  4],
                                              [-1,  3,  5],
                                              [ 8,  4,  0],
                                              [ 0, -1, -1],
                                              [ 3, -1,  2],
                                              [ 5, -1, -1]], dtype=int))
                                             
    # Test data from .tri file
    assert_array_equal(cr.tri_tri,  np.array([[10,  1, 19],
                                              [ 0,  3, 16],
                                              [ 2,  5, 20],
                                              [ 4,  7, 24],
                                              [ 6,  9, 26],
                                              [ 8, 11, 32],
                                              [12, 15, 18],
                                              [22, 21, 25],
                                              [30, 29, 33]], dtype=int))
                                             
                                             

if __name__=='__main__':
    test_child_reader()

    
