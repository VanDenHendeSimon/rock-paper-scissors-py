from PySide2 import QtWidgets, QtGui
import random
import sys
import os

# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QtWidgets.QApplication(sys.argv)


class RockPaperScissors(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # Define main layout of the application
        self.layout = QtWidgets.QVBoxLayout()

        # Horizontal layouts for players and scores
        self.names_layout = QtWidgets.QHBoxLayout()
        self.score_layout = QtWidgets.QHBoxLayout()

        self.player = 'Player'
        self.player_label = QtWidgets.QLabel(self.player)
        self.computer_label = QtWidgets.QLabel('Computer')

        self.player_score = QtWidgets.QLabel('0')
        self.computer_score = QtWidgets.QLabel('0')

        self.names_layout.addWidget(self.player_label)
        self.names_layout.addStretch(1)
        self.names_layout.addWidget(self.computer_label)

        self.score_layout.addWidget(self.player_score)
        self.score_layout.addStretch(1)
        self.score_layout.addWidget(self.computer_score)

        self.layout.addLayout(self.names_layout)
        self.layout.addLayout(self.score_layout)
        self.layout.addStretch(1)

        # Horizontal layout for images for both choices
        self.images = QtWidgets.QHBoxLayout()

        self.player_img = QtWidgets.QLabel()
        self.computer_img = QtWidgets.QLabel()

        self.player_img.setPixmap(QtGui.QPixmap('./images/01_rock.jpg').scaled(400, 400))
        self.computer_img.setPixmap(QtGui.QPixmap('./images/01_rock.jpg').scaled(400, 400))

        self.images.addWidget(self.player_img)
        self.images.addWidget(self.computer_img)

        self.layout.addLayout(self.images)

        # Game Stuff
        # Horizontal layout to store buttons for the choices
        self.button_layout = QtWidgets.QHBoxLayout()

        # Derive choices list from images folder rather than hard coding
        self.images = sorted(os.listdir('./images/'))
        self.choices = []
        for img in self.images:
            # Strip out image name from formatted file path
            img = img.split('_')[1]
            img = img.split('.jpg')[0]

            # Add image basename as a choice
            self.choices.append(img)

        # Set window title dynamically, driven by the list of choices
        self.setWindowTitle(', '.join(self.choices))

        # Create dict to store buttons, key = choice, value = button object
        self.buttons = {}
        for choice in self.choices:
            # create new button
            button = QtWidgets.QPushButton(choice)
            button.setCheckable(True)
            button.clicked.connect(self.clicked)

            # add new button to a dictionary
            self.buttons.update({choice: button})

            # add new button to the layout
            self.button_layout.addWidget(button)

        # Add buttons to the layout
        self.layout.addLayout(self.button_layout)

        # User feedback in the UI
        self.outcome = QtWidgets.QLabel('Make your choice to start the game')
        self.layout.addWidget(self.outcome)

        # Finalizing widget
        self.setLayout(self.layout)

    def compare(self, user_choice):
        """
        Randomly pick a choice from the list and compare it to the choice made by the user.
        Also set feedback labels, change images and update score based on the outcome

        :param user_choice: Label of the button clicked by the user
        """
        # Pick random choice
        computer_choice = self.choices[random.randint(0, len(self.choices)-1)]

        # Fetch indexes of both choices
        user_choice_index = int(self.choices.index(user_choice))
        computer_choice_index = int(self.choices.index(computer_choice))

        # Do the comparison
        if user_choice_index == computer_choice_index:
            # Tie
            outcome = '%s vs %s -> it\'s a tie!' % (user_choice, computer_choice)
        else:
            if (user_choice_index - 1) % len(self.choices) == computer_choice_index:
                # Player wins
                outcome = '%s beats %s, Player wins' % (user_choice, computer_choice)
                self.player_score.setText(str(int(self.player_score.text())+1))
            else:
                # Computer wins
                outcome = '%s beats %s, Computer wins' % (computer_choice, user_choice)
                self.computer_score.setText(str(int(self.computer_score.text()) + 1))

        # Set images
        player_img_path = './images/0%d_%s.jpg' % (user_choice_index+1, user_choice)
        computer_img_path = './images/0%d_%s.jpg' % (computer_choice_index+1, computer_choice)

        player_image = QtGui.QPixmap(player_img_path)
        computer_image = QtGui.QPixmap(computer_img_path)

        self.player_img.setPixmap(player_image.scaled(400, 400))
        self.computer_img.setPixmap(computer_image.scaled(400, 400))

        # Set outcome text
        self.outcome.setText(outcome)

    def clicked(self):
        """
        Run over all buttons created, which are stored in a dict (key = button's label, value = the button object)
        Log the user's choice and proceed comparing against the computer's choice
        """
        for button in self.buttons.keys():
            if self.buttons[button].isChecked():
                # Check vs computer
                self.compare(button)
                # Turn the button back off
                self.buttons[button].toggle()

    def run(self):
        """
        Runs the application and shows the window
        """
        # Show the window
        self.show()
        # Run the qt application
        qt_app.exec_()


game = RockPaperScissors()
game.run()

