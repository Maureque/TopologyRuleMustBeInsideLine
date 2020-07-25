# encoding: utf-8

import gvsig
import sys

from gvsig import geom
from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
# from org.gvsig.expressionevaluator import GeometryExpressionEvaluatorLocator
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRule

from deleteLineAction import DeleteLineAction
from markLineAction import MarkLineAction

class MustBeInsideLineRule(AbstractTopologyRule):
    
    geomName = None
    expression = None
    expressionBuilder = None
    
    def __init__(self, plan, factory, tolerance, dataSet1, dataSet2):
        AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1, dataSet2)
        self.addAction(DeleteLineAction())
        self.addAction(MarkLineAction())
    
    def contains(self, line1, theDataSet2, tolerance1):
        result = [False, []]
        if theDataSet2.getSpatialIndex() != None:
            for featureReference in theDataSet2.query(line1):
                feature2 = featureReference.getFeature()
                polygon2 = feature2.getDefaultGeometry()
                if tolerance1 > 0:
                    buffer2 = polygon2.buffer(tolerance1)
                else:
                    buffer2 = polygon2
                if buffer2.contains(line1):
                    result[0] = True
                    break
        else:
            if self.expression == None:
                self.expression = ExpressionEvaluatorLocator.getManager().createExpression()
                self.expressionBuilder = ExpressionEvaluatorLocator.getManager().createExpressionBuilder()
                # self.expressionBuilder = GeometryExpressionEvaluatorLocator.getManager().createExpressionBuilder()
                store2 = theDataSet2.getFeatureStore()
                self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()
                self.expression.setPhrase(
                self.expressionBuilder.ifnull(
                        self.expressionBuilder.column(self.geomName),
                        self.expressionBuilder.constant(False),
                        self.expressionBuilder.ST_Contains(
                            self.expressionBuilder.ST_Buffer(
                                self.expressionBuilder.column(self.geomName),
                                tolerance1
                            ),
                            self.expressionBuilder.geometry(line1)
                        )
                    ).toString()
                )
            if theDataSet2.findFirst(self.expression) != None:
                result[0] = True
        return result
    
    def check(self, taskStatus, report, feature1):
        try:
            line1 = feature1.getDefaultGeometry()
            tolerance1 = self.getTolerance()
            theDataSet2 = self.getDataSet2()
            geometryType1 = line1.getGeometryType()
            if geometryType1.getSubType() == geom.D2 or geometryType1.getSubType() == geom.D2M:
                if geometryType1.getType() == geom.LINE or geometryType1.isTypeOf(geom.LINE):
                    result = self.contains(line1, theDataSet2, tolerance1)
                    if not result[0]:
                        report.addLine(self,
                            self.getDataSet1(),
                            self.getDataSet2(),
                            line1,
                            line1,
                            feature1.getReference(),
                            None,
                            -1,
                            -1,
                            False,
                            "The line is not contained.",
                            ""
                        )
                else:
                    if geometryType1.getType() == geom.MULTILINE or geometryType1.isTypeOf(geom.MULTILINE):
                        n1 = line1.getPrimitivesNumber()
                        for i in range(0, n1 + 1):
                            result = self.contains(buffer1, theDataSet2, tolerance1)
                            if not result[0]:
                                report.addLine(self,
                                    self.getDataSet1(),
                                    self.getDataSet2(),
                                    line1,
                                    line1,
                                    feature1.getReference(),
                                    None,
                                    -1,
                                    -1,
                                    False,
                                    "The multiline is not contained.",
                                    ""
                                )
            else:
                report.addLine(self,
                    self.getDataSet1(),
                    self.getDataSet2(),
                    line1,
                    line1,
                    feature1.getReference(),
                    None,
                    -1,
                    -1,
                    False,
                    "Unsupported geometry subtype.",
                    ""
                )
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass
