ui_folder="./src/ui"

ui_recompile:
	pyside6-uic $(ui_folder)/layouts/main_window.ui -o $(ui_folder)/main_window_view.py
	pyside6-uic $(ui_folder)/layouts/destination_folder.ui -o $(ui_folder)/ui_destination_folder.py