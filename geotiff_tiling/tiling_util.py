import numpy as np
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
from affine import Affine
from pyproj import Proj
from pyproj import transform

class MosiacBuilder():
    """ A class to manage building mosaics from geotiff images. 
    """

    def __init__(self, filepath, builder_name=None, side_len=1000):
        """ Initialize the builder. Note, this step is not very memory intensive. 
        
        Args:
            - filepath (str): the full filepath to the TILED geotiff
            - builder_name (str): the optional name of the object
            - side_len (int): the pixel value of the side length of a mosiac tile
        
        """
        self.filepath = filepath
        self.src = rasterio.open(self.filepath)
        self.shape = self.src.shape
        self.NAME = builder_name
        self.PAD_VALUE = 255 # for empty tiles on the edges of the frame
        self.MOSIAC_SIDE_LENGTH = side_len


    def get_window(self, row, col, side_len, return_win=False):
        """ A method to get a subset of a given raster given 
        row/column offsets from (0,0). 

        ARGS:
            - row (int): offset along latitude, y axis offset'
            - col (int): offset along longitude, x axis offset
            - side_len (int): how large is the image?
            - return_win (bool): if True, return the window object

        RETURNS:
            - subset (np.array): a window from the original raster. NOTE: by
                default this array is channels first, RGB: (3, side_len, side_len)

            - window (affine.Affine): DEPENDS ON BOOL FLAG: `return_win` set to True. 
                transformation associated with top-left corner
                of `subset`. Used for translation to lat/lon
        """
        window = rasterio.windows.Window(col, row, side_len, side_len)
        subset = self.src.read(window=window)    

        if return_win:
            return subset, window
        else: 
            return subset

    def get_latlon_point(self, row, col):
        """ Get lat andf lon from a single point 
        
        ARGS:
            - col (int): offset along longitude, x axis offset
            - row (int): offset along latitude, y axis offset'

        RETURNS:
            - lat (float): latitude
            - lon (float): longitude
        """
        p1 = Proj(self.src.crs)
        window = rasterio.windows.Window(col, row, 1, 1)
        trnsfrm = self.src.window_transform(window)
        T1 = trnsfrm * Affine.translation(0.5, 0.5)
        p2 = Proj(proj='latlong', datum='WGS84')
        x, y = self.src.xy(row, col)
        lon, lat = transform(p1, p2, x, y)
        return lat, lon

    
    def build_mosaic(self):
        """ A method to build a set number of SQUARE
        images with a given side length from a raster.side_len.

        NOTE: update the side length attribute to change the size of a tile
        
        RETURNS:
            - tiles (list of np.array): a list of subsets
            - center_coords (list of list): a list of [lat, lon] coordinates for the
                center of an image
        """

        side_len = self.MOSIAC_SIDE_LENGTH

        tiles = []
        center_coords = []

        row_idx = 0
        clip_num = 0

        for i in range(int(self.shape[0] / side_len)+1):
            col_idx = 0
            for j in range(int(self.shape[1] / side_len)+1):

                clip_num += 1
                if clip_num % 500 == 0:
                    print(f"Working on clip number: {clip_num}")

                # get clip
                clip = self.get_window(row_idx, col_idx, side_len)

                # handle non-square clips
                if clip.shape[1] != side_len or clip.shape[2] != side_len:
                    pad = np.full((3, side_len, side_len), self.PAD_VALUE)
                    pad[:, 0:clip.shape[1], 0:clip.shape[2]] = clip
                    clip = pad.copy()

                tiles.append(clip)

                # get center lat/lon
                lat, lon = self.get_latlon_point(row_idx + side_len // 2, col_idx + side_len // 2)

                center_coords.append([lat, lon])

                # increment counters
                col_idx += side_len
            row_idx += side_len

        return tiles, center_coords


    def chunker(self, arr, chunksize):
        """ a function to divide a large vector 
        into equal subparts.

        Args:
            - arr (iterable): array to chunk
            - chunksize (int): number of indices per chunk
        
        Returns: 
            - indices (list of tuple): (start, stop)
        """
        return (arr[pos:pos + chunksize] for pos in range(0, len(arr), chunksize))


    def laz_build_mosaic(self, chunksize=1000):
        """ A generator method to build a set number of SQUARE
        images with a given side length from a raster.side_len.

        NOTE: update the side length attribute to change the size of a tile

        ARGS:
            - chunksize (int): the number of tiles to evaluate 
                per yeild
        
        Yields:
            - tiles (list of np.array): a list of subsets
            - center_coords (list of list): a list of [lat, lon] coordinates for the
                center of an image
        """

        side_len = self.MOSIAC_SIDE_LENGTH

        center_coords = []

        row_idx = 0
        clip_num = 0

        corner_indices = []

        for i in range(int(self.shape[0] / side_len)+1):
            col_idx = 0
            for j in range(int(self.shape[1] / side_len)+1):

                _args = (row_idx, col_idx, side_len)

                corner_indices.append(_args)

                # # get center lat/lon
                # lat, lon = self.get_latlon_point(row_idx + side_len // 2, col_idx + side_len // 2)

                # center_coords.append([lat, lon])

                # increment counters
                col_idx += side_len
            row_idx += side_len

        test = self.chunker(corner_indices, chunksize)

        return test #, center_coords
   


def build_fig(title="", axis_off=False, size=(5, 5), 
              y_lab="", x_lab="", title_size=15, dpi=300):
    """A function to build a matplotlib figure. Primary
    goal is to sandardize the easy stuff.
    Args:
        - title (str): the title of the plot
        - axis_off (bool): should the axis be printed?
        - size (tuple): how big should the plot be?
        - y_lab (str): y axis label
        - x_lab (str): x axis label
    Returns:
        fig (plt.figure)
    """
    fig = plt.figure(figsize=size, 
                     facecolor='w',
                     dpi=dpi)
    fig.suptitle(title, fontsize=title_size)
    plt.xlabel(x_lab, fontsize=title_size)
    plt.ylabel(y_lab, fontsize=title_size)
    
    if axis_off:
        plt.axis('off')
    return fig