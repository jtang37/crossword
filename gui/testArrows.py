import sys
import os
sys.path.append(r'C:\Users\psatt\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QRunnable, QThreadPool, QObject
from copy import deepcopy
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF

class SizeInputApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Square Grid App")
        self.setGeometry(100, 100, 600, 600)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setFocusPolicy(Qt.StrongFocus)

        # Set a layout for the central widget
        layout = QVBoxLayout()

        # Create label and entry for user input
        self.label = QLabel("Enter a number:")
        self.label.setStyleSheet("background-color: white")
        layout.addWidget(self.label)

        self.entry = QLineEdit()
        self.entry.setStyleSheet("background-color: white")
        layout.addWidget(self.entry)

        # Create submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("background-color: white")
        self.submit_button.clicked.connect(self.create_grid)
        layout.addWidget(self.submit_button)

        # Create a QGraphicsView to draw the grid
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.view)

        # Set the layout for the central widget
        self.central_widget.setLayout(layout)

        self.size = 0
        self.grid_rects = None
        self.active_row = 0
        self.active_col = 0
        self.active_rect = None

    def create_grid(self):
        try:
            self.size = int(self.entry.text())
            self.initialize_grid()
            self.draw_grid()
            self.highlight_initial_square()  # Highlight the initial square
        except ValueError:
            self.label.setText("Invalid input. Please enter a valid number.")

    def initialize_grid(self):
        self.grid_rects = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.scene.clear()

    def draw_grid(self):
        global square_size
        square_size = min(self.view.width(), self.view.height()) / self.size
        pen = QPen(Qt.black)
        brush = QBrush(QColor(255, 255, 255))  # White brush

        for i in range(self.size):
            for j in range(self.size):
                x = i * square_size
                y = j * square_size

                rect_item = QGraphicsRectItem(QRectF(x, y, square_size, square_size))
                rect_item.setPen(pen)
                rect_item.setBrush(brush)
                self.scene.addItem(rect_item)
                self.grid_rects[j][i] = rect_item

    def highlight_initial_square(self):
        if self.grid_rects and 0 <= self.active_row < self.size and 0 <= self.active_col < self.size:
            self.active_rect = self.grid_rects[self.active_row][self.active_col]
            self.active_rect.setBrush(QBrush(QColor(0, 255, 0)))  # Highlight the active square

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.handle_arrow_key(0, 1)  # Move right: Increment column index
        elif event.key() == Qt.Key_Left:
            self.handle_arrow_key(0, -1)  # Move left: Decrement column index
        elif event.key() == Qt.Key_Down:
            self.handle_arrow_key(1, 0)  # Move down: Increment row index
        elif event.key() == Qt.Key_Up:
            self.handle_arrow_key(-1, 0)  # Move up: Decrement row index
        else:
            super().keyPressEvent(event)

    def handle_arrow_key(self, dx, dy):
        new_row = self.active_row + dy
        new_col = self.active_col + dx

        if 0 <= new_row < self.size and 0 <= new_col < self.size:
            if self.active_text_item:
                self.active_text_item.clearFocus()

            self.active_row = new_row
            self.active_col = new_col
            self.active_text_item = self.grid_texts[new_row][new_col]
            self.active_text_item.setFocus(Qt.MouseFocusReason)
            
            if self.active_rect:
                self.active_rect.setBrush(QBrush(QColor(255, 255, 255)))  # Reset previous square color
            self.active_rect = self.grid_rects[new_row][new_col]
            self.active_rect.setBrush(QBrush(QColor(0, 255, 0)))  # Highlight the active square
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = SizeInputApp()
    mainWin.show()  # Show the main window
    app.exec_()     # Start the event loop
