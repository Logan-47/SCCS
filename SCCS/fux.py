#!/usr/bin/python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import sqlite3

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
sql = "SELECT * FROM users"
cursor.execute(sql)
data = cursor.fetchall()
# print(data)

class WindowMain():

    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.builder.connect_signals(self)
        self.builder.connect_signals(self)

        self.mainWindow = self.builder.get_object('MainWindow')
        self.mainWindow.show_all()


        self.dialog = self.builder.get_object('dialog')
        self.response = self.dialog.run()
        self.dialog.hide()

        self.data_list_store = Gtk.ListStore(str,str, str)
        for item in data:
            # print(item)
            self.data_list_store.append(list(item))

        self.data_tree_view = self.builder.get_object('data_tree_view')
        self.data_tree_view.set_model(self.data_list_store)
        # print(self.data_tree_view)
        for i,col_title in enumerate(['Name','Age','Profession']):

            # Render means how to draw data
            renderer = Gtk.CellRendererText()
            # create columns (text is column number)
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            #make Column Sortable
            column.set_sort_column_id(i)
            # add column to treeview
            self.data_tree_view.append_column(column)

    def on_about_button_clicked(self, widget, data=None):
        # pop About Dialog
        self.aboutDialog = self.builder.get_object("aboutDialog")
        self.response = self.aboutDialog.run()
        self.aboutDialog.hide()

    def on_add_clicked(self, widget, data=None):
        # pop Add Dialog
        self.addDialog = self.builder.get_object('addDialog')
        self.response = self.addDialog.run()


    def on_dialog_add_clicked(self,widget,data=None):
        # Add Data to Database
        self.addName = self.builder.get_object('addName')
        self.addAge = self.builder.get_object('addAge')
        self.addProfession = self.builder.get_object('addProfession')
        self.name = self.addName.get_text()
        self.age = self.addAge.get_text()
        self.profession = self.addProfession.get_text()
        print(f"Name: {self.name} \nAge: {self.age} \nProfession: {self.profession}\n")
        # Add Sql Query to send Data to Database
        self.addDialog.hide()

    def on_dialog_remove_clicked(self,widget,data=None):
        # remove Dialog window
        self.addDialog.hide()

    def on_remove_clicked(self, widget, data=None):
        # delete data from database
        print("you clicked remove button")

    def on_edit_clicked(self, widget, data=None):
        # edit data
        print("you clicked edit button")

    def on_mainwindow_destroy(self, widget, data=None):
        # main Window Destroyer
        Gtk.main_quit()

    def on_about_dialog_activate(self, widget, data=None):
        # pop about dialog window
        self.aboutDialog = self.builder.get_object('aboutDialog')
        self.aboutDialog.run()
        self.aboutDialog.hide()

    def on_quit_clicked(self, widget, data=None):
        # quits Main Window
        self.mainWindow.destroy()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    window = WindowMain()
    window.main()
