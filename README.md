# TopologyRuleMustBeInsideLine

The rule requires that the lines in the input layer must be covered by any of the polygons from the coverage layer, if this is not the case the error report is created.

For example, it is useful when lines must be inside of the limits of areas, like when you have streams of water and you want to comprobe if they are within hydrographic basins. Another useful application could be when lines may fully or partially coincide with area boundaries but cannot extend beyond polygons, such as departamental highways that must be within department boundaries.

![Rule image](https://github.com/Maureque/TopologyRuleMustBeInsideLine/blob/master/MustBeInside_d/mustBeInsideLine.png "Rule image")
