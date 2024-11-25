# SPDX-FileCopyrightText: 2024 EasyReflectometryApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyReflectometryApp project <https://github.com/easyscience/EasyReflectometryApp>

import os
import sys
from pathlib import Path

from EasyApp.Logic.Logging import console
from PySide6.QtCore import qInstallMessageHandler
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterSingletonType

try:  # Needed by installer
    from EasyReflectometryApp.Backends.Py import PyBackend
    from EasyReflectometryApp.Backends.Py.helpers import Application
except ImportError:  # Running locally
    from Backends.Py import PyBackend
    from Backends.Py.helpers import Application

CURRENT_DIR = Path(__file__).parent  # path to qml components of the current project
EASYAPP_DIR = CURRENT_DIR / '..' / '..' / 'EasyApp' / 'src'  # path to qml components of the easyapp module
# MAIN_QML = CURRENT_DIR / 'main.qml'  # path to the root qml file


if __name__ == '__main__':
    qInstallMessageHandler(console.qmlMessageHandler)
    console.debug('Custom Qt message handler defined')

    app = Application(sys.argv)  # Create the QApplication (Not QGuiApplication)
    console.debug(f'Qt Application created {app}')

    engine = QQmlApplicationEngine()
    console.debug(f'QML application engine created {engine}')

    qmlRegisterSingletonType(PyBackend, 'Backends', 1, 0, 'PyBackend')
    console.debug('Backend class is registered to be accessible from QML via the name PyBackend')

    engine.addImportPath(EASYAPP_DIR)
    engine.addImportPath(CURRENT_DIR)
    console.debug('Paths added where QML searches for components')

    dirs = os.listdir('.')
    console.debug(f'{dirs}')
    path_main_qml = Path('main.qml')
    if not path_main_qml.exists():
        path_main_qml = CURRENT_DIR / path_main_qml

    engine.load(path_main_qml)
    console.debug('Main QML component loaded')

    console.debug('Application event loop is about to start')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
