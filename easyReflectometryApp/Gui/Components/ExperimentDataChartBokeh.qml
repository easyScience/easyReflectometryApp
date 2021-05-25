import QtQuick 2.13

import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.experimentPlotRangesObj
    sldPlotRanges: ExGlobals.Constants.proxy.plotting1d.sldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: "R(q)"
}
