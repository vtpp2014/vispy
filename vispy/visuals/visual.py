# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

from __future__ import division

from ..util.event import EmitterGroup, Event

"""
API Issues to work out:

  * Need Visual.bounds() as described here:
    https://github.com/vispy/vispy/issues/141

"""


class Visual(object):
    """
    Abstract class representing a drawable object.

    At a minimum, Visual subclasses should extend the draw() method. 

    Events:

    update : Event
        Emitted when the visual has changed and needs to be redrawn.
    bounds_change : Event
        Emitted when the bounds of the visual have changed.

    """

    def __init__(self, **kwargs):
        self.events = EmitterGroup(source=self,
                                   auto_connect=True,
                                   update=Event,
                                   bounds_change=Event,
                                   )

    def _update(self):
        """
        This method is called internally whenever the Visual needs to be 
        redrawn. By default, it emits the update event.
        """
        self.events.update()

    def draw(self, transforms):
        """
        Draw this visual now.
        The default implementation does nothing.
        
        This function is called automatically when the visual needs to be drawn
        as part of a scenegraph, or when calling 
        ``SceneCanvas.draw_visual(...)``. It is uncommon to call this method 
        manually.
        
        The *transforms* argument is a TransformSystem instance that provides 
        access to transforms that the visual
        may use to determine its relationship to the document coordinate
        system (which provides physical measurements) and the framebuffer
        coordinate system (which is necessary for antialiasing calculations). 
        
        Vertex transformation can be done either on the CPU using 
        Transform.map(), or on the GPU using the GLSL functions generated by 
        Transform.shader_map().
        """
        pass

    def bounds(self, mode, axis):
        """ Return the (min, max) bounding values describing the location of
        this node in its local coordinate system.
        
        Parameters
        ----------
        mode : str
            Describes the type of boundary requested. Can be "visual", "data",
            or "mouse".
        axis : 0, 1, 2
            The axis along which to measure the bounding values.
        
        Returns
        -------
        None or (min, max) tuple. 
        
        Notes
        -----
        This is used primarily to allow automatic ViewBox zoom/pan.
        By default, this method returns None which indicates the object should 
        be ignored for automatic zooming along *axis*.
        
        A scenegraph may also use this information to cull visuals from the
        display list.
        
        """
        return None

    def update(self):
        """
        Emit an event to inform listeners that this Visual needs to be redrawn.
        """
        self.events.update()