"""
🎮 Enhanced AI Gold Grid Trading System v4.0 - CAPITAL + ROLE DASHBOARD
main.py

🆕 NEW FEATURES v4.0:
✅ Capital Dashboard (Zones, Drawdown, Trading Mode)
✅ Role Distribution Display (HG/PW/RH/SC)
✅ Recovery Panel (Suggestions & Actions)
✅ Risk Status Dashboard (Progressive Intelligence)
✅ One-click Actions (Emergency, Rebalance, Harvest)
✅ Integration กับ capital_manager + role_manager + enhanced_risk_manager

🎯 Modern Portfolio Management GUI
ไม่ซับซ้อน + ใช้งานง่าย + ข้อมูลครบถ้วน
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Import Enhanced System Components
from mt5_connector import MT5Connector
from signal_generator import EnhancedSignalGenerator  # v4.0
from order_manager import OrderManager
from position_monitor import EnhancedPositionMonitor  # v4.0
from lot_calculator import EnhancedLotCalculator  # v4.0
from performance_tracker import PerformanceTracker
from enhanced_risk_manager import EnhancedRiskManager  # v4.0
from capital_manager import CapitalManager  # 🆕
from order_manager import OrderRoleManager  # 🆕

class ModernAITradingGUI:
    """
    🎮 Modern AI Gold Grid Trading GUI v4.0
    
    🆕 Capital + Role Intelligence Dashboard:
    - Real-time Capital Status
    - Role Distribution Monitoring
    - Recovery Intelligence Panel
    - Progressive Risk Dashboard
    - One-click Portfolio Actions
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Modern AI Gold Grid Trading System v4.0")
        self.root.geometry("1600x1000")  # ขยายขนาดสำหรับ dashboard ใหม่
        self.root.configure(bg="#0f0f0f")  # สีพื้นหลังเข้มกว่า
        
        # ตัวแปรระบบ
        self.config = self.load_config()
        self.is_trading = False
        self.trading_thread = None
        self.gui_update_active = True
        
        # Initialize Traditional Components
        self.mt5_connector = MT5Connector()
        self.performance_tracker = None
        
        # 🆕 Initialize Enhanced Components
        self.capital_manager = None
        self.role_manager = None  
        self.enhanced_risk_manager = None
        self.enhanced_signal_generator = None
        self.enhanced_position_monitor = None
        self.enhanced_lot_calculator = None
        self.order_manager = None
        
        # 🆕 Dashboard Data Variables
        self.capital_status = {}
        self.role_distribution = {}
        self.risk_assessment = {}
        self.recovery_suggestions = {}
        self.portfolio_metrics = {}
        
        # Setup Enhanced GUI
        self.setup_modern_gui()
        self.start_enhanced_updates()
        
        # Log system start
        self.log("🚀 Modern AI Gold Grid Trading System v4.0 Started")
        self.log("💰 Capital Management: Enabled")
        self.log("🎭 Role Intelligence: Enabled") 
        self.log("🛡️ Enhanced Risk Management: Enabled")
        
        # Auto initialization
        self.initialize_enhanced_system()

    def load_config(self) -> Dict:
        """โหลดการตั้งค่าระบบ Enhanced"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.log("✅ Enhanced configuration loaded successfully")
                return config
        except Exception as e:
            self.log(f"❌ Error loading config: {e}")
            return self._get_default_enhanced_config()
    
    def _get_default_enhanced_config(self) -> Dict:
        """การตั้งค่าเริ่มต้นสำหรับ Enhanced System"""
        return {
            "trading": {
                "symbol": "XAUUSD.v",
                "timeframe": "M5",
                "max_positions": 50
            },
            "capital_management": {
                "initial_capital": 10000,
                "zones": {
                    "safe": {"allocation_percent": 50, "base_lot": 0.01, "max_lot": 0.05},
                    "growth": {"allocation_percent": 35, "base_lot": 0.02, "max_lot": 0.10},
                    "aggressive": {"allocation_percent": 15, "base_lot": 0.03, "max_lot": 0.20}
                },
                "drawdown_thresholds": {
                    "conservative": 20.0,
                    "emergency": 25.0,
                    "max": 30.0
                }
            },
            "order_roles": {
                "distribution": {
                    "HG": {"target_percentage": 25, "max_percentage": 30},
                    "PW": {"target_percentage": 40, "max_percentage": 45},
                    "RH": {"target_percentage": 20, "max_percentage": 25},
                    "SC": {"target_percentage": 15, "max_percentage": 20}
                }
            },
            "risk_management": {
                "max_positions": 50,
                "max_daily_trades": 80,
                "max_daily_loss": -300.0,
                "min_margin_level": 150.0
            }
        }
    
    def setup_modern_gui(self):
        """สร้าง Modern GUI Layout"""
        
        # ==========================================
        # 🎯 MODERN HEADER SECTION
        # ==========================================
        header_frame = tk.Frame(self.root, bg="#1a1a2e", height=70)
        header_frame.pack(fill="x", padx=5, pady=2)
        header_frame.pack_propagate(False)
        
        # Title และ Status
        title_label = tk.Label(
            header_frame, text="🚀 Modern AI Gold Grid Trading v4.0", 
            font=("Arial", 18, "bold"), fg="#00d4aa", bg="#1a1a2e"
        )
        title_label.pack(side="left", padx=15, pady=20)
        
        self.system_status_label = tk.Label(
            header_frame, text="🔍 Initializing System...", 
            font=("Arial", 11, "bold"), fg="#ffd700", bg="#1a1a2e"
        )
        self.system_status_label.pack(side="right", padx=15, pady=20)
        
        # ==========================================
        # 🔍 MT5 CONNECTION SECTION (Compact)
        # ==========================================
        connection_frame = tk.LabelFrame(
            self.root, text="🔍 MT5 Connection & Account", 
            font=("Arial", 10, "bold"), fg="#00d4aa", bg="#16213e"
        )
        connection_frame.pack(fill="x", padx=5, pady=2)
        
        self._setup_compact_mt5_panel(connection_frame)
        
        # ==========================================
        # 💰 CAPITAL + ROLE DASHBOARD (NEW!)
        # ==========================================
        dashboard_main_frame = tk.Frame(self.root, bg="#0f0f0f")
        dashboard_main_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        # Top Dashboard Row
        top_dashboard = tk.Frame(dashboard_main_frame, bg="#0f0f0f", height=200)
        top_dashboard.pack(fill="x", pady=2)
        top_dashboard.pack_propagate(False)
        
        self._setup_capital_dashboard(top_dashboard)
        self._setup_role_dashboard(top_dashboard)
        self._setup_risk_dashboard(top_dashboard)
        
        # Middle Dashboard Row
        middle_dashboard = tk.Frame(dashboard_main_frame, bg="#0f0f0f", height=250)
        middle_dashboard.pack(fill="x", pady=2)
        middle_dashboard.pack_propagate(False)
        
        self._setup_positions_table(middle_dashboard)
        self._setup_recovery_panel(middle_dashboard)
        
        # Bottom Dashboard Row  
        bottom_dashboard = tk.Frame(dashboard_main_frame, bg="#0f0f0f", height=180)
        bottom_dashboard.pack(fill="x", pady=2)
        bottom_dashboard.pack_propagate(False)
        
        self._setup_performance_panel(bottom_dashboard)
        self._setup_action_panel(bottom_dashboard)
        
        # ==========================================
        # 📝 LOG SECTION (Compact)
        # ==========================================
        log_frame = tk.LabelFrame(
            self.root, text="📝 System Log", 
            font=("Arial", 9, "bold"), fg="#00d4aa", bg="#16213e"
        )
        log_frame.pack(fill="x", padx=5, pady=2)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=4, font=("Consolas", 8),
            bg="#0a0a0a", fg="#cccccc", wrap="word"
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=3)
    
    # ==========================================
    # 🔍 COMPACT MT5 CONNECTION PANEL
    # ==========================================
    
    def _setup_compact_mt5_panel(self, parent):
        """🔍 Setup Compact MT5 Panel"""
        
        # Single row layout
        controls_frame = tk.Frame(parent, bg="#16213e")
        controls_frame.pack(fill="x", padx=10, pady=8)
        
        # MT5 Status
        self.mt5_status_label = tk.Label(
            controls_frame, text="🔴 Disconnected", 
            font=("Arial", 10, "bold"), fg="#ff6b6b", bg="#16213e"
        )
        self.mt5_status_label.pack(side="left", padx=5)
        
        # Quick Actions
        self.scan_button = tk.Button(
            controls_frame, text="🔍 Scan", command=self.scan_mt5_terminals,
            bg="#4a90e2", fg="white", font=("Arial", 9), width=8
        )
        self.scan_button.pack(side="left", padx=3)
        
        self.connect_button = tk.Button(
            controls_frame, text="🔗 Connect", command=self.connect_mt5,
            bg="#50c878", fg="white", font=("Arial", 9), width=8
        )
        self.connect_button.pack(side="left", padx=3)
        
        # Account Info
        self.account_info_label = tk.Label(
            controls_frame, text="Account: Not Connected", 
            font=("Consolas", 9), fg="#cccccc", bg="#16213e"
        )
        self.account_info_label.pack(side="right", padx=10)
        
        # Trading Controls
        self.start_button = tk.Button(
            controls_frame, text="🚀 Start Trading", command=self.start_trading,
            bg="#00d4aa", fg="white", font=("Arial", 10, "bold"), width=12
        )
        self.start_button.pack(side="right", padx=5)
        
        self.stop_button = tk.Button(
            controls_frame, text="🛑 Stop Trading", command=self.stop_trading,
            bg="#ff6b6b", fg="white", font=("Arial", 10, "bold"), width=12, state="disabled"
        )
        self.stop_button.pack(side="right", padx=3)
    
    # ==========================================
    # 💰 CAPITAL DASHBOARD (NEW!)
    # ==========================================
    
    def _setup_capital_dashboard(self, parent):
        """💰 Setup Capital Dashboard"""
        
        capital_frame = tk.LabelFrame(
            parent, text="💰 Capital Management", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e", width=520
        )
        capital_frame.pack(side="left", fill="both", expand=False, padx=3, pady=3)
        capital_frame.pack_propagate(False)
        
        # Capital Header
        header_frame = tk.Frame(capital_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=8, pady=5)
        
        self.capital_mode_label = tk.Label(
            header_frame, text="🟢 NORMAL MODE", 
            font=("Arial", 12, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.capital_mode_label.pack(side="left")
        
        self.drawdown_label = tk.Label(
            header_frame, text="Drawdown: 0.0%", 
            font=("Arial", 10), fg="#ffaa00", bg="#1a1a2e"
        )
        self.drawdown_label.pack(side="right")
        
        # Capital Zones Display
        zones_frame = tk.Frame(capital_frame, bg="#1a1a2e")
        zones_frame.pack(fill="x", padx=8, pady=3)
        
        tk.Label(zones_frame, text="Capital Zones:", 
                font=("Arial", 9, "bold"), fg="white", bg="#1a1a2e").pack(anchor="w")
        
        # Zone indicators
        zones_indicator_frame = tk.Frame(zones_frame, bg="#1a1a2e")
        zones_indicator_frame.pack(fill="x", pady=2)
        
        self.safe_zone_label = tk.Label(
            zones_indicator_frame, text="🟢 Safe 50%", 
            font=("Arial", 9), fg="#00ff88", bg="#1a1a2e"
        )
        self.safe_zone_label.pack(side="left", padx=5)
        
        self.growth_zone_label = tk.Label(
            zones_indicator_frame, text="🟡 Growth 35%", 
            font=("Arial", 9), fg="#ffd700", bg="#1a1a2e"
        )
        self.growth_zone_label.pack(side="left", padx=5)
        
        self.aggressive_zone_label = tk.Label(
            zones_indicator_frame, text="🔴 Aggressive 15%", 
            font=("Arial", 9), fg="#ff6b6b", bg="#1a1a2e"
        )
        self.aggressive_zone_label.pack(side="left", padx=5)
        
        # Capital Metrics
        metrics_frame = tk.Frame(capital_frame, bg="#1a1a2e")
        metrics_frame.pack(fill="x", padx=8, pady=3)
        
        self.capital_metrics_text = tk.Text(
            metrics_frame, height=5, font=("Consolas", 9),
            bg="#0a0a1a", fg="#cccccc", wrap="word", state="disabled"
        )
        self.capital_metrics_text.pack(fill="both", expand=True)
    
    def _setup_role_dashboard(self, parent):
        """🎭 Setup Role Distribution Dashboard"""
        
        role_frame = tk.LabelFrame(
            parent, text="🎭 Role Distribution", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e", width=400
        )
        role_frame.pack(side="left", fill="both", expand=False, padx=3, pady=3)
        role_frame.pack_propagate(False)
        
        # Role Header
        header_frame = tk.Frame(role_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=8, pady=5)
        
        self.role_balance_label = tk.Label(
            header_frame, text="Balance: GOOD", 
            font=("Arial", 11, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.role_balance_label.pack(side="left")
        
        self.total_positions_label = tk.Label(
            header_frame, text="Total: 0", 
            font=("Arial", 10), fg="#ffaa00", bg="#1a1a2e"
        )
        self.total_positions_label.pack(side="right")
        
        # Role Indicators
        roles_frame = tk.Frame(role_frame, bg="#1a1a2e")
        roles_frame.pack(fill="x", padx=8, pady=3)
        
        # สร้าง role indicators
        self.role_indicators = {}
        role_colors = {
            'HG': '#3498db',  # Blue - Hedge Guard
            'PW': '#2ecc71',  # Green - Profit Walker  
            'RH': '#e74c3c',  # Red - Recovery Hunter
            'SC': '#f39c12'   # Orange - Scalp Capture
        }
        
        for i, (role, color) in enumerate(role_colors.items()):
            role_row = tk.Frame(roles_frame, bg="#1a1a2e")
            role_row.pack(fill="x", pady=1)
            
            role_label = tk.Label(
                role_row, text=f"{role}:", 
                font=("Arial", 9, "bold"), fg=color, bg="#1a1a2e", width=4
            )
            role_label.pack(side="left")
            
            count_label = tk.Label(
                role_row, text="0 (0%)", 
                font=("Consolas", 9), fg="white", bg="#1a1a2e", width=12
            )
            count_label.pack(side="left", padx=5)
            
            performance_label = tk.Label(
                role_row, text="$0.00", 
                font=("Consolas", 9), fg="#ffaa00", bg="#1a1a2e"
            )
            performance_label.pack(side="right")
            
            self.role_indicators[role] = {
                'count': count_label,
                'performance': performance_label
            }
    
    def _setup_risk_dashboard(self, parent):
        """🛡️ Setup Risk Status Dashboard"""
        
        risk_frame = tk.LabelFrame(
            parent, text="🛡️ Risk Assessment", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e", width=350
        )
        risk_frame.pack(side="left", fill="both", expand=False, padx=3, pady=3)
        risk_frame.pack_propagate(False)
        
        # Risk Header
        header_frame = tk.Frame(risk_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=8, pady=5)
        
        self.risk_level_label = tk.Label(
            header_frame, text="🟢 LOW RISK", 
            font=("Arial", 12, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.risk_level_label.pack(side="left")
        
        self.risk_score_label = tk.Label(
            header_frame, text="Score: 0.00", 
            font=("Arial", 10), fg="#ffaa00", bg="#1a1a2e"
        )
        self.risk_score_label.pack(side="right")
        
        # Risk Metrics
        metrics_frame = tk.Frame(risk_frame, bg="#1a1a2e")
        metrics_frame.pack(fill="x", padx=8, pady=3)
        
        self.risk_metrics_text = tk.Text(
            metrics_frame, height=7, font=("Consolas", 8),
            bg="#0a0a1a", fg="#cccccc", wrap="word", state="disabled"
        )
        self.risk_metrics_text.pack(fill="both", expand=True)
    
    # ==========================================
    # 📊 POSITIONS TABLE (Enhanced)
    # ==========================================
    
    def _setup_positions_table(self, parent):
        """📊 Setup Enhanced Positions Table"""
        
        positions_frame = tk.LabelFrame(
            parent, text="📊 Active Positions (Role-Enhanced)", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e"
        )
        positions_frame.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        
        # Table Header
        header_frame = tk.Frame(positions_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=5, pady=3)
        
        self.positions_count_label = tk.Label(
            header_frame, text="Positions: 0", 
            font=("Arial", 10, "bold"), fg="#ffaa00", bg="#1a1a2e"
        )
        self.positions_count_label.pack(side="left")
        
        self.net_profit_label = tk.Label(
            header_frame, text="Net P/L: $0.00", 
            font=("Arial", 10, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.net_profit_label.pack(side="right")
        
        # Enhanced Treeview Table
        table_frame = tk.Frame(positions_frame, bg="#1a1a2e")
        table_frame.pack(fill="both", expand=True, padx=5, pady=3)
        
        # คอลัมน์ enhanced
        columns = ("Ticket", "Role", "Type", "Volume", "Price", "Current", "Profit", "Age", "Status")
        
        self.positions_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )
        
        # กำหนด column widths
        column_widths = {
            "Ticket": 80, "Role": 50, "Type": 60, "Volume": 70, 
            "Price": 80, "Current": 80, "Profit": 80, "Age": 60, "Status": 100
        }
        
        for col in columns:
            width = column_widths.get(col, 80)
            self.positions_tree.heading(col, text=col)
            self.positions_tree.column(col, width=width, minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.positions_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.positions_tree.xview)
        
        self.positions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table และ scrollbars
        self.positions_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
    
    # ==========================================
    # 🔄 RECOVERY PANEL (NEW!)
    # ==========================================
    
    def _setup_recovery_panel(self, parent):
        """🔄 Setup Recovery Intelligence Panel"""
        
        recovery_frame = tk.LabelFrame(
            parent, text="🔄 Recovery Intelligence", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e", width=350
        )
        recovery_frame.pack(side="right", fill="both", expand=False, padx=3, pady=3)
        recovery_frame.pack_propagate(False)
        
        # Recovery Header
        header_frame = tk.Frame(recovery_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=8, pady=5)
        
        self.recovery_status_label = tk.Label(
            header_frame, text="✅ No Recovery Needed", 
            font=("Arial", 10, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.recovery_status_label.pack()
        
        # Recovery Opportunities
        opps_frame = tk.Frame(recovery_frame, bg="#1a1a2e")
        opps_frame.pack(fill="x", padx=8, pady=3)
        
        tk.Label(opps_frame, text="Recovery Opportunities:", 
                font=("Arial", 9, "bold"), fg="white", bg="#1a1a2e").pack(anchor="w")
        
        self.recovery_opportunities_label = tk.Label(
            opps_frame, text="Profitable: 0 | Small Loss: 0", 
            font=("Consolas", 9), fg="#ffaa00", bg="#1a1a2e"
        )
        self.recovery_opportunities_label.pack(anchor="w", padx=10)
        
        # Quick Recovery Actions
        actions_frame = tk.Frame(recovery_frame, bg="#1a1a2e")
        actions_frame.pack(fill="x", padx=8, pady=5)
        
        tk.Label(actions_frame, text="Quick Actions:", 
                font=("Arial", 9, "bold"), fg="white", bg="#1a1a2e").pack(anchor="w")
        
        # Action buttons
        buttons_frame = tk.Frame(actions_frame, bg="#1a1a2e")
        buttons_frame.pack(fill="x", pady=3)
        
        self.harvest_profits_button = tk.Button(
            buttons_frame, text="🌾 Harvest", command=self.harvest_profits,
            bg="#2ecc71", fg="white", font=("Arial", 8), width=10
        )
        self.harvest_profits_button.pack(side="left", padx=2)
        
        self.rebalance_button = tk.Button(
            buttons_frame, text="⚖️ Rebalance", command=self.rebalance_portfolio,
            bg="#3498db", fg="white", font=("Arial", 8), width=10
        )
        self.rebalance_button.pack(side="left", padx=2)
        
        self.emergency_close_button = tk.Button(
            buttons_frame, text="🚨 Emergency", command=self.emergency_close_all,
            bg="#e74c3c", fg="white", font=("Arial", 8), width=10
        )
        self.emergency_close_button.pack(side="left", padx=2)
        
        # Recovery Suggestions
        suggestions_frame = tk.Frame(recovery_frame, bg="#1a1a2e")
        suggestions_frame.pack(fill="both", expand=True, padx=8, pady=3)
        
        tk.Label(suggestions_frame, text="Suggestions:", 
                font=("Arial", 9, "bold"), fg="white", bg="#1a1a2e").pack(anchor="w")
        
        self.recovery_suggestions_text = tk.Text(
            suggestions_frame, height=4, font=("Consolas", 8),
            bg="#0a0a1a", fg="#cccccc", wrap="word", state="disabled"
        )
        self.recovery_suggestions_text.pack(fill="both", expand=True, pady=2)
    
    # ==========================================
    # 📈 PERFORMANCE PANEL (Enhanced)
    # ==========================================
    
    def _setup_performance_panel(self, parent):
        """📈 Setup Enhanced Performance Panel"""
        
        performance_frame = tk.LabelFrame(
            parent, text="📈 Performance & Analytics", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e"
        )
        performance_frame.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        
        # Performance Metrics Grid
        metrics_grid = tk.Frame(performance_frame, bg="#1a1a2e")
        metrics_grid.pack(fill="x", padx=8, pady=5)
        
        # Row 1: Basic Metrics
        row1 = tk.Frame(metrics_grid, bg="#1a1a2e")
        row1.pack(fill="x", pady=2)
        
        self.net_profit_metric = tk.Label(
            row1, text="Net P/L: $0.00", 
            font=("Arial", 10, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.net_profit_metric.pack(side="left")
        
        self.win_rate_metric = tk.Label(
            row1, text="Win Rate: 0%", 
            font=("Arial", 10), fg="#ffaa00", bg="#1a1a2e"
        )
        self.win_rate_metric.pack(side="right")
        
        # Row 2: Advanced Metrics
        row2 = tk.Frame(metrics_grid, bg="#1a1a2e")
        row2.pack(fill="x", pady=2)
        
        self.avg_trade_metric = tk.Label(
            row2, text="Avg Trade: $0.00", 
            font=("Arial", 10), fg="#cccccc", bg="#1a1a2e"
        )
        self.avg_trade_metric.pack(side="left")
        
        self.profit_factor_metric = tk.Label(
            row2, text="P.Factor: 0.00", 
            font=("Arial", 10), fg="#cccccc", bg="#1a1a2e"
        )
        self.profit_factor_metric.pack(side="right")
        
        # Performance Chart Area
        chart_frame = tk.Frame(performance_frame, bg="#1a1a2e")
        chart_frame.pack(fill="both", expand=True, padx=8, pady=3)
        
        self.performance_chart_text = tk.Text(
            chart_frame, height=6, font=("Consolas", 8),
            bg="#0a0a1a", fg="#cccccc", wrap="word", state="disabled"
        )
        self.performance_chart_text.pack(fill="both", expand=True)
    
    def _setup_action_panel(self, parent):
        """🎯 Setup One-click Action Panel"""
        
        action_frame = tk.LabelFrame(
            parent, text="🎯 Portfolio Actions", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e", width=300
        )
        action_frame.pack(side="right", fill="both", expand=False, padx=3, pady=3)
        action_frame.pack_propagate(False)
        
        # Signal Status
        signal_frame = tk.Frame(action_frame, bg="#1a1a2e")
        signal_frame.pack(fill="x", padx=8, pady=5)
        
        tk.Label(signal_frame, text="Current Signal:", 
                font=("Arial", 9, "bold"), fg="white", bg="#1a1a2e").pack(anchor="w")
        
        self.current_signal_label = tk.Label(
            signal_frame, text="⏳ WAIT", 
            font=("Arial", 12, "bold"), fg="#ffaa00", bg="#1a1a2e"
        )
        self.current_signal_label.pack()
        
        self.signal_strength_label = tk.Label(
            signal_frame, text="Strength: 0%", 
            font=("Arial", 9), fg="#cccccc", bg="#1a1a2e"
        )
        self.signal_strength_label.pack()
        
        # Portfolio Actions
        actions_frame = tk.Frame(action_frame, bg="#1a1a2e")
        actions_frame.pack(fill="x", padx=8, pady=5)
        
        tk.Label(actions_frame, text="Portfolio Actions:", 
                font=("Arial", 9, "bold"), fg="white", bg="#1a1a2e").pack(anchor="w")
        
        # Action buttons grid
        button_grid = tk.Frame(actions_frame, bg="#1a1a2e")
        button_grid.pack(fill="x", pady=3)
        
        # Row 1
        row1 = tk.Frame(button_grid, bg="#1a1a2e")
        row1.pack(fill="x", pady=1)
        
        self.close_profits_button = tk.Button(
            row1, text="💰 Close Profits", command=self.close_profitable_positions,
            bg="#2ecc71", fg="white", font=("Arial", 8), width=12
        )
        self.close_profits_button.pack(side="left", padx=1)
        
        self.close_losses_button = tk.Button(
            row1, text="💸 Close Losses", command=self.close_losing_positions,
            bg="#e74c3c", fg="white", font=("Arial", 8), width=12
        )
        self.close_losses_button.pack(side="right", padx=1)
        
        # Row 2
        row2 = tk.Frame(button_grid, bg="#1a1a2e")
        row2.pack(fill="x", pady=1)
        
        self.optimize_margin_button = tk.Button(
            row2, text="📊 Optimize Margin", command=self.optimize_margin,
            bg="#3498db", fg="white", font=("Arial", 8), width=12
        )
        self.optimize_margin_button.pack(side="left", padx=1)
        
        self.balance_volume_button = tk.Button(
            row2, text="⚖️ Balance Volume", command=self.balance_volume,
            bg="#9b59b6", fg="white", font=("Arial", 8), width=12
        )
        self.balance_volume_button.pack(side="right", padx=1)
        
        # System Status
        status_frame = tk.Frame(action_frame, bg="#1a1a2e")
        status_frame.pack(fill="x", padx=8, pady=5)
        
        self.system_health_label = tk.Label(
            status_frame, text="System Health: ✅", 
            font=("Arial", 9, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.system_health_label.pack()
        
        self.last_update_label = tk.Label(
            status_frame, text="Last Update: --:--:--", 
            font=("Arial", 8), fg="#888888", bg="#1a1a2e"
        )
        self.last_update_label.pack()
    
    # ==========================================
    # 🔄 ENHANCED SYSTEM INITIALIZATION
    # ==========================================
    
    def initialize_enhanced_system(self):
        """🔄 เริ่มต้นระบบ Enhanced Components"""
        try:
            if not self.mt5_connector.is_connected:
                self.log("⏳ Waiting for MT5 connection...")
                return
            
            self.log("🔄 Initializing Enhanced AI Components...")
            
            # 1. สร้าง Capital Manager
            self.capital_manager = CapitalManager(self.config)
            self.log("💰 Capital Manager initialized")
            
            # 2. สร้าง Role Manager
            self.role_manager = OrderRoleManager(self.mt5_connector, self.config)
            self.log("🎭 Role Manager initialized")
            
            # 3. สร้าง Enhanced Risk Manager
            self.enhanced_risk_manager = EnhancedRiskManager(
                self.mt5_connector, self.config,
                capital_manager=self.capital_manager,
                role_manager=self.role_manager
            )
            self.log("🛡️ Enhanced Risk Manager initialized")
            
            # 4. สร้าง Enhanced Signal Generator  
            self.enhanced_signal_generator = EnhancedSignalGenerator(
                self.mt5_connector, self.config,
                capital_manager=self.capital_manager,
                role_manager=self.role_manager
            )
            self.log("🎯 Enhanced Signal Generator initialized")
            
            # 5. สร้าง Enhanced Position Monitor
            self.enhanced_position_monitor = EnhancedPositionMonitor(
                self.mt5_connector, self.config,
                capital_manager=self.capital_manager,
                role_manager=self.role_manager
            )
            self.log("📊 Enhanced Position Monitor initialized")
            
            # 6. สร้าง Enhanced Lot Calculator
            self.enhanced_lot_calculator = EnhancedLotCalculator(
                self.mt5_connector, self.config,
                capital_manager=self.capital_manager,
                role_manager=self.role_manager
            )
            self.log("💹 Enhanced Lot Calculator initialized")
            
            # 7. สร้าง Order Manager (if needed)
            if not self.order_manager:
                self.order_manager = OrderManager(self.mt5_connector, self.config)
                self.log("📝 Order Manager initialized")
            
            # 8. สร้าง Performance Tracker
            if not self.performance_tracker:
                self.performance_tracker = PerformanceTracker(self.mt5_connector, self.config)
                self.log("📈 Performance Tracker initialized")
            
            # Set cross-references
            if self.enhanced_signal_generator:
                self.enhanced_signal_generator.set_risk_manager(self.enhanced_risk_manager)
            
            self.log("✅ Enhanced AI System initialized successfully!")
            self.update_system_status("✅ Enhanced AI System Ready")
            
        except Exception as e:
            self.log(f"❌ Enhanced system initialization error: {e}")
            self.update_system_status("❌ System Error")
    
    # ==========================================
    # 🔄 ENHANCED UPDATE METHODS
    # ==========================================
    
    def start_enhanced_updates(self):
        """🔄 เริ่ม Enhanced GUI Updates"""
        
        def enhanced_update_loop():
            """🔄 Enhanced Update Loop"""
            while self.gui_update_active:
                try:
                    # อัพเดทแบบ interval ต่างกัน
                    current_time = datetime.now()
                    
                    # ทุก 2 วินาที - ข้อมูลพื้นฐาน
                    if current_time.second % 2 == 0:
                        self.update_basic_displays()
                    
                    # ทุก 5 วินาที - capital + role
                    if current_time.second % 5 == 0:
                        self.update_capital_dashboard()
                        self.update_role_dashboard()
                    
                    # ทุก 10 วินาที - risk + recovery
                    if current_time.second % 10 == 0:
                        self.update_risk_dashboard()
                        self.update_recovery_panel()
                    
                    # ทุก 15 วินาที - performance
                    if current_time.second % 15 == 0:
                        self.update_performance_panel()
                    
                    # ทุกนาที - positions table
                    if current_time.second == 0:
                        self.update_enhanced_positions_table()
                    
                    time.sleep(1)
                    
                except Exception as e:
                    self.log(f"❌ Enhanced update error: {e}")
                    time.sleep(5)  # หน่วงเมื่อเกิดข้อผิดพลาด
        
        update_thread = threading.Thread(target=enhanced_update_loop, daemon=True)
        update_thread.start()
        self.log("🔄 Enhanced GUI updates started")
    
    def update_basic_displays(self):
        """📊 อัพเดทข้อมูลพื้นฐาน"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            # อัพเดท timestamp
            current_time = datetime.now().strftime("%H:%M:%S")
            self.last_update_label.config(text=f"Last Update: {current_time}")
            
            # อัพเดท account info
            account_info = self.mt5_connector.get_account_info()
            if account_info:
                balance = account_info.get('balance', 0)
                equity = account_info.get('equity', 0)
                free_margin = account_info.get('free_margin', 0)
                
                account_text = f"Balance: ${balance:.2f} | Equity: ${equity:.2f} | Free: ${free_margin:.2f}"
                self.account_info_label.config(text=account_text)
            
        except Exception as e:
            pass  # Silent fail for basic updates
    
    def update_capital_dashboard(self):
        """💰 อัพเดท Capital Dashboard"""
        try:
            if not self.capital_manager:
                return
            
            # ดึง capital status
            capital_status = self.capital_manager.get_capital_status()
            self.capital_status = capital_status
            
            # อัพเดท trading mode
            trading_mode = capital_status.get('trading_mode', 'normal')
            drawdown = capital_status.get('current_drawdown_percent', 0)
            
            mode_colors = {
                'normal': ('#00ff88', '🟢'),
                'conservative': ('#ffd700', '🟡'), 
                'emergency': ('#ff6b6b', '🔴'),
                'recovery': ('#00d4aa', '🔄')
            }
            
            color, emoji = mode_colors.get(trading_mode, ('#cccccc', '⚪'))
            self.capital_mode_label.config(
                text=f"{emoji} {trading_mode.upper()} MODE",
                fg=color
            )
            
            # อัพเดท drawdown
            drawdown_color = '#00ff88' if drawdown < 10 else '#ffd700' if drawdown < 20 else '#ff6b6b'
            self.drawdown_label.config(
                text=f"Drawdown: {drawdown:.1f}%",
                fg=drawdown_color
            )
            
            # อัพเดท zone status
            available_zones = capital_status.get('available_zones', [])
            
            # Reset colors
            for zone_label in [self.safe_zone_label, self.growth_zone_label, self.aggressive_zone_label]:
                zone_label.config(fg="#666666")
            
            # Highlight available zones
            if 'safe' in available_zones:
                self.safe_zone_label.config(fg="#00ff88")
            if 'growth' in available_zones:
                self.growth_zone_label.config(fg="#ffd700")
            if 'aggressive' in available_zones:
                self.aggressive_zone_label.config(fg="#ff6b6b")
            
            # อัพเดท capital metrics
            zone_utilization = capital_status.get('zone_utilization', {})
            capital_efficiency = capital_status.get('capital_efficiency', 0)
            
            metrics_text = f"""Capital Efficiency: {capital_efficiency:.2f}
Zone Utilization:
• Safe Zone: {zone_utilization.get('safe_percent', 0):.1f}%
• Growth Zone: {zone_utilization.get('growth_percent', 0):.1f}%  
• Aggressive Zone: {zone_utilization.get('aggressive_percent', 0):.1f}%

Available Capital: ${capital_status.get('available_capital', 0):.2f}
Reserved Capital: ${capital_status.get('reserved_capital', 0):.2f}"""
            
            self.capital_metrics_text.config(state="normal")
            self.capital_metrics_text.delete(1.0, tk.END)
            self.capital_metrics_text.insert(tk.END, metrics_text)
            self.capital_metrics_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Capital dashboard update error: {e}")
    
    def update_role_dashboard(self):
        """🎭 อัพเดท Role Distribution Dashboard"""
        try:
            if not self.role_manager:
                return
            
            # ดึง role distribution
            role_status = self.role_manager.get_role_distribution()
            self.role_distribution = role_status
            
            role_counts = role_status.get('role_counts', {})
            total_positions = role_status.get('total_positions', 0)
            balance_quality = role_status.get('balance_quality', 'unknown')
            
            # อัพเดท total positions
            self.total_positions_label.config(text=f"Total: {total_positions}")
            
            # อัพเดท balance status
            balance_colors = {
                'excellent': '#00ff88',
                'good': '#00d4aa',
                'fair': '#ffd700',
                'poor': '#ff6b6b'
            }
            
            balance_color = balance_colors.get(balance_quality, '#cccccc')
            self.role_balance_label.config(
                text=f"Balance: {balance_quality.upper()}",
                fg=balance_color
            )
            
            # อัพเดท role indicators
            for role in ['HG', 'PW', 'RH', 'SC']:
                count = role_counts.get(role, 0)
                percentage = (count / total_positions * 100) if total_positions > 0 else 0
                
                # อัพเดท count
                self.role_indicators[role]['count'].config(text=f"{count} ({percentage:.0f}%)")
                
                # อัพเดท performance (ถ้ามี position monitor)
                if self.enhanced_position_monitor:
                    role_performance = self.enhanced_position_monitor.get_role_performance()
                    role_profit = role_performance.get(role, {}).get('total_profit', 0)
                    
                    profit_color = '#00ff88' if role_profit > 0 else '#ff6b6b' if role_profit < 0 else '#ffaa00'
                    self.role_indicators[role]['performance'].config(
                        text=f"${role_profit:.2f}",
                        fg=profit_color
                    )
            
        except Exception as e:
            self.log(f"❌ Role dashboard update error: {e}")
    
    def update_risk_dashboard(self):
        """🛡️ อัพเดท Risk Status Dashboard"""
        try:
            if not self.enhanced_risk_manager:
                return
            
            # ดึง risk assessment
            risk_status = self.enhanced_risk_manager.check_risk_levels()
            self.risk_assessment = risk_status
            
            # อัพเดท risk level
            overall_risk = risk_status.get('overall_risk', 'unknown')
            risk_score = risk_status.get('risk_score', 0)
            
            risk_colors = {
                'low': ('#00ff88', '🟢'),
                'medium': ('#ffd700', '🟡'),
                'high': ('#ff6b6b', '🟠'),
                'critical': ('#ff3333', '🔴'),
                'emergency': ('#ff0000', '🚨')
            }
            
            color, emoji = risk_colors.get(overall_risk, ('#cccccc', '⚪'))
            self.risk_level_label.config(
                text=f"{emoji} {overall_risk.upper()} RISK",
                fg=color
            )
            
            self.risk_score_label.config(text=f"Score: {risk_score:.2f}")
            
            # อัพเดท risk metrics
            warnings = risk_status.get('warnings', [])
            restrictions = risk_status.get('restrictions', [])
            
            metrics_text = f"""Can Trade: {'✅' if risk_status.get('can_trade', False) else '❌'}
Emergency Stop: {'🚨' if risk_status.get('emergency_stop', False) else '✅'}

Active Warnings: {len(warnings)}
Active Restrictions: {len(restrictions)}

Recent Warnings:"""
            
            # แสดง warnings ล่าสุด
            for warning in warnings[-3:]:
                metrics_text += f"\n• {warning[:40]}..."
            
            if restrictions:
                metrics_text += f"\n\nRestrictions:"
                for restriction in restrictions[-2:]:
                    metrics_text += f"\n• {restriction[:35]}..."
            
            self.risk_metrics_text.config(state="normal")
            self.risk_metrics_text.delete(1.0, tk.END)
            self.risk_metrics_text.insert(tk.END, metrics_text)
            self.risk_metrics_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Risk dashboard update error: {e}")
    
    def update_recovery_panel(self):
        """🔄 อัพเดท Recovery Intelligence Panel"""
        try:
            if not self.enhanced_risk_manager:
                return
            
            # ดึง recovery recommendations
            recovery_data = self.enhanced_risk_manager.get_recovery_recommendations()
            self.recovery_suggestions = recovery_data
            
            # อัพเดท recovery status
            recovery_mode = recovery_data.get('recovery_mode', False)
            
            if recovery_mode:
                self.recovery_status_label.config(
                    text="🔄 Recovery Mode Active",
                    fg="#ff6b6b"
                )
            else:
                self.recovery_status_label.config(
                    text="✅ No Recovery Needed", 
                    fg="#00ff88"
                )
            
            # อัพเดท recovery opportunities
            if self.enhanced_position_monitor:
                # ดึงข้อมูล opportunities
                positions = self.mt5_connector.get_positions()
                if positions:
                    profitable_count = len([p for p in positions if p.get('profit', 0) >= 1.0])
                    small_loss_count = len([p for p in positions if -10 <= p.get('profit', 0) < 0])
                    
                    self.recovery_opportunities_label.config(
                        text=f"Profitable: {profitable_count} | Small Loss: {small_loss_count}"
                    )
            
            # อัพเดท suggestions
            suggestions = recovery_data.get('suggested_actions', [])
            
            suggestions_text = ""
            if recovery_mode and suggestions:
                suggestions_text = "Active Recommendations:\n"
                for i, suggestion in enumerate(suggestions[:4]):
                    suggestions_text += f"{i+1}. {suggestion}\n"
            else:
                suggestions_text = "Portfolio Status: Healthy\n\nNo recovery actions needed.\n\nSystem operating normally."
            
            self.recovery_suggestions_text.config(state="normal")
            self.recovery_suggestions_text.delete(1.0, tk.END)
            self.recovery_suggestions_text.insert(tk.END, suggestions_text)
            self.recovery_suggestions_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Recovery panel update error: {e}")
    
    def update_enhanced_positions_table(self):
        """📊 อัพเดท Enhanced Positions Table"""
        try:
            # Clear existing data
            for item in self.positions_tree.get_children():
                self.positions_tree.delete(item)
            
            # ดึงข้อมูล positions
            positions = self.mt5_connector.get_positions()
            if not positions:
                self.positions_count_label.config(text="Positions: 0")
                self.net_profit_label.config(text="Net P/L: $0.00")
                return
            
            # คำนวณ metrics
            total_positions = len(positions)
            total_profit = sum([p.get('profit', 0) for p in positions])
            
            # อัพเดท header
            self.positions_count_label.config(text=f"Positions: {total_positions}")
            
            profit_color = '#00ff88' if total_profit > 0 else '#ff6b6b' if total_profit < 0 else '#ffaa00'
            self.net_profit_label.config(
                text=f"Net P/L: ${total_profit:.2f}",
                fg=profit_color
            )
            
            # เพิ่ม positions ลงใน table
            for position in positions:
                # ดึง role จาก role manager
                role = "Unknown"
                if self.role_manager:
                    role = self.role_manager.get_position_role(position.get('ticket', 0))
                
                # คำนวณ age
                open_time = position.get('time', datetime.now())
                if isinstance(open_time, (int, float)):
                    open_time = datetime.fromtimestamp(open_time)
                
                age = datetime.now() - open_time
                age_str = f"{age.total_seconds()/3600:.1f}h"
                
                # กำหนด status
                profit = position.get('profit', 0)
                if profit >= 5.0:
                    status = "🔥 Strong"
                elif profit >= 1.0:
                    status = "✅ Profit"
                elif profit >= -5.0:
                    status = "⏳ Hold"
                elif profit >= -20.0:
                    status = "⚠️ Watch"
                else:
                    status = "🚨 Risk"
                
                # เพิ่มลงใน tree
                values = (
                    position.get('ticket', 0),
                    role,
                    'BUY' if position.get('type', 0) == 0 else 'SELL',
                    f"{position.get('volume', 0):.2f}",
                    f"{position.get('price_open', 0):.5f}",
                    f"{position.get('price_current', 0):.5f}",
                    f"${profit:.2f}",
                    age_str,
                    status
                )
                
                self.positions_tree.insert("", "end", values=values)
            
        except Exception as e:
            self.log(f"❌ Positions table update error: {e}")
    
    def update_performance_panel(self):
        """📈 อัพเดท Performance Panel"""
        try:
            if not self.performance_tracker:
                return
            
            # ดึงข้อมูล performance
            session_metrics = self.performance_tracker.get_session_metrics()
            
            # อัพเดท basic metrics
            net_profit = session_metrics.get('net_profit', 0)
            win_rate = session_metrics.get('profitable_trade_percent', 0)
            avg_trade = session_metrics.get('average_trade', 0)
            profit_factor = session_metrics.get('profit_factor', 0)
            
            # อัพเดท labels
            profit_color = '#00ff88' if net_profit > 0 else '#ff6b6b' if net_profit < 0 else '#ffaa00'
            self.net_profit_metric.config(text=f"Net P/L: ${net_profit:.2f}", fg=profit_color)
            
            win_color = '#00ff88' if win_rate >= 60 else '#ffd700' if win_rate >= 40 else '#ff6b6b'
            self.win_rate_metric.config(text=f"Win Rate: {win_rate:.0f}%", fg=win_color)
            
            self.avg_trade_metric.config(text=f"Avg Trade: ${avg_trade:.2f}")
            self.profit_factor_metric.config(text=f"P.Factor: {profit_factor:.2f}")
            
            # Performance chart/text
            chart_text = f"""📊 Session Performance Summary:

Total Trades: {session_metrics.get('total_trades', 0)}
Winning Trades: {session_metrics.get('winning_trades', 0)}
Losing Trades: {session_metrics.get('losing_trades', 0)}

Gross Profit: ${session_metrics.get('gross_profit', 0):.2f}
Gross Loss: ${session_metrics.get('gross_loss', 0):.2f}

ROI: {session_metrics.get('roi_percent', 0):.2f}%
Max Consecutive Wins: {session_metrics.get('max_consecutive_wins', 0)}
Max Consecutive Losses: {session_metrics.get('max_consecutive_losses', 0)}"""
            
            self.performance_chart_text.config(state="normal")
            self.performance_chart_text.delete(1.0, tk.END)
            self.performance_chart_text.insert(tk.END, chart_text)
            self.performance_chart_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Performance panel update error: {e}")
    
    # ==========================================
    # 🔍 MT5 CONNECTION METHODS (Streamlined)
    # ==========================================
    
    def scan_mt5_terminals(self):
        """🔍 สแกน MT5 Terminals"""
        try:
            self.log("🔍 Scanning for MT5 terminals...")
            self.update_system_status("🔍 Scanning...")
            
            # ใช้ threading เพื่อไม่ให้ GUI แขวน
            def scan_thread():
                try:
                    terminals = self.mt5_connector.scan_terminals()
                    
                    # อัพเดท GUI ใน main thread
                    self.root.after(0, lambda: self._update_terminals_list(terminals))
                    
                except Exception as e:
                    self.log(f"❌ Terminal scan error: {e}")
                    self.root.after(0, lambda: self.update_system_status("❌ Scan Failed"))
            
            threading.Thread(target=scan_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Scan terminals error: {e}")
    
    def _update_terminals_list(self, terminals: List[Dict]):
        """📝 อัพเดทรายการ terminals"""
        try:
            if terminals:
                self.log(f"✅ Found {len(terminals)} MT5 terminals")
                self.update_system_status(f"✅ Found {len(terminals)} Terminals")
            else:
                self.log("❌ No MT5 terminals found")
                self.update_system_status("❌ No Terminals Found")
        except Exception as e:
            self.log(f"❌ Terminal list update error: {e}")
    
    def connect_mt5(self):
        """🔗 เชื่อมต่อ MT5"""
        try:
            self.log("🔗 Connecting to MT5...")
            self.update_system_status("🔗 Connecting...")
            
            def connect_thread():
                try:
                    success = self.mt5_connector.connect()
                    
                    if success:
                        # อัพเดท GUI
                        self.root.after(0, self._on_mt5_connected)
                    else:
                        self.root.after(0, self._on_mt5_connection_failed)
                        
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda: self.log(f"❌ MT5 connection error: {error_msg}"))
            
            threading.Thread(target=connect_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Connect MT5 error: {e}")
    
    def _on_mt5_connected(self):
        """✅ เมื่อเชื่อมต่อ MT5 สำเร็จ"""
        try:
            self.log("✅ MT5 connected successfully")
            self.update_system_status("✅ MT5 Connected")
            
            # อัพเดท connection status
            self.mt5_status_label.config(text="🟢 Connected", fg="#00ff88")
            
            # เปิดใช้งาน/ปิดใช้งาน buttons
            self.connect_button.config(state="disabled")
            self.scan_button.config(state="disabled")
            self.start_button.config(state="normal")
            
            # เริ่มต้น Enhanced System
            self.initialize_enhanced_system()
            
            # อัพเดท account info
            account_info = self.mt5_connector.get_account_info()
            if account_info:
                account_text = f"Account: {account_info.get('login', 'Unknown')} | ${account_info.get('balance', 0):.2f}"
                self.account_info_label.config(text=account_text)
            
        except Exception as e:
            self.log(f"❌ MT5 connection callback error: {e}")
    
    def _on_mt5_connection_failed(self):
        """❌ เมื่อเชื่อมต่อ MT5 ไม่สำเร็จ"""
        try:
            self.log("❌ MT5 connection failed")
            self.update_system_status("❌ Connection Failed")
            self.mt5_status_label.config(text="🔴 Failed", fg="#ff6b6b")
            
        except Exception as e:
            self.log(f"❌ Connection failed callback error: {e}")
    
    def disconnect_mt5(self):
        """🔌 ตัด MT5 connection"""
        try:
            self.log("🔌 Disconnecting MT5...")
            
            # หยุด trading ก่อน
            if self.is_trading:
                self.stop_trading()
                time.sleep(1)
            
            # Disconnect
            self.mt5_connector.disconnect()
            
            # อัพเดท GUI
            self.mt5_status_label.config(text="🔴 Disconnected", fg="#ff6b6b")
            self.update_system_status("🔌 Disconnected")
            
            # Reset buttons
            self.connect_button.config(state="normal")
            self.scan_button.config(state="normal") 
            self.start_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            
            self.log("✅ MT5 disconnected")
            
        except Exception as e:
            self.log(f"❌ Disconnect error: {e}")
    
    # ==========================================
    # 🚀 ENHANCED TRADING CONTROL
    # ==========================================
    
    def start_trading(self):
        """🚀 เริ่ม Enhanced Trading System"""
        try:
            if not self.mt5_connector.is_connected:
                messagebox.showerror("Error", "กรุณาเชื่อมต่อ MT5 ก่อน")
                return
            
            if not self.enhanced_risk_manager:
                messagebox.showerror("Error", "Enhanced Risk Manager ไม่พร้อม")
                return
            
            # ตรวจสอบ risk ก่อนเริ่ม
            risk_status = self.enhanced_risk_manager.check_risk_levels()
            
            if risk_status.get('emergency_stop', False):
                messagebox.showerror("Risk Warning", "ไม่สามารถเทรดได้: Emergency stop active")
                return
            
            if not risk_status.get('can_trade', False):
                result = messagebox.askyesno(
                    "Risk Warning", 
                    "Risk level สูง แต่ยังสามารถเทรดได้\nต้องการเริ่มเทรดหรือไม่?"
                )
                if not result:
                    return
            
            self.log("🚀 Starting Enhanced Trading System...")
            
            # เริ่ม trading thread
            self.is_trading = True
            self.trading_thread = threading.Thread(target=self._enhanced_trading_loop, daemon=True)
            self.trading_thread.start()
            
            # อัพเดท GUI
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.update_system_status("🚀 Trading Active")
            
            self.log("✅ Enhanced Trading System started")
            
        except Exception as e:
            self.log(f"❌ Start trading error: {e}")
            messagebox.showerror("Error", f"ไม่สามารถเริ่มเทรดได้: {e}")
    
    def stop_trading(self):
        """🛑 หยุด Trading System"""
        try:
            self.log("🛑 Stopping Enhanced Trading System...")
            
            self.is_trading = False
            
            # รอให้ trading thread จบ
            if self.trading_thread and self.trading_thread.is_alive():
                self.trading_thread.join(timeout=3)
            
            # อัพเดท GUI
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.update_system_status("🛑 Trading Stopped")
            
            self.log("✅ Enhanced Trading System stopped")
            
        except Exception as e:
            self.log(f"❌ Stop trading error: {e}")
    
    def _enhanced_trading_loop(self):
        """🔄 Enhanced Trading Loop"""
        try:
            self.log("🔄 Enhanced trading loop started")
            
            while self.is_trading:
                try:
                    # 1. ตรวจสอบ risk levels
                    if self.enhanced_risk_manager:
                        risk_status = self.enhanced_risk_manager.check_risk_levels()
                        
                        if risk_status.get('emergency_stop', False):
                            self.log("🚨 Emergency stop triggered - stopping trading")
                            break
                        
                        if not risk_status.get('can_trade', True):
                            self.log("⏳ Trading restricted - waiting...")
                            time.sleep(30)  # รอ 30 วินาที
                            continue
                    
                    # 2. สร้าง signal
                    if self.enhanced_signal_generator:
                        signal = self.enhanced_signal_generator.generate_enhanced_signal()
                        
                        if signal and signal.get('action') in ['BUY', 'SELL']:
                            self.log(f"🎯 Signal: {signal['action']} (Strength: {signal.get('strength', 0)*100:.1f}%)")
                            
                            # อัพเดท signal display
                            self.root.after(0, lambda: self._update_signal_display(signal))
                            
                            # 3. Execute trade
                            self._execute_enhanced_trade(signal)
                    
                    # 4. Monitor positions
                    if self.enhanced_position_monitor:
                        self.enhanced_position_monitor.monitor_and_close_positions()
                    
                    # 5. Update performance
                    if self.performance_tracker:
                        self.performance_tracker.update_session_stats()
                    
                    # Sleep before next iteration
                    time.sleep(10)  # 10 วินาทีต่อรอบ
                    
                except Exception as e:
                    self.log(f"❌ Trading loop error: {e}")
                    time.sleep(30)  # หน่วงนานกว่าเมื่อเกิด error
            
            self.log("🔄 Enhanced trading loop stopped")
            
        except Exception as e:
            self.log(f"❌ Trading loop critical error: {e}")
        finally:
            # Cleanup
            self.root.after(0, self._on_trading_stopped)
    
    def _execute_enhanced_trade(self, signal: Dict):
        """🎯 Execute Enhanced Trade"""
        try:
            if not self.order_manager or not self.enhanced_lot_calculator:
                return
            
            # คำนวณ lot size
            lot_calc_result = self.enhanced_lot_calculator.calculate_enhanced_lot_size(
                signal_strength=signal.get('strength', 0),
                market_conditions=signal.get('market_conditions', {}),
                suggested_role=signal.get('suggested_role', 'PW')
            )
            
            volume = lot_calc_result.get('recommended_lot', 0.01)
            role = lot_calc_result.get('assigned_role', signal.get('suggested_role', 'PW'))
            
            # Validate trade ด้วย risk manager
            validation = self.enhanced_risk_manager.validate_new_trade(
                order_type=signal['action'].lower(),
                volume=volume,
                role=role
            )
            
            if not validation.get('approved', False):
                self.log(f"🚫 Trade rejected: {validation.get('restrictions', ['Unknown reason'])[0]}")
                return
            
            # ใช้ recommended values
            final_volume = validation.get('recommended_volume', volume)
            final_role = validation.get('recommended_role', role)
            
            # Execute order
            order_result = self.order_manager.place_market_order(
                action=signal['action'],
                volume=final_volume
            )
            
            if order_result.get('success', False):
                ticket = order_result.get('ticket', 0)
                
                # บันทึก role
                if self.role_manager:
                    self.role_manager.assign_role_to_position(ticket, final_role)
                
                self.log(f"✅ Trade executed: {signal['action']} {final_volume} lots (Role: {final_role})")
                
            else:
                self.log(f"❌ Trade execution failed: {order_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.log(f"❌ Enhanced trade execution error: {e}")
    
    def _update_signal_display(self, signal: Dict):
        """🎯 อัพเดท Signal Display"""
        try:
            action = signal.get('action', 'WAIT')
            strength = signal.get('strength', 0) * 100
            
            signal_colors = {
                'BUY': '#00ff88',
                'SELL': '#ff6b6b',
                'WAIT': '#ffaa00'
            }
            
            signal_emojis = {
                'BUY': '🟢',
                'SELL': '🔴', 
                'WAIT': '⏳'
            }
            
            color = signal_colors.get(action, '#cccccc')
            emoji = signal_emojis.get(action, '⚪')
            
            self.current_signal_label.config(
                text=f"{emoji} {action}",
                fg=color
            )
            
            self.signal_strength_label.config(text=f"Strength: {strength:.1f}%")
            
        except Exception as e:
            self.log(f"❌ Signal display update error: {e}")
    
    # ==========================================
    # 🎯 ONE-CLICK ACTIONS (NEW!)
    # ==========================================
    
    def harvest_profits(self):
        """🌾 Harvest Profitable Positions"""
        try:
            if not self.enhanced_position_monitor:
                messagebox.showwarning("Warning", "Position Monitor ไม่พร้อม")
                return
            
            result = messagebox.askyesno(
                "Confirm Harvest", 
                "ต้องการปิด positions ที่มีกำไร ≥ $1.0 หรือไม่?"
            )
            
            if not result:
                return
            
            self.log("🌾 Harvesting profitable positions...")
            
            def harvest_thread():
                try:
                    # ใช้ position monitor's harvest method
                    harvest_result = self.enhanced_position_monitor.harvest_profitable_positions()
                    
                    closed_count = harvest_result.get('positions_closed', 0)
                    total_profit = harvest_result.get('total_profit_harvested', 0)
                    
                    self.log(f"🌾 Harvest completed: {closed_count} positions, ${total_profit:.2f} profit")
                    
                except Exception as e:
                    self.log(f"❌ Harvest error: {e}")
            
            threading.Thread(target=harvest_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Harvest profits error: {e}")
    
    def rebalance_portfolio(self):
        """⚖️ Rebalance Portfolio Roles"""
        try:
            if not self.role_manager:
                messagebox.showwarning("Warning", "Role Manager ไม่พร้อม")
                return
            
            result = messagebox.askyesno(
                "Confirm Rebalance", 
                "ต้องการปรับสมดุล role distribution หรือไม่?"
            )
            
            if not result:
                return
            
            self.log("⚖️ Rebalancing portfolio roles...")
            
            def rebalance_thread():
                try:
                    # ใช้ role manager's rebalance method
                    rebalance_result = self.role_manager.rebalance_roles()
                    
                    changes_made = rebalance_result.get('changes_made', 0)
                    self.log(f"⚖️ Rebalance completed: {changes_made} role changes")
                    
                except Exception as e:
                    self.log(f"❌ Rebalance error: {e}")
            
            threading.Thread(target=rebalance_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Portfolio rebalance error: {e}")
    
    def emergency_close_all(self):
        """🚨 Emergency Close All Positions"""
        try:
            result = messagebox.askyesno(
                "⚠️ Emergency Close", 
                "🚨 WARNING: ต้องการปิด positions ทั้งหมดหรือไม่?\n\nการกระทำนี้ไม่สามารถยกเลิกได้!"
            )
            
            if not result:
                return
            
            self.log("🚨 EMERGENCY CLOSE ALL POSITIONS!")
            
            def emergency_thread():
                try:
                    # Execute emergency protocol
                    if self.enhanced_risk_manager:
                        protocol_result = self.enhanced_risk_manager.execute_emergency_protocol("loss")
                        self.log(f"🚨 Emergency protocol executed: {protocol_result.get('actions_taken', [])}")
                    
                    # ปิด positions ทั้งหมด
                    positions = self.mt5_connector.get_positions()
                    if positions:
                        closed_count = 0
                        total_recovery = 0.0
                        
                        for position in positions:
                            if self.mt5_connector.close_position(position.get('ticket')):
                                closed_count += 1
                                total_recovery += position.get('profit', 0)
                        
                        self.log(f"🚨 Emergency closed: {closed_count} positions, Recovery: ${total_recovery:.2f}")
                    
                    # หยุด trading
                    if self.is_trading:
                        self.is_trading = False
                        self.root.after(0, self._on_trading_stopped)
                    
                except Exception as e:
                    self.log(f"❌ Emergency close error: {e}")
            
            threading.Thread(target=emergency_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Emergency close error: {e}")
    
    def close_profitable_positions(self):
        """💰 Close Profitable Positions Only"""
        try:
            if not self.enhanced_position_monitor:
                messagebox.showwarning("Warning", "Position Monitor ไม่พร้อม")
                return
            
            self.log("💰 Closing profitable positions...")
            
            def close_profits_thread():
                try:
                    close_result = self.enhanced_position_monitor.close_profitable_positions(min_profit=1.0)
                    
                    closed_count = close_result.get('positions_closed', 0)
                    total_profit = close_result.get('total_profit', 0)
                    
                    self.log(f"💰 Closed {closed_count} profitable positions: ${total_profit:.2f}")
                    
                except Exception as e:
                    self.log(f"❌ Close profits error: {e}")
            
            threading.Thread(target=close_profits_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Close profitable error: {e}")
    
    def close_losing_positions(self):
        """💸 Close Losing Positions"""
        try:
            result = messagebox.askyesno(
                "Confirm Close Losses", 
                "ต้องการปิด positions ขาดทุนหรือไม่?\n\nจะปิดเฉพาะที่ขาดทุนมากกว่า $50"
            )
            
            if not result:
                return
            
            self.log("💸 Closing high-loss positions...")
            
            def close_losses_thread():
                try:
                    positions = self.mt5_connector.get_positions()
                    if not positions:
                        return
                    
                    closed_count = 0
                    total_loss = 0.0
                    
                    for position in positions:
                        profit = position.get('profit', 0)
                        
                        if profit <= -50.0:  # ขาดทุนมากกว่า $50
                            if self.mt5_connector.close_position(position.get('ticket')):
                                closed_count += 1
                                total_loss += profit
                    
                    self.log(f"💸 Closed {closed_count} high-loss positions: ${total_loss:.2f}")
                    
                except Exception as e:
                    self.log(f"❌ Close losses error: {e}")
            
            threading.Thread(target=close_losses_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Close losing error: {e}")
    
    def optimize_margin(self):
        """📊 Optimize Margin Usage"""
        try:
            if not self.enhanced_position_monitor:
                messagebox.showwarning("Warning", "Position Monitor ไม่พร้อม")
                return
            
            self.log("📊 Optimizing margin usage...")
            
            def optimize_thread():
                try:
                    # ใช้ position monitor's margin optimization
                    optimize_result = self.enhanced_position_monitor.optimize_margin_usage()
                    
                    actions_taken = optimize_result.get('actions_taken', [])
                    margin_saved = optimize_result.get('margin_freed', 0)
                    
                    self.log(f"📊 Margin optimized: {len(actions_taken)} actions, ${margin_saved:.2f} freed")
                    
                except Exception as e:
                    self.log(f"❌ Margin optimization error: {e}")
            
            threading.Thread(target=optimize_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Optimize margin error: {e}")
    
    def balance_volume(self):
        """⚖️ Balance Portfolio Volume"""
        try:
            if not self.enhanced_position_monitor:
                messagebox.showwarning("Warning", "Position Monitor ไม่พร้อม") 
                return
            
            self.log("⚖️ Balancing portfolio volume...")
            
            def balance_thread():
                try:
                    # ใช้ position monitor's volume balancing
                    balance_result = self.enhanced_position_monitor.balance_portfolio_volume()
                    
                    adjustments = balance_result.get('adjustments_made', [])
                    new_balance = balance_result.get('new_balance_ratio', 0)
                    
                    self.log(f"⚖️ Volume balanced: {len(adjustments)} adjustments, ratio: {new_balance:.2f}")
                    
                except Exception as e:
                    self.log(f"❌ Volume balance error: {e}")
            
            threading.Thread(target=balance_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Balance volume error: {e}")
    
    def _on_trading_stopped(self):
        """🛑 Trading Stopped Callback"""
        try:
            self.is_trading = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.update_system_status("🛑 Trading Stopped")
            
        except Exception as e:
            self.log(f"❌ Trading stopped callback error: {e}")
    
    # ==========================================
    # 🔧 UTILITY METHODS
    # ==========================================
    
    def update_system_status(self, status: str):
        """🔄 อัพเดท System Status"""
        try:
            self.system_status_label.config(text=status)
            
            # อัพเดท system health indicator
            if "Error" in status or "Failed" in status:
                self.system_health_label.config(text="System Health: ❌", fg="#ff6b6b")
            elif "Active" in status or "Connected" in status:
                self.system_health_label.config(text="System Health: ✅", fg="#00ff88")
            else:
                self.system_health_label.config(text="System Health: ⏳", fg="#ffaa00")
                
        except Exception as e:
            self.log(f"❌ Status update error: {e}")
    
    def log(self, message: str):
        """📝 Enhanced Logging"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            
            if hasattr(self, 'log_text') and self.log_text:
                self.log_text.insert(tk.END, log_message)
                self.log_text.see(tk.END)
                
                # จำกัดจำนวน log lines
                lines = self.log_text.get(1.0, tk.END).split('\n')
                if len(lines) > 200:  # เพิ่มจาก 100 → 200
                    self.log_text.delete(1.0, f"{len(lines)-200}.0")
            
            # Print to console
            print(log_message.strip())
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            print(f"Log error: {e}")
    
    def on_closing(self):
        """🔒 Enhanced Shutdown Procedure"""
        try:
            self.log("🔒 Shutting down Enhanced AI Trading System...")
            
            # หยุด GUI updates
            self.gui_update_active = False
            
            # หยุด trading
            if self.is_trading:
                self.stop_trading()
                time.sleep(2)
            
            # Save enhanced session data
            if self.capital_manager:
                self.capital_manager.save_session_data()
                self.log("💰 Capital session data saved")
            
            if self.role_manager:
                self.role_manager.save_role_history()
                self.log("🎭 Role history saved")
            
            if self.performance_tracker:
                self.performance_tracker.save_session_stats()
                self.log("📈 Performance data saved")
            
            # Disconnect MT5
            if self.mt5_connector.is_connected:
                self.mt5_connector.disconnect()
                self.log("🔌 MT5 disconnected")
            
            self.log("✅ Enhanced system shutdown completed")
            
            # ปิดโปรแกรม
            self.root.destroy()
            
        except Exception as e:
            print(f"❌ Shutdown error: {e}")
            self.root.destroy()
    
    # ==========================================
    # 🎮 ADVANCED GUI FEATURES
    # ==========================================
    
    def show_advanced_analytics(self):
        """📊 แสดง Advanced Analytics Window"""
        try:
            analytics_window = tk.Toplevel(self.root)
            analytics_window.title("📊 Advanced Analytics")
            analytics_window.geometry("800x600")
            analytics_window.configure(bg="#1a1a1a")
            
            # Capital Analytics
            capital_frame = tk.LabelFrame(
                analytics_window, text="💰 Capital Analytics",
                fg="#00d4aa", bg="#1a1a2e"
            )
            capital_frame.pack(fill="x", padx=10, pady=5)
            
            if self.capital_manager:
                capital_report = self.capital_manager.get_detailed_report()
                
                capital_text = tk.Text(capital_frame, height=8, bg="#0a0a1a", fg="#cccccc")
                capital_text.pack(fill="x", padx=5, pady=5)
                
                capital_text.insert(tk.END, json.dumps(capital_report, indent=2))
                capital_text.config(state="disabled")
            
            # Role Analytics
            role_frame = tk.LabelFrame(
                analytics_window, text="🎭 Role Analytics",
                fg="#00d4aa", bg="#1a1a2e"
            )
            role_frame.pack(fill="x", padx=10, pady=5)
            
            if self.role_manager:
                role_report = self.role_manager.get_comprehensive_report()
                
                role_text = tk.Text(role_frame, height=8, bg="#0a0a1a", fg="#cccccc")
                role_text.pack(fill="x", padx=5, pady=5)
                
                role_text.insert(tk.END, json.dumps(role_report, indent=2))
                role_text.config(state="disabled")
            
            # Risk Analytics
            risk_frame = tk.LabelFrame(
                analytics_window, text="🛡️ Risk Analytics",
                fg="#00d4aa", bg="#1a1a2e"
            )
            risk_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            if self.enhanced_risk_manager:
                risk_report = self.enhanced_risk_manager.get_risk_metrics_analysis()
                
                risk_text = tk.Text(risk_frame, bg="#0a0a1a", fg="#cccccc")
                risk_text.pack(fill="both", expand=True, padx=5, pady=5)
                
                risk_text.insert(tk.END, json.dumps(risk_report, indent=2))
                risk_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Advanced analytics error: {e}")
    
    def setup_menu_bar(self):
        """🔧 Setup Menu Bar"""
        try:
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # System Menu
            system_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="🔧 System", menu=system_menu)
            
            system_menu.add_command(label="🔄 Refresh All", command=self.refresh_all_displays)
            system_menu.add_command(label="💾 Save Settings", command=self.save_settings)
            system_menu.add_command(label="📊 Advanced Analytics", command=self.show_advanced_analytics)
            system_menu.add_separator()
            system_menu.add_command(label="🔒 Exit", command=self.on_closing)
            
            # Trading Menu
            trading_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="📈 Trading", menu=trading_menu)
            
            trading_menu.add_command(label="🚀 Start Trading", command=self.start_trading)
            trading_menu.add_command(label="🛑 Stop Trading", command=self.stop_trading)
            trading_menu.add_separator()
            trading_menu.add_command(label="🌾 Harvest Profits", command=self.harvest_profits)
            trading_menu.add_command(label="⚖️ Rebalance Portfolio", command=self.rebalance_portfolio)
            trading_menu.add_command(label="🚨 Emergency Close", command=self.emergency_close_all)
            
            # Analytics Menu
            analytics_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="📊 Analytics", menu=analytics_menu)
            
            analytics_menu.add_command(label="💰 Capital Report", command=self.show_capital_report)
            analytics_menu.add_command(label="🎭 Role Report", command=self.show_role_report)
            analytics_menu.add_command(label="🛡️ Risk Report", command=self.show_risk_report)
            analytics_menu.add_command(label="📈 Performance Report", command=self.show_performance_report)
            
        except Exception as e:
            self.log(f"❌ Menu setup error: {e}")
    
    def refresh_all_displays(self):
        """🔄 Refresh ทุก displays"""
        try:
            self.log("🔄 Refreshing all displays...")
            
            self.update_capital_dashboard()
            self.update_role_dashboard()
            self.update_risk_dashboard()
            self.update_recovery_panel()
            self.update_performance_panel()
            self.update_enhanced_positions_table()
            
            self.log("✅ All displays refreshed")
            
        except Exception as e:
            self.log(f"❌ Refresh error: {e}")
    
    def save_settings(self):
        """💾 บันทึกการตั้งค่า"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.log("💾 Settings saved successfully")
            messagebox.showinfo("Success", "การตั้งค่าถูกบันทึกแล้ว")
            
        except Exception as e:
            self.log(f"❌ Save settings error: {e}")
            messagebox.showerror("Error", f"ไม่สามารถบันทึกการตั้งค่าได้: {e}")
    
    # ==========================================
    # 📊 REPORT WINDOWS
    # ==========================================
    
    def show_capital_report(self):
        """💰 แสดง Capital Report Window"""
        try:
            if not self.capital_manager:
                messagebox.showwarning("Warning", "Capital Manager ไม่พร้อม")
                return
            
            report_window = tk.Toplevel(self.root)
            report_window.title("💰 Capital Management Report")
            report_window.geometry("600x500")
            report_window.configure(bg="#1a1a1a")
            
            # Get report data
            capital_report = self.capital_manager.get_detailed_report()
            
            # Display report
            report_text = scrolledtext.ScrolledText(
                report_window, font=("Consolas", 10),
                bg="#0a0a1a", fg="#cccccc", wrap="word"
            )
            report_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Format report
            formatted_report = self._format_capital_report(capital_report)
            report_text.insert(tk.END, formatted_report)
            report_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Capital report error: {e}")
    
    def show_role_report(self):
        """🎭 แสดง Role Report Window"""
        try:
            if not self.role_manager:
                messagebox.showwarning("Warning", "Role Manager ไม่พร้อม")
                return
            
            report_window = tk.Toplevel(self.root)
            report_window.title("🎭 Role Distribution Report")  
            report_window.geometry("600x500")
            report_window.configure(bg="#1a1a1a")
            
            # Get report data
            role_report = self.role_manager.get_comprehensive_report()
            
            # Display report
            report_text = scrolledtext.ScrolledText(
                report_window, font=("Consolas", 10),
                bg="#0a0a1a", fg="#cccccc", wrap="word"
            )
            report_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Format report
            formatted_report = self._format_role_report(role_report)
            report_text.insert(tk.END, formatted_report)
            report_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Role report error: {e}")
    
    def show_risk_report(self):
        """🛡️ แสดง Risk Report Window"""
        try:
            if not self.enhanced_risk_manager:
                messagebox.showwarning("Warning", "Enhanced Risk Manager ไม่พร้อม")
                return
            
            report_window = tk.Toplevel(self.root)
            report_window.title("🛡️ Enhanced Risk Assessment Report")
            report_window.geometry("700x600")
            report_window.configure(bg="#1a1a1a")
            
            # Get comprehensive risk data
            risk_summary = self.enhanced_risk_manager.get_enhanced_risk_summary()
            risk_metrics = self.enhanced_risk_manager.get_risk_metrics_analysis()
            
            # Tabbed interface
            notebook = ttk.Notebook(report_window)
            notebook.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Tab 1: Risk Summary
            summary_frame = tk.Frame(notebook, bg="#1a1a1a")
            notebook.add(summary_frame, text="📊 Risk Summary")
            
            summary_text = scrolledtext.ScrolledText(
                summary_frame, font=("Consolas", 9),
                bg="#0a0a1a", fg="#cccccc", wrap="word"
            )
            summary_text.pack(fill="both", expand=True, padx=5, pady=5)
            
            formatted_summary = self._format_risk_summary(risk_summary)
            summary_text.insert(tk.END, formatted_summary)
            summary_text.config(state="disabled")
            
            # Tab 2: Risk Metrics
            metrics_frame = tk.Frame(notebook, bg="#1a1a1a")
            notebook.add(metrics_frame, text="📈 Risk Metrics")
            
            metrics_text = scrolledtext.ScrolledText(
                metrics_frame, font=("Consolas", 9),
                bg="#0a0a1a", fg="#cccccc", wrap="word"
            )
            metrics_text.pack(fill="both", expand=True, padx=5, pady=5)
            
            metrics_text.insert(tk.END, json.dumps(risk_metrics, indent=2))
            metrics_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Risk report error: {e}")
    
    def show_performance_report(self):
        """📈 แสดง Performance Report Window"""
        try:
            if not self.performance_tracker:
                messagebox.showwarning("Warning", "Performance Tracker ไม่พร้อม")
                return
            
            report_window = tk.Toplevel(self.root)
            report_window.title("📈 Performance Analysis Report")
            report_window.geometry("600x500")
            report_window.configure(bg="#1a1a1a")
            
            # Get performance data
            performance_data = self.performance_tracker.get_comprehensive_report()
            
            # Display report
            report_text = scrolledtext.ScrolledText(
                report_window, font=("Consolas", 10),
                bg="#0a0a1a", fg="#cccccc", wrap="word"
            )
            report_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Format performance report
            formatted_report = self._format_performance_report(performance_data)
            report_text.insert(tk.END, formatted_report)
            report_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Performance report error: {e}")
    
    # ==========================================
    # 🎨 REPORT FORMATTING METHODS
    # ==========================================
    
    def _format_capital_report(self, report: Dict) -> str:
        """💰 Format Capital Report"""
        try:
            formatted = f"""
💰 CAPITAL MANAGEMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

📊 CURRENT STATUS:
Trading Mode: {report.get('trading_mode', 'Unknown')}
Current Drawdown: {report.get('current_drawdown_percent', 0):.2f}%
Available Capital: ${report.get('available_capital', 0):.2f}

💎 CAPITAL ZONES:
Safe Zone (50%): ${report.get('safe_zone_capital', 0):.2f}
Growth Zone (35%): ${report.get('growth_zone_capital', 0):.2f}
Aggressive Zone (15%): ${report.get('aggressive_zone_capital', 0):.2f}

🎯 UTILIZATION:
Safe Utilization: {report.get('zone_utilization', {}).get('safe_percent', 0):.1f}%
Growth Utilization: {report.get('zone_utilization', {}).get('growth_percent', 0):.1f}%
Aggressive Utilization: {report.get('zone_utilization', {}).get('aggressive_percent', 0):.1f}%

📈 EFFICIENCY:
Capital Efficiency: {report.get('capital_efficiency', 0):.3f}
Risk-Adjusted Return: {report.get('risk_adjusted_return', 0):.2f}%
"""
            return formatted
            
        except Exception as e:
            return f"❌ Capital report formatting error: {e}"
    
    def _format_role_report(self, report: Dict) -> str:
        """🎭 Format Role Report"""
        try:
            role_counts = report.get('role_counts', {})
            total_positions = report.get('total_positions', 0)
            
            formatted = f"""
🎭 ROLE DISTRIBUTION REPORT  
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

📊 CURRENT DISTRIBUTION:
Total Positions: {total_positions}
Balance Quality: {report.get('balance_quality', 'Unknown')}

🎯 ROLE BREAKDOWN:
"""
            
            role_names = {
                'HG': 'Hedge Guard',
                'PW': 'Profit Walker', 
                'RH': 'Recovery Hunter',
                'SC': 'Scalp Capture'
            }
            
            for role, name in role_names.items():
                count = role_counts.get(role, 0)
                percentage = (count / total_positions * 100) if total_positions > 0 else 0
                
                formatted += f"\n{role} ({name}): {count} positions ({percentage:.1f}%)"
            
            # Performance by role
            if 'role_performance' in report:
                formatted += f"\n\n💰 PERFORMANCE BY ROLE:"
                for role, perf in report['role_performance'].items():
                    profit = perf.get('total_profit', 0)
                    avg_profit = perf.get('avg_profit', 0)
                    formatted += f"\n{role}: ${profit:.2f} total, ${avg_profit:.2f} avg"
            
            return formatted
            
        except Exception as e:
            return f"❌ Role report formatting error: {e}"
    
    def _format_risk_summary(self, summary: Dict) -> str:
        """🛡️ Format Risk Summary"""
        try:
            formatted = f"""
🛡️ ENHANCED RISK ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

📊 OVERALL ASSESSMENT:
Risk Level: {summary.get('overall_risk_level', 'Unknown')}
Risk Score: {summary.get('risk_score', 0):.3f}/1.000
Can Trade: {'✅ YES' if summary.get('can_trade', False) else '❌ NO'}
Emergency Stop: {'🚨 ACTIVE' if summary.get('emergency_stop', False) else '✅ NORMAL'}

💰 CAPITAL STATUS:
Trading Mode: {summary.get('trading_mode', 'Unknown')}
Available Zones: {summary.get('available_capital_zones', 'Unknown')}
Current Drawdown: {summary.get('current_drawdown', 0):.2f}%

🎭 ROLE STATUS:
Role Balance: {summary.get('role_balance_status', 'Unknown')}
Total Positions: {sum(summary.get('role_counts', {}).values())}

📈 PORTFOLIO HEALTH:
Active Warnings: {summary.get('active_warnings', 0)}
Active Restrictions: {summary.get('active_restrictions', 0)}
Consecutive Losses: {summary.get('consecutive_losses', 0)}
Position Usage: {summary.get('position_usage', 0):.1f}%

🔄 RECOVERY STATUS:
Recovery Mode: {'✅ ACTIVE' if summary.get('recovery_mode_active', False) else '❌ INACTIVE'}
Recovery Opportunities: {summary.get('recovery_opportunities', 0)}
"""
            return formatted
            
        except Exception as e:
            return f"❌ Risk summary formatting error: {e}"
    
    def _format_performance_report(self, report: Dict) -> str:
        """📈 Format Performance Report"""
        try:
            formatted = f"""
📈 PERFORMANCE ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

💰 FINANCIAL METRICS:
Net Profit: ${report.get('net_profit', 0):.2f}
Gross Profit: ${report.get('gross_profit', 0):.2f}
Gross Loss: ${report.get('gross_loss', 0):.2f}
Profit Factor: {report.get('profit_factor', 0):.3f}

📊 TRADE STATISTICS:
Total Trades: {report.get('total_trades', 0)}
Winning Trades: {report.get('winning_trades', 0)}
Losing Trades: {report.get('losing_trades', 0)}
Win Rate: {report.get('profitable_trade_percent', 0):.1f}%

📈 AVERAGES:
Average Trade: ${report.get('average_trade', 0):.2f}
Average Win: ${report.get('average_win', 0):.2f}
Average Loss: ${report.get('average_loss', 0):.2f}

🔄 STREAKS:
Max Consecutive Wins: {report.get('max_consecutive_wins', 0)}
Max Consecutive Losses: {report.get('max_consecutive_losses', 0)}
Current Streak: {report.get('current_streak', 0)}

💹 RETURNS:
ROI: {report.get('roi_percent', 0):.2f}%
Total Return: {report.get('total_return_percent', 0):.2f}%
"""
            return formatted
            
        except Exception as e:
            return f"❌ Performance report formatting error: {e}"

# ==========================================
# 🚀 APPLICATION ENTRY POINT
# ==========================================

def main():
    """🚀 เริ่มต้น Modern AI Gold Grid Trading System v4.0"""
    
    print("🚀 Modern AI Gold Grid Trading System v4.0")
    print("=" * 60)
    print("💰 Capital Management: Enabled")
    print("🎭 Role Intelligence: Enabled") 
    print("🛡️ Enhanced Risk Management: Enabled")
    print("🔄 Recovery Intelligence: Enabled")
    print("=" * 60)
    print("🎮 Starting Enhanced GUI...")
    
    # Create Modern GUI
    root = tk.Tk()
    app = ModernAITradingGUI(root)
    
    # Setup menu bar
    app.setup_menu_bar()
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start GUI
    try:
        print("✅ Modern AI Trading GUI started successfully")
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        app.on_closing()
    except Exception as e:
        print(f"❌ GUI error: {e}")
        try:
            app.on_closing()
        except:
            pass

if __name__ == "__main__":
    main()