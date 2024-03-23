from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPen

class NodeVisualizer(QMainWindow):
    def __init__(self, root, parent=None):
        super(NodeVisualizer, self).__init__(parent)
        self.setWindowTitle("Node Tree Visualization")
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, central_widget)
        layout.addWidget(self.view)
        self.positions = {}
        self.level_widths = {}
        self.draw_nodes(root, 0, 0, "")
    def draw_nodes(self, node, x, y, path):
        radius = 30
        horizontal_spacing = 200
        vertical_spacing = 200
        current_path = path + "/" + node.name
        level = len(current_path.split('/')) - 1
        if level not in self.level_widths:
            self.level_widths[level] = 0
        width = self.level_widths[level]
        self.level_widths[level] += 1
        x = width * horizontal_spacing
        self.positions[current_path] = (x, y)
        ellipse = QGraphicsEllipseItem(QRectF(x, y, radius*2, radius*2))
        ellipse.setBrush(QBrush(Qt.white))
        self.scene.addItem(ellipse)
        text_y_offset = -20
        text = QGraphicsTextItem(node.name)
        text.setPos(x + radius/4, y + text_y_offset)
        font = QFont()
        font.setBold(True)
        text.setFont(font)
        text.setDefaultTextColor(QColor(Qt.red))
        self.scene.addItem(text)
        child_y = y + vertical_spacing
        for child in node.children:
            self.draw_nodes(child, x, child_y, current_path)
            child_x, _ = self.positions[current_path + "/" + child.name]
            self.scene.addLine(x + radius, y + radius*2, child_x + radius, child_y, QPen(Qt.black))
