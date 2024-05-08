from PyQt6.QtWidgets import *
from VotingAppQT import *
import csv
import darkdetect


class Logic(QMainWindow, Ui_VotingApp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__Seb_vote = 0
        self.__Beau_vote = 0

        self.Submit_Vote.clicked.connect(lambda: self.submit())
        self.Results.clicked.connect(lambda: self.results())
        self.Results.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def submit(self) -> None:
        """
        This function makes the submits the ID and vote chosen and clears after submit has been chosen.
        """
        self.theme()
        try:
            ID = int(self.ID_Enter.text())
            Voted = False
            with open('votes.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    if str(ID) in line:
                        self.Vote_Status.setStyleSheet('color: Red')
                        self.Vote_Status.setText('You already voted')
                        Voted = True
            Vote = -1
            if self.Vote_Seb.isChecked():
                Vote = 'Sebastian'
            elif self.Vote_Beau.isChecked():
                Vote = 'Beau'
            elif Vote == -1:
                self.theme()
                self.Vote_Status.setText('You didn\'t vote')
            if Voted == False and Vote != -1:
                with open('votes.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    voter_info = [ID, Vote]
                    csv_writer.writerow(voter_info)
                self.Vote_Status.setText('Submitted Vote')
                self.Vote_Status.setStyleSheet('color: Green')
                self.clear()
        except ValueError:
            self.Vote_Status.setText('Not a valid Voter ID')

    def clear(self) -> None:
        """
        The function clears all inputs when submit button is clicked
        """
        self.ID_Enter.clear()
        if self.Vote_Seb.isChecked():
            self.Vote_Seb.setAutoExclusive(False)
            self.Vote_Seb.setChecked(False)
            self.Vote_Seb.setAutoExclusive(True)
        else:
            self.Vote_Beau.setAutoExclusive(False)
            self.Vote_Beau.setChecked(False)
            self.Vote_Beau.setAutoExclusive(True)

    def theme(self) -> None:
        """
        Checks the theme of the computer screen and changes text color accordingly
        """
        if darkdetect.theme() == 'Dark':
            self.Vote_Status.setStyleSheet('color: White')
        if darkdetect.theme() == 'Light':
            self.Vote_Status.setStyleSheet('color: Black')

    def vote_count(self) -> None:
        """
        Counts the number of votes for each candidate
        """
        with open('votes.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[1] == 'Sebastian':
                    self.__Seb_vote += 1
                else:
                    self.__Beau_vote += 1

    def results(self) -> None:
        """
        Gets voting results and finds the winner
        """
        self.vote_count()
        if self.__Seb_vote > self.__Beau_vote:
            self.label.setText(f'Sebastian wins with {self.__Seb_vote} votes.')
        else:
            self.label.setText(f'Beau wins with {self.__Beau_vote} votes.')