import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QFile
import sweetviz as sv
import pandas as pd
from sklearn.model_selection import train_test_split
import lazypredict
from lazypredict.Supervised import LazyClassifier
from lazypredict.Supervised import LazyRegressor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('InisghtBoost')
        self.setGeometry(100, 100, 800, 600)

        # Load stylesheet
        stylesheet = QFile("styles.qss")
        stylesheet.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(str(stylesheet.readAll(), encoding='utf-8'))

        # Create the stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create three pages and add them to the stacked widget
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)

        # Page 1 layout and widgets
        self.page1_layout = QVBoxLayout()
        self.page1_label = QLabel('Home Page')
        self.page2_button = QPushButton('EDA')
        self.page2_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.page3_button = QPushButton('AutoML')
        self.page3_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.page1_layout.addWidget(self.page1_label)
        self.page1_layout.addWidget(self.page2_button)
        self.page1_layout.addWidget(self.page3_button)
        self.page1.setLayout(self.page1_layout)

        # Page 2 layout and widgets
        #display the loading bar of sweetviz as it runs its report#
        self.page2_layout = QVBoxLayout()
        self.page2_label = QLabel('EDA')
        self.back_button = QPushButton('Go Back to Home')
        self.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.file_button = QPushButton('Upload File')
        self.file_button.clicked.connect(self.open_file_dialog)
        self.page2_layout.addWidget(self.page2_label)
        self.page2_layout.addWidget(self.file_button)
        self.page2_layout.addWidget(self.back_button)
        self.page2.setLayout(self.page2_layout)

        # Page 3 layout and widgets
        self.page3_layout = QVBoxLayout()
        self.page3_label = QLabel('AutoML')
        self.input_label = QLabel('Enter feature:')
        self.feature_input = QLineEdit()
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_feature)
        self.result_label = QLabel('')
        self.back_button = QPushButton('Go Back to Home')
        self.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.file_button = QPushButton('Upload File')
        self.file_button.clicked.connect(self.open_file_dialog_ML)
        self.page3_layout.addWidget(self.page3_label)
        self.page3_layout.addWidget(self.file_button)
        self.page3_layout.addWidget(self.input_label)
        self.page3_layout.addWidget(self.feature_input)
        self.page3_layout.addWidget(self.save_button)
        self.page3_layout.addWidget(self.result_label)
        self.page3_layout.addWidget(self.back_button)
        self.page3.setLayout(self.page3_layout)
    
    def save_feature(self):
        self.feature = self.feature_input.text()
        self.result_label.setText(f'Feature saved: {self.feature}')
        
    def save_text_input(self):
        self.feature = self.text_input.text()
        print(self.feature)

        # Add text input
        self.text_input = QLineEdit()
        self.page3_layout.addWidget(self.text_input)

        # Add save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_text_input)
        self.page3_layout.addWidget(self.save_button)

        # Add other widgets to layout
        self.page3_layout.addWidget(self.page3_label)
        self.page3_layout.addWidget(self.back_button)
        self.page3.setLayout(self.page3_layout)
        
    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;CSV Files (*.csv)", options=options)
        if file_name:
            df = pd.read_csv(file_name)
            report = sv.analyze([df, file_name])
            report.show_html()
    
          
#########################################################################################################################################################################
            
    def open_file_dialog_ML(self):
        self.feature = self.feature_input.text()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;CSV Files (*.csv)", options=options)
        if file_name:
            df = pd.read_csv(file_name)
        X = df.loc[:, df.columns != self.feature]
        Y = df[self.feature]
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        multiple_ML_model = LazyRegressor(verbose=0, ignore_warnings=True, predictions=True)
        models, predictions = multiple_ML_model.fit(X_train, X_test, y_train, y_test)
        predictions_df = pd.DataFrame(predictions)
        models_df = pd.DataFrame(models)
        print(models_df)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())