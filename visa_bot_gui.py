import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import json
import threading
import queue
import logging
import sv_ttk
import re
from run_bot_backend import run_automation

COUNTRY_CODES = [
    {"name": "Afghanistan", "dial_code": "+93", "code": "AF"},
    {"name": "Albania", "dial_code": "+355", "code": "AL"},
    {"name": "Algeria", "dial_code": "+213", "code": "DZ"},
    {"name": "AmericanSamoa", "dial_code": "+1 684", "code": "AS"},
    {"name": "Andorra", "dial_code": "+376", "code": "AD"},
    {"name": "Angola", "dial_code": "+244", "code": "AO"},
    {"name": "Anguilla", "dial_code": "+1 264", "code": "AI"},
    {"name": "Antigua and Barbuda", "dial_code": "+1268", "code": "AG"},
    {"name": "Argentina", "dial_code": "+54", "code": "AR"},
    {"name": "Armenia", "dial_code": "+374", "code": "AM"},
    {"name": "Aruba", "dial_code": "+297", "code": "AW"},
    {"name": "Australia", "dial_code": "+61", "code": "AU"},
    {"name": "Austria", "dial_code": "+43", "code": "AT"},
    {"name": "Azerbaijan", "dial_code": "+994", "code": "AZ"},
    {"name": "Bahamas", "dial_code": "+1 242", "code": "BS"},
    {"name": "Bahrain", "dial_code": "+973", "code": "BH"},
    {"name": "Bangladesh", "dial_code": "+880", "code": "BD"},
    {"name": "Barbados", "dial_code": "+1 246", "code": "BB"},
    {"name": "Belarus", "dial_code": "+375", "code": "BY"},
    {"name": "Belgium", "dial_code": "+32", "code": "BE"},
    {"name": "Belize", "dial_code": "+501", "code": "BZ"},
    {"name": "Benin", "dial_code": "+229", "code": "BJ"},
    {"name": "Bermuda", "dial_code": "+1 441", "code": "BM"},
    {"name": "Bhutan", "dial_code": "+975", "code": "BT"},
    {"name": "Bosnia and Herzegovina", "dial_code": "+387", "code": "BA"},
    {"name": "Botswana", "dial_code": "+267", "code": "BW"},
    {"name": "Brazil", "dial_code": "+55", "code": "BR"},
    {"name": "British Indian Ocean Territory", "dial_code": "+246", "code": "IO"},
    {"name": "Bulgaria", "dial_code": "+359", "code": "BG"},
    {"name": "Burkina Faso", "dial_code": "+226", "code": "BF"},
    {"name": "Burundi", "dial_code": "+257", "code": "BI"},
    {"name": "Cambodia", "dial_code": "+855", "code": "KH"},
    {"name": "Cameroon", "dial_code": "+237", "code": "CM"},
    {"name": "Canada", "dial_code": "+1", "code": "CA"},
    {"name": "Cape Verde", "dial_code": "+238", "code": "CV"},
    {"name": "Cayman Islands", "dial_code": "+ 345", "code": "KY"},
    {"name": "Central African Republic", "dial_code": "+236", "code": "CF"},
    {"name": "Chad", "dial_code": "+235", "code": "TD"},
    {"name": "Chile", "dial_code": "+56", "code": "CL"},
    {"name": "China", "dial_code": "+86", "code": "CN"},
    {"name": "Christmas Island", "dial_code": "+61", "code": "CX"},
    {"name": "Colombia", "dial_code": "+57", "code": "CO"},
    {"name": "Comoros", "dial_code": "+269", "code": "KM"},
    {"name": "Congo", "dial_code": "+242", "code": "CG"},
    {"name": "Cook Islands", "dial_code": "+682", "code": "CK"},
    {"name": "Costa Rica", "dial_code": "+506", "code": "CR"},
    {"name": "Croatia", "dial_code": "+385", "code": "HR"},
    {"name": "Cuba", "dial_code": "+53", "code": "CU"},
    {"name": "Cyprus", "dial_code": "+537", "code": "CY"},
    {"name": "Czech Republic", "dial_code": "+420", "code": "CZ"},
    {"name": "Denmark", "dial_code": "+45", "code": "DK"},
    {"name": "Djibouti", "dial_code": "+253", "code": "DJ"},
    {"name": "Dominica", "dial_code": "+1 767", "code": "DM"},
    {"name": "Dominican Republic", "dial_code": "+1 849", "code": "DO"},
    {"name": "Ecuador", "dial_code": "+593", "code": "EC"},
    {"name": "Egypt", "dial_code": "+20", "code": "EG"},
    {"name": "El Salvador", "dial_code": "+503", "code": "SV"},
    {"name": "Equatorial Guinea", "dial_code": "+240", "code": "GQ"},
    {"name": "Eritrea", "dial_code": "+291", "code": "ER"},
    {"name": "Estonia", "dial_code": "+372", "code": "EE"},
    {"name": "Ethiopia", "dial_code": "+251", "code": "ET"},
    {"name": "Faroe Islands", "dial_code": "+298", "code": "FO"},
    {"name": "Fiji", "dial_code": "+679", "code": "FJ"},
    {"name": "Finland", "dial_code": "+358", "code": "FI"},
    {"name": "France", "dial_code": "+33", "code": "FR"},
    {"name": "French Guiana", "dial_code": "+594", "code": "GF"},
    {"name": "French Polynesia", "dial_code": "+689", "code": "PF"},
    {"name": "Gabon", "dial_code": "+241", "code": "GA"},
    {"name": "Gambia", "dial_code": "+220", "code": "GM"},
    {"name": "Georgia", "dial_code": "+995", "code": "GE"},
    {"name": "Germany", "dial_code": "+49", "code": "DE"},
    {"name": "Ghana", "dial_code": "+233", "code": "GH"},
    {"name": "Gibraltar", "dial_code": "+350", "code": "GI"},
    {"name": "Greece", "dial_code": "+30", "code": "GR"},
    {"name": "Greenland", "dial_code": "+299", "code": "GL"},
    {"name": "Grenada", "dial_code": "+1 473", "code": "GD"},
    {"name": "Guadeloupe", "dial_code": "+590", "code": "GP"},
    {"name": "Guam", "dial_code": "+1 671", "code": "GU"},
    {"name": "Guatemala", "dial_code": "+502", "code": "GT"},
    {"name": "Guinea", "dial_code": "+224", "code": "GN"},
    {"name": "Guinea-Bissau", "dial_code": "+245", "code": "GW"},
    {"name": "Guyana", "dial_code": "+595", "code": "GY"},
    {"name": "Haiti", "dial_code": "+509", "code": "HT"},
    {"name": "Honduras", "dial_code": "+504", "code": "HN"},
    {"name": "Hungary", "dial_code": "+36", "code": "HU"},
    {"name": "Iceland", "dial_code": "+354", "code": "IS"},
    {"name": "India", "dial_code": "+91", "code": "IN"},
    {"name": "Indonesia", "dial_code": "+62", "code": "ID"},
    {"name": "Iraq", "dial_code": "+964", "code": "IQ"},
    {"name": "Ireland", "dial_code": "+353", "code": "IE"},
    {"name": "Israel", "dial_code": "+972", "code": "IL"},
    {"name": "Italy", "dial_code": "+39", "code": "IT"},
    {"name": "Jamaica", "dial_code": "+1 876", "code": "JM"},
    {"name": "Japan", "dial_code": "+81", "code": "JP"},
    {"name": "Jordan", "dial_code": "+962", "code": "JO"},
    {"name": "Kazakhstan", "dial_code": "+7 7", "code": "KZ"},
    {"name": "Kenya", "dial_code": "+254", "code": "KE"},
    {"name": "Kiribati", "dial_code": "+686", "code": "KI"},
    {"name": "Kuwait", "dial_code": "+965", "code": "KW"},
    {"name": "Kyrgyzstan", "dial_code": "+996", "code": "KG"},
    {"name": "Latvia", "dial_code": "+371", "code": "LV"},
    {"name": "Lebanon", "dial_code": "+961", "code": "LB"},
    {"name": "Lesotho", "dial_code": "+266", "code": "LS"},
    {"name": "Liberia", "dial_code": "+231", "code": "LR"},
    {"name": "Liechtenstein", "dial_code": "+423", "code": "LI"},
    {"name": "Lithuania", "dial_code": "+370", "code": "LT"},
    {"name": "Luxembourg", "dial_code": "+352", "code": "LU"},
    {"name": "Madagascar", "dial_code": "+261", "code": "MG"},
    {"name": "Malawi", "dial_code": "+265", "code": "MW"},
    {"name": "Malaysia", "dial_code": "+60", "code": "MY"},
    {"name": "Maldives", "dial_code": "+960", "code": "MV"},
    {"name": "Mali", "dial_code": "+223", "code": "ML"},
    {"name": "Malta", "dial_code": "+356", "code": "MT"},
    {"name": "Marshall Islands", "dial_code": "+692", "code": "MH"},
    {"name": "Martinique", "dial_code": "+596", "code": "MQ"},
    {"name": "Mauritania", "dial_code": "+222", "code": "MR"},
    {"name": "Mauritius", "dial_code": "+230", "code": "MU"},
    {"name": "Mayotte", "dial_code": "+262", "code": "YT"},
    {"name": "Mexico", "dial_code": "+52", "code": "MX"},
    {"name": "Monaco", "dial_code": "+377", "code": "MC"},
    {"name": "Mongolia", "dial_code": "+976", "code": "MN"},
    {"name": "Montenegro", "dial_code": "+382", "code": "ME"},
    {"name": "Montserrat", "dial_code": "+1664", "code": "MS"},
    {"name": "Morocco", "dial_code": "+212", "code": "MA"},
    {"name": "Myanmar", "dial_code": "+95", "code": "MM"},
    {"name": "Namibia", "dial_code": "+264", "code": "NA"},
    {"name": "Nauru", "dial_code": "+674", "code": "NR"},
    {"name": "Nepal", "dial_code": "+977", "code": "NP"},
    {"name": "Netherlands", "dial_code": "+31", "code": "NL"},
    {"name": "Netherlands Antilles", "dial_code": "+599", "code": "AN"},
    {"name": "New Caledonia", "dial_code": "+687", "code": "NC"},
    {"name": "New Zealand", "dial_code": "+64", "code": "NZ"},
    {"name": "Nicaragua", "dial_code": "+505", "code": "NI"},
    {"name": "Niger", "dial_code": "+227", "code": "NE"},
    {"name": "Nigeria", "dial_code": "+234", "code": "NG"},
    {"name": "Niue", "dial_code": "+683", "code": "NU"},
    {"name": "Norfolk Island", "dial_code": "+672", "code": "NF"},
    {"name": "Northern Mariana Islands", "dial_code": "+1 670", "code": "MP"},
    {"name": "Norway", "dial_code": "+47", "code": "NO"},
    {"name": "Oman", "dial_code": "+968", "code": "OM"},
    {"name": "Pakistan", "dial_code": "+92", "code": "PK"},
    {"name": "Palau", "dial_code": "+680", "code": "PW"},
    {"name": "Panama", "dial_code": "+507", "code": "PA"},
    {"name": "Papua New Guinea", "dial_code": "+675", "code": "PG"},
    {"name": "Paraguay", "dial_code": "+595", "code": "PY"},
    {"name": "Peru", "dial_code": "+51", "code": "PE"},
    {"name": "Philippines", "dial_code": "+63", "code": "PH"},
    {"name": "Poland", "dial_code": "+48", "code": "PL"},
    {"name": "Portugal", "dial_code": "+351", "code": "PT"},
    {"name": "Puerto Rico", "dial_code": "+1 939", "code": "PR"},
    {"name": "Qatar", "dial_code": "+974", "code": "QA"},
    {"name": "Romania", "dial_code": "+40", "code": "RO"},
    {"name": "Rwanda", "dial_code": "+250", "code": "RW"},
    {"name": "Samoa", "dial_code": "+685", "code": "WS"},
    {"name": "San Marino", "dial_code": "+378", "code": "SM"},
    {"name": "Saudi Arabia", "dial_code": "+966", "code": "SA"},
    {"name": "Senegal", "dial_code": "+221", "code": "SN"},
    {"name": "Serbia", "dial_code": "+381", "code": "RS"},
    {"name": "Seychelles", "dial_code": "+248", "code": "SC"},
    {"name": "Sierra Leone", "dial_code": "+232", "code": "SL"},
    {"name": "Singapore", "dial_code": "+65", "code": "SG"},
    {"name": "Slovakia", "dial_code": "+421", "code": "SK"},
    {"name": "Slovenia", "dial_code": "+386", "code": "SI"},
    {"name": "Solomon Islands", "dial_code": "+677", "code": "SB"},
    {"name": "South Africa", "dial_code": "+27", "code": "ZA"},
    {"name": "South Georgia and the South Sandwich Islands", "dial_code": "+500", "code": "GS"},
    {"name": "Spain", "dial_code": "+34", "code": "ES"},
    {"name": "Sri Lanka", "dial_code": "+94", "code": "LK"},
    {"name": "Sudan", "dial_code": "+249", "code": "SD"},
    {"name": "Suriname", "dial_code": "+597", "code": "SR"},
    {"name": "Swaziland", "dial_code": "+268", "code": "SZ"},
    {"name": "Sweden", "dial_code": "+46", "code": "SE"},
    {"name": "Switzerland", "dial_code": "+41", "code": "CH"},
    {"name": "Tajikistan", "dial_code": "+992", "code": "TJ"},
    {"name": "Thailand", "dial_code": "+66", "code": "TH"},
    {"name": "Togo", "dial_code": "+228", "code": "TG"},
    {"name": "Tokelau", "dial_code": "+690", "code": "TK"},
    {"name": "Tonga", "dial_code": "+676", "code": "TO"},
    {"name": "Trinidad and Tobago", "dial_code": "+1 868", "code": "TT"},
    {"name": "Tunisia", "dial_code": "+216", "code": "TN"},
    {"name": "Turkey", "dial_code": "+90", "code": "TR"},
    {"name": "Turkmenistan", "dial_code": "+993", "code": "TM"},
    {"name": "Turks and Caicos Islands", "dial_code": "+1 649", "code": "TC"},
    {"name": "Tuvalu", "dial_code": "+688", "code": "TV"},
    {"name": "Uganda", "dial_code": "+256", "code": "UG"},
    {"name": "Ukraine", "dial_code": "+380", "code": "UA"},
    {"name": "United Arab Emirates", "dial_code": "+971", "code": "AE"},
    {"name": "United Kingdom", "dial_code": "+44", "code": "GB"},
    {"name": "United States", "dial_code": "+1", "code": "US"},
    {"name": "Uruguay", "dial_code": "+598", "code": "UY"},
    {"name": "Uzbekistan", "dial_code": "+998", "code": "UZ"},
    {"name": "Vanuatu", "dial_code": "+678", "code": "VU"},
    {"name": "Wallis and Futuna", "dial_code": "+681", "code": "WF"},
    {"name": "Yemen", "dial_code": "+967", "code": "YE"},
    {"name": "Zambia", "dial_code": "+260", "code": "ZM"},
    {"name": "Zimbabwe", "dial_code": "+263", "code": "ZW"},
    {"name": "land Islands", "dial_code": "", "code": "AX"},
    {"name": "Antarctica", "dial_code": "", "code": "AQ"},
    {"name": "Bolivia, Plurinational State of", "dial_code": "+591", "code": "BO"},
    {"name": "Brunei Darussalam", "dial_code": "+673", "code": "BN"},
    {"name": "Cocos (Keeling) Islands", "dial_code": "+61", "code": "CC"},
    {"name": "Congo, The Democratic Republic of the", "dial_code": "+243", "code": "CD"},
    {"name": "Cote d'Ivoire", "dial_code": "+225", "code": "CI"},
    {"name": "Falkland Islands (Malvinas)", "dial_code": "+500", "code": "FK"},
    {"name": "Guernsey", "dial_code": "+44", "code": "GG"},
    {"name": "Holy See (Vatican City State)", "dial_code": "+379", "code": "VA"},
    {"name": "Hong Kong", "dial_code": "+852", "code": "HK"},
    {"name": "Iran, Islamic Republic of", "dial_code": "+98", "code": "IR"},
    {"name": "Isle of Man", "dial_code": "+44", "code": "IM"},
    {"name": "Jersey", "dial_code": "+44", "code": "JE"},
    {"name": "Korea, Democratic People's Republic of", "dial_code": "+850", "code": "KP"},
    {"name": "Korea, Republic of", "dial_code": "+82", "code": "KR"},
    {"name": "Lao People's Democratic Republic", "dial_code": "+856", "code": "LA"},
    {"name": "Libyan Arab Jamahiriya", "dial_code": "+218", "code": "LY"},
    {"name": "Macao", "dial_code": "+853", "code": "MO"},
    {"name": "Macedonia, The Former Yugoslav Republic of", "dial_code": "+389", "code": "MK"},
    {"name": "Micronesia, Federated States of", "dial_code": "+691", "code": "FM"},
    {"name": "Moldova, Republic of", "dial_code": "+373", "code": "MD"},
    {"name": "Mozambique", "dial_code": "+258", "code": "MZ"},
    {"name": "Palestinian Territory, Occupied", "dial_code": "+970", "code": "PS"},
    {"name": "Pitcairn", "dial_code": "+872", "code": "PN"},
    {"name": "Réunion", "dial_code": "+262", "code": "RE"},
    {"name": "Russia", "dial_code": "+7", "code": "RU"},
    {"name": "Saint Barthélemy", "dial_code": "+590", "code": "BL"},
    {"name": "Saint Helena, Ascension and Tristan Da Cunha", "dial_code": "+290", "code": "SH"},
    {"name": "Saint Kitts and Nevis", "dial_code": "+1 869", "code": "KN"},
    {"name": "Saint Lucia", "dial_code": "+1 758", "code": "LC"},
    {"name": "Saint Martin", "dial_code": "+590", "code": "MF"},
    {"name": "Saint Pierre and Miquelon", "dial_code": "+508", "code": "PM"},
    {"name": "Saint Vincent and the Grenadines", "dial_code": "+1 784", "code": "VC"},
    {"name": "Sao Tome and Principe", "dial_code": "+239", "code": "ST"},
    {"name": "Somalia", "dial_code": "+252", "code": "SO"},
    {"name": "Svalbard and Jan Mayen", "dial_code": "+47", "code": "SJ"},
    {"name": "Syrian Arab Republic", "dial_code": "+963", "code": "SY"},
    {"name": "Taiwan, Province of China", "dial_code": "+886", "code": "TW"},
    {"name": "Tanzania, United Republic of", "dial_code": "+255", "code": "TZ"},
    {"name": "Timor-Leste", "dial_code": "+670", "code": "TL"},
    {"name": "Venezuela, Bolivarian Republic of", "dial_code": "+58", "code": "VE"},
    {"name": "Viet Nam", "dial_code": "+84", "code": "VN"},
    {"name": "Virgin Islands, British", "dial_code": "+1 284", "code": "VG"},
    {"name": "Virgin Islands, U.S.", "dial_code": "+1 340", "code": "VI"}
]

class GuiLogger(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.queue = queue.Queue()
        self.text_widget.after(100, self.poll_log_queue)

    def emit(self, record):
        self.queue.put(self.format(record))

    def poll_log_queue(self):
        while True:
            try:
                record = self.queue.get(block=False)
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tk.END, record + '\n')
                self.text_widget.configure(state='disabled')
                self.text_widget.see(tk.END)
            except queue.Empty:
                break
        self.text_widget.after(100, self.poll_log_queue)

class ToolTip(object):
    """Create a tooltip for a given widget."""
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        self.tw = None

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tw, text=self.text, justify='left',
                       background='#ffffff', relief='solid', borderwidth=1,
                       font=("Segoe UI", 8))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

class VisaBotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visa Bot Professional")
        self.geometry("800x800")

        sv_ttk.set_theme("light")

        self.config = self.load_config()
        self.create_widgets()
        self.setup_logging()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.deiconify()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load config.json: {e}")
            return {"profiles": {}}

    def save_config(self):
         with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Header Frame
        header_frame = ttk.Frame(self, padding=(20, 10, 20, 20))
        header_frame.grid(row=0, column=0, sticky=tk.EW)
        header_frame.columnconfigure(1, weight=1)

        ttk.Label(header_frame, text="Profile:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=(0, 10), pady=5, sticky=tk.W)
        self.profile_var = tk.StringVar()
        self.profile_dropdown = ttk.Combobox(header_frame, textvariable=self.profile_var, font=('Segoe UI', 10), state="readonly")
        self.profile_dropdown['values'] = [''] + list(self.config.get('profiles', {}).keys())
        self.profile_dropdown.grid(row=0, column=1, sticky=tk.EW)
        self.profile_dropdown.bind("<<ComboboxSelected>>", self.on_profile_select)

        self.new_profile_btn = ttk.Button(header_frame, text="New", command=self.new_profile)
        self.new_profile_btn.grid(row=0, column=2, padx=(5,0))
        ToolTip(self.new_profile_btn, "Create a new blank profile")

        self.delete_profile_btn = ttk.Button(header_frame, text="Delete", command=self.delete_profile)
        self.delete_profile_btn.grid(row=0, column=3, padx=(5,0))
        ToolTip(self.delete_profile_btn, "Delete the selected profile")
        
        # Main content frame
        content_frame = ttk.Frame(self, padding=(20, 0, 20, 10))
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(0, weight=1)

        paned_window = ttk.PanedWindow(content_frame, orient=tk.VERTICAL)
        paned_window.grid(row=0, column=0, sticky="nsew")

        form_container = ttk.Frame(paned_window)
        form_container.columnconfigure(0, weight=1)
        paned_window.add(form_container, weight=3)
        
        self.fields = {}
        
        # --- Account Details Group ---
        account_group = ttk.LabelFrame(form_container, text="Account Details", padding=15)
        account_group.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))
        account_group.columnconfigure(1, weight=1)
        
        ttk.Label(account_group, text="Email:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        self.email_var = self._create_entry(account_group, 0, 1)
        self.fields['email'] = self.email_var

        ttk.Label(account_group, text="Password:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
        self.password_var = self._create_entry(account_group, 1, 1, show="*")
        self.fields['password'] = self.password_var

        # --- Application Details Group ---
        app_details_group = ttk.LabelFrame(form_container, text="Application Details", padding=15)
        app_details_group.grid(row=1, column=0, sticky=tk.EW, pady=10)
        app_details_group.columnconfigure(1, weight=1)
        
        ttk.Label(app_details_group, text="Center:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        self.fields['center'] = self._create_combobox(app_details_group, 0, 1, ["", "Cairo", "Alexandria"])
        
        ttk.Label(app_details_group, text="Visa Type:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
        visa_types = ["Tourism", "Business", "Family Visit", "Work", "Study"]
        self.fields['visa_type'] = self._create_combobox(app_details_group, 1, 1, visa_types)

        ttk.Label(app_details_group, text="Destination:").grid(row=2, column=0, padx=5, pady=8, sticky=tk.W)
        self.fields['destination'] = self._create_entry(app_details_group, 2, 1)

        ttk.Label(app_details_group, text="Service Level:").grid(row=3, column=0, padx=5, pady=8, sticky=tk.W)
        service_levels = ["Standard-EGP 1750", "VIP-EGP 3810"]
        self.fields['service_level'] = self._create_combobox(app_details_group, 3, 1, service_levels)

        ttk.Label(app_details_group, text="Number of Visas:").grid(row=4, column=0, padx=5, pady=8, sticky=tk.W)
        self.fields['num_visas'] = self._create_entry(app_details_group, 4, 1)

        # Log area frame
        log_container = ttk.LabelFrame(paned_window, text="Logs", padding=15)
        paned_window.add(log_container, weight=2)
        log_container.rowconfigure(0, weight=1)
        log_container.columnconfigure(0, weight=1)
        
        self.log_area = scrolledtext.ScrolledText(log_container, state='disabled', wrap=tk.WORD, height=10, font=("Consolas", 9))
        self.log_area.grid(row=0, column=0, sticky="nsew")
        
        # Footer Frame
        footer_frame = ttk.Frame(self, padding=(20, 10))
        footer_frame.grid(row=2, column=0, sticky=tk.EW)
        footer_frame.columnconfigure(1, weight=1)
        
        self.progress_bar = ttk.Progressbar(footer_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=tk.EW, padx=(0,10))

        self.save_btn = ttk.Button(footer_frame, text="Save Profile", command=self.save_profile)
        self.save_btn.grid(row=0, column=1, padx=5, sticky=tk.E)
        ToolTip(self.save_btn, "Save the current profile details")

        self.start_btn = ttk.Button(footer_frame, text="Start Bot", command=self.start_bot, style="Accent.TButton")
        self.start_btn.grid(row=0, column=2, padx=5, sticky=tk.E)
        ToolTip(self.start_btn, "Start the automation process")
    
    def _create_entry(self, parent, row, col, **kwargs):
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var, **kwargs)
        entry.grid(row=row, column=col, padx=5, pady=8, sticky=tk.EW)
        return var

    def _create_combobox(self, parent, row, col, values, **kwargs):
        var = tk.StringVar()
        combobox = ttk.Combobox(parent, textvariable=var, state="readonly", **kwargs)
        combobox['values'] = values
        combobox.grid(row=row, column=col, padx=5, pady=8, sticky=tk.EW)
        return var

    def _create_checkbox(self, parent, row, col, text, **kwargs):
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(parent, text=text, variable=var, **kwargs)
        checkbox.grid(row=row, column=col, padx=5, pady=8, sticky=tk.W)
        return var

    def _create_phone_entry(self, parent, row):
        ttk.Label(parent, text="Phone:").grid(row=row, column=0, padx=5, pady=8, sticky=tk.W)
        phone_frame = ttk.Frame(parent)
        phone_frame.grid(row=row, column=1, padx=5, pady=8, sticky=tk.EW)
        
        self.phone_code_var = tk.StringVar()
        code_cb = ttk.Combobox(phone_frame, textvariable=self.phone_code_var, width=8, state="readonly")
        code_cb['values'] = sorted([c['dial_code'] for c in COUNTRY_CODES if c['dial_code']])
        code_cb.set("+91")
        code_cb.pack(side=tk.LEFT, padx=(0, 5))

        self.phone_number_var = tk.StringVar()
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_number_var)
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.fields['phone'] = (self.phone_code_var, self.phone_number_var)

    def _create_dob_entry(self, parent, row):
        ttk.Label(parent, text="Date of Birth:").grid(row=row, column=0, padx=5, pady=8, sticky=tk.W)
        dob_frame = ttk.Frame(parent)
        dob_frame.grid(row=row, column=1, padx=5, pady=8, sticky=tk.EW)
        
        self.dob_day_var = self._create_combobox(dob_frame, 0, 0, [f"{d:02d}" for d in range(1, 32)])
        self.dob_day_var.set("Day")
        dob_frame.pack_propagate(False) # Prevent resizing
        
        self.dob_month_var = self._create_combobox(dob_frame, 0, 1, [f"{m:02d}" for m in range(1, 13)])
        self.dob_month_var.set("Month")

        self.dob_year_var = self._create_combobox(dob_frame, 0, 2, [str(y) for y in range(2024, 1939, -1)])
        self.dob_year_var.set("Year")

    def new_profile(self):
        self.profile_var.set('')
        self.on_profile_select()
        messagebox.showinfo("New Profile", "Fields cleared. Enter a new profile name and save.")

    def delete_profile(self):
        profile_name = self.profile_var.get()
        if not profile_name:
            messagebox.showwarning("Warning", "No profile selected to delete.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the profile '{profile_name}'?"):
            del self.config['profiles'][profile_name]
            self.save_config()
            self.profile_dropdown['values'] = [''] + list(self.config.get('profiles', {}).keys())
            self.new_profile()
            messagebox.showinfo("Success", f"Profile '{profile_name}' has been deleted.")

    def on_profile_select(self, event=None):
        profile_name = self.profile_var.get()
        profile_data = self.config.get('profiles', {}).get(profile_name)

        if not profile_data: # Handles new profile or clearing selection
            for key, var_or_tuple in self.fields.items():
                var_or_tuple.set('')
            return

        # Load data into fields
        for key, var_or_tuple in self.fields.items():
            var_or_tuple.set(profile_data.get(key, ''))

    def save_profile(self):
        profile_name = simpledialog.askstring("Save Profile", "Enter profile name:", initialvalue=self.profile_var.get(), parent=self)
        if not profile_name:
            return

        if profile_name not in self.config['profiles']:
             self.config['profiles'][profile_name] = {}
        
        for key, var_or_tuple in self.fields.items():
            self.config['profiles'][profile_name][key] = var_or_tuple.get()
        
        self.save_config()
        
        self.profile_dropdown['values'] = [''] + list(self.config.get('profiles', {}).keys())
        self.profile_var.set(profile_name)
        messagebox.showinfo("Success", f"Profile '{profile_name}' saved successfully.")

    def start_bot(self):
        profile_name = self.profile_var.get()
        if not profile_name:
            messagebox.showerror("Error", "Please select a profile before starting the bot.")
            return

        profile_data = self.config.get('profiles', {}).get(profile_name)
        proxy_config = self.config.get('proxy', {})
        almaviva_url = self.config.get('almaviva_url')
        selectors = self.config.get('selectors', {})
        
        self.set_ui_state('disabled')
        self.progress_bar.start()
        
        self.bot_thread = threading.Thread(
            target=self.run_automation_wrapper, 
            args=(profile_data, proxy_config, almaviva_url, selectors), 
            daemon=True
        )
        self.bot_thread.start()

    def run_automation_wrapper(self, *args):
        try:
            run_automation(*args, headless=False) # Always run visibly from GUI
        finally:
            self.after(0, self.on_bot_finished)

    def on_bot_finished(self):
        self.progress_bar.stop()
        self.set_ui_state('normal')
        messagebox.showinfo("Finished", "The bot has finished its task.")

    def set_ui_state(self, state):
        """Enable or disable all interactive widgets."""
        for widget in [self.start_btn, self.save_btn, self.profile_dropdown, self.new_profile_btn, self.delete_profile_btn]:
            widget.config(state=state)
        # You could extend this to disable all form entry fields as well if desired

    def setup_logging(self):
        log_handler = GuiLogger(self.log_area)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(log_handler)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            self.destroy()

if __name__ == "__main__":
    # Ensure country codes list is clean
    for item in COUNTRY_CODES:
        if item['dial_code'] is None:
            item['dial_code'] = ''
            
    app = VisaBotGUI()
    app.mainloop()
