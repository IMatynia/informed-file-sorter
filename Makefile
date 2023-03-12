ui_folder="./src/ui"

ui_recompile:
	pyside6-uic $(ui_folder)/layouts/main_window.ui -o $(ui_folder)/main_window_view.py