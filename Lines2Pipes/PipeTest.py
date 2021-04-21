#Author-Autodesk Inc.
#Description-Select a path to create a pipe.

import adsk.core, adsk.fusion, traceback

pipeRadius = 0.4/10
pipeThickness = '0.4mm'

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
            return

        sel = ui.selectEntity('Select a path to create a pipe', 'Edges,SketchCurves')
        selObj = sel.entity

        comp = design.rootComponent

        # create path
        feats = comp.features
        chainedOption = adsk.fusion.ChainedCurveOptions.connectedChainedCurves
        if adsk.fusion.BRepEdge.cast(selObj):
            chainedOption = adsk.fusion.ChainedCurveOptions.tangentChainedCurves
        path = adsk.fusion.Path.create(selObj, chainedOption)

        path = feats.createPath(selObj)


        # create profile
        planes = comp.constructionPlanes
        planeInput = planes.createInput()
        planeInput.setByDistanceOnPath(selObj, adsk.core.ValueInput.createByReal(0))
        plane = planes.add(planeInput)

        sketches = comp.sketches
        sketch = sketches.add(plane)


        center = plane.geometry.origin
        center = sketch.modelToSketchSpace(center)
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(center, pipeRadius)
        profile = sketch.profiles[0]


        # Set the expression of the parameter
        # Add a diameter constraint.
        skDim = sketch.sketchDimensions.addDiameterDimension(circle, adsk.core.Point3D.create(5,5,0), True)
        # Set the expression of the parameter controlling the dimension constraint.
        skDim.parameter.expression = 'D_fillament'

        profile = sketch.profiles[0]

        # create sweep
        sweepFeats = feats.sweepFeatures
        sweepInput = sweepFeats.createInput(profile, path, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        sweepInput.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
        sweepFeat = sweepFeats.add(sweepInput)
        sketch.isVisible
        # app.activeViewport.refresh()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
