import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

class EditableTextItem(QGraphicsTextItem):
    textChanged = pyqtSignal(str, int, int)  # Custom signal to track text changes and grid coordinates

    def keyPressEvent(self, event):
        # Emit the custom signal when text changes
        super().keyPressEvent(event)
        self.textChanged.emit(self.toPlainText(), int(self.pos().x() / self.boundingRect().width()), int(self.pos().y() / self.boundingRect().height()))

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

    def create_grid(self):
        # Retrieve user input and store it in the "size" variable
        try:
            self.size = int(self.entry.text())
            self.submit_button.hide()
            self.label.hide()
            self.entry.hide()
            self.initialize_grid()
            self.draw_grid()
        except ValueError:
            self.label.setText("Invalid input. Please enter a valid number.")

    def initialize_grid(self):
        # Initialize the grid data with empty strings
        self.grid_data = [["" for _ in range(self.size)] for _ in range(self.size)]

    def draw_grid(self):
        if self.size is not None:
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
                    print(f"{str(i)}, {str(i)}")

                    # Connect the text item's textChanged signal
                    text_item.textChanged.connect(lambda text, i=i, j=j: self.on_text_changed(text, i, j))

    def on_text_changed(self, text, i, j):
        # Update the grid data when the user enters text
        if 0 <= i < self.size and 0 <= j < self.size:
            print(f"{str(i)}, {str(j)}")
            self.grid_data[j][i] = text

            # Print the grid data (list of lists) to the console
            for row in self.grid_data:
                print(row)

            # Check if the entered text is a period ('.') and draw a black square if it is
            if text == '.':
                self.draw_black_square(i, j)

    def draw_black_square(self, i, j):
        # Draw a black square in the specified grid cell
        if 0 <= i < self.size and 0 <= j < self.size:
            square_size = min(self.width(), self.height()) / self.size
            brush = QBrush(QColor(0, 0, 0))  # Black brush
            rect_item = QGraphicsRectItem(QRectF(i * square_size, j * square_size, square_size, square_size))
            rect_item.setBrush(brush)
            self.scene.addItem(rect_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = SizeInputApp()
    mainWin.show()
    app.exec_()
