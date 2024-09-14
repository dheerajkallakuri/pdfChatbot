import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QProgressBar, QFileDialog, QLabel, QHBoxLayout, QSplitter, QFrame, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QTextBlockFormat
from ragModel import get_pdf_content, get_conversation, get_response
from grammarCheck import get_grammarCheck

class PDFChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create main layout
        mainLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # PDF Section
        self.pdfLabel = QLabel("No PDF Uploaded")
        self.pdfLabel.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        self.uploadButton = QPushButton("Upload PDF")
        self.progressBar = QProgressBar()
        self.analyseButton = QPushButton("Analyse")

        self.uploadButton.clicked.connect(self.uploadPDF)
        self.analyseButton.clicked.connect(self.analysePDF)

        leftLayout.addWidget(self.pdfLabel)
        leftLayout.addWidget(self.uploadButton)
        leftLayout.addWidget(self.progressBar)
        leftLayout.addWidget(self.analyseButton)

        # Chatbot Section
        self.chatArea = QTextEdit()
        self.chatArea.setReadOnly(True)
        self.chatArea.setHtml("<html></html>")
        self.chatArea.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                padding: 5px;
            }
            QScrollBar:vertical {
                border: 1px solid #ddd;
                background: #f1f1f1;
                width: 2px;  /* Width of the scrollbar */
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: 1px solid #ddd;
                background: #f1f1f1;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: #f1f1f1;
            }
        """)

        self.userInput = QTextEdit()
        self.userInput.setFixedHeight(50)
        self.userInput.setStyleSheet("""
            border: 1px solid #ddd; 
            border-radius: 5px; 
            padding: 5px; 
            font-family: Arial, sans-serif;
        """)
        self.userInput.setPlaceholderText("Type a message...")

        self.sendButton = QPushButton("Send")
        self.sendButton.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            padding: 10px; 
            font-family: Arial, sans-serif;
        """)

        self.sendButton.clicked.connect(self.sendMessage)

        # Make chat area scrollable
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setWidget(self.chatArea)

        rightLayout.addWidget(self.scrollArea)
        rightLayout.addWidget(self.userInput)
        rightLayout.addWidget(self.sendButton)

        # Combine layouts
        splitter = QSplitter(Qt.Horizontal)
        leftFrame = QFrame()
        leftFrame.setLayout(leftLayout)
        rightFrame = QFrame()
        rightFrame.setLayout(rightLayout)
        
        splitter.addWidget(leftFrame)
        splitter.addWidget(rightFrame)
        mainLayout.addWidget(splitter)

        self.setLayout(mainLayout)
        self.setWindowTitle('PDF Chat Bot Interface')
        self.resize(800, 600)

    def uploadPDF(self):
        # Handle PDF upload
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            self.pdfFilePath = fileName  # Store the full file path
            self.pdfLabel.setText(f"{fileName.split('/')[-1]}")  # Only display the file name in the label

    def analysePDF(self):
        # Handle PDF analysis
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)

        # Check if a PDF file has been uploaded
        if not hasattr(self, 'pdfFilePath') or not self.pdfFilePath:
            self.show_message("No PDF Uploaded", "No PDF files are uploaded for analysis. Please upload a PDF first.")
            return

        # Get PDF content using the full file path
        pdf_content = get_pdf_content([self.pdfFilePath])
        self.progressBar.setValue(20)

        # Get conversation by processing the PDF content
        conversation = get_conversation(pdf_content)
        self.progressBar.setValue(70)

        # Store conversation for later use by chatbot
        self.conversation = conversation
        self.progressBar.setValue(100)

        # Notify user that analysis is complete
        self.addChatBotMessage("Analysis complete. The bot is ready to respond.")

    def sendMessage(self):
        # Handle sending message to the chat bot
        user_message = self.userInput.toPlainText()
        user_message = get_grammarCheck(user_message)
        if user_message:
            self.addUserMessage(user_message)
            # Simulate bot response
            if not hasattr(self, 'conversation'):
                self.addChatBotMessage("Please upload and analyze a PDF first.")
                return
            bot_response = get_response(self.conversation, user_message)
            self.addChatBotMessage(bot_response)
            self.userInput.clear()

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def addUserMessage(self, message):
        cursor = self.chatArea.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Set user message format
        user_format = QTextCharFormat()
        user_format.setForeground(QColor("white"))
        user_format.setFontWeight(QFont.Bold)

        # Set block format for right alignment
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignRight)
        
        cursor.insertBlock(block_format)
        cursor.insertText(f"{message}\n", user_format)
        cursor.movePosition(QTextCursor.End)
        
        self.chatArea.setTextCursor(cursor)
        # Scroll to the bottom of the chat area
        self.chatArea.verticalScrollBar().setValue(self.chatArea.verticalScrollBar().maximum())

    def addChatBotMessage(self, message):
        cursor = self.chatArea.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Set bot message format
        bot_format = QTextCharFormat()
        bot_format.setForeground(QColor("green"))
        bot_format.setFontWeight(QFont.Bold)

        # Set block format for left alignment
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignLeft)
        
        cursor.insertBlock(block_format)
        cursor.insertText(f"{message}\n", bot_format)
        cursor.movePosition(QTextCursor.End)
        
        self.chatArea.setTextCursor(cursor)
        # Scroll to the bottom of the chat area
        self.chatArea.verticalScrollBar().setValue(self.chatArea.verticalScrollBar().maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFChatBotApp()
    ex.show()
    sys.exit(app.exec_())
