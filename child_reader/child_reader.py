 # -*- coding: utf-8 -*-
"""
child_reader.py

Reads output from CHILD model.

Created on Thu Aug 20 16:23:47 2015

@author: gtucker
"""

import os
from numpy import zeros, ones, array

_BASIC_CHILD_EXTENSIONS = [ 'nodes',
                      'edges',
                      'tri',
                      'z' ]


class ChildRun(object):
    """
    Represents files generated by a CHILD model run.
    """
    def __init__(self, filename):
        """
        Finds and opens CHILD output files with a given base name.
        """
        # find and open the files        
        self.open_child_files(filename)
        
        # find out the time associated with the first time slice in file
        self.current_time = self.read_current_time()
        self.current_time_slice = 0
        
        # find out how many nodes there are (at least in first time slice,
        # usually the same in all time slices). Also, how many edges and
        # triangles.
        self.number_of_nodes = self.read_number_of_nodes()
        self.number_of_edges = self.read_number_of_edges()
        self.number_of_triangles = self.read_number_of_triangles()
        
        # create the arrays needed to store the data for one time slice
        self.create_data_arrays()
        
        
    def open_child_files(self, name):
        """
        Looks for, and if possible, opens CHILD files with the given base name.
        Raises an IOError if one or more of the required files cannot be 
        found.
        
        Example
        -------
        >>> for ext in _BASIC_CHILD_EXTENSIONS:
        ...     f = open('test.'+ext, 'w')
        ...     f.close()
        >>> f = open('only_one_file.nodes', 'w')
        >>> f.close()
        >>> cr = ChildRun('test')
        >>> cr = ChildRun('test.edges')
        """
        basename = os.path.splitext(name)[0]
        try:
            self.nodefile = open(basename+'.nodes', 'r')
            self.edgefile = open(basename+'.edges', 'r')
            self.trifile = open(basename+'.tri', 'r')
            self.zfile = open(basename+'.z', 'r')
            self.areafile = open(basename+'.area', 'r')
            self.netfile = open(basename+'.net', 'r')
            self.qfile = open(basename+'.q', 'r')
            self.slopefile = open(basename+'.slp', 'r')
            self.taufile = open(basename+'.tau', 'r')
            self.vareafile = open(basename+'.varea', 'r')
        except IOError:
            print('Can not find one or more files for run called '+basename)
            raise IOError
            
            
    def read_next_timeslice(self):
        """
        Reads data for the next timeslice for the current run.
        """
        self.read_node_data()
        self.read_drainage_areas()
        self.read_flow_dirs()
        self.read_discharges()
        self.read_slopes()
        self.read_shear_stresses()
        self.read_voronoi_areas()
        self.read_elevations()
        self.read_edge_data()
        self.read_triangle_data()
        
        
    def read_node_data(self):
        """
        Reads node data for the current time slice.
        """
        # read the current time
        tm = float(self.nodefile.readline())
        self.current_time = tm
        
        # read the number of nodes
        nn = int(self.nodefile.readline())
        if nn!=self.number_of_nodes:
            # Number of nodes has changed; need to re-size the node arrays
            self.number_of_nodes = nn
            self.create_node_arrays()
        
        # read info for all the nodes
        for n in xrange(nn):
            line = self.nodefile.readline()
            line = line.split()
            assert len(line)==4, 'Error in node file'
            self.x[n] = float(line[0])
            self.y[n] = float(line[1])
            self.edg_at_node[n] = int(line[2])
            self.bnd[n] = int(line[3])
            
            
    def read_drainage_areas(self):
        """
        Reads data for drainage area from .area file.
        """
        tm = self.areafile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        self.number_of_core_nodes = int(self.areafile.readline())
        for n in range(self.number_of_core_nodes):
            self.drainage_area[n] = float(self.areafile.readline())
            
            
    def read_flow_dirs(self):
        """
        Reads direction of flow (receiver node ID) from .net file.
        """
        tm = self.netfile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        self.number_of_core_nodes = int(self.netfile.readline())
        for n in range(self.number_of_core_nodes):
            self.drains_to[n] = int(self.netfile.readline())
        
            
    def read_discharges(self):
        """
        Reads data for discharge from .q file.
        """
        tm = self.qfile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        nn = int(self.qfile.readline())
        assert nn==self.number_of_nodes, 'Mismatch in node numbers in q file'
        for n in range(nn):
            self.q[n] = float(self.qfile.readline())
            
            
    def read_slopes(self):
        """
        Reads data for slope from .slp file.
        """
        tm = self.slopefile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        nn = int(self.slopefile.readline())
        assert nn==self.number_of_nodes, 'Mismatch in node numbers in .slp file'
        for n in range(nn):
            self.slope[n] = float(self.slopefile.readline())
            
            
    def read_shear_stresses(self):
        """
        Reads data for shear stress from .tau file.
        """
        tm = self.taufile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        nn = int(self.taufile.readline())
        assert nn==self.number_of_nodes, 'Mismatch in node numbers in .slp file'
        for n in range(nn):
            self.tau[n] = float(self.taufile.readline())
            
            
    def read_voronoi_areas(self):
        """
        Reads data for voronoi cell area from .varea file.
        """
        tm = self.vareafile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        nn = int(self.vareafile.readline())
        assert nn==self.number_of_nodes, 'Mismatch in node numbers in .slp file'
        for n in range(nn):
            self.voronoi_area[n] = float(self.vareafile.readline())
            
            
    def read_elevations(self):
        """
        Reads data for elevations from .z file.
        """
        tm = self.zfile.readline()
        assert float(tm)==self.current_time, 'Time in .area file does not match current time'
        nn = int(self.zfile.readline())
        assert nn==self.number_of_nodes, 'Mismatch in node numbers in .slp file'
        for n in range(nn):
            self.z[n] = float(self.zfile.readline())
            
            
    def read_current_time(self):
        """
        Reads and returns the current time in the output files.
        """
        # Get the current position in the file
        curpos = self.zfile.tell()
        print 'current position is ', curpos
        
        # Read the line containing the time
        self.current_time = float(self.zfile.readline())
        print 'current position is now ', curpos
        print 'current time is now ', self.current_time
        
        # Go back to the previous location
        self.zfile.seek(curpos)
        print 'current position is finally ', curpos
        print 'and current time is  ', self.current_time
        
        
    def read_number_of_nodes(self):
        """
        Reads and returns number of nodes in current time slice.
        """
        # Remember position in file
        curpos = self.zfile.tell()
        
        # Read the line that should be time
        self.zfile.readline()
        
        # Read the line that should be number of nodes
        nn = int(self.zfile.readline())
        print 'there are',nn, 'nodes'
        
        # Return to the previous position
        self.zfile.seek(curpos)
        
        return nn
        
        
    def read_number_of_edges(self):
        """
        Reads and returns number of edges in current time slice.
        """
        # Remember position in file
        curpos = self.edgefile.tell()
        
        # Read the line that should be time
        self.edgefile.readline()
        
        # Read the line that should be number of nodes
        ne = int(self.edgefile.readline())
        print 'there are',ne, 'edges'
        
        # Return to the previous position
        self.edgefile.seek(curpos)
        
        return ne
        
        
    def read_number_of_triangles(self):
        """
        Reads and returns number of triangles in current time slice.
        """
        # Remember position in file
        curpos = self.trifile.tell()
        
        # Read the line that should be time
        self.trifile.readline()
        
        # Read the line that should be number of nodes
        nt = int(self.trifile.readline())
        print 'there are',nt, 'edges'
        
        # Return to the previous position
        self.trifile.seek(curpos)
        
        return nt
        
        
    def create_node_arrays(self):
        """Creates (or re-creates) the arrays of length equal to the 
        number of nodes."""
        
        # Create arrays for node-based info
        nn = self.number_of_nodes
        self.x = zeros(nn)
        self.y = zeros(nn)
        self.z = zeros(nn)
        self.edg_at_node = zeros(nn, dtype=int)
        self.bnd = zeros(nn, dtype=int)
        
        # Create array for drainage areas
        self.drainage_area = zeros(nn)

        # Create array for drainage directions (ID of receiver node)
        self.drains_to = -ones(nn, dtype=int)

        # Create array for discharges
        self.q = zeros(nn)

        # Create array for slopes
        self.slope = zeros(nn)

        # Create array for shear stresses
        self.tau = zeros(nn)

        # Create array for Voronoi cell areas
        self.voronoi_area = zeros(nn)

        
    def create_edge_arrays(self):
        """Creates (or re-creates) the arrays of length equal to the 
        number of edges."""
        
        # Create arrays for node-based info
        ne = self.number_of_edges
        self.edge_tail = zeros(ne, dtype=int)
        self.edge_head = zeros(ne, dtype=int)
        self.ccw_edge = zeros(ne, dtype=int)

        
    def create_triangle_arrays(self):
        """Creates (or re-creates) the arrays of length equal to the 
        number of triangles."""
        
        # Create arrays for node-based info
        nt = self.number_of_triangles
        self.tri_vertex = zeros((nt, 3), dtype=int)
        self.tri_edge = zeros((nt, 3), dtype=int)
        self.tri_tri = zeros((nt, 3), dtype=int)

        
    def create_data_arrays(self):
        """Creates the various arrays needed to store CHILD variables for one
        time slice."""
        self.create_node_arrays()
        self.create_edge_arrays()   
        self.create_triangle_arrays()
        

    def read_edge_data(self):
        """
        Reads edge data for the current time slice from the .edges file.
        """
        # read the current time
        tm = float(self.edgefile.readline())
        self.current_time = tm
        
        # read the number of nodes
        ne = int(self.edgefile.readline())
        if ne!=self.number_of_edges:
            # Number of nodes has changed; need to re-size the node arrays
            self.number_of_edges = ne
            self.create_edge_arrays()
        
        # read info for all the nodes
        for e in xrange(ne):
            line = self.edgefile.readline()
            line = line.split()
            assert len(line)==3, 'Error in edge file'
            self.edge_tail[e] = int(line[0])
            self.edge_head[e] = int(line[1])
            self.ccw_edge[e] = int(line[2])
            
            
    def read_triangle_data(self):
        """
        Reads edge data for the current time slice from the .edges file.
        """
        # read the current time
        tm = float(self.trifile.readline())
        self.current_time = tm
        
        # read the number of nodes
        nt = int(self.trifile.readline())
        if nt!=self.number_of_triangles:
            # Number of nodes has changed; need to re-size the node arrays
            self.number_of_triangles = nt
            self.create_triangle_arrays()
        
        # read info for all the nodes
        for t in xrange(nt):
            line = self.trifile.readline()
            line = line.split()
            assert len(line)==9, 'Error in tri file'
            self.tri_vertex[t][:] = array(line[0:3], dtype=int)
            self.tri_edge[t][:] = array(line[3:6], dtype=int)
            self.tri_tri[t][:] = array(line[6:9], dtype=int)
            
        print self.tri_vertex
        print self.tri_edge
        print self.tri_tri
        
            
            
        
        
def child_files_exist_with_name(the_name):
    """
    Returns True if file with specified name plus each of the standard 
    extensions exists at the current location, False otherwise.
    
    Parameters
    ----------
    basename : str
        Base name for CHILD run.
        
    Example
    -------
    >>> for ext in _BASIC_CHILD_EXTENSIONS:
    ...     f = open('test.'+ext, 'w')
    ...     f.close()
    >>> f = open('only_one_file.nodes', 'w')
    >>> f.close()
    >>> child_files_exist_with_name('test')
    True
    >>> child_files_exist_with_name('no_such_file')
    False
    >>> child_files_exist_with_name('only_one_file')
    False
    >>> child_files_exist_with_name('test.nodes')
    True
    """
    basename = os.path.splitext(the_name)[0]  # remove any extension
    for ext in _BASIC_CHILD_EXTENSIONS:
        if not os.path.exists(basename+'.'+ext):
            return False
    return True


def open_childrun(filename):
    """
    Creates and returns an instance of a childrun object, or throws an IOError.
    """
    return ChildRun(filename)
    

if __name__=='__main__':
    import doctest
    doctest.testmod()
    