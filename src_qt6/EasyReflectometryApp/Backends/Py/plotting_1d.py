import numpy as np
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from EasyApp.Logic.Logging import console

from easyreflectometry import Project as ProjectLib
from easyreflectometry.data import DataSet1D

from .helpers import IO 

PLOT_BACKEND = 'QtCharts'

class Plotting1d(QObject):
    currentLib1dChanged = Signal()
    useAcceleration1dChanged = Signal()
    chartRefsChanged = Signal()
    sldChartRangesChanged = Signal()
    sampleChartRangesChanged = Signal()
    experimentChartRangesChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._project_lib = project_lib
        self._proxy = parent
        self._currentLib1d = 'QtCharts'
        self._useAcceleration1d = True
        self._model_index = 0
        self._chartRefs = {

            'QtCharts': {
                'samplePage': {
                    'sampleSerie': None,
                    'sldSerie': None,
                },
                'experimentPage': {
                    'measuredSerie': None,
                    'varianceUpperSerie': None,
                    'varianceLowerSerie': None,
                },
            }
        }

    @property
    def sample_data(self) -> DataSet1D:
        try:
            data = self._project_lib.sample_data_for_model_at_index()
        except IndexError:
            data = DataSet1D(
                name='Sample Data empty',
                    x=np.empty(0),
                    y=np.empty(0),
            )
        return data

    @property
    def sld_data(self) -> DataSet1D:
        try:
            data = self._project_lib.sld_data_for_model_at_index()
        except IndexError:
            data = DataSet1D(
                name='SLD Data empty',
                    x=np.empty(0),
                    y=np.empty(0),
            )
        return data

    @property
    def experiment_data(self) -> DataSet1D:
        try:
            data = self._project_lib.experimental_data_for_model_at_index()
        except IndexError:
            data = DataSet1D(
                name='Experiment Data empty',
                    x=np.empty(0),
                    y=np.empty(0),
                    ey=np.empty(0),
                    ex=np.empty(0),
            )
        return data

    # Sample
    @Property(float, notify=sampleChartRangesChanged)
    def sampleMaxX(self):
        return self.sample_data.x.max()

    @Property(float, notify=sampleChartRangesChanged)
    def sampleMinX(self):
        return self.sample_data.x.min()
    
    @Property(float, notify=sampleChartRangesChanged)
    def sampleMaxY(self):
        return np.log10(self.sample_data.y.max())

    @Property(float, notify=sampleChartRangesChanged)
    def sampleMinY(self):
        return np.log10(self.sample_data.y.min())
    
    # SLD
    @Property(float, notify=sldChartRangesChanged)
    def sldMaxX(self):
        return self.sld_data.x.max()

    @Property(float, notify=sldChartRangesChanged)
    def sldMinX(self):
        return self.sld_data.x.min()
    
    @Property(float, notify=sldChartRangesChanged)
    def sldMaxY(self):
        return self.sld_data.y.max()

    @Property(float, notify=sldChartRangesChanged)
    def sldMinY(self):
        return self.sld_data.y.min()

    # Experiment
    @Property(float, notify=experimentChartRangesChanged)
    def experimentMaxX(self):
        return self.experiment_data.x.max()

    @Property(float, notify=experimentChartRangesChanged)
    def experimentMinX(self):
        return self.experiment_data.x.min()
    
    @Property(float, notify=experimentChartRangesChanged)
    def experimentMaxY(self):
        return np.log10(self.experiment_data.y.max())

    @Property(float, notify=experimentChartRangesChanged)
    def experimentMinY(self):
        return np.log10(self.experiment_data.y.min())

    @Property(str, notify=currentLib1dChanged)
    def currentLib1d(self):
        return self._currentLib1d

    @currentLib1d.setter
    def currentLib1d(self, newValue):
        if self._currentLib1d == newValue:
            return
        self._currentLib1d = newValue
        self.currentLib1dChanged.emit()

    @Property(bool, notify=useAcceleration1dChanged)
    def useAcceleration1d(self):
        return self._useAcceleration1d

    @useAcceleration1d.setter
    def useAcceleration1d(self, newValue):
        if self._useAcceleration1d == newValue:
            return
        self._useAcceleration1d = newValue
        self.useAcceleration1dChanged.emit()

    @Property('QVariant', notify=chartRefsChanged)
    def chartRefs(self):
        return self._chartRefs

    @Slot(int)
    def setModelIndex(self, value: int) -> None:
        self._model_index = value

    @Slot(str, str, 'QVariant')
    def setQtChartsReflectometrySerieRef(self, page:str, serie:str, ref: QObject):
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))

    @Slot(str, str, 'QVariant')
    def setQtChartsSldSerieRef(self, page:str, serie:str, ref: QObject):
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))

    @Slot(str, str, 'QVariant')
    def setQtChartsExperimentSerieRef(self, page:str, serie:str, ref: QObject):
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))

    def refreshSamplePage(self):
        self.drawCalculatedOnSampleChart()
        self.drawCalculatedOnSldChart()

    def refreshExperimentPage(self):
        self.drawMeasuredOnExperimentChart()

    def drawCalculatedOnSampleChart(self):
        if PLOT_BACKEND == 'QtCharts':
            self.qtchartsReplaceCalculatedOnSampleChartAndRedraw()

    def drawCalculatedOnSldChart(self):
        if PLOT_BACKEND == 'QtCharts':
            self.qtchartsReplaceCalculatedOnSldChartAndRedraw()

    def drawMeasuredOnExperimentChart(self):
        if PLOT_BACKEND == 'QtCharts':
            self.qtchartsReplaceMeasuredOnExperimentChartAndRedraw()

    def qtchartsReplaceCalculatedOnSampleChartAndRedraw(self):
        series = self._chartRefs['QtCharts']['samplePage']['sampleSerie']
        series.clear()
        nr_points = 0
        for point in self.sample_data.data_points():
            series.append(point[0], np.log10(point[1]))
            nr_points = nr_points + 1
        console.debug(IO.formatMsg('sub', 'Calc curve', f'{nr_points} points', 'on sample page', 'replaced'))

    def qtchartsReplaceCalculatedOnSldChartAndRedraw(self):
        series = self._chartRefs['QtCharts']['samplePage']['sldSerie']
        series.clear()
        nr_points = 0
        for point in self.sld_data.data_points():
            series.append(point[0], point[1])
            nr_points = nr_points + 1
        console.debug(IO.formatMsg('sub', 'Sld curve', f'{nr_points} points', 'on sample page', 'replaced'))

    def qtchartsReplaceMeasuredOnExperimentChartAndRedraw(self):
        series_measured = self._chartRefs['QtCharts']['experimentPage']['measuredSerie']
        series_measured.clear()
        series_variance_upper = self._chartRefs['QtCharts']['experimentPage']['varianceUpperSerie']
        series_variance_upper.clear()
        series_variance_lower = self._chartRefs['QtCharts']['experimentPage']['varianceLowerSerie']
        series_variance_lower.clear()
        nr_points = 0
        for point in self.experiment_data.data_points():
            if point[0] < self._project_lib.q_max and self._project_lib.q_min < point[0]:
                series_measured.append(point[0], np.log10(point[1]))
                series_variance_upper.append(point[0], np.log10(point[1] + np.sqrt(point[2])))
                series_variance_lower.append(point[0], np.log10(point[1] - np.sqrt(point[2])))
                nr_points = nr_points + 1

        console.debug(IO.formatMsg('sub', 'Measurede curve', f'{nr_points} points', 'on experiment page', 'replaced'))