# Visa Appointment Bot

This is an automated bot to assist in booking visa appointments through the Almaviva Visa website. It features a graphical user interface built with Tkinter and an automation backend powered by Selenium.

## Features
- **Profile Management**: Supports multiple user profiles that can be configured and saved.
- **GUI Interface**: A simple Tkinter GUI to select a user, manage settings, and start the bot.
- **Proxy Support**: Can be configured to run through an HTTP/HTTPS proxy.
- **Automated Booking**: Logs in, navigates to the appointment section, and repeatedly checks for available slots.
- **Headless Operation**: Can be run from the command line for automated scheduling.
- **Live Logging**: See real-time status updates from the bot in the GUI.

## Project Files
- `visa_bot_gui.py`: The main GUI application.
- `run_bot_backend.py`: The Selenium automation logic.
- `config.json`: Configuration file for user profiles and proxy settings.
- `requirements.txt`: A list of required Python packages.
- `setup.bat`: A batch script to initialize the project and install dependencies.
- `auto_run_bot.bat`: A batch script for running the bot via a scheduled task.
- `README.md`: This instruction file.

---

## 1. Setup Instructions

1.  **Install Python**: Make sure you have Python 3 installed on your system.
2.  **Run Setup Script**: Double-click on `setup.bat`. This will:
    - Create a Python virtual environment in a folder named `venv`.
    - Install all the required packages from `requirements.txt`.
3.  **Wait for setup to complete**: The script will pause when it's finished.

---

## 2. Configuration

Before running the bot, you must configure your user profiles and proxy settings in `config.json`.

1.  **Open `config.json`**: Use a text editor like Notepad to open the file.
2.  **Configure Proxy**:
    - If you need to use a proxy, set `"enabled": true`.
    - Change `"server": "http://your_proxy_server:port"` to your actual proxy address.
    - If your proxy does not require authentication, leave `username` and `password` as empty strings.
    - If you do not need a proxy, set `"enabled": false`.
3.  **Configure User Profiles**:
    - The file comes with three sample profiles: `"User 1"`, `"User 2"`, and `"User 3"`.
    - Fill in the details for each profile you intend to use: `email`, `password`, `center`, `visa_type`, etc.
4.  **Configure Selectors (Crucial Step)**:
    - The bot's ability to interact with the website depends entirely on the selectors. These will likely change over time.
    - Open the Almaviva website in your browser and use the Developer Tools (F12) to inspect the HTML elements for the login form, buttons, and other fields.
    - Update the `value` for each item in the `selectors` section of `config.json` to match the website.
    - You can use different `by` methods: `ID`, `XPATH`, `CLASS_NAME`, `NAME`, `CSS_SELECTOR`.

---

## 3. Running the Bot

### Using the GUI (Recommended)

1.  Double-click `visa_bot_gui.py` to start the application.
2.  **Select a Profile**: Use the dropdown menu to select the user profile you configured. The details will load in the form.
3.  **Save Changes (Optional)**: If you make any changes in the fields, you can click "Save Profile" to update your `config.json`.
4.  **Start the Bot**: Click "Start Bot". A new Chrome window will open and the automation will begin.
5.  **Monitor Logs**: Watch the log area in the GUI for real-time updates on the bot's progress.

### Important Note on Selectors

The bot uses **placeholder selectors** defined in `config.json`. **These will almost certainly need to be updated** to match the live website's HTML. If the bot fails during login or form filling, it is almost always because a selector has changed on the website.

---

## 4. Packaging as an .EXE File

To create a standalone executable:

1.  Make sure you have run `setup.bat` and the virtual environment is active.
2.  Open a command prompt (`cmd.exe`) in the project directory.
3.  Activate the virtual environment by running: `venv\Scripts\activate`
4.  Run the following PyInstaller command:
    ```
    pyinstaller --onefile --windowed --add-data "config.json;." visa_bot_gui.py
    ```
5.  The final `.exe` file will be located in the `dist` folder.

---

## 5. Scheduling with Task Scheduler

To run the bot automatically every day:

1.  **Open Task Scheduler** on Windows.
2.  Click **Create Basic Task...**
    - **Name**: "Visa Bot Runner"
    - **Trigger**: Select "Daily" and set a time.
    - **Action**: Select "Start a program".
    - **Program/script**: Click "Browse..." and select the `auto_run_bot.bat` file from the project folder.
3.  **Finish** the wizard. The task will now run at your specified time.

---

## 6. Troubleshooting

- **Errors in CMD**: If the `.exe` file doesn't run, launch it from a command prompt (`cmd.exe`) to see any error messages.
- **Bot fails on Login/Form Filling**: This is the most common issue. The website's selectors have likely changed. You must update the `selectors` section in your `config.json` file.
- **ChromeDriver Issues**: Ensure your version of Google Chrome is compatible with the `chromedriver` managed by Selenium. Selenium usually handles this, but corporate policies might interfere.
- **Proxy Failure**: Double-check your proxy server address and port in `config.json`. Ensure the proxy is running and accessible. 