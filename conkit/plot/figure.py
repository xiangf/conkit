# BSD 3-Clause License
#
# Copyright (c) 2016-18, University of Liverpool
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""A module containing generic Figure related objects"""

__author__ = "Felix Simkovic"
__date__ = "08 Jan 2018"
__version__ = "0.2"

import os
import matplotlib.collections as mcoll
import matplotlib.pyplot as plt


class Figure(object):
    """A Figure class to store common features"""

    def __init__(self, ax=None, legend=True):
        """Initialise a new :obj:`conkit.plot.Figure` object
            
        Parameters
        ----------
        ax : :obj:`Axes <matplotlib.pyplot.Axes>`
           A pre-defined :obj:`Axes <matplotlib.pyplot.Axes>` 

           If ``None`` is provided, a new plot will be created

        legend : bool, optional
           Draw a legend on the plot [default: True]
        
        """
        if ax is None:
            import matplotlib.pyplot as plt
            self._fig, self._ax = plt.subplots()
        else:
            self._fig = ax.get_figure()
            self._ax = ax
        self.legend = legend

    def __repr__(self):
        return self.__class__.__name__

    def _patch_scatter(self, x, y, facecolor="#ffffff", edgecolor="#000000", radius=0.5, linewidth=1.0):
        """Draw scatter points as :obj:`Circles <matplotlib.pyplot.Circle>` to control width for discrete data"""
        if len(x) != len(y):
            raise ValueError("Unequal x and y data provided")

        if isinstance(facecolor, str):
            fc = [facecolor] * len(x)
        else:
            if len(facecolor) != len(x):
                raise ValueError("Unequal x/y data and facecolors provided")
            fc = facecolor

        if isinstance(edgecolor, str):
            ec = [edgecolor] * len(x)
        else:
            if len(edgecolor) != len(x):
                raise ValueError("Unequal x/y data and edgecolors provided")
            ec = edgecolor

        if isinstance(linewidth, float) or isinstance(linewidth, int):
            lw = [linewidth] * len(x)
        else:
            if len(linewidth) != len(x):
                raise ValueError("Unequal x/y data and linewidths provided")
            lw = linewidth

        if isinstance(radius, float) or isinstance(radius, int):
            r = [radius] * len(x)
        else:
            if len(radius) != len(x):
                raise ValueError("Unequal x/y data and radii provided")
            r = radius

        # Credits to https://stackoverflow.com/a/48174228/3046533
        circles = [
            plt.Circle((xi, yi), facecolor=fci, edgecolor=eci, radius=ri, linewidth=lwi)
            for xi, yi, fci, eci, ri, lwi in zip(x, y, fc, ec, r, lw)
        ]
        if len(circles) > 0:
            patch_collection = mcoll.PatchCollection(circles, match_original=True)
            self.ax.add_collection(patch_collection)

    def savefig(self, filename, dpi=300, overwrite=False):
        if os.path.isfile(filename) and not overwrite:
            raise RuntimeError("File exists: %s! Please rename or remove." % filename)
        else:
            self._fig.savefig(filename, dpi=dpi, bbox_inches="tight")

    @property
    def fig(self):
        return self._fig

    @property
    def ax(self):
        return self._ax
