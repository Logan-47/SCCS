#!/usr/bin/python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import sqlite3

try:
    connection = sqlite3.connect('db.sqlite')
except Error as e:
    print(e)

cursor = connection.cursor()
sql = "SELECT * FROM software"
cursor.execute(sql)
data = cursor.fetchall()
# print(data)

class WindowMain():

    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.builder.connect_signals(self)
        self.builder.connect_signals(self)

        #main_window
        self.mainWindow = self.builder.get_object('MainWindow')
        self.mainWindow.show_all()

        # dialog box
        self.dialog = self.builder.get_object('dialog')
        self.response = self.dialog.run()
        self.dialog.hide()

        self.data_list_store = Gtk.ListStore(int,str, str,str,str)
        for item in data:
            
            # print(item)
            self.data_list_store.append(list(item))

        self.data_tree_view = self.builder.get_object('data_tree_view')
        self.data_tree_view.set_model(self.data_list_store)
        # print(self.data_tree_view)
        for i,col_title in enumerate(['id','Name','Type','Category','Description']):

            # Render means how to draw data
            renderer = Gtk.CellRendererText()
            
            # create columns (text is column number)
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            
            #make Column Sortable
            column.set_sort_column_id(i)
            
            # add column to treeview
            self.data_tree_view.append_column(column)
        
        self.editMainType = self.builder.get_object('editMainType').hide()
        self.editCategory = self.builder.get_object('editCategory').hide()
        self.editSoftwareDescription = self.builder.get_object('editSoftwareDescription').hide()
        self.editlable = self.builder.get_object('editlable').hide()

        self.removeMainType = self.builder.get_object('removeMainType').hide()
        self.removeCategory = self.builder.get_object('removeCategory').hide()
        self.removeSoftwareDescription = self.builder.get_object('removeSoftwareDescription').hide()
        self.removelable = self.builder.get_object('removelable').hide()

    def resolve(self):
        self.editMainType = self.builder.get_object('editMainType').hide()
        self.editCategory = self.builder.get_object('editCategory').hide()
        self.editSoftwareDescription = self.builder.get_object('editSoftwareDescription').hide()
        self.editlable = self.builder.get_object('editlable').hide()

        self.removeMainType = self.builder.get_object('removeMainType').hide()
        self.removeCategory = self.builder.get_object('removeCategory').hide()
        self.removeSoftwareDescription = self.builder.get_object('removeSoftwareDescription').hide()
        self.removelable = self.builder.get_object('removelable').hide()
    
    def refreshed(self):
        # print('called')
        # print(self.data_list_store)
        self.data_list_store.clear()

    def on_Search_Clicked(self, data=None):
        self.searchEntry = self.builder.get_object('search_entry')
        search_term = self.searchEntry.get_text()

        self.refreshed()
        sql = f"SELECT * FROM software WHERE name LIKE '%{search_term}%'"
        cursor.execute(sql)
        data = cursor.fetchall()

        for item in data:
            self.data_list_store.append(list(item))
        

        # self.data_tree_view = self.builder.get_object('data_tree_view')
        self.data_tree_view.set_model(self.data_list_store)

    
    def on_Sort_By_Name_Clicked(self,data=None):
        self.refreshed()
        sql = "SELECT * FROM software ORDER BY name ASC"
        cursor.execute(sql)
        data = cursor.fetchall()

        for item in data:
            self.data_list_store.append(list(item))
        

        # self.data_tree_view = self.builder.get_object('data_tree_view')
        self.data_tree_view.set_model(self.data_list_store)

    def on_Sort_By_Main_Type_Clicked(self,data=None):
        self.refreshed()
        sql = "SELECT * FROM software ORDER BY typemain ASC"
        cursor.execute(sql)
        data = cursor.fetchall()

        for item in data:
            self.data_list_store.append(list(item))
        

        # self.data_tree_view = self.builder.get_object('data_tree_view')
        self.data_tree_view.set_model(self.data_list_store)

    def on_refresh_clicked(self, data=None):
        self.refreshed()
        sql = "SELECT * FROM software"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        for item in data:
            self.data_list_store.append(list(item))
        

        # self.data_tree_view = self.builder.get_object('data_tree_view')
        self.data_tree_view.set_model(self.data_list_store)

    

    def on_name_combo_changed(self,addMainType):
        self.store = Gtk.ListStore(str)
        self.store.clear()
        self.checkMainType = self.builder.get_object('addMainType')
        self.categoryBox = self.builder.get_object('categoryComboBox')
        
        if self.checkMainType.get_text() == "Application Software":
            self.store.append(['Operating System'])
            self.store.append(['Device Driver'])
            self.store.append(['Firmware'])
            self.store.append(['Translator'])
            self.store.append(['Utility'])
        else:
            self.store.append(['Types Of SystemSoftware'])
        
        self.categoryBox.set_model(self.store)
        

    def on_about_button_clicked(self, widget, data=None):
        # pop About Dialog
        self.aboutDialog = self.builder.get_object("aboutDialog")
        self.response = self.aboutDialog.run()
        self.aboutDialog.hide()

    def on_add_clicked(self, widget, data=None):
        # pop Add Dialog
        self.addDialog = self.builder.get_object('addDialog')
        self.response = self.addDialog.run()

    def on_tree_selected(self, data=None):
        print("called")
        tree_sel = self.data_tree_view.get_selection()
        (tm, ti) = tree_sel.get_selected()
        print(tm.get_value(ti, 0))
    
    def on_dialog_add_clicked(self,widget,data=None):
        
        # Add Data to Database
        self.addName = self.builder.get_object('addName')
        self.addMainType = self.builder.get_object('addMainType')
        self.addSoftwareDescription = self.builder.get_object('addSoftwareDescription')
        self.categoryBox = self.builder.get_object('addCategoryType')

        buffer = self.addSoftwareDescription.get_buffer()
        
        start,end = buffer.get_bounds()
        
        self.name = self.addName.get_text()
        # print(self.name)
        self.description = buffer.get_text(start,end,False)
        self.MainType = self.addMainType.get_text()
        self.category = self.categoryBox.get_text()
        
        # Add Sql Query to send Data to Database
        sql = f"SELECT * FROM software WHERE name='{self.name}'"
        cursor.execute(sql)
        data = cursor.fetchall()

        if not data:
            sqlQuery = f"INSERT INTO software(name,typemain,category,description) VALUES('{self.name}','{self.MainType}','{self.category}','{self.description}')"
            print(sqlQuery)
            cursor.execute(sqlQuery)
            connection.commit()
            self.addDialog.hide()
        else:
            print(data)
            self.addName.set_text("software name is already taken")
            

    def on_dialog_remove_clicked(self,widget,data=None):
        # remove Dialog window
        self.addDialog.hide()

    def on_remove_clicked(self, widget, data=None):
        # delete data from database
        # print("you clicked remove button")
        self.removeDialog = self.builder.get_object('removeDialog')
        self.response = self.removeDialog.run()

    def on_edit_clicked(self, widget, data=None):
        # edit data
        self.editDialog = self.builder.get_object('editDialog')
        self.response = self.editDialog.run()
        # print("you clicked edit button")

    def on_edit_dialog_remove_clicked(self,widget,data=None):
        # remove Dialog window
        self.resolve()
        self.editDialog.hide()

    def on_edit_dialog_enter_clicked(self, widget, data=None):
        self.editName = self.builder.get_object('editName')
        self.checkName = self.editName.get_text()
        sql = f"SELECT * FROM software WHERE name='{self.editName.get_text()}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            self.editName.set_text('no software FOund')
        else:  
            data = list(data)
            # print(data)
            self.resultId = data[0][0]
            resultName = data[0][1]
            resultMainType = data[0][2]
            resultCategory = data[0][3]
            resultDescription = data[0][4]
            self.editMainType = self.builder.get_object('editMainType')
            self.editCategory = self.builder.get_object('editCategory')
            self.editSoftwareDescription = self.builder.get_object('editSoftwareDescription')
            self.editlable = self.builder.get_object('editlable')

            self.editMainType.show()
            self.editCategory.show()
            self.editSoftwareDescription.show()
            self.editlable.show()

            self.editMainType.set_text(resultMainType)
            self.editCategory.set_text(resultCategory)
            buffer = self.editSoftwareDescription.get_buffer()
            buffer.set_text(resultDescription)

    def on_edit_update_clicked(self, widget, data=None):
        # Add Data to Database
        self.editName = self.builder.get_object('editName')
        self.editMainType = self.builder.get_object('editMainType')
        self.editSoftwareDescription = self.builder.get_object('editSoftwareDescription')
        self.editcategory = self.builder.get_object('addCategory')

        buffer = self.editSoftwareDescription.get_buffer()
        
        start,end = buffer.get_bounds()
        
        self.name = self.editName.get_text()
        # print(self.name)
        self.description = buffer.get_text(start,end,False)
        self.MainType = self.editMainType.get_text()
        self.category = self.editCategory.get_text()
        
        # Add Sql Query to send Data to Database
        if self.name != self.checkName: 
            sql = f"SELECT * FROM software WHERE name='{self.name}'"
            cursor.execute(sql)
            data = cursor.fetchall()
        # else:
            

        if not data:
            sqlQuery = f"UPDATE software SET name='{self.name}',typemain='{self.MainType}',category='{self.category}',description='{self.description}' WHERE id='{self.resultId}'"
            print(sqlQuery)
            cursor.execute(sqlQuery)
            connection.commit()
            self.editDialog.hide()
        else:
            print(data)
            self.editName.set_text("software name is already taken")


    def on_mainwindow_destroy(self, widget, data=None):
        # main Window Destroyer
        Gtk.main_quit()

    def on_remove_dialog_cancel_clicked(self, widget, data=None):
        self.resolve()
        self.removeDialog.hide()

    def on_remove_dialog_enter_clicked(self, widget, data=None):
        self.removeName = self.builder.get_object('removeName')
        sql = f"SELECT * FROM software WHERE name='{self.removeName.get_text()}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            self.removeName.set_text('no software found')
        else: 
            data = list(data)
            # print(data)
            resultName = data[0][1]
            resultMainType = data[0][2]
            resultCategory = data[0][3]
            resultDescription = data[0][4]
            self.removeMainType = self.builder.get_object('removeMainType')
            self.removeCategory = self.builder.get_object('removeCategory')
            self.removeSoftwareDescription = self.builder.get_object('removeSoftwareDescription')
            self.removelable = self.builder.get_object('removelable')

            self.removeMainType.show()
            self.removeCategory.show()
            self.removeSoftwareDescription.show()
            self.removelable.show()

            self.removeMainType.set_text(resultMainType)
            self.removeCategory.set_text(resultCategory)
            buffer = self.removeSoftwareDescription.get_buffer()
            buffer.set_text(resultDescription)

    def on_about_dialog_activate(self, widget, data=None):
        # pop about dialog window
        self.aboutDialog = self.builder.get_object('aboutDialog')
        self.aboutDialog.run()
        self.aboutDialog.hide()

    def on_delete_clicked(self, widget, data=None):
        print("clicked deleted")
        self.name = self.builder.get_object('removeName')
        sql = f"select * from software where name='{self.name.get_text()}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            self.name.set_text('no software found')
        else:
            sql = f"DELETE FROM software WHERE name='{self.name.get_text()}'"
            print(sql)
            cursor.execute(sql)

            connection.commit()
            self.removeDialog.hide()



    def on_quit_clicked(self, widget, data=None):
        # quits Main Window
        self.mainWindow.destroy()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    window = WindowMain()
    window.main()
