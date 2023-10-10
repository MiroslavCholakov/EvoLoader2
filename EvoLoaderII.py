from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QCheckBox, QLabel, QTextEdit, QListWidget, QFileDialog, QMessageBox, QDialog, QHBoxLayout

from PyQt6.QtGui import QAction, QDesktopServices, QIcon
from PyQt6.QtCore import Qt, QUrl
import sys
import os
import re
import pyautogui
import keyboard
from dictionaries import MAX_TIER, ALL_CLASS_LIST, RECIPES

class EvoFileReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_width = 400
        self.original_height = 400
        self.dir_contents = {}
        self.selected_classes = []
        self.setWindowTitle("Evo File Reader")
        self.setGeometry(100, 100, 400, 400)
        self.VERSION = "v1.2"
        self.ICON = "load.ico" if os.path.isfile("load.ico") else ""
        self.wc3_path = ""
        self.custom_commands_loaded = False

        self.USER = os.getlogin()
        self.MAX_TIER = MAX_TIER
        self.ALL_CLASS_LIST = ALL_CLASS_LIST
        self.RECIPES = RECIPES
        self.DEFAULT_PATH = f"C:\\Users\\{self.USER}\\Documents\\Warcraft III"
        self.CHANGELOG_FILE_NAME = "changelog.txt"
        self.active_profile = ""
        self.profiles = []
        self.custom_path = ""
        self.selected_class = ""
        self.class_list = []
        self.selected_code = ""
        self.updating_information = False
        self.get_class_names()
        self.init_ui()
        self.load_warcraft3_path()

    def init_ui(self):
        self.setWindowTitle(f"Evo File Reader {self.VERSION}")
        if self.ICON:
           self.setWindowIcon(QIcon(self.ICON))
        self.setGeometry(100, 100, self.original_width, self.original_height)
        self.setup_menu_bar()
        self.setup_ui_elements()

    def setup_menu_bar(self):
        menubar = self.menuBar()
        self.create_config_menu(menubar)
        self.create_guides_menu(menubar)
        self.create_help_menu(menubar)

    def visit_website(self, website_url): #function that redirects the user to the given website (usually guides)
        try:
            QDesktopServices.openUrl(QUrl(website_url))
        except Exception as e:
             self.show_error_message("Error Opening Guide", f"Guide Unavailable: {str(e)}")
             

    def create_config_menu(self, menu_bar): #Creates the Configuration menu
        edit_menu = menu_bar.addMenu('Config')
        set_path_action = QAction('Set Warcraft3 path', self)
        set_path_action.triggered.connect(self.change_path)
        edit_menu.addAction(set_path_action)
        
        close_action = QAction('Close application', self)
        close_action.triggered.connect(self.close)
        edit_menu.addAction(close_action)
        
    def create_guides_menu(self, menu_bar): #Creates the reference to Guides from google drive
        links_menu = menu_bar.addMenu('Guides')
        
        website1_action = QAction('Item and Hero Overview', self)
        website1_action.triggered.connect(lambda: self.visit_website('https://docs.google.com/spreadsheets/d/14zNW97MHv36gPqpNYqmT9otvMl2QMwdtU1pQbqJu7y4/edit#gid=131284763'))
        links_menu.addAction(website1_action)

        website2_action = QAction('Imp1 and Imp2 Builds', self)
        website2_action.triggered.connect(lambda: self.visit_website('https://docs.google.com/spreadsheets/d/1Cs8I6MxSha8qqvd6Uhx12uGIdAZdE4Lt_sVSOD87_g8/edit#gid=1284668198'))
        links_menu.addAction(website2_action)
        
        website3_action = QAction('Imp3 Builds', self)
        website3_action.triggered.connect(lambda: self.visit_website('https://docs.google.com/spreadsheets/d/1yEQB5QBiDHKHVKtGY6Vj5HagTPjuQeRst1nR0dNI89s/edit#gid=1284668198'))
        links_menu.addAction(website3_action)

        website4_action = QAction('Quickcast Guide', self)
        website4_action.triggered.connect(lambda: self.visit_website('https://www.hiveworkshop.com/threads/custom-grid-hotkey-configuration-for-quick-cast.340352/'))
        links_menu.addAction(website4_action)
        
    def create_help_menu(self, menu_bar): #Adds the Godly Farm Check, changelog and about
        help_menu = menu_bar.addMenu('Help')
        godly_check_action = QAction('Godly Farm Check', self)
        godly_check_action.triggered.connect(self.display_godly_advancement)
        help_menu.addAction(godly_check_action)
        
        changelog_action = QAction('Changelog', self)
        changelog_action.triggered.connect(self.display_changelog)
        help_menu.addAction(changelog_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.display_about)
        help_menu.addAction(about_action)

    def setup_ui_elements(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Top layout for checkboxes, buttons, and combo box
        top_layout = QHBoxLayout()

        # Checkboxes
        self.checkbutton_max_level = QCheckBox('Max Level', self)
        self.checkbutton_max_level.stateChanged.connect(self.update_class_list)
        top_layout.addWidget(self.checkbutton_max_level)

        self.checkbutton_tier_4 = QCheckBox('Tier 4', self)
        self.checkbutton_tier_4.stateChanged.connect(self.update_class_list)
        top_layout.addWidget(self.checkbutton_tier_4)

        # Spacer to push buttons and combo box to the right
        top_layout.addStretch()

        # Label, ComboBox, and Buttons
        self.label = QLabel('Profile:', self)
        top_layout.addWidget(self.label)

        self.combo = QComboBox(self)
        self.combo.currentIndexChanged.connect(self.update_selected_profile)
        top_layout.addWidget(self.combo)

        self.button_refresh = QPushButton('Refresh', self)
        self.button_refresh.clicked.connect(self.refresh)
        top_layout.addWidget(self.button_refresh)

        self.button_load_code = QPushButton('Load code', self)
        self.button_load_code.clicked.connect(self.copy_code)
        top_layout.addWidget(self.button_load_code)

        main_layout.addLayout(top_layout)

        # Bottom layout for class listbox and textbox
        bottom_layout = QHBoxLayout()

        # Listbox
        self.listbox = QListWidget(self)
        self.listbox.currentRowChanged.connect(self.get_selected_list_item)
        bottom_layout.addWidget(self.listbox)

        # Textbox
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        bottom_layout.addWidget(self.textbox)

        main_layout.addLayout(bottom_layout)    


    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)


    def load_warcraft3_path(self):
        # Assuming that configuration.txt is in the same directory as the script
        try:
            config_file_name = 'configuration.txt'
            config_file_path = os.path.join(os.path.dirname(sys.argv[0]), config_file_name) if getattr(sys, 'frozen', False) else config_file_name
        
            if os.path.exists(config_file_path):
                with open(config_file_path, 'r') as file:
                    stored_path = file.readline().strip()

                    if os.path.exists(stored_path) and os.path.isdir(stored_path):
                        self.wc3_path = stored_path
                        self.update_gui()
                        return

        # Default path if configuration.txt doesn't exist or is invalid
            self.wc3_path = self.DEFAULT_PATH
        except Exception as e:
            QMessageBox.warning(self,"Error Loading Warcraft3 Path", f"An error occurred while loading the Warcraft3 path: {str(e)}")
        self.listbox.clear()
        self.update_gui()
        
    def save_warcraft3_path(self, path):
        try:
            config_file_name = 'configuration.txt'
            config_file_path = os.path.join(os.path.dirname(sys.argv[0]), config_file_name) if getattr(sys, 'frozen', False) else config_file_name

            with open(config_file_path, 'w') as file:
                file.write(path)
        except Exception as e:
           QMessageBox.warning(self,"Error Saving Warcraft3 Path", f"configuration.txt not found: {str(e)}")
    
    def change_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Select Warcraft3 Path")
        if new_path:
            self.wc3_path = os.path.normpath(os.path.join(new_path, "CustomMapData", "Twilight's Eve Evo"))
            self.save_warcraft3_path(self.wc3_path)
            self.update_gui()     

    def update_config_file(self):
        if os.path.isfile("configuration.txt"):
            os.remove("configuration.txt")
        with open("configuration.txt", "w", encoding="utf-8") as f:
            f.write(self.active_profile + "\n" + self.custom_path)

    def get_stash_items(self, content, file_name):
        stash_items = []
        for stash in ["", "2", "3", "4", "5", "6"]:
            stash_list = []
            for item_num in range(1, 7):
                try:
                    stash_item = re.search(f'call Preload\( "Stash{stash} Item {item_num}: (.*?)" \)', content).group(1).replace("|r", "")
                    if stash_item[:2].lower() == "|c":
                        stash_item = stash_item[10:]
                    if stash_item == " ":
                        continue
                    stash_list.append(stash_item)
                except:
                    pass
            stash_items.append(stash_list)
        return stash_items
   
    def get_class_information(self, c_folder):
        gold = 0
        shards = 0
        items = []
        stash_items = []
        load_code = ""

        txt_files = [file for file in os.listdir(c_folder) if file.endswith('.txt') and any(char.isdigit() for char in file)]

        if not txt_files:
            return

        txt_file_path = os.path.join(c_folder, max(txt_files, key=lambda x: int(''.join(filter(str.isdigit, x)))))
        with open(txt_file_path, "r") as f:
            content = f.read()
            gold = re.search(r'call Preload\(\ "Gold: (.*?)" \)', content).group(1)
            shards = re.search(r'call Preload\(\ "Power Shard: (.*?)" \)', content).group(1)
            load_code = re.search(r'call Preload\(\ "-l (.*?)" \)', content).group(1)
        for x in range(1, 7):
            item = re.search(fr'call Preload\(\ "Item {x}: (.*?)" \)', content).group(1).replace("|r", "")
            # Remove color codes from the item name
            item = re.sub(r'\|c[0-9A-Fa-f]{8}', '', item)
            if item[:3].lower() == "|cf":
                item = item[10:]
            items.append(item)
            


            stash_items = self.get_stash_items(content, txt_file_path)

        result = {
            'gold': gold,
            'shards': shards,
            'load_code': load_code,  # Add the 'code' information to the result dictionary
            'items': items,
            'stash_items': stash_items,
            'filename': os.path.basename(txt_file_path)
        }
        return result

    def get_class_names(self):
        class_names = []
        profile_path = os.path.join(self.custom_path, "CustomMapData", "Twilight's Eve Evo", self.active_profile)
        if os.path.exists(profile_path):    
            class_list = {}
            for evo_class_name in os.listdir(profile_path):
                class_path = os.path.join(profile_path, evo_class_name)
                if os.path.isdir(class_path) and self.class_is_valid(evo_class_name):
                    class_info = self.get_class_information(class_path)
                    class_list[evo_class_name] = {
                        'class_name': evo_class_name,
                        'gold': class_info['gold'],
                        'shards': class_info['shards'],
                        'code': class_info['load_code'],
                        'items': class_info['items'],
                        'stash_items': class_info['stash_items'],
                    }
                    class_names.append(evo_class_name)
            self.classes[self.active_profile] = class_list
            return class_names

    def class_is_valid(self, class_name):
        if class_name in self.ALL_CLASS_LIST:
            return True
        return False

    def get_class_level_and_file(self, class_name):
        class_files = os.listdir(os.path.join(self.custom_path, "CustomMapData", "Twilight's Eve Evo", self.active_profile, class_name))
        class_files = [file for file in class_files if file.startswith("[Level ") and file.endswith("].txt")]
        class_files.sort(key=EvoFileReader.natural_keys)
        highest_class_file = class_files[-1]
        class_level = highest_class_file[7:-5]
        return class_level, os.path.join(self.custom_path, "CustomMapData", "Twilight's Eve Evo", self.active_profile, class_name, highest_class_file)

    def update_information(self, selected_class):
        self.textbox.setPlainText(selected_class + "\n\n")

        selected_class_name = re.sub(r'\s*\[\d+\]', '', selected_class)

        if selected_class_name in self.classes.get(self.active_profile, {}):
            # Update the class info from classes
            class_info = self.classes[self.active_profile][selected_class_name]

            # Display information in the QTextEdit
            self.textbox.append("Gold: " + str(class_info['gold']))
            self.textbox.append("Power Shards: " + str(class_info['shards']))
            self.textbox.append("\nload_code: " + class_info['load_code'] + "\n")

            # Display items
            for item in class_info['items']:
                self.textbox.append("Item: " +  re.sub(r'\|c[0-9A-Fa-f]{8}', '', item))

            # Display stash items
            for i, stash_items in enumerate(class_info['stash_items']):
                text = ", ".join(stash_items)
                if text != "":
                    self.textbox.append(f"\nStash{i + 1}: {text}")

        else:
            return
            
    def update_class_list(self):
        self.listbox.clear()
        selected_profile = self.combo.currentText().strip()  # Strip extra spaces
        if selected_profile not in self.classes:
            path_str = os.path.join(self.wc3_path, selected_profile) 
            return

        class_list = self.classes[selected_profile]

        for class_name, evo_class in class_list.items():
            if self.checkbutton_tier_4.isChecked() and class_name not in self.MAX_TIER:
                continue

            # Extract class name from folder name
            # Modified line to extract class name without level
            extracted_class_name = re.sub(r'\s*\[\d+\]$', '', class_name)

            # Look for .txt files in the class folder
            class_folder_path = os.path.join(self.wc3_path, selected_profile, class_name)

            # Standardize path format
            class_folder_path = class_folder_path.replace('\\', '/')
            if os.path.exists(class_folder_path):
                txt_files = [file for file in os.listdir(class_folder_path) if file.endswith('.txt')]

                # Check if there is a .txt file with the expected format
                max_level = None
                for txt_file in txt_files:
                    match = re.match(r'\[Level (\d+)\]\.txt', txt_file)
                    if match:
                        level_from_filename = int(match.group(1))
                        if max_level is None or level_from_filename > max_level:
                            max_level = level_from_filename

                # Additional filtering by max level
                if self.checkbutton_max_level.isChecked() and max_level != 300:
                    continue

                # Use the extracted class name from the folder
                self.listbox.addItem(f"{extracted_class_name} [{max_level}]")

        self.get_selected_list_item()

    def update_gui(self):
        try:
            profiles_path = self.wc3_path
            self.update_profiles()
            self.combo.clear()
            self.combo.addItems(self.profiles)

            if len(self.profiles) == 1:
                self.combo.setCurrentIndex(0)
            else:
                index = self.combo.findText(self.active_profile)
                if index != -1:
                    self.combo.setCurrentIndex(index)

            self.update_class_list()
        except Exception as e:
            QMessageBox.warning(self,"Error updating gui")
            return

    def load_config(self):
        if os.path.isfile("configuration.txt"):
            with open("configuration.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) != 2:
                    return "", ""
                else:
                    loaded_active_profile = lines[0].replace("\n", "")
                    loaded_custom_path = lines[1].replace("\n", "")
                    return loaded_active_profile, loaded_custom_path

    def load_custom_commands(self):
         if os.path.exists("customcommands.txt"):
            with open("customcommands.txt", "r") as f:
                lines = f.readlines()
                for command_lines in lines:
                    stripped = command_lines.strip()
                    self.paste_code(stripped)

    def get_profiles(self):
        path = os.path.normpath(os.path.join(self.custom_path, "CustomMapData", "Twilight's Eve Evo"))
        wc3_names_directories = []
        try:
            for wc3_names_directory in os.listdir(path):
                full_path = os.path.join(path, wc3_names_directory)
                if os.path.isdir(full_path):
                    wc3_names_directories.append(wc3_names_directory)
            return wc3_names_directories
        except Exception as e:
            QMessageBox.warning(self, "Profile directories not found.")
            return []
    
    def update_profiles(self):
        try:
            # Check if the path exists
            if not os.path.exists(self.wc3_path):
                raise FileNotFoundError(f"Profiles path not found: {self.wc3_path}")

            # List the directories (profiles) in the self.wc3_path
            profiles_list = [profile for profile in os.listdir(self.wc3_path) if os.path.isdir(os.path.join(self.wc3_path, profile))]
            if not profiles_list:
                # Display an error message if profiles list is empty
                QMessageBox.warning(self, "Evo Files Not Found", "No profiles found in the specified path.")
                return
            self.profiles = sorted(profiles_list)
            self.classes = {}

            for profile in self.profiles:
                profile_path = os.path.join(self.wc3_path, profile)

                # List the directories (classes) in the profile_path
                classes_list = [evo_class for evo_class in os.listdir(profile_path) if os.path.isdir(os.path.join(profile_path, evo_class))]

                self.classes[profile] = {}

                for evo_class in classes_list:
                    class_path = os.path.join(profile_path, evo_class)
                    class_info = self.get_class_information(class_path)
                    self.classes[profile][evo_class] = class_info
        except FileNotFoundError as e:
            QMessageBox.warning(self, "Evo Files Not Found", f"{e}")
            
        except Exception as e:
            QMessageBox.warning(self, "Error Updating Profiles", f"An error occurred while updating profiles: {str(e)}")

        

    def copy_code(self):
        global custom_commands_loaded
        selected_item = self.listbox.currentItem()
        if selected_item is not None:
            selected_class_with_level = selected_item.text()
            selected_class = re.sub(r'\s*\[\d+\]', '', selected_class_with_level)
            if selected_class in self.classes[self.active_profile]:
                self.selected_code = self.classes[self.active_profile][selected_class]['load_code']
            else:
                return
            try:
                if self.selected_code is not None:
                    if len(self.selected_code) >= 124:
                        first_half = self.selected_code[0:124]
                        second_half = self.selected_code[124:]
                        self.paste_code('-rp')
                        self.paste_code('-lc')
                        self.paste_code(first_half)
                        self.paste_code(second_half)
                        self.paste_code('-le')
                        self.paste_code('-c')
                    else:
                        self.paste_code('-rp')
                        self.paste_code('-l ' + self.selected_code)
                        self.paste_code('-c')

                if not self.custom_commands_loaded:
                    self.load_custom_commands()
                    self.custom_commands_loaded = True
            except IndexError:
                 QMessageBox.warning(self, "Warcraft III Not Running", "Warcraft III is not running.")
            except Exception as e:
            # Handle other exceptions
                 QMessageBox.warning(self, "Error Pasting Code", f"An error occurred while pasting the code: {str(e)}")
        else:
            return

    def paste_code(self, pasted_item):
            war3 = pyautogui.getWindowsWithTitle('Warcraft III')[0]
            war3.activate()

            keyboard.press_and_release('enter')  # Press Enter to open the chat
            keyboard.write(pasted_item)  # Type the pasted item
            keyboard.press_and_release('enter')
            
    def refresh(self):
        try:
            # Clear the textbox and listbox
            self.custom_commands_loaded = False
            self.listbox.clear()
            self.textbox.clear()
            # Update profiles and classes
            self.update_profiles()
            # Clear and update the combo box with profiles
            self.combo.clear()
            self.combo.addItems(self.profiles)
            # Set the current profile based on the active_profile
            if len(self.profiles) == 1:
                self.combo.setCurrentIndex(0)
            else:
                index = self.combo.findText(self.active_profile)
                if index != -1:
                    self.combo.setCurrentIndex(index)
            # Update the class list
            self.update_class_list()
        except Exception as e:
            QMessageBox.warning(self, "Error Refreshing", f"An error occurred while refreshing: {str(e)}")
        
    def get_missing_items(self, checking_for, items, missing_items):
        for material in self.RECIPES[checking_for]["materials"]:
            if material in items:
                items.remove(material)
            elif material in self.RECIPES:
                self.get_missing_items(material, items, missing_items)
            else:
                missing_items.append(material)
        return missing_items
        
    def main(self):
        profiles = self.get_profiles()
        if profiles:
            if self.active_profile == "":
                self.active_profile = profiles[0]
                self.update_config_file()

            class_name_list = self.get_class_names()       
            if self.class_list:
                self.update_gui()
    
    def get_selected_list_item(self):
        if not self.updating_information:
            self.updating_information = True
            try:
                selected_item = self.listbox.currentItem()
                if selected_item is not None:
                    selected_class_with_level = selected_item.text()
                    selected_class = re.sub(r'\s*\[\d+\]', '', selected_class_with_level)

                    if self.active_profile in self.classes and selected_class in self.classes[self.active_profile]:
                        class_info = self.classes[self.active_profile][selected_class]

                        # Update class_list
                        self.classes[self.active_profile][selected_class] = {
                            'gold': class_info['gold'],
                            'shards': class_info['shards'],
                            'load_code': class_info['load_code'],
                            'items': [re.sub(r'\|c[0-9A-Fa-f]{8}', '', item) for item in class_info['items']],
                            'stash_items': class_info['stash_items'],
                        }
                        # Update the GUI with the information
                        self.update_information(selected_class)
                        # Print the updated class_list for the specific class
                    else:
                        return
                  
                    return selected_class
            finally:
                self.updating_information = False


    def update_selected_profile(self):
        self.active_profile = self.combo.currentText()
        self.update_class_list()

    def display_godly_advancement(self):
            gadv_window = QDialog(self)
            main_window_rect = self.geometry()
            gadv_window_x = main_window_rect.x() + main_window_rect.width() + 10  # Adjust the offset as needed
            gadv_window_y = main_window_rect.y()
            gadv_window.setGeometry(gadv_window_x, gadv_window_y, 300, 400)
            gadv_window.setWindowTitle("Godly progress")
    
            gadv_textbox = QTextEdit(gadv_window)
            gadv_textbox.setGeometry(0, 0, 300, 400)

            gadv_textbox.insertPlainText(f"{self.selected_class}\n\nMissing items:\n\n")

            items = []
            selected_item = self.listbox.currentItem()
            if selected_item is not None:
                selected_class_with_level = selected_item.text()
                selected_class = re.sub(r'\s*\[\d+\]', '', selected_class_with_level)
                if selected_class in self.classes[self.active_profile]:
                    class_details = self.classes[self.active_profile][selected_class]
                    items = class_details["items"]
                    for stash in class_details["stash_items"]:
                        items += stash

                    missing_items = self.get_missing_items("Godly", items, [])

                    # replace scrap for simplification
                    for i in range(len(missing_items)):
                        if missing_items[i] in ["Mythical Weapon Piece", "Mythical Handle Piece", "Mythical Armor Piece"]:
                            missing_items[i] = "Godly Material"

                    missing = [[missing_items.count(i), i] for i in set(missing_items)]
                    missing.sort(reverse=True)
                    for index, missing_item in enumerate(missing):
                        gadv_textbox.insertPlainText(f"{missing[index][0]:<2} {missing[index][1]}\n")

                    gadv_textbox.setReadOnly(True)
                    gadv_window.exec()
                else:
                    QMessageBox.warning(self, "Class can't be found in the selected profile.")
                    return
            else:
                QMessageBox.warning(self, "No Class Selected", "Please select a class to check Godly Farm progress.")
                return
            
    def display_changelog(self):
        changelog_path = os.path.join(self.custom_path, self.CHANGELOG_FILE_NAME)
        if os.path.isfile(changelog_path):
            with open(changelog_path, 'r', encoding='utf-8') as f:
                changelog_content = f.read()
                QMessageBox.information(self, "Changelog", changelog_content)
        else:
            QMessageBox.warning(self, "Changelog Not Found", "Changelog file not found.")

    def display_about(self):
        QMessageBox.about(self, "About Evo File Reader", "Evo File Reader\n\nVersion: {}\n\nAuthor: MiroBG".format(self.VERSION))

    
    def natural_keys(text):
        return [int(c) if c.isdigit() else c for c in re.split('(\d+)', text)]
    
class GodlyAdvancementDialog(QDialog):
    def __init__(self, selected_class, items, stash_items):
        super(GodlyAdvancementDialog, self).__init__()

        self.setWindowTitle("Godly Progress")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.textbox = QTextEdit(self)
        layout.addWidget(self.textbox)

        self.textbox.insertPlainText(f"{selected_class}\n\nMissing items:\n\n")

        missing_items = EvoFileReader().get_missing_items("Godly", items, stash_items)

        # Replace scrap for simplification
        for i in range(len(missing_items)):
            if missing_items[i] in ["Mythical Weapon Piece", "Mythical Handle Piece", "Mythical Armor Piece"]:
                missing_items[i] = "Godly Material"

        missing = [[missing_items.count(i), i] for i in set(missing_items)]
        missing.sort(reverse=True)
        for index, missing_item in enumerate(missing):
            self.textbox.insertPlainText(f"{missing[index][0]:<2} {missing[index][1]}\n")

        self.textbox.setReadOnly(True)

        self.setLayout(layout)  
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EvoFileReader()
    window.show()
    sys.exit(app.exec())