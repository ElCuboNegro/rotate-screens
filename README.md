# Screen Rotation Utility
A Python utility that enables quick rotation of monitors using special keyboard keys (F13 - F17) for rotating multiple screens in 90-degree increments. Designed to work with Nvidia video cards and supports multiple monitors.

## Features
Rotate monitors between landscape and portrait modes with a single key press.
Supports up to four monitors, each mapped to different hotkeys.
Easily reset all monitors to default orientation (landscape).
Logs all actions and errors to a file for debugging and tracking.

### Hotkey Mappings
F13: Reset all monitors to the default landscape orientation (0 degrees).
F14: Rotate Monitor 1 between landscape (0 degrees) and portrait (90 degrees).
F15: Rotate Monitor 2 between landscape (0 degrees) and portrait (90 degrees).
F16: Rotate Monitor 3 between landscape (0 degrees) and portrait (90 degrees).
F17: Rotate Monitor 4 between landscape (0 degrees) and portrait (90 degrees).

## Requirements
Python: Version 3.6 or higher.
Windows OS: Tested on Windows 10/11.
Nvidia GPU: Required for full functionality.

## Dependencies
This project requires the following Python libraries:

`keyboard`
`pywin32`
`logging`

You can install the necessary dependencies with the following command:

`pip install keyboard pywin32`

# Installation

## Clone or Download the Repository:

Clone the repository or download the project files from the provided link.

```bash
git clone https://github.com/ElCuboNegro/rotate-screens.git
cd rotate-screens
```

## Install Dependencies:

Install all required Python packages using pip.

```bash
pip install -r requirements.txt
```

Run the Script:

Execute the script with administrative privileges to allow changes to display settings.

```bash
python rotate_screens.py
```

# Packaging and Delivery

To distribute the project as a standalone executable, follow the steps below:

## Create an Executable with PyInstaller
First, ensure that PyInstaller is installed:

```bash
pip install pyinstaller
```

Then, create a standalone executable using the following command:

```bash
pyinstaller --onefile rotate_screens.py
```

This will generate an executable inside the dist/ folder. The generated executable can now be distributed without requiring the user to install Python or dependencies.

# Running the Executable Automatically on Startup
If you'd like the screen rotation utility to start automatically when Windows boots up, follow these steps:

## Create a Shortcut:

Navigate to the `dist/` folder where the executable is located.
Right-click the `rotate_screens.exe` file and select Create shortcut.
Move Shortcut to Startup Folder:

Press `Win + R` and type shell:startup to open the Startup folder.
Move the shortcut you just created into this folder.
Ensure Administrator Privileges:

Right-click the shortcut, go to `Properties → Shortcut → Advanced`... and check the Run as administrator box.
This ensures that the script runs with the necessary privileges each time the computer starts.

# Logging
The utility logs all its actions and errors in a log file stored in the user's home directory under `.rotatescreen_logs.txt`. This log is useful for debugging and understanding how the utility interacts with the system.

# Troubleshooting
Administrator Privileges: Ensure that the script is run with administrative privileges, as modifying display settings requires elevated permissions.
Unsupported Monitors: Not all monitors support rotation. Verify that your monitors support the intended orientation changes by attempting to rotate them manually in the Windows display settings.
Hotkey Issues: If F13-F17 keys are not working, try mapping the functionality to other keys using the keyboard library (instructions in the code).

# Contributing
Fork the repository.
Create your feature branch (git checkout -b feature/my-feature).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/my-feature).
Open a pull request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
This project utilizes the `pywin32` library for interacting with Windows APIs and the keyboard library for hotkey detection.