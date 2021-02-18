import random
import os
import tkinter
from tkinter import messagebox
from selenium import webdriver
from time import sleep
from dotenv import load_dotenv

class Window(tkinter.Frame):

    def __init__(self,master):
        tkinter.Frame.__init__(self, master)
        self.master=master
        self.pack(fill=tkinter.BOTH, expand=1)
        
        self.pickMovie()

    def pickMovie(self):
        with open('movies.txt', 'r') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]
        movie = random.choice(lines)
        sleep(0.01)
        self.isItOkMovie(movie)

    def isItOkMovie(self, movie):
        self.movieText = tkinter.Label(self.master, text=movie)
        self.movieText.place(x=70, y=70)
        self.okButton = tkinter.Button(self.master, text="Lets watch!", command= lambda: self.openDownloadSite(movie))
        self.againButton = tkinter.Button(self.master, text="Spin again", command=self.removeWigets)
        self.okButton.pack()
        self.againButton.pack()

    def openDownloadSite(self, movie):
        driver = webdriver.Firefox(executable_path='geckodriver.exe')
        driver.get("https://www.linkomanija.net/")

        USER = os.getenv('M_USERNAME')
        PASS = os.getenv('M_PASSWORD')

        driver.find_element_by_xpath('//*[@id="username"]').send_keys(USER)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(PASS)
        driver.find_element_by_xpath('/html/body/div[2]/form/fieldset/div[3]/div[1]/input').click()

        driver.find_element_by_xpath('//*[@id="search"]').send_keys(movie)
        driver.find_element_by_xpath('//*[@id="searchsubmit"]').click()

        self.askToRemove(movie)
    
    def askToRemove(self, movie):
        msgbox = messagebox.askquestion('Remove Movie', 'Do you want to remove \"{}\" from the list?'.format(movie))
        if msgbox == 'yes':
            self.removeMovieFromFile(movie)

    def removeMovieFromFile(self, movie):
        with open('movies.txt', 'r') as f:
            lines = f.readlines()
        with open("movies.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != movie:
                    f.write(line)


    def removeWigets(self):
        self.movieText.destroy()
        self.okButton.destroy()
        self.againButton.destroy()
        self.pickMovie()


def main():
    load_dotenv()
    root=tkinter.Tk()
    Window(root)
    root.wm_title("Movie Picker")
    root.geometry("500x200")
    root.mainloop()

if __name__ == "__main__":
    main()