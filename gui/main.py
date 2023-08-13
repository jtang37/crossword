import sys
import os
sys.path.append(r'C:\Users\psatt\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QRunnable, QThreadPool, QObject
from copy import deepcopy
import threading

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from Crossword_Generator import Generate
from Crossword_Generator import stop_generate

square_size = []

class GenerateStopException(Exception):
    pass

class EditableTextItem(QGraphicsTextItem):
    textChanged = pyqtSignal(str, int, int)  # Custom signal to track text changes and grid coordinates

    def keyPressEvent(self, event):
        # Emit the custom signal when text changes
        super().keyPressEvent(event)
        self.textChanged.emit(self.toPlainText(), int(self.pos().x() / self.boundingRect().width()), int(self.pos().y() / self.boundingRect().height()))

class GenerateWorker(QRunnable):
    def __init__(self, xw, seed):
        super().__init__()
        self.xw = xw
        self.seed = seed
        self.generator = Generate(xw, seed)

    def run(self):
        #try:
        self.generator.generate()
        #except GenerateStopException as e:
            #print(e)

class SizeInputApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Square Grid App")
        self.setGeometry(100, 100, 600, 600)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

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

        # Initialize size variable and grid data
        self.size = None
        self.grid_data = None
        self.grid_rects = None

        # Create the "Run" button
        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("background-color: white")
        self.run_button.clicked.connect(self.run_crossword_generator)
        layout.addWidget(self.run_button)

        # Create the "Stop" button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: white")
        self.stop_button.clicked.connect(self.stop_crossword_generator)
        layout.addWidget(self.stop_button)

        self.threadpool = QThreadPool()
        
    def create_grid(self):
        # Retrieve user input and store it in the "size" variable
        try:
            self.size = int(self.entry.text())
            #self.submit_button.hide()
            #self.label.hide()
            #self.entry.hide()
            self.initialize_grid()
            self.draw_grid()
        except ValueError:
            self.label.setText("Invalid input. Please enter a valid number.")

    def initialize_grid(self):
        # Initialize the grid data with empty strings
        self.grid_data = [["" for _ in range(self.size)] for _ in range(self.size)]
        self.grid_rects = [[QGraphicsRectItem() for _ in range(self.size)] for _ in range(self.size)]

    def create_text_changed_handler(self, i, j):
        def handler(text):
            self.on_text_changed(text, i, j)
        return handler

    def draw_grid(self):
        if self.size is not None:
            global square_size
            square_size = min(self.width(), self.height()) / self.size
            pen = QPen(Qt.black)
            brush = QBrush(QColor(255, 255, 255))  # White brush
            font = QFont("Arial", int(square_size * 0.4))

            self.scene.clear()
            

            for i in range(self.size):
                for j in range(self.size):
                    x = i * square_size
                    y = j * square_size

                    rect_item = QGraphicsRectItem(QRectF(x, y, square_size, square_size))
                    rect_item.setPen(pen)
                    rect_item.setBrush(brush)
                    self.scene.addItem(rect_item)
                    self.grid_rects[j][i] = rect_item

                    # Create an editable text item for each square
                    text_item = EditableTextItem("", rect_item)
                    text_item.setDefaultTextColor(Qt.black)
                    text_item.setFont(font)
                    text_item.setTextWidth(square_size)
                    text_item.setTextInteractionFlags(Qt.TextEditorInteraction)  # Allow editing

                    # Adjust the positioning to place text within the grid cell
                    # Center the text within the cell
                    text_item.setPos(x + (square_size - text_item.boundingRect().width()) / 2,
                                     y + (square_size - text_item.boundingRect().height()) / 2)

                    # Connect the text item's textChanged signal
                    text_item.textChanged.connect(self.create_text_changed_handler(i, j))

    
    
    def run_crossword_generator(self):
        xw = deepcopy(self.grid_data)
        for i in range(self.size):
            for j in range(self.size):
                if xw[i][j].isalpha() and xw[i][j].islower():
                    xw[i][j] = xw[i][j].upper()
                if xw[i][j] == '':
                    xw[i][j] = ' '
                elif xw[i][j] == '.':
                    xw[i][j] = '■'

        seed = [14, 12]

        Generate(xw, seed)
        #self.run_button.setEnabled(False)
        #worker = GenerateWorker(xw, seed)
        #worker.signals.finished.connect(self.generate_finished)
        #self.threadpool.start(worker)

    def generate_finished(self):
        self.run_button.setEnabled(True)
    
    def stop_crossword_generator(self):
        raise GenerateStopException

    def on_text_changed(self, text, i, j):
        # Update the grid data when the user enters text
        print(f"{str(j)}, {str(i)}\n")
        if 0 <= i < self.size and 0 <= j < self.size:
            
            self.grid_data[j][i] = text

            # Print the grid data (list of lists) to the console
            for row in self.grid_data:
                print(row)

            # Check if the entered text is a period ('.') and draw a black square if it is
            if text == '.':
                self.draw_black_square(i, j)
            elif text.isalpha() or text == '':
                self.draw_white_square(i, j)
                
           

    def draw_black_square(self, i, j):
        # Draw a black square in the specified grid cell
        global square_size
        if 0 <= i < self.size and 0 <= j < self.size:
        #    square_size = min(self.width(), self.height()) / self.size
            brush = QBrush(QColor(0, 0, 0))  # Black brush
            rect_item = self.grid_rects[j][i]
            #QGraphicsRectItem(QRectF(i * square_size, j * square_size, square_size, square_size))
            rect_item.setBrush(brush)
            self.scene.addItem(rect_item)

    def draw_white_square(self, i, j):
        # Draw a black square in the specified grid cell
        global square_size
        if 0 <= i < self.size and 0 <= j < self.size:
        #    square_size = min(self.width(), self.height()) / self.size
            brush = QBrush(Qt.NoBrush)  # No brush
            rect_item = self.grid_rects[j][i]
            #QGraphicsRectItem(QRectF(i * square_size, j * square_size, square_size, square_size))
            rect_item.setBrush(brush)
            self.scene.addItem(rect_item)

    '''def draw_white_square(self, i, j):
    # Draw a white square in the specified grid cell
        if 0 <= i < self.size and 0 <= j < self.size:
            items = self.scene.items(QRectF(i * square_size, j * square_size, square_size, square_size))
        for item in items:
            if isinstance(item, QGraphicsRectItem):
                brush = QBrush(Qt.NoBrush)  # No fill
                item.setBrush(brush)
                break'''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = SizeInputApp()
    mainWin.show()  # Show the main window
    app.exec_()     # Start the event loop
    
