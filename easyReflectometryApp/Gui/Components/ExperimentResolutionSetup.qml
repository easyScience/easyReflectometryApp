import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    EaComponents.TableViewLabel {
        horizontalAlignment: Text.AlignRight
        width: elementWidth()
        text: qsTr("Resolution type:")
    }
    EaElements.ComboBox {
        width: elementWidth()
        model: ["Constant dq/q"]
    }

    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: elementWidth()
        text: qsTr("dq/q:")
    }
    EaElements.Parameter {
        id: res
        enabled: true
        width: elementWidth()
        anchors.verticalCenter: parent.verticalCenter
        units: "%"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.resolutionAsObj.res, 3)
        onEditingFinished: updateParameters()
    }

    // Logic

    function elementWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 4) / 4
    }

    function updateParameters() {
        const json = {
            "res": parseFloat(res.text),
        }
        ExGlobals.Constants.proxy.resolutionAsObj = JSON.stringify(json)
    }
}
