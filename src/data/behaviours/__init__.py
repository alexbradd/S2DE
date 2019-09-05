"""
docs you might read before this one:
- engine.gameobject module
- engine.basecomponents module

The behaviours package contains every child of the Behaviour class. They have
been put in a separate package to remove the need of constantly changing the
engine package when adding and removing Components. This makes it easier for
the user to add its Components as they aren't tangled in the base engine's code.

Every class contained in this package has to import the Behaviour class from
the engine package and expose itself in this __init__ file.

A script can be used to automate adding new Behaviours.
"""
# expose classes in modules for easy access
from behaviours.boxrenderer import BoxRenderer
from behaviours.sphererenderer import CircleRenderer
from behaviours.textrenderer import TextRenderer

