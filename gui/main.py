import sys
import os
sys.path.append(r'C:\Users\psatt\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QRunnable, QThreadPool, QObject
from copy import deepcopy


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from Crossword_Generator import Generate


square_size = []

class GenerateStopException(Exception):
    pass

class EditableTextItem(QGraphicsTextItem):
    textChanged = pyqtSignal(str, int, int)  # Custom signal to track text changes and grid coordinates
    clicked = pyqtSignal(int, int)  # Custom signal to track click events
     
    def keyPressEvent(self, event):
        # Emit the custom signal when text changes
        super().keyPressEvent(event)
        self.textChanged.emit(self.toPlainText(), int(self.pos().x() / self.boundingRect().width()), int(self.pos().y() / self.boundingRect().height()))

    def mousePressEvent(self, event):
        self.clicked.emit(int(self.pos().x() / self.boundingRect().width()), int(self.pos().y() / self.boundingRect().height()))

'''
class ClickableRectItem(QGraphicsRectItem):
    clicked = pyqtSignal(int, int)

    def __init__(self, x, y, size):
        super().__init__(QRectF(x, y, size, size))
        self.setPen(QPen(Qt.black))
        self.setBrush(QBrush(QColor(255, 255, 255)))  # White brush
        self.size = size

    def mousePressEvent(self, event):
        self.clicked.emit(
            int(self.pos().x() / self.size),
            int(self.pos().y() / self.size),
        )
'''
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
        self.active_text_tem = None
        
        # Create the "Run" button
        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("background-color: white")
        self.run_button.clicked.connect(self.run_crossword_generator)
        layout.addWidget(self.run_button)

        # Create the "Stop" button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: white")
        #self.stop_button.clicked.connect(self.stop_crossword_generator)
        layout.addWidget(self.stop_button)

        self.active_square = [0,0]
        self.installEventFilter(self)
    '''
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            self.handle_arrow_key(event.key())
        else:
            super().keyPressEvent(event)
   
    def eventFilter(self, source, event):
        if source == self:
            if event.type() == QEvent.KeyPress:
                key = event.key()

                if key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
                    self.handle_arrow_key(key)
                    return True  # Event is handled

        return super().eventFilter(source, event)
    '''

    def handle_arrow_key(self, key):
        i, j = self.active_square

        if key == Qt.Key_Up and j > 0:
            j -= 1
        elif key == Qt.Key_Down and j < self.size - 1:
            j += 1
        elif key == Qt.Key_Left and i > 0:
            i -= 1
        elif key == Qt.Key_Right and i < self.size - 1:
            i += 1
        self.update_active(i, j)

        
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
        self.text_items = [[EditableTextItem() for _ in range(self.size)] for _ in range(self.size)]
        self.active_text_item = self.text_items[0][0]
        
    def create_text_changed_handler(self, i, j):
        def handler(text):
            self.on_text_changed(text)
        return handler
    
    def create_text_clicked_handler(self, i, j):
        def handler():
            self.update_active(i,j)
        return handler

    def create_rect_clicked_handler(self, i, j):
        def handler():
            print("hi")
            #self.update_active(i,j)
        return handler
    
    def update_active(self, i, j):
        if self.grid_data[self.active_square[0]][self.active_square[1]] != ".":
            self.draw_white_square(self.active_square[0], self.active_square[1])
        self.active_square = [i, j]  # Update active_square when text box is clicked
        self.active_text_item = self.text_items[i][j]  # Update active_text_item when a text box is clicked
        self.color_active_square(i,j)
        print(self.active_square)
            
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
                    x = j * square_size
                    y = i * square_size

                    rect_item = QGraphicsRectItem(QRectF(x, y, square_size, square_size))
                    #rect_item = ClickableRectItem(x, y, square_size)
                    rect_item.setPen(pen)
                    rect_item.setBrush(brush)
                    self.scene.addItem(rect_item)
                    self.grid_rects[i][j] = rect_item

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

                    text_item.clicked.connect(self.create_text_clicked_handler(i, j))  # Connect the clicked signal
                    #rect_item.clicked.connect(self.create_rect_clicked_handler(i, j))
    
    
    def create_rect_clicked_handler(self, i, j):
        def handler():
            print("hi")
            #self.update_active(i, j)
        return handler
    
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

        seed = [0, 0]

        Generate(xw, seed)
        #self.run_button.setEnabled(False)
        #worker = GenerateWorker(xw, seed)
        #worker.signals.finished.connect(self.generate_finished)
        #self.threadpool.start(worker)

    def generate_finished(self):
        self.run_button.setEnabled(True)
    
    #def stop_crossword_generator(self):
    #    raise GenerateStopException
    
    
    def on_text_changed(self, text):
        # Update the grid data when the user enters text

        i = self.active_square[0]
        j = self.active_square[1]
        
        print(f"{str(i)}, {str(j)}\n")
        if 0 <= i < self.size and 0 <= j < self.size:
            
            self.grid_data[i][j] = text

            # Print the grid data (list of lists) to the console
            for row in self.grid_data:
                print(row)

            # Check if the entered text is a period ('.') and draw a black square if it is
            if text == '.':
                self.draw_black_square(i, j)
            elif text.isalpha() or text == '':
                self.draw_white_square(i, j)
               
           
    def color_active_square(self, i, j):
        global square_size
        if 0 <= i < self.size and 0 <= j < self.size:
            brush = QBrush(QColor(0, 0, 255, 100))  # Transparent blue brush (R,G,B,A)
            rect_item = self.grid_rects[i][j]
            rect_item.setBrush(brush)
            self.scene.addItem(rect_item)

        
    def draw_black_square(self, i, j):
        # Draw a black square in the specified grid cell
        global square_size
        if 0 <= i < self.size and 0 <= j < self.size:
        #    square_size = min(self.width(), self.height()) / self.size
            brush = QBrush(QColor(0, 0, 0))  # Black brush
            rect_item = self.grid_rects[i][j]
            #QGraphicsRectItem(QRectF(i * square_size, j * square_size, square_size, square_size))
            rect_item.setBrush(brush)
            self.scene.addItem(rect_item)

    def draw_white_square(self, i, j):
        # Draw a white square in the specified grid cell
        global square_size
        if 0 <= i < self.size and 0 <= j < self.size:
        #    square_size = min(self.width(), self.height()) / self.size
            brush = QBrush(Qt.NoBrush)  # No brush
            rect_item = self.grid_rects[i][j]
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
    
