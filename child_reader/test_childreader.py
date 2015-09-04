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

    assert cr.current_time==0.0, 'time error'
    assert cr.number_of_nodes==9, 'num nodes should be 9'
    assert_array_equal(np.round(cr.x, decimals=1), \
                       np.array([480.8, 0.0, 0.0, 0.0, 500.0, 1000.0, 1000.0, \
                       1000.0, 500.0]))
    
if __name__=='__main__':
    test_child_reader()

    
    