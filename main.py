"""
🚀 Modern AI Gold Grid Trading System v5.0 - CLEAN & STABLE VERSION
main.py

🎯 OBJECTIVES:
✅ Clean, Simple & Working Architecture
✅ Proper Error Handling & Recovery
✅ Modular Component Integration
✅ Real-time GUI with Threading
✅ Production-ready Stability

🔧 FIXED ISSUES:
✅ Method Name Mismatches
✅ Component Integration Errors
✅ Threading Stability
✅ GUI Update Loops
✅ Error Handling

"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Import System Components - MATCH ACTUAL FILES
from mt5_connector import MT5Connector
from signal_generator import SignalGenerator                    
from position_monitor import PositionMonitor                    
from lot_calculator import LotCalculator, create_lot_calculator 
from performance_tracker import PerformanceTracker
from enhanced_risk_manager import EnhancedRiskManager
from capital_manager import CapitalManager, create_capital_manager          
from order_manager import OrderRoleManager, create_order_role_manager       
from order_manager import OrderManager, create_order_manager, integrate_order_manager_with_system

class ModernAITradingSystem:
    """
    🚀 Modern AI Gold Grid Trading System v5.0
    
    Clean & Stable Architecture:
    - Simple GUI with Essential Features
    - Robust Error Handling
    - Modular Component Loading
    - Thread-safe Operations
    """
    
    def __init__(self, root):
        """🎯 Initialize Clean Trading System"""
        
        self.root = root
        self.root.title("🚀 Modern AI Gold Trading System v5.0")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f1419")
        
        # Core System Variables
        self.config = self.load_config()
        self.is_trading = False
        self.trading_thread = None
        self.gui_update_active = True
        self.last_signal_time = datetime.now()
        
        # Terminal Management
        self.selected_terminal = None
        self.available_terminals = []
        
        # Initialize Core Components
        self.mt5_connector = MT5Connector()
        self.components = {}  # Dynamic component storage
        self.system_status = "🔄 Initializing..."
        
        # Trading Statistics
        self.stats = {
            'total_positions': 0,
            'net_profit': 0.0,
            'win_rate': 0.0,
            'last_signal': 'N/A'
        }
        
        # Setup GUI
        self.create_gui()
        self.start_gui_updates()
        
        # Log initialization
        self.log("🚀 Modern AI Trading System v5.0 Started")
        self.log("🎯 Clean Architecture Loaded")
        
    def load_config(self) -> Dict:
        """📋 Load Configuration"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config
            else:
                return self.get_default_config()
        except Exception as e:
            self.log(f"⚠️ Config load error: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """🔧 Default Configuration"""
        return {
            "trading": {
                "symbol": "XAUUSD.v",
                "timeframe": "M5",
                "max_positions": 50,
                "base_lot_size": 0.01
            },
            "risk_management": {
                "max_daily_loss": -500.0,
                "max_drawdown": 30.0,
                "stop_loss": 50.0,
                "take_profit": 100.0
            },
            "capital_management": {
                "initial_capital": 5000.0,
                "safe_zone_percent": 50,
                "growth_zone_percent": 35,
                "aggressive_zone_percent": 15
            }
        }

    # ==========================================
    # 🎨 GUI SETUP
    # ==========================================
    
    def create_gui(self):
        """🎨 Create Clean Modern GUI"""
        
        # Header
        self.create_header()
        
        # Main Content Area
        main_frame = tk.Frame(self.root, bg="#0f1419")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left Panel - Connection & Control
        left_frame = tk.Frame(main_frame, bg="#1e2328", width=350)
        left_frame.pack(side="left", fill="y", padx=(0, 5))
        left_frame.pack_propagate(False)
        
        self.create_connection_panel(left_frame)
        self.create_control_panel(left_frame)
        self.create_stats_panel(left_frame)
        
        # Right Panel - Logs & Information
        right_frame = tk.Frame(main_frame, bg="#1e2328")
        right_frame.pack(side="right", fill="both", expand=True)
        
        self.create_log_panel(right_frame)
        self.create_advanced_panel(right_frame)
        
    def create_header(self):
        """🎯 Create Header Section"""
        header_frame = tk.Frame(self.root, bg="#1a1a2e", height=60)
        header_frame.pack(fill="x", padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🚀 Modern AI Gold Trading System v5.0", 
            font=("Arial", 16, "bold"), 
            fg="#00d4aa", bg="#1a1a2e"
        )
        title_label.pack(side="left", padx=15, pady=15)
        
        # System Status
        self.status_label = tk.Label(
            header_frame, 
            text=self.system_status, 
            font=("Arial", 12, "bold"), 
            fg="#ffd700", bg="#1a1a2e"
        )
        self.status_label.pack(side="right", padx=15, pady=15)
    
    def create_connection_panel(self, parent):
        """🔌 MT5 Connection Panel with Terminal Scanner"""
        conn_frame = tk.LabelFrame(
            parent, text="🔌 MT5 Connection & Terminal Scanner", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1e2328"
        )
        conn_frame.pack(fill="x", padx=10, pady=5)
        
        # Connection Status
        self.connection_status = tk.Label(
            conn_frame, text="❌ Disconnected", 
            font=("Arial", 10, "bold"), fg="#ff4444", bg="#1e2328"
        )
        self.connection_status.pack(pady=5)
        
        # Terminal Scanner Buttons
        scanner_frame = tk.Frame(conn_frame, bg="#1e2328")
        scanner_frame.pack(pady=5, padx=10, fill="x")
        
        self.scan_button = tk.Button(
            scanner_frame, text="🔍 Scan Terminals", 
            command=self.scan_mt5_terminals,
            bg="#3498db", fg="white", font=("Arial", 9, "bold"),
            width=12
        )
        self.scan_button.pack(side="left", padx=2)
        
        self.connect_button = tk.Button(
            scanner_frame, text="🔌 Connect MT5", 
            command=self.connect_mt5,
            bg="#00aa44", fg="white", font=("Arial", 9, "bold"),
            width=12, state="disabled"
        )
        self.connect_button.pack(side="right", padx=2)
        
        # Account Info
        self.account_info = tk.Label(
            conn_frame, text="Account: --\nBalance: $--", 
            font=("Arial", 9), fg="#cccccc", bg="#1e2328", justify="left"
        )
        self.account_info.pack(pady=5)
        
        # Terminal Status
        self.terminal_status = tk.Label(
            conn_frame, text="🔍 Click 'Scan Terminals' to start", 
            font=("Arial", 8), fg="#888888", bg="#1e2328"
        )
        self.terminal_status.pack(pady=2)
    
    def create_control_panel(self, parent):
        """🎮 Trading Control Panel"""
        control_frame = tk.LabelFrame(
            parent, text="🎮 Trading Control", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1e2328"
        )
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Trading Buttons
        button_frame = tk.Frame(control_frame, bg="#1e2328")
        button_frame.pack(pady=10, padx=10)
        
        self.start_button = tk.Button(
            button_frame, text="🚀 Start Trading", 
            command=self.start_trading,
            bg="#00aa44", fg="white", font=("Arial", 11, "bold"),
            width=15
        )
        self.start_button.pack(pady=5, fill="x")
        
        self.stop_button = tk.Button(
            button_frame, text="🛑 Stop Trading", 
            command=self.stop_trading,
            bg="#cc3333", fg="white", font=("Arial", 11, "bold"),
            width=15, state="disabled"
        )
        self.stop_button.pack(pady=5, fill="x")
        
        # Initialize Components Button
        self.init_button = tk.Button(
            button_frame, text="🔄 Initialize Components", 
            command=self.initialize_components,
            bg="#3498db", fg="white", font=("Arial", 10),
            width=15, state="disabled"
        )
        self.init_button.pack(pady=5, fill="x")
        
        # Component Status Display
        self.component_status = tk.Label(
            control_frame, text="🔧 Components: Not Initialized", 
            font=("Arial", 9), fg="#888888", bg="#1e2328"
        )
        self.component_status.pack(pady=5)
    
    def create_stats_panel(self, parent):
        """📊 Statistics Panel"""
        stats_frame = tk.LabelFrame(
            parent, text="📊 Trading Statistics", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1e2328"
        )
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        # Statistics Labels
        self.positions_label = tk.Label(
            stats_frame, text="Positions: 0", 
            font=("Arial", 10), fg="#cccccc", bg="#1e2328"
        )
        self.positions_label.pack(anchor="w", padx=10, pady=2)
        
        self.profit_label = tk.Label(
            stats_frame, text="Net Profit: $0.00", 
            font=("Arial", 10), fg="#cccccc", bg="#1e2328"
        )
        self.profit_label.pack(anchor="w", padx=10, pady=2)
        
        self.winrate_label = tk.Label(
            stats_frame, text="Win Rate: 0.0%", 
            font=("Arial", 10), fg="#cccccc", bg="#1e2328"
        )
        self.winrate_label.pack(anchor="w", padx=10, pady=2)
        
        self.last_signal_label = tk.Label(
            stats_frame, text="Last Signal: N/A", 
            font=("Arial", 10), fg="#cccccc", bg="#1e2328"
        )
        self.last_signal_label.pack(anchor="w", padx=10, pady=2)
    
    def create_log_panel(self, parent):
        """📝 Log Panel"""
        log_frame = tk.LabelFrame(
            parent, text="📝 System Logs", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1e2328"
        )
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Log Text Area
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            font=("Consolas", 9),
            bg="#0f1419", fg="#cccccc",
            insertbackground="#cccccc",
            wrap=tk.WORD
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_advanced_panel(self, parent):
        """🔧 Advanced Options Panel"""
        advanced_frame = tk.LabelFrame(
            parent, text="🔧 Advanced Options", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1e2328"
        )
        advanced_frame.pack(fill="x", padx=10, pady=5)
        
        # Quick Actions
        actions_frame = tk.Frame(advanced_frame, bg="#1e2328")
        actions_frame.pack(pady=10, padx=10)
        
        self.close_all_button = tk.Button(
            actions_frame, text="🚨 Close All Positions", 
            command=self.close_all_positions,
            bg="#e74c3c", fg="white", font=("Arial", 9),
            width=20
        )
        self.close_all_button.pack(side="left", padx=5)
        
        self.refresh_button = tk.Button(
            actions_frame, text="🔄 Refresh Data", 
            command=self.refresh_data,
            bg="#17a2b8", fg="white", font=("Arial", 9),
            width=15
        )
        self.refresh_button.pack(side="right", padx=5)

    # ==========================================
    # 🔍 TERMINAL SCANNER & MT5 CONNECTION
    # ==========================================
    
    def scan_mt5_terminals(self):
        """🔍 สแกน MT5 Terminals"""
        try:
            self.log("🔍 Scanning for MT5 terminals...")
            self.system_status = "🔍 Scanning Terminals..."
            self.scan_button.config(state="disabled", text="🔄 Scanning...")
            
            # ใช้ threading เพื่อไม่ให้ GUI แขวน
            def scan_thread():
                try:
                    # สแกน terminals
                    terminals = self.mt5_connector.find_running_mt5_installations()
                    
                    # อัพเดท GUI ใน main thread
                    self.root.after(0, lambda: self._update_terminals_list(terminals))
                    
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda: self.log(f"❌ Terminal scan error: {error_msg}"))
                    self.root.after(0, lambda: self._on_scan_failed())
            
            threading.Thread(target=scan_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Scan terminals error: {e}")
            self._on_scan_failed()
    
    def _update_terminals_list(self, terminals):
        """📝 อัพเดทรายการ terminals"""
        try:
            self.scan_button.config(state="normal", text="🔍 Scan Terminals")
            
            if terminals:
                self.log(f"✅ Found {len(terminals)} MT5 terminals")
                self.system_status = f"✅ Found {len(terminals)} Terminal(s)"
                self.terminal_status.config(
                    text=f"✅ Found {len(terminals)} terminal(s) - Ready to select",
                    fg="#44ff44"
                )
                
                # เก็บรายการ terminals
                self.available_terminals = terminals
                
                # แสดง Terminal Selection Dialog
                self._show_terminal_selection_dialog(terminals)
                
            else:
                self.log("❌ No MT5 terminals found")
                self.system_status = "❌ No Terminals Found"
                self.terminal_status.config(
                    text="❌ No terminals found - Please open MT5 first",
                    fg="#ff4444"
                )
                
                # แสดง Help Message
                messagebox.showinfo(
                    "No Terminals Found", 
                    "ไม่พบ MT5 Terminals ที่ทำงานอยู่\n\n" +
                    "วิธีแก้ไข:\n" +
                    "1. เปิด MetaTrader 5 และ Login\n" +
                    "2. รอสักครู่ให้โปรแกรมเสถียร\n" +
                    "3. กด 'Scan Terminals' อีกครั้ง"
                )
                
        except Exception as e:
            self.log(f"❌ Terminal list update error: {e}")
            self._on_scan_failed()
    
    def _on_scan_failed(self):
        """❌ เมื่อ scan ล้มเหลว"""
        self.scan_button.config(state="normal", text="🔍 Scan Terminals")
        self.system_status = "❌ Scan Failed"
        self.terminal_status.config(
            text="❌ Scan failed - Check if MT5 is running",
            fg="#ff4444"
        )
    
    def _show_terminal_selection_dialog(self, terminals):
        """🖥️ แสดง Dialog เลือก MT5 Terminal"""
        try:
            # สร้างหน้าต่างเลือก Terminal
            selection_window = tk.Toplevel(self.root)
            selection_window.title("🔍 Select MT5 Terminal")
            selection_window.geometry("700x500")
            selection_window.configure(bg="#1a1a2e")
            selection_window.resizable(False, False)
            
            # ทำให้อยู่ด้านหน้า
            selection_window.transient(self.root)
            selection_window.grab_set()
            
            # Header
            header_frame = tk.Frame(selection_window, bg="#1a1a2e")
            header_frame.pack(fill="x", padx=15, pady=15)
            
            tk.Label(
                header_frame,
                text=f"🔍 Found {len(terminals)} MT5 Terminal(s)",
                font=("Arial", 16, "bold"), fg="#00d4aa", bg="#1a1a2e"
            ).pack()
            
            tk.Label(
                header_frame,
                text="Please select the terminal you want to connect to:",
                font=("Arial", 11), fg="#ffffff", bg="#1a1a2e"
            ).pack(pady=(8, 0))
            
            # Terminal List Frame
            list_frame = tk.Frame(selection_window, bg="#1a1a2e")
            list_frame.pack(fill="both", expand=True, padx=15, pady=10)
            
            # Listbox with Scrollbar
            listbox_frame = tk.Frame(list_frame, bg="#1a1a2e")
            listbox_frame.pack(fill="both", expand=True)
            
            scrollbar = tk.Scrollbar(listbox_frame)
            scrollbar.pack(side="right", fill="y")
            
            self.terminal_listbox = tk.Listbox(
                listbox_frame,
                font=("Consolas", 10),
                bg="#0f0f0f", fg="#ffffff",
                selectbackground="#3498db", selectforeground="#ffffff",
                yscrollcommand=scrollbar.set,
                height=15,
                selectmode=tk.SINGLE
            )
            self.terminal_listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=self.terminal_listbox.yview)
            
            # เพิ่มรายการ terminals
            for i, terminal in enumerate(terminals):
                try:
                    broker = getattr(terminal, 'broker', 'Unknown Broker')
                    exe_type = "64-bit" if "64" in str(getattr(terminal, 'executable_type', '')) else "32-bit"
                    status = "🟢 Running" if getattr(terminal, 'is_running', False) else "🔴 Stopped"
                    path = str(getattr(terminal, 'path', 'Unknown Path'))
                    path_short = "..." + path[-50:] if len(path) > 50 else path
                    
                    # Main terminal info
                    main_info = f"[{i+1:2d}] {broker} ({exe_type}) - {status}"
                    path_info = f"     📁 {path_short}"
                    
                    self.terminal_listbox.insert(tk.END, main_info)
                    self.terminal_listbox.insert(tk.END, path_info)
                    self.terminal_listbox.insert(tk.END, "")  # Separator
                    
                except Exception as e:
                    # Fallback display
                    self.terminal_listbox.insert(tk.END, f"[{i+1:2d}] Terminal {i+1} - Available")
                    self.terminal_listbox.insert(tk.END, f"     📁 {str(terminal)}")
                    self.terminal_listbox.insert(tk.END, "")
            
            # Buttons Frame
            button_frame = tk.Frame(selection_window, bg="#1a1a2e")
            button_frame.pack(fill="x", padx=15, pady=15)
            
            # Select Button
            def on_select():
                try:
                    selection = self.terminal_listbox.curselection()
                    if not selection:
                        messagebox.showwarning("No Selection", "Please select a terminal first!")
                        return
                    
                    # คำนวณ terminal index (เพราะมี separator lines)
                    selected_line = selection[0]
                    terminal_index = selected_line // 3  # 3 lines per terminal
                    
                    if terminal_index < len(terminals):
                        selected_terminal = terminals[terminal_index]
                        
                        # เก็บการเลือก
                        self.selected_terminal = selected_terminal
                        
                        # อัพเดท connector
                        if hasattr(self.mt5_connector, 'set_selected_terminal'):
                            self.mt5_connector.set_selected_terminal(selected_terminal)
                        
                        # อัพเดท GUI
                        broker_name = getattr(selected_terminal, 'broker', 'Selected Terminal')
                        self.log(f"✅ Selected: {broker_name}")
                        self.terminal_status.config(
                            text=f"✅ Selected: {broker_name} - Ready to connect",
                            fg="#44ff44"
                        )
                        
                        # เปิดใช้งาน Connect button
                        self.connect_button.config(
                            state="normal", 
                            text="🔗 Connect",
                            bg="#00aa44"
                        )
                        self.system_status = f"✅ Terminal Selected"
                        
                        # ปิดหน้าต่าง
                        selection_window.destroy()
                    
                except Exception as e:
                    self.log(f"❌ Terminal selection error: {e}")
                    messagebox.showerror("Selection Error", f"Failed to select terminal: {e}")
            
            # Connect Button
            tk.Button(
                button_frame, text="🔗 Select & Continue", 
                command=on_select,
                bg="#00d4aa", fg="white", font=("Arial", 12, "bold"),
                width=18, height=2
            ).pack(side="left", padx=5)
            
            # Cancel Button
            def on_cancel():
                selection_window.destroy()
                self.system_status = "❌ Selection Cancelled"
                self.terminal_status.config(
                    text="❌ Selection cancelled - Click scan to retry",
                    fg="#ff8888"
                )
            
            tk.Button(
                button_frame, text="❌ Cancel", 
                command=on_cancel,
                bg="#e74c3c", fg="white", font=("Arial", 12),
                width=12, height=2
            ).pack(side="right", padx=5)
            
            # เพิ่มคำแนะนำ
            tip_frame = tk.Frame(selection_window, bg="#1a1a2e")
            tip_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            tk.Label(
                tip_frame,
                text="💡 Tip: Double-click on a terminal to select it quickly",
                font=("Arial", 9), fg="#888888", bg="#1a1a2e"
            ).pack()
            
            # Double-click handler
            def on_double_click(event):
                on_select()
            
            self.terminal_listbox.bind("<Double-Button-1>", on_double_click)
            
            # Center the window
            selection_window.update_idletasks()
            x = (selection_window.winfo_screenwidth() // 2) - (selection_window.winfo_width() // 2)
            y = (selection_window.winfo_screenheight() // 2) - (selection_window.winfo_height() // 2)
            selection_window.geometry(f"+{x}+{y}")
            
            # Focus on first terminal
            if terminals:
                self.terminal_listbox.selection_set(0)
                self.terminal_listbox.focus_set()
            
        except Exception as e:
            self.log(f"❌ Terminal selection dialog error: {e}")
            messagebox.showerror("Dialog Error", f"Failed to show terminal selection: {e}")

    def connect_mt5(self):
        """🔗 เชื่อมต่อ MT5"""
        try:
            # ตรวจสอบว่าเลือก terminal แล้วหรือยัง
            if not hasattr(self, 'selected_terminal') or not self.selected_terminal:
                messagebox.showwarning(
                    "No Terminal Selected", 
                    "Please scan and select a terminal first!\n\n" +
                    "Steps:\n" +
                    "1. Click '🔍 Scan Terminals'\n" +
                    "2. Select a terminal from the list\n" +
                    "3. Click '🔗 Connect'"
                )
                return
            
            terminal = self.selected_terminal
            broker_name = getattr(terminal, 'broker', 'Selected Terminal')
            self.log(f"🔗 Connecting to: {broker_name}")
            self.system_status = "🔗 Connecting..."
            self.connect_button.config(state="disabled", text="🔄 Connecting...")
            
            def connect_thread():
                try:
                    # เชื่อมต่อ MT5
                    if hasattr(self.mt5_connector, 'connect_to_selected_terminal'):
                        success = self.mt5_connector.connect_to_selected_terminal(terminal)
                    else:
                        # Fallback to standard connection
                        success = self.mt5_connector.initialize()
                    
                    if success:
                        self.root.after(0, self._on_mt5_connected)
                    else:
                        self.root.after(0, self._on_mt5_connection_failed)
                        
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda: self.log(f"❌ MT5 connection error: {error_msg}"))
                    self.root.after(0, self._on_mt5_connection_failed)
            
            threading.Thread(target=connect_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Connect MT5 error: {e}")
            self._on_mt5_connection_failed()

    def _on_mt5_connected(self):
        """✅ เมื่อเชื่อมต่อ MT5 สำเร็จ"""
        try:
            self.log("✅ MT5 connected successfully!")
            self.system_status = "✅ MT5 Connected"
            
            # อัพเดท connection status
            self.connection_status.config(text="✅ Connected", fg="#44ff44")
            self.terminal_status.config(
                text="✅ Connected & Ready for trading",
                fg="#44ff44"
            )
            
            # อัพเดท buttons
            self.connect_button.config(
                state="normal", 
                text="🔌 Reconnect", 
                bg="#3498db"
            )
            self.scan_button.config(state="normal")
            self.init_button.config(state="normal")
            
            # อัพเดท account info
            self.update_account_info()
            
            # 🆕 AUTO-INITIALIZE COMPONENTS
            self.log("🔄 Auto-initializing AI components...")
            # ใช้ threading เพื่อไม่ให้ GUI แขวน
            threading.Thread(target=self.initialize_components, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ MT5 connected callback error: {e}")

    def _on_mt5_connection_failed(self):
        """❌ เมื่อเชื่อมต่อ MT5 ล้มเหลว"""
        try:
            self.log("❌ MT5 connection failed")
            self.system_status = "❌ Connection Failed"
            
            # อัพเดท GUI
            self.connection_status.config(text="❌ Connection Failed", fg="#ff4444")
            self.terminal_status.config(
                text="❌ Connection failed - Try reconnecting",
                fg="#ff4444"
            )
            
            # Reset buttons
            self.connect_button.config(
                state="normal", 
                text="🔗 Retry Connect",
                bg="#e74c3c"
            )
            
            # แสดง error message
            messagebox.showerror(
                "Connection Failed",
                "Failed to connect to MT5 terminal.\n\n" +
                "Please check:\n" +
                "1. MT5 is running and logged in\n" +
                "2. No other applications are using MT5\n" +
                "3. Try selecting a different terminal"
            )
            
        except Exception as e:
            self.log(f"❌ Connection failed callback error: {e}")
    
    def update_account_info(self):
        """💰 Update Account Information"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            account_info = self.mt5_connector.get_account_info()
            if account_info:
                login = account_info.get('login', '--')
                balance = account_info.get('balance', 0)
                equity = account_info.get('equity', 0)
                
                self.account_info.config(
                    text=f"Account: {login}\nBalance: ${balance:,.2f}\nEquity: ${equity:,.2f}"
                )
                
        except Exception as e:
            self.log(f"⚠️ Account info update error: {e}")

    # ==========================================
    # 🔄 COMPONENT MANAGEMENT
    # ==========================================
    
    def initialize_components(self):
        """🔄 Initialize Trading Components - WITH SMART ERROR HANDLING"""
        try:
            self.log("🔄 Initializing trading components...")
            
            if not self.mt5_connector.is_connected:
                self.log("❌ MT5 not connected. Cannot initialize components.")
                if hasattr(self, 'component_status'):
                    self.component_status.config(
                        text="❌ Components: MT5 Not Connected",
                        fg="#ff4444"
                    )
                messagebox.showerror("Error", "Please connect to MT5 first!")
                return
            
            # Show initializing status
            if hasattr(self, 'component_status'):
                self.component_status.config(
                    text="🔄 Components: Initializing...",
                    fg="#ffaa00"
                )
            
            # Initialize components safely
            self.components = {}
            initialization_success = 0
            total_components = 0
            
            # Try to initialize each component - ALL COMPONENTS SHOULD BE AVAILABLE
            components_to_init = [
                ('capital_manager', self.init_capital_manager),
                ('signal_generator', self.init_signal_generator),
                ('lot_calculator', self.init_lot_calculator),
                ('risk_manager', self.init_risk_manager),
                ('position_monitor', self.init_position_monitor),
                ('performance_tracker', self.init_performance_tracker)
            ]
            
            for comp_name, init_func in components_to_init:
                total_components += 1
                try:
                    if init_func():
                        initialization_success += 1
                        self.log(f"✅ {comp_name} initialized")
                    else:
                        self.log(f"⚠️ {comp_name} initialization failed")
                except Exception as e:
                    self.log(f"❌ {comp_name} error: {e}")
            
            # Update system status
            if initialization_success == total_components:
                self.system_status = f"🚀 System Ready ({initialization_success}/{total_components})"
                if hasattr(self, 'component_status'):
                    self.component_status.config(
                        text=f"✅ Components: All Ready ({initialization_success}/{total_components})",
                        fg="#44ff44"
                    )
                self.start_button.config(state="normal")
                self.log("🚀 All components initialized successfully!")
            else:
                self.system_status = f"⚠️ Partial Init ({initialization_success}/{total_components})"
                if hasattr(self, 'component_status'):
                    self.component_status.config(
                        text=f"⚠️ Components: Partial ({initialization_success}/{total_components})",
                        fg="#ffaa00"
                    )
                if initialization_success >= max(1, total_components // 2):
                    self.start_button.config(state="normal")
                    self.log("⚠️ System partially ready - basic trading enabled")
                else:
                    if hasattr(self, 'component_status'):
                        self.component_status.config(
                            text=f"❌ Components: Failed ({initialization_success}/{total_components})",
                            fg="#ff4444"
                        )
                    self.log("❌ Too many component failures - trading disabled")
            
        except Exception as e:
            self.log(f"❌ Component initialization error: {e}")
            self.system_status = "❌ Init Failed"
            if hasattr(self, 'component_status'):
                self.component_status.config(
                    text="❌ Components: Initialization Failed",
                    fg="#ff4444"
                )

    def init_capital_manager(self) -> bool:
        """💰 Initialize Capital Manager"""
        try:
            self.components['capital_manager'] = create_capital_manager(
                self.mt5_connector, 
                self.config
            )
            return self.components['capital_manager'] is not None
        except Exception as e:
            self.log(f"Capital Manager error: {e}")
            return False
    
    def init_signal_generator(self) -> bool:
        """📊 Initialize Signal Generator"""
        try:
            self.components['signal_generator'] = SignalGenerator(
                self.mt5_connector, 
                self.config
            )
            return self.components['signal_generator'] is not None
        except Exception as e:
            self.log(f"Signal Generator error: {e}")
            return False
    
    def init_lot_calculator(self) -> bool:
        """📏 Initialize Lot Calculator"""
        try:
            self.components['lot_calculator'] = create_lot_calculator(
                self.mt5_connector, 
                self.config
            )
            return self.components['lot_calculator'] is not None
        except Exception as e:
            self.log(f"Lot Calculator error: {e}")
            return False
    
    def init_risk_manager(self) -> bool:
        """🛡️ Initialize Risk Manager"""
        try:
            self.components['risk_manager'] = EnhancedRiskManager(
                self.mt5_connector, 
                self.config
            )
            return self.components['risk_manager'] is not None
        except Exception as e:
            self.log(f"Risk Manager error: {e}")
            return False
    
    def init_position_monitor(self) -> bool:
        """👁️ Initialize Position Monitor"""
        try:
            self.components['position_monitor'] = PositionMonitor(
                self.mt5_connector, 
                self.config
            )
            return self.components['position_monitor'] is not None
        except Exception as e:
            self.log(f"Position Monitor error: {e}")
            return False
    
    def init_performance_tracker(self) -> bool:
        """📈 Initialize Performance Tracker"""
        try:
            self.components['performance_tracker'] = PerformanceTracker(self.config)
            return self.components['performance_tracker'] is not None
        except Exception as e:
            self.log(f"Performance Tracker error: {e}")
            return False

    # ==========================================
    # 🎯 TRADING OPERATIONS
    # ==========================================
    
    def start_trading(self):
        """🚀 Start Trading System"""
        try:
            if self.is_trading:
                self.log("⚠️ Trading already running")
                return
            
            if not self.mt5_connector.is_connected:
                messagebox.showerror("Error", "Please connect to MT5 first!")
                return
            
            self.is_trading = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start trading thread
            self.trading_thread = threading.Thread(target=self.trading_loop, daemon=True)
            self.trading_thread.start()
            
            self.system_status = "🎯 Trading Active"
            self.log("🚀 Trading system started!")
            
        except Exception as e:
            self.log(f"❌ Start trading error: {e}")
            self.is_trading = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def stop_trading(self):
        """🛑 Stop Trading System"""
        try:
            if not self.is_trading:
                return
            
            self.is_trading = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            # Wait for trading thread to finish
            if self.trading_thread and self.trading_thread.is_alive():
                self.trading_thread.join(timeout=3.0)
            
            self.system_status = "🛑 Trading Stopped"
            self.log("🛑 Trading system stopped")
            
        except Exception as e:
            self.log(f"❌ Stop trading error: {e}")
    
    def trading_loop(self):
        """🔄 Main Trading Loop - Enhanced with Component Checking"""
        try:
            self.log("🔄 Trading loop started")
            
            loop_count = 0
            while self.is_trading:
                loop_start = time.time()
                loop_count += 1
                
                try:
                    # 1. Update account info
                    self.update_account_info()
                    
                    # 2. Update trading statistics 
                    self.update_trading_stats()
                    
                    # 3. Check if components are ready
                    components_ready = len(self.components) > 0
                    
                    if components_ready:
                        # 4. Generate signals (if available)
                        if 'signal_generator' in self.components:
                            try:
                                signals = self.components['signal_generator'].get_signals()
                                if signals:
                                    self.log(f"📊 Generated {len(signals)} signals")
                                    for signal in signals:
                                        self.process_signal(signal)
                                elif loop_count % 20 == 0:  # Log every 20 loops
                                    self.log("📊 No trading signals generated")
                            except Exception as sig_error:
                                self.log(f"⚠️ Signal generation error: {sig_error}")
                        
                        # 5. Monitor positions (if available)
                        if 'position_monitor' in self.components:
                            try:
                                self.components['position_monitor'].monitor_positions()
                            except Exception as mon_error:
                                self.log(f"⚠️ Position monitoring error: {mon_error}")
                        
                        # 6. Update performance (if available)
                        if 'performance_tracker' in self.components:
                            try:
                                self.components['performance_tracker'].update_session_metrics()
                            except Exception as perf_error:
                                self.log(f"⚠️ Performance tracking error: {perf_error}")
                    else:
                        # Components not ready - basic monitoring only
                        if loop_count % 30 == 0:  # Log every 30 loops (10 minutes)
                            self.log("⚠️ AI components not initialized - basic monitoring mode")
                            self.log("💡 Click '🔄 Initialize Components' to enable AI features")
                    
                    # 7. Simple market monitoring (always active)
                    if loop_count % 10 == 0:  # Every 10 loops
                        try:
                            symbol = self.config.get('trading', {}).get('symbol', 'XAUUSD.v')
                            import MetaTrader5 as mt5
                            tick = mt5.symbol_info_tick(symbol)
                            if tick:
                                self.log(f"💰 {symbol}: Bid={tick.bid}, Ask={tick.ask}")
                        except:
                            pass
                    
                    # 8. Sleep with adaptive timing
                    loop_duration = time.time() - loop_start
                    
                    if components_ready:
                        sleep_time = max(5, 15 - loop_duration)  # Active mode: 15 seconds
                    else:
                        sleep_time = max(10, 30 - loop_duration)  # Basic mode: 30 seconds
                    
                    time.sleep(sleep_time)
                    
                except Exception as loop_error:
                    self.log(f"⚠️ Trading loop iteration error: {loop_error}")
                    time.sleep(30)  # Longer sleep on error
                    
        except Exception as e:
            self.log(f"❌ Trading loop critical error: {e}")
        finally:
            self.log("🔄 Trading loop ended")
    
    def process_signal(self, signal: Dict):
        """🎯 Process Trading Signal"""
        try:
            action = signal.get('action', 'WAIT')
            
            if action == 'WAIT':
                return
            
            # Log signal
            strength = signal.get('strength', 0.0)
            price = signal.get('current_price', 0.0)
            self.log(f"📊 Signal: {action} | Strength: {strength:.3f} | Price: {price}")
            
            # Simple order placement (if components available)
            if 'lot_calculator' in self.components and 'risk_manager' in self.components:
                
                # Calculate lot size
                lot_size = self.components['lot_calculator'].calculate_lot_size(
                    signal.get('suggested_lot_size', 0.01)
                )
                
                # Risk check
                risk_check = self.components['risk_manager'].validate_trade(action, lot_size)
                
                if risk_check.get('approved', False):
                    # Place order
                    order_result = self.place_order(action, lot_size, price)
                    if order_result:
                        self.log(f"✅ Order placed: {action} {lot_size} lots at {price}")
                        self.last_signal_time = datetime.now()
                    else:
                        self.log(f"❌ Order placement failed")
                else:
                    self.log(f"🛡️ Trade blocked by risk management: {risk_check.get('reason', 'Unknown')}")
            else:
                self.log(f"📊 Signal received but components not ready for execution")
                
        except Exception as e:
            self.log(f"❌ Signal processing error: {e}")
    
    def place_order(self, action: str, lot_size: float, price: float) -> bool:
        """📋 Place Trading Order - FIXED METHOD CALLS"""
        try:
            symbol = self.config.get('trading', {}).get('symbol', 'XAUUSD.v')
            
            # FIXED: ใช้ MT5 library โดยตรงสำหรับการวาง order
            import MetaTrader5 as mt5
            
            # เตรียม request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot_size,
                "deviation": 20,
                "magic": 12345,  # Magic number
                "comment": f"AI Trade - {action}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # กำหนด type ตาม action
            if action.upper() == 'BUY':
                request["type"] = mt5.ORDER_TYPE_BUY
                request["price"] = mt5.symbol_info_tick(symbol).ask
            elif action.upper() == 'SELL':
                request["type"] = mt5.ORDER_TYPE_SELL
                request["price"] = mt5.symbol_info_tick(symbol).bid
            else:
                self.log(f"❌ Invalid action: {action}")
                return False
            
            # ส่ง order
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Order successful: {action} {lot_size} lots at {request['price']}")
                return True
            else:
                self.log(f"❌ Order failed: {result.retcode} - {result.comment}")
                return False
            
        except Exception as e:
            self.log(f"❌ Order placement error: {e}")
            return False

    # ==========================================
    # 📊 DATA UPDATE & STATISTICS
    # ==========================================
    
    def update_trading_stats(self):
        """📊 Update Trading Statistics - FIXED METHOD CALLS"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            # Get current positions - FIXED: ใช้ MT5 library โดยตรง
            positions = []
            try:
                import MetaTrader5 as mt5
                positions_raw = mt5.positions_get()
                
                if positions_raw:
                    for pos in positions_raw:
                        positions.append({
                            'ticket': pos.ticket,
                            'symbol': pos.symbol,
                            'type': 'BUY' if pos.type == 0 else 'SELL',
                            'volume': pos.volume,
                            'price_open': pos.price_open,
                            'profit': pos.profit,
                            'time': pos.time
                        })
            except Exception as e:
                self.log(f"⚠️ Failed to get positions: {e}")
                positions = []
            
            # Calculate statistics
            total_positions = len(positions)
            net_profit = sum([pos.get('profit', 0) for pos in positions])
            
            # Update stats
            self.stats['total_positions'] = total_positions
            self.stats['net_profit'] = net_profit
            self.stats['last_signal'] = self.last_signal_time.strftime("%H:%M:%S") if self.last_signal_time else "N/A"
            
            # Calculate win rate (simplified approach)
            try:
                if 'performance_tracker' in self.components:
                    perf_data = self.components['performance_tracker'].get_performance_summary()
                    self.stats['win_rate'] = perf_data.get('win_rate', 0.0)
                elif positions:
                    # Simple calculation: profitable positions / total positions
                    profitable = len([p for p in positions if p.get('profit', 0) > 0])
                    self.stats['win_rate'] = (profitable / total_positions * 100) if total_positions > 0 else 0.0
                else:
                    self.stats['win_rate'] = 0.0
            except Exception as e:
                self.stats['win_rate'] = 0.0
            
        except Exception as e:
            self.log(f"⚠️ Stats update error: {e}")
    
    def start_gui_updates(self):
        """🔄 Start GUI Update Thread"""
        def gui_update_loop():
            while self.gui_update_active:
                try:
                    if hasattr(self, 'root') and self.root.winfo_exists():
                        # Schedule updates on main thread
                        self.root.after(0, self.update_gui_elements)
                    time.sleep(2)  # Update every 2 seconds
                except:
                    break
        
        update_thread = threading.Thread(target=gui_update_loop, daemon=True)
        update_thread.start()
    
    def update_gui_elements(self):
        """🎨 Update GUI Elements (Main Thread)"""
        try:
            # Update system status
            if hasattr(self, 'status_label'):
                self.status_label.config(text=self.system_status)
            
            # Update statistics
            if hasattr(self, 'positions_label'):
                self.positions_label.config(text=f"Positions: {self.stats['total_positions']}")
            
            if hasattr(self, 'profit_label'):
                profit = self.stats['net_profit']
                color = "#44ff44" if profit >= 0 else "#ff4444"
                self.profit_label.config(text=f"Net Profit: ${profit:.2f}", fg=color)
            
            if hasattr(self, 'winrate_label'):
                self.winrate_label.config(text=f"Win Rate: {self.stats['win_rate']:.1f}%")
            
            if hasattr(self, 'last_signal_label'):
                self.last_signal_label.config(text=f"Last Signal: {self.stats['last_signal']}")
                
        except Exception as e:
            # Silently handle GUI update errors
            pass

    # ==========================================
    # 🔧 UTILITY FUNCTIONS
    # ==========================================
    
    def close_all_positions(self):
        """🚨 Close All Positions - FIXED METHOD CALLS"""
        try:
            if not self.mt5_connector.is_connected:
                messagebox.showerror("Error", "MT5 not connected!")
                return
            
            result = messagebox.askyesno(
                "Confirm", 
                "Are you sure you want to close ALL positions?"
            )
            
            if result:
                self.log("🚨 Closing all positions...")
                
                # FIXED: ใช้ MT5 library โดยตรงเพื่อปิด positions
                try:
                    import MetaTrader5 as mt5
                    positions = mt5.positions_get()
                    
                    if not positions:
                        self.log("ℹ️ No positions to close")
                        messagebox.showinfo("Info", "No positions to close")
                        return
                    
                    closed_count = 0
                    for pos in positions:
                        try:
                            # สร้าง close request
                            request = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": pos.symbol,
                                "volume": pos.volume,
                                "type": mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY,
                                "position": pos.ticket,
                                "deviation": 20,
                                "magic": 0,
                                "comment": "Emergency close all",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC,
                            }
                            
                            # ส่ง order
                            result = mt5.order_send(request)
                            if result.retcode == mt5.TRADE_RETCODE_DONE:
                                closed_count += 1
                                self.log(f"✅ Closed position {pos.ticket}")
                            else:
                                self.log(f"❌ Failed to close {pos.ticket}: {result.retcode}")
                                
                        except Exception as pos_error:
                            self.log(f"❌ Position close error {pos.ticket}: {pos_error}")
                    
                    self.log(f"✅ Closed {closed_count} out of {len(positions)} positions")
                    messagebox.showinfo("Success", f"Closed {closed_count} positions")
                    
                except Exception as close_error:
                    self.log(f"❌ Close all error: {close_error}")
                    messagebox.showerror("Error", f"Failed to close positions: {close_error}")
                
        except Exception as e:
            self.log(f"❌ Close all positions error: {e}")
            messagebox.showerror("Error", f"Failed to close positions: {e}")
    
    def refresh_data(self):
        """🔄 Refresh All Data"""
        try:
            self.log("🔄 Refreshing data...")
            self.update_account_info()
            self.update_trading_stats()
            self.log("✅ Data refreshed")
        except Exception as e:
            self.log(f"❌ Data refresh error: {e}")
    
    def log(self, message: str):
        """📝 Log Message"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            # Print to console
            print(log_entry.strip())
            
            # Add to GUI log (if available)
            if hasattr(self, 'log_text'):
                self.log_text.insert(tk.END, log_entry)
                self.log_text.see(tk.END)
                
                # Keep log size manageable
                lines = int(self.log_text.index('end-1c').split('.')[0])
                if lines > 1000:
                    self.log_text.delete('1.0', '500.0')
                    
        except Exception:
            # Silently handle logging errors
            pass
    
    def on_closing(self):
        """🚪 Handle Application Close"""
        try:
            self.gui_update_active = False
            
            if self.is_trading:
                result = messagebox.askyesno(
                    "Confirm Exit", 
                    "Trading is active. Stop trading and exit?"
                )
                if result:
                    self.stop_trading()
                else:
                    return
            
            self.log("👋 Shutting down Modern AI Trading System...")
            
            # Cleanup
            if hasattr(self, 'mt5_connector') and self.mt5_connector:
                self.mt5_connector.shutdown()
            
            self.root.quit()
            
        except Exception as e:
            print(f"Shutdown error: {e}")
            self.root.quit()

# ==========================================
# 🚀 APPLICATION ENTRY POINT
# ==========================================

def main():
    """🚀 Launch Modern AI Trading System v5.0"""
    
    print("=" * 60)
    print("🚀 Modern AI Gold Trading System v5.0")
    print("💎 Clean & Stable Architecture")
    print("🎯 Production-Ready Trading Platform")
    print("=" * 60)
    
    try:
        # Create and run application
        root = tk.Tk()
        app = ModernAITradingSystem(root)
        
        # Handle window closing
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Start application
        print("✅ Starting GUI...")
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
    
    print("👋 Modern AI Trading System shutdown complete")

if __name__ == "__main__":
    main()