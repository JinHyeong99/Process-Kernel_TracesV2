from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QProgressDialog, QAction
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QColor
from program_util import extract_activity_name, set_log_first, set_log_second, build_node_tree
from program_visualize import NodeVisualizer
from program_util import bfs_backtrack_on_range
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer

class LogLoaderThread(QThread):
    finished = pyqtSignal()
    resultReady = pyqtSignal(object)

    def __init__(self, file_path):
        super(LogLoaderThread, self).__init__()
        self.file_path = file_path

    def run(self):
        log = xes_importer.apply(self.file_path)
        self.resultReady.emit(log)
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Finding Kernel-Traces Program")
        self.setGeometry(100, 100, 1400, 500)
        self.setupUI()
        self.previous_level = 1

    def setupUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        hLayout = QHBoxLayout()
        self.prevLevelLabel = QLabel("Previous Level:")
        self.prevLevelInput = QLineEdit("1")
        self.prevLevelInput.setFixedWidth(50)
        self.runBfsButton = QPushButton("Run BFS Backtrack")
        self.runBfsButton.clicked.connect(self.runBfsBacktrack)

        hLayout.addWidget(self.prevLevelLabel)
        hLayout.addWidget(self.prevLevelInput)
        hLayout.addWidget(self.runBfsButton)
        layout.addLayout(hLayout)

        self.createMenuBar()

    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        openAction = QAction("&Open", self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XES File", "", "XES Files (*.xes)")
        if file_path:
            self.progressDialog = QProgressDialog("Reading XES file...", "Cancel", 0, 0, self)
            self.progressDialog.setCancelButton(None)
            self.progressDialog.setModal(True)
            self.progressDialog.show()

            self.thread = LogLoaderThread(file_path)
            self.thread.finished.connect(self.progressDialog.close)
            self.thread.resultReady.connect(self.displayLog)
            self.thread.start()

    def displayLog(self, log):
        self.textEdit.clear()
        log_activity = extract_activity_name(log)
        first_set_log_activity = set_log_first(log_activity)
        kernel_traces = set_log_second(first_set_log_activity)
        self.textEdit.setTextColor(QColor(Qt.red))
        self.textEdit.append(f"The number of Kernel-Traces: {len(kernel_traces)}")
        self.textEdit.setTextColor(QColor(Qt.black))
        for case_index, case in enumerate(kernel_traces):
            self.textEdit.append(f"Case {case_index+1}: " + "--> ".join(case))

        node_tree = build_node_tree(kernel_traces)
        self.visualizer = NodeVisualizer(node_tree)
        self.visualizer.show()
        self.log = log

    def runBfsBacktrack(self):
        try:
            self.previous_level = int(self.prevLevelInput.text())
        except ValueError:
            self.previous_level = 1
            self.prevLevelInput.setText("1")

        kernel_traces = extract_activity_name(self.log)
        first_set_log_activity = set_log_first(kernel_traces)
        self.log_activity = set_log_second(first_set_log_activity)
        node_tree = build_node_tree(self.log_activity)
        
        completed_subtrees = bfs_backtrack_on_range(node_tree, self.previous_level)
        self.textEdit.setTextColor(QColor(Qt.red))
        self.textEdit.append(f"\nBFS Backtrack with Previous Level {self.previous_level}")
        self.textEdit.append(f"The number of Ktrace-Tree Traverse-Order: Breadth-First: {len(completed_subtrees)}")
        self.textEdit.setTextColor(QColor(Qt.black))
        for subtree in completed_subtrees:
            self.textEdit.append("--> ".join(subtree))

