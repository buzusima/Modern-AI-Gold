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
from signal_generator import SignalGenerator                    # ✅ Class: SignalGenerator (ไม่ใช่ EnhancedSignalGenerator)
from position_monitor import PositionMonitor                    # ✅ ต้องเช็คว่ามีไฟล์นี้ไหม หรือใช้ชื่ออื่น
from lot_calculator import LotCalculator, create_lot_calculator # ✅ Class: LotCalculator (ไม่ใช่ EnhancedLotCalculator)
from performance_tracker import PerformanceTracker
from enhanced_risk_manager import EnhancedRiskManager
from capital_manager import CapitalManager, create_capital_manager          # ✅ มี factory function
from order_manager import OrderRoleManager, create_order_role_manager       # ✅ มี OrderRoleManager ในไฟล์ order_manager.py
from order_manager import OrderManager, create_order_manager, integrate_order_manager_with_system # ✅ Central Order Manager

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
        self.signal_generator = None           # ✅ ชื่อถูกต้อง (ไม่ใช่ enhanced_signal_generator)
        self.position_monitor = None           # ✅ ชื่อถูกต้อง (ไม่ใช่ enhanced_position_monitor)
        self.lot_calculator = None             # ✅ ชื่อถูกต้อง (ไม่ใช่ enhanced_lot_calculator)
        self.order_manager = None              # ✅ Central Order Manager
        self.order_executor = None             # ✅ เพิ่มตัวแปรนี้
                
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
    
    def _initialize_role_indicators(self):
        """🎭 สร้าง role indicators dictionary"""
        self.role_indicators = {
            'HG': {'count': None, 'performance': None},
            'PW': {'count': None, 'performance': None}, 
            'RH': {'count': None, 'performance': None},
            'SC': {'count': None, 'performance': None}
        }
    
    def _ensure_required_widgets(self):
        """✅ ตรวจสอบและสร้าง widgets ที่จำเป็น"""
        try:
            # ตรวจสอบ trading_mode_label
            if not hasattr(self, 'trading_mode_label') or not self.trading_mode_label:
                # สร้าง dummy label
                self.trading_mode_label = tk.Label(self.root, text="Mode: UNKNOWN", bg="#1a1a2e", fg="#cccccc")
            
            # ตรวจสอบ role_indicators
            if not hasattr(self, 'role_indicators') or not self.role_indicators:
                self._initialize_role_indicators()
            
            # ตรวจสอบ widgets อื่นๆ ที่สำคัญ
            required_widgets = [
                'drawdown_label', 'safe_zone_label', 'growth_zone_label', 'aggressive_zone_label',
                'capital_metrics_text', 'total_positions_label', 'role_balance_label',
                'risk_level_label', 'risk_score_label', 'risk_metrics_text',
                'recovery_count_label', 'recovery_suggestions_text',
                'performance_metrics_text', 'positions_summary_label'
            ]
            
            for widget_name in required_widgets:
                if not hasattr(self, widget_name) or not getattr(self, widget_name):
                    # สร้าง dummy widget
                    setattr(self, widget_name, tk.Label(self.root, text="--", bg="#1a1a2e", fg="#888888"))
            
            self.log("✅ Required widgets ensured")
            
        except Exception as e:
            self.log(f"❌ Widget ensure error: {e}")

    def load_config(self) -> Dict:
        """โหลดการตั้งค่าระบบ Enhanced - FIXED"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # ใช้ print แทน self.log เพราะ GUI ยังไม่ได้ setup
            print("✅ Enhanced configuration loaded successfully")
            
            # Validate critical sections
            required_sections = ["system", "trading", "capital_management", "order_roles"]
            missing_sections = []
            
            for section in required_sections:
                if section not in config:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"⚠️ Missing config sections: {missing_sections}")
                print("🔧 Using default values for missing sections")
                
                # เพิ่ม default sections
                config = self._add_default_config_sections(config, missing_sections)
            
            return config
            
        except FileNotFoundError:
            print("❌ config.json not found, creating default configuration")
            return self._create_default_config()
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in config.json: {e}")
            print("🔧 Using default configuration")
            return self._create_default_config()
            
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            print("🔧 Using default configuration")
            return self._create_default_config()
    
    def _add_default_config_sections(self, config: Dict, missing_sections: List[str]) -> Dict:
        """เพิ่ม default sections ที่หายไป"""
        try:
            defaults = {
                "system": {
                    "name": "Modern AI Gold Grid Trading System",
                    "version": "4.0.0",
                    "mode": "production"
                },
                "trading": {
                    "symbol": "XAUUSD.v",
                    "timeframe": "M5",
                    "max_positions": 60,
                    "auto_trading": True
                },
                "capital_management": {
                    "initial_capital": 7500.0,
                    "max_drawdown_percent": 30.0,
                    "capital_zones": {
                        "safe_zone_percent": 50.0,
                        "growth_zone_percent": 35.0,
                        "aggressive_zone_percent": 15.0
                    }
                },
                "order_roles": {
                    "auto_assignment": True,
                    "role_evolution": True,
                    "role_quotas": {
                        "HG": 25.0,
                        "PW": 40.0,
                        "RH": 20.0,
                        "SC": 15.0
                    }
                }
            }
            
            # เพิ่มเฉพาะ sections ที่หายไป
            for section in missing_sections:
                if section in defaults:
                    config[section] = defaults[section]
                    print(f"✅ Added default {section} configuration")
            
            return config
            
        except Exception as e:
            print(f"❌ Error adding default sections: {e}")
            return config

    def _create_default_config(self) -> Dict:
        """สร้าง default configuration ใหม่"""
        try:
            default_config = {
                "system": {
                    "name": "Modern AI Gold Grid Trading System",
                    "version": "4.0.0",
                    "mode": "production",
                    "description": "Capital-aware AI trading with order role intelligence"
                },
                "trading": {
                    "symbol": "XAUUSD.v",
                    "timeframe": "M5",
                    "market_orders_only": True,
                    "signal_cooldown_seconds": 45,
                    "max_signals_per_hour": 50,
                    "max_positions": 60,
                    "auto_trading": True,
                    "high_frequency_mode": True
                },
                "capital_management": {
                    "initial_capital": 7500.0,
                    "max_drawdown_percent": 30.0,
                    "conservative_trigger": 20.0,
                    "emergency_trigger": 25.0,
                    "capital_zones": {
                        "safe_zone_percent": 50.0,
                        "growth_zone_percent": 35.0,
                        "aggressive_zone_percent": 15.0
                    },
                    "zone_risk_limits": {
                        "safe": {
                            "max_risk_per_trade": 0.5,
                            "max_total_risk": 5.0,
                            "max_positions": 25,
                            "base_lot": 0.01,
                            "max_lot": 0.05
                        },
                        "growth": {
                            "max_risk_per_trade": 1.0,
                            "max_total_risk": 10.0,
                            "max_positions": 25,
                            "base_lot": 0.02,
                            "max_lot": 0.10
                        },
                        "aggressive": {
                            "max_risk_per_trade": 2.0,
                            "max_total_risk": 15.0,
                            "max_positions": 10,
                            "base_lot": 0.03,
                            "max_lot": 0.20
                        }
                    }
                },
                "order_roles": {
                    "auto_assignment": True,
                    "role_evolution": True,
                    "portfolio_balancing": True,
                    "role_quotas": {
                        "HG": 25.0,
                        "PW": 40.0,
                        "RH": 20.0,
                        "SC": 15.0
                    },
                    "role_settings": {
                        "HG": {
                            "max_age_hours": 48,
                            "min_profit_threshold": 4.0,
                            "max_loss_tolerance": -60.0,
                            "defensive": True
                        },
                        "PW": {
                            "max_age_hours": 24,
                            "min_profit_threshold": 2.5,
                            "max_loss_tolerance": -35.0,
                            "profit_trailing": True
                        },
                        "RH": {
                            "max_age_hours": 12,
                            "min_profit_threshold": 1.0,
                            "max_loss_tolerance": -25.0,
                            "recovery_focused": True
                        },
                        "SC": {
                            "max_age_hours": 2,
                            "min_profit_threshold": 0.5,
                            "max_loss_tolerance": -8.0,
                            "quick_profit": True
                        }
                    }
                },
                "risk_management": {
                    "max_risk_per_trade": 2.0,
                    "max_daily_risk": 10.0,
                    "max_positions": 60,
                    "emergency_stop_loss": -500.0,
                    "daily_profit_target": 100.0,
                    "max_daily_trades": 80,
                    "max_daily_loss": -300.0,
                    "min_margin_level": 150.0
                }
            }
            
            print("🔧 Created default configuration")
            
            # บันทึก default config
            try:
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                print("💾 Default config saved to config.json")
            except Exception as save_error:
                print(f"⚠️ Could not save default config: {save_error}")
            
            return default_config
            
        except Exception as e:
            print(f"❌ Error creating default config: {e}")
            # Return minimal config as fallback
            return {
                "system": {"version": "4.0.0"},
                "trading": {"symbol": "XAUUSD.v", "max_positions": 60},
                "capital_management": {"initial_capital": 7500.0},
                "order_roles": {"auto_assignment": True}
            }
            
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
        """💰 Setup Capital Dashboard - เพิ่ม widgets ที่ขาดหาย"""
        
        capital_frame = tk.LabelFrame(
            parent, text="💰 Capital Management", 
            font=("Arial", 11, "bold"), fg="#00d4aa", bg="#1a1a2e", width=520
        )
        capital_frame.pack(side="left", fill="both", expand=False, padx=3, pady=3)
        capital_frame.pack_propagate(False)
        
        # Capital Header
        header_frame = tk.Frame(capital_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=8, pady=5)
        
        # ✅ เพิ่ม trading_mode_label ที่ขาดหาย
        self.trading_mode_label = tk.Label(
            header_frame, text="Mode: NORMAL", 
            font=("Arial", 12, "bold"), fg="#00ff88", bg="#1a1a2e"
        )
        self.trading_mode_label.pack(side="left")
        
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
            zones_indicator_frame, text="🟢 Safe $0", 
            font=("Arial", 9), fg="#00ff88", bg="#1a1a2e"
        )
        self.safe_zone_label.pack(side="left", padx=5)
        
        self.growth_zone_label = tk.Label(
            zones_indicator_frame, text="🟡 Growth $0", 
            font=("Arial", 9), fg="#ffd700", bg="#1a1a2e"
        )
        self.growth_zone_label.pack(side="left", padx=5)
        
        self.aggressive_zone_label = tk.Label(
            zones_indicator_frame, text="🔴 Aggressive $0", 
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
        """🔄 เริ่มต้นระบบ Enhanced Components v4.0 - FIXED ตามไฟล์จริง"""
        try:
            if not self.mt5_connector.is_connected:
                self.log("⏳ Waiting for MT5 connection...")
                return
            
            self.log("🔄 Initializing Enhanced AI Components v4.0...")
            
            # 1. สร้าง Capital Manager - ✅ CORRECTED
            self.capital_manager = create_capital_manager(self.mt5_connector, self.config)
            if self.capital_manager:
                self.log("💰 Capital Manager initialized")
            else:
                self.log("❌ Capital Manager initialization failed")
                
            # 2. สร้าง Role Manager - ✅ CORRECTED (มีในไฟล์ order_manager.py)
            self.role_manager = create_order_role_manager(self.config)
            if self.role_manager:
                self.log("🎭 Role Manager initialized")
            else:
                self.log("❌ Role Manager initialization failed")
                
            # 3. สร้าง Lot Calculator - ✅ CORRECTED
            self.lot_calculator = create_lot_calculator(self.mt5_connector, self.config)
            if self.lot_calculator and self.capital_manager:
                self.lot_calculator.set_capital_manager(self.capital_manager)
                self.log("📏 Lot Calculator initialized + capital integration")
            else:
                self.log("❌ Lot Calculator initialization failed")
                
            # 4. สร้าง Enhanced Risk Manager - ✅ CORRECTED
            self.enhanced_risk_manager = EnhancedRiskManager(
                self.mt5_connector, self.config,
                capital_manager=self.capital_manager,
                role_manager=self.role_manager
            )
            if self.enhanced_risk_manager:
                self.log("🛡️ Enhanced Risk Manager initialized")
            else:
                self.log("❌ Risk Manager initialization failed")
                
            # 5. สร้าง Order Executor - ✅ FIXED (ไม่มีไฟล์แยก ใช้ built-in)
            # ใช้ built-in order execution จาก mt5_connector แทน
            self.order_executor = self.mt5_connector  # ใช้ mt5_connector ที่มี send_order methods
            if self.order_executor:
                self.log("⚡ Order Executor (MT5 built-in) initialized")
            else:
                self.log("❌ Order Executor initialization failed")
                
            # 🆕 6. สร้าง Central Order Manager v4.0 - ✅ CORRECTED
            self.order_manager = create_order_manager(self.mt5_connector, self.config)
            if self.order_manager:
                self.log("🎯 Central Order Manager v4.0 initialized")
                
                # 🔗 Integration ทุก components เข้า Order Manager
                components = {
                    'capital_manager': self.capital_manager,
                    'role_manager': self.role_manager,
                    'lot_calculator': self.lot_calculator,
                    'order_executor': self.order_executor,
                    'risk_manager': self.enhanced_risk_manager,
                    'signal_generator': None  # จะเซ็ตทีหลัง
                }
                
                integration_status = integrate_order_manager_with_system(self.order_manager, components)
                
                if integration_status:
                    self.log("✅ Order Manager integration successful")
                    self.log(f"   Components: {sum(1 for v in integration_status.values() if v == '✅')}/7 connected")
                else:
                    self.log("⚠️ Order Manager integration partially failed")
            else:
                self.log("❌ Central Order Manager initialization failed")
                
            # 7. สร้าง Signal Generator - ✅ FIXED (ไม่ต้องใช้ candlestick_analyzer)
            # Signal Generator สามารถทำงานได้โดยไม่ต้องมี candlestick_analyzer
            self.signal_generator = SignalGenerator(None, self.config)  # ส่ง None เป็น analyzer
            
            if self.signal_generator:
                # Link กับ capital manager และ role manager
                if hasattr(self.signal_generator, 'set_capital_manager') and self.capital_manager:
                    self.signal_generator.set_capital_manager(self.capital_manager)
                    
                if hasattr(self.signal_generator, 'set_role_manager') and self.role_manager:
                    self.signal_generator.set_role_manager(self.role_manager)
                
                # Link signal generator กับ order manager
                if self.order_manager:
                    self.order_manager.set_signal_generator(self.signal_generator)
                    
                self.log("🎯 Signal Generator initialized + integrations linked")
            else:
                self.log("❌ Signal Generator initialization failed")
                
            # 8. สร้าง Position Monitor - ✅ FIXED (เช็คว่ามีไฟล์หรือใช้ built-in)
            try:
                self.position_monitor = PositionMonitor(self.mt5_connector, self.config)
                
                if self.position_monitor:
                    # Link กับ capital manager และ role manager ถ้ามี method
                    if hasattr(self.position_monitor, 'set_capital_manager') and self.capital_manager:
                        self.position_monitor.set_capital_manager(self.capital_manager)
                        
                    if hasattr(self.position_monitor, 'set_role_manager') and self.role_manager:
                        self.position_monitor.set_role_manager(self.role_manager)
                        
                    self.log("📊 Position Monitor initialized")
                else:
                    self.log("❌ Position Monitor initialization failed")
            except Exception as e:
                self.log(f"⚠️ Position Monitor not available: {e}")
                self.position_monitor = None
                
            # 9. สร้าง Performance Tracker - ✅ CORRECTED
            if not self.performance_tracker:
                self.performance_tracker = PerformanceTracker(self.config)
                if self.performance_tracker:
                    self.log("📈 Performance Tracker initialized")
            
            # ✅ Final System Status Check
            system_status = self.get_system_integration_status()
            ready_components = sum(1 for status in system_status.values() if status)
            total_components = len(system_status)
            
            if ready_components >= 6:  # อย่างน้อย 6/9 components
                self.log(f"✅ Enhanced AI System v4.0 ready! ({ready_components}/{total_components} components)")
                self.log("🚀 Central Order Management System active")
                self.log("💰 Capital-aware trading enabled")
                self.log("🎭 Role intelligence enabled") 
            else:
                self.log(f"⚠️ System partially ready ({ready_components}/{total_components} components)")
                self.log("🔧 Some features may be limited")
                
        except Exception as e:
            self.log(f"❌ Enhanced system initialization error: {e}")
            import traceback
            self.log(f"📋 Error details: {traceback.format_exc()}")

    def get_system_integration_status(self) -> Dict[str, bool]:
        """🔗 ตรวจสอบสถานะการเชื่อมต่อทั้งระบบ"""
        try:
            return {
                'mt5_connector': self.mt5_connector and self.mt5_connector.is_connected,
                'capital_manager': self.capital_manager is not None,
                'role_manager': self.role_manager is not None,
                'lot_calculator': self.enhanced_lot_calculator is not None,
                'risk_manager': self.enhanced_risk_manager is not None,
                'order_executor': self.order_executor is not None,
                'order_manager': self.order_manager is not None,  # 🆕
                'signal_generator': self.enhanced_signal_generator is not None,
                'position_monitor': self.enhanced_position_monitor is not None
            }
        except Exception as e:
            return {}

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
        """💰 อัพเดท Capital Dashboard - แก้ไข method calls"""
        try:
            if not self.capital_manager:
                return
            
            # ✅ แก้ไข: ใช้ update_capital_status() แทน get_capital_status()
            capital_status = self.capital_manager.update_capital_status()
            self.capital_status = capital_status
            
            # อัพเดท trading mode - ตรวจสอบ widget ก่อน
            trading_mode = capital_status.get('trading_mode', 'unknown')
            mode_colors = {
                'normal': '#00ff88',
                'reduced': '#ffd700', 
                'conservative': '#ffaa00',
                'emergency': '#ff6b6b'
            }
            
            mode_color = mode_colors.get(trading_mode, '#cccccc')
            
            # ✅ ตรวจสอบว่ามี widget ก่อนใช้
            if hasattr(self, 'trading_mode_label') and self.trading_mode_label:
                self.trading_mode_label.config(
                    text=f"Mode: {trading_mode.upper()}",
                    fg=mode_color
                )
            
            # อัพเดท drawdown
            current_drawdown = capital_status.get('current_drawdown', 0)
            if hasattr(self, 'drawdown_label') and self.drawdown_label:
                self.drawdown_label.config(text=f"Drawdown: {current_drawdown:.2f}%")
            
            # อัพเดท zone indicators
            zones = capital_status.get('capital_zones', {})
            
            if hasattr(self, 'safe_zone_label') and self.safe_zone_label:
                self.safe_zone_label.config(
                    text=f"🟢 Safe ${zones.get('safe_zone', 0):,.0f}"
                )
            if hasattr(self, 'growth_zone_label') and self.growth_zone_label:
                self.growth_zone_label.config(
                    text=f"🟡 Growth ${zones.get('growth_zone', 0):,.0f}"
                )
            if hasattr(self, 'aggressive_zone_label') and self.aggressive_zone_label:
                self.aggressive_zone_label.config(
                    text=f"🔴 Aggressive ${zones.get('aggressive_zone', 0):,.0f}"
                )
            
            # อัพเดท metrics
            current_capital = capital_status.get('current_capital', 0)
            initial_capital = capital_status.get('initial_capital', 0)
            peak_capital = capital_status.get('peak_capital', 0)
            
            # คำนวณ reserved capital (ถ้าไม่มีใน status)
            total_zones = sum(zones.values()) if zones else 0
            reserved_capital = max(0, current_capital - total_zones)
            
            metrics_text = f"""Current Capital: ${current_capital:,.2f}
Initial Capital: ${initial_capital:,.2f}
Peak Capital: ${peak_capital:,.2f}
Capital Change: ${current_capital - initial_capital:,.2f}
Reserved Capital: ${reserved_capital:,.2f}"""
        
            if hasattr(self, 'capital_metrics_text') and self.capital_metrics_text:
                self.capital_metrics_text.config(state="normal")
                self.capital_metrics_text.delete(1.0, tk.END)
                self.capital_metrics_text.insert(tk.END, metrics_text)
                self.capital_metrics_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Capital dashboard update error: {e}")
    
    def update_role_dashboard(self):
        """🎭 อัพเดท Role Distribution Dashboard - แก้ไข method calls"""
        try:
            if not self.role_manager:
                return
            
            # ✅ แก้ไข: ใช้ get_portfolio_role_distribution() แทน get_role_distribution()
            role_status = self.role_manager.get_portfolio_role_distribution()
            
            # ตรวจสอบว่าได้ข้อมูลหรือไม่
            if 'error' in role_status:
                self.log(f"❌ Role distribution error: {role_status['error']}")
                return
                
            self.role_distribution = role_status
            
            # ดึงข้อมูลจาก distribution report
            role_data = role_status.get('roles', {})
            total_positions = role_status.get('total_positions', 0)
            balance_status = role_status.get('balance_status', 'unknown')
            
            # อัพเดท total positions - ตรวจสอบ widget ก่อน
            if hasattr(self, 'total_positions_label') and self.total_positions_label:
                self.total_positions_label.config(text=f"Total: {total_positions}")
            
            # อัพเดท balance status
            balance_colors = {
                'balanced': '#00ff88',
                'imbalanced': '#ffd700', 
                'severely_imbalanced': '#ff6b6b'
            }
            
            # แปลง balance_status เป็นคำที่เข้าใจง่าย
            balance_display = {
                'balanced': 'GOOD',
                'imbalanced': 'FAIR',
                'severely_imbalanced': 'POOR'
            }.get(balance_status, 'UNKNOWN')
            
            balance_color = balance_colors.get(balance_status, '#cccccc')
            
            if hasattr(self, 'role_balance_label') and self.role_balance_label:
                self.role_balance_label.config(
                    text=f"Balance: {balance_display}",
                    fg=balance_color
                )
            
            # อัพเดท role indicators - ตรวจสอบว่ามี dict ก่อน
            if hasattr(self, 'role_indicators') and self.role_indicators:
                for role in ['HG', 'PW', 'RH', 'SC']:
                    if role in self.role_indicators:
                        role_info = role_data.get(role, {})
                        count = role_info.get('count', 0)
                        percentage = role_info.get('percentage', 0)
                        
                        # อัพเดท count
                        if 'count' in self.role_indicators[role]:
                            self.role_indicators[role]['count'].config(text=f"{count} ({percentage:.0f}%)")
                        
                        # อัพเดท performance - หา profit จาก position_monitor
                        role_profit = 0
                        if hasattr(self, 'position_monitor') and self.position_monitor:
                            try:
                                # ลองเรียกใช้ method สำหรับ role performance
                                if hasattr(self.position_monitor, 'get_role_performance'):
                                    role_performance = self.position_monitor.get_role_performance()
                                    if role_performance and role in role_performance:
                                        role_profit = role_performance[role].get('total_profit', 0)
                            except:
                                pass  # ใช้ค่าเริ่มต้น 0
                        
                        profit_color = '#00ff88' if role_profit > 0 else '#ff6b6b' if role_profit < 0 else '#ffaa00'
                        if 'performance' in self.role_indicators[role]:
                            self.role_indicators[role]['performance'].config(
                                text=f"${role_profit:.2f}",
                                fg=profit_color
                            )
            
        except Exception as e:
            self.log(f"❌ Role dashboard update error: {e}")


    def update_risk_dashboard(self):
        """🛡️ อัพเดท Risk Status Dashboard - แก้ไข method calls"""
        try:
            if not self.enhanced_risk_manager:
                return
            
            # ✅ แก้ไข method call
            if hasattr(self.enhanced_risk_manager, 'assess_comprehensive_risk'):
                risk_status = self.enhanced_risk_manager.assess_comprehensive_risk()
            elif hasattr(self.enhanced_risk_manager, 'get_risk_status'):
                risk_status = self.enhanced_risk_manager.get_risk_status()
            else:
                # Fallback: สร้างข้อมูล dummy
                risk_status = {
                    'overall_risk': 'medium',
                    'risk_score': 0.5,
                    'can_trade': True,
                    'emergency_stop': False,
                    'warnings': [],
                    'restrictions': []
                }
            
            self.risk_assessment = risk_status
            
            # อัพเดท risk level - ตรวจสอบ widget ก่อน
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
            
            if hasattr(self, 'risk_level_label') and self.risk_level_label:
                self.risk_level_label.config(
                    text=f"{emoji} {overall_risk.upper()} RISK",
                    fg=color
                )
            
            if hasattr(self, 'risk_score_label') and self.risk_score_label:
                self.risk_score_label.config(text=f"Score: {risk_score:.2f}")
            
            # อัพเดท risk metrics - ตรวจสอบ widget ก่อน
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
            
            if hasattr(self, 'risk_metrics_text') and self.risk_metrics_text:
                self.risk_metrics_text.config(state="normal")
                self.risk_metrics_text.delete(1.0, tk.END)
                self.risk_metrics_text.insert(tk.END, metrics_text)
                self.risk_metrics_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Risk dashboard update error: {e}")
    
    def update_recovery_panel(self):
        """🔄 อัพเดท Recovery Panel - แก้ไข method calls"""
        try:
            if not self.enhanced_risk_manager:
                return
            
            # ✅ แก้ไข method call
            if hasattr(self.enhanced_risk_manager, 'get_recovery_recommendations'):
                recovery_data = self.enhanced_risk_manager.get_recovery_recommendations()
            else:
                # Fallback: สร้างข้อมูล dummy
                recovery_data = {
                    'recommendations': ['📊 ระบบทำงานปกติ'],
                    'recovery_opportunities': 0,
                    'suggested_actions': [],
                    'priority_level': 'low'
                }
            
            self.recovery_suggestions = recovery_data
            
            # อัพเดท recovery info - ตรวจสอบ widget ก่อน
            recommendations = recovery_data.get('recommendations', [])
            opportunities = recovery_data.get('recovery_opportunities', 0)
            
            if hasattr(self, 'recovery_count_label') and self.recovery_count_label:
                self.recovery_count_label.config(text=f"Opportunities: {opportunities}")
            
            # อัพเดท suggestions
            suggestions_text = "🔄 Recovery Suggestions:\n\n"
            for i, rec in enumerate(recommendations[:4], 1):
                suggestions_text += f"{i}. {rec}\n"
            
            if not recommendations:
                suggestions_text += "✅ No recovery actions needed"
            
            if hasattr(self, 'recovery_suggestions_text') and self.recovery_suggestions_text:
                self.recovery_suggestions_text.config(state="normal")
                self.recovery_suggestions_text.delete(1.0, tk.END)
                self.recovery_suggestions_text.insert(tk.END, suggestions_text)
                self.recovery_suggestions_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Recovery panel update error: {e}")
    
    def update_enhanced_positions_table(self):
        """📋 อัพเดท Enhanced Positions Table - แก้ไข method calls"""
        try:
            # ✅ แก้ไข method call สำหรับ MT5Connector
            if hasattr(self.mt5_connector, 'get_positions'):
                positions = self.mt5_connector.get_positions()
            else:
                # Fallback: ใช้ MT5 library โดยตรง
                import MetaTrader5 as mt5
                positions_raw = mt5.positions_get()
                positions = []
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
            
            # อัพเดท positions table - ตรวจสอบว่ามี Treeview ก่อน
            if hasattr(self, 'positions_tree') and self.positions_tree:
                # ล้างข้อมูลเก่า
                for item in self.positions_tree.get_children():
                    self.positions_tree.delete(item)
                
                # เพิ่มข้อมูลใหม่
                for pos in positions[:20]:  # แสดงแค่ 20 ตัวแรก
                    profit_color = 'green' if pos.get('profit', 0) > 0 else 'red'
                    
                    self.positions_tree.insert('', 'end', values=(
                        pos.get('ticket', ''),
                        pos.get('symbol', ''),
                        pos.get('type', ''),
                        f"{pos.get('volume', 0):.2f}",
                        f"{pos.get('price_open', 0):.5f}",
                        f"{pos.get('profit', 0):.2f}"
                    ))
            
            # อัพเดท positions summary
            total_positions = len(positions)
            total_profit = sum(pos.get('profit', 0) for pos in positions)
            
            if hasattr(self, 'positions_summary_label') and self.positions_summary_label:
                summary_color = '#00ff88' if total_profit >= 0 else '#ff6b6b'
                self.positions_summary_label.config(
                    text=f"Positions: {total_positions} | Total P&L: ${total_profit:.2f}",
                    fg=summary_color
                )
            
        except Exception as e:
            self.log(f"❌ Positions table update error: {e}")
    
    def update_performance_panel(self):
        """📈 อัพเดท Performance Panel - แก้ไข method calls"""
        try:
            if not self.performance_tracker:
                return
            
            # ✅ แก้ไข: ใช้ get_current_metrics() แทน get_session_metrics()
            # เพราะ get_session_metrics() return เป็น string, ไม่ใช่ dict
            if hasattr(self.performance_tracker, 'get_current_metrics'):
                performance_data = self.performance_tracker.get_current_metrics()
            elif hasattr(self.performance_tracker, 'calculate_performance_metrics'):
                # Fallback: ใช้ calculate_performance_metrics
                full_metrics = self.performance_tracker.calculate_performance_metrics()
                if 'error' in full_metrics:
                    # ถ้า error ใช้ข้อมูล session stats โดยตรง
                    performance_data = {
                        'net_profit': getattr(self.performance_tracker, 'session_stats', {}).get('total_profit', 0),
                        'total_trades': getattr(self.performance_tracker, 'session_stats', {}).get('winning_trades', 0) + getattr(self.performance_tracker, 'session_stats', {}).get('losing_trades', 0),
                        'win_rate': 0,
                        'profit_factor': 1.0
                    }
                else:
                    # Extract data จาก full metrics
                    basic_metrics = full_metrics.get('basic_metrics', {})
                    profitability_metrics = full_metrics.get('profitability_metrics', {})
                    
                    performance_data = {
                        'net_profit': profitability_metrics.get('net_profit', 0),
                        'total_trades': basic_metrics.get('total_trades', 0),
                        'win_rate': basic_metrics.get('win_rate_percent', 0),
                        'profit_factor': profitability_metrics.get('profit_factor', 1.0),
                        'winning_trades': basic_metrics.get('winning_trades', 0),
                        'losing_trades': basic_metrics.get('losing_trades', 0),
                        'gross_profit': profitability_metrics.get('gross_profit', 0),
                        'gross_loss': profitability_metrics.get('gross_loss', 0),
                        'roi_percent': profitability_metrics.get('roi_percent', 0),
                        'average_trade': profitability_metrics.get('average_trade', 0),
                        'max_consecutive_wins': basic_metrics.get('max_consecutive_wins', 0),
                        'max_consecutive_losses': basic_metrics.get('max_consecutive_losses', 0)
                    }
            else:
                # Fallback: สร้างข้อมูล dummy จาก session_stats โดยตรง
                session_stats = getattr(self.performance_tracker, 'session_stats', {})
                total_trades = session_stats.get('winning_trades', 0) + session_stats.get('losing_trades', 0)
                win_rate = (session_stats.get('winning_trades', 0) / total_trades * 100) if total_trades > 0 else 0
                
                performance_data = {
                    'net_profit': session_stats.get('total_profit', 0),
                    'total_trades': total_trades,
                    'win_rate': win_rate,
                    'profit_factor': 1.0,
                    'winning_trades': session_stats.get('winning_trades', 0),
                    'losing_trades': session_stats.get('losing_trades', 0),
                    'gross_profit': session_stats.get('gross_profit', 0),
                    'gross_loss': session_stats.get('gross_loss', 0),
                    'roi_percent': 0,
                    'average_trade': session_stats.get('total_profit', 0) / total_trades if total_trades > 0 else 0,
                    'max_consecutive_wins': session_stats.get('max_consecutive_wins', 0),
                    'max_consecutive_losses': session_stats.get('max_consecutive_losses', 0)
                }
            
            # ตรวจสอบว่าได้ข้อมูลเป็น dict
            if not isinstance(performance_data, dict):
                self.log(f"❌ Performance data is not dict: {type(performance_data)}")
                return
            
            self.portfolio_metrics = performance_data
            
            # ดึงค่าสำคัญ
            net_profit = performance_data.get('net_profit', 0)
            total_trades = performance_data.get('total_trades', 0)
            win_rate = performance_data.get('win_rate', 0)
            average_trade = performance_data.get('average_trade', 0)
            profit_factor = performance_data.get('profit_factor', 1.0)
            
            # อัพเดท performance metrics - ตรวจสอบ widgets ก่อน
            if hasattr(self, 'net_profit_metric') and self.net_profit_metric:
                profit_color = '#00ff88' if net_profit > 0 else '#ff6b6b' if net_profit < 0 else '#ffaa00'
                self.net_profit_metric.config(text=f"Net P/L: ${net_profit:.2f}", fg=profit_color)
            
            if hasattr(self, 'win_rate_metric') and self.win_rate_metric:
                win_color = '#00ff88' if win_rate >= 60 else '#ffd700' if win_rate >= 40 else '#ff6b6b'
                self.win_rate_metric.config(text=f"Win Rate: {win_rate:.0f}%", fg=win_color)
            
            if hasattr(self, 'avg_trade_metric') and self.avg_trade_metric:
                self.avg_trade_metric.config(text=f"Avg Trade: ${average_trade:.2f}")
            
            if hasattr(self, 'profit_factor_metric') and self.profit_factor_metric:
                self.profit_factor_metric.config(text=f"P.Factor: {profit_factor:.2f}")
            
            # อัพเดท performance summary
            chart_text = f"""📊 Session Performance Summary:

Total Trades: {total_trades}
Winning Trades: {performance_data.get('winning_trades', 0)}
Losing Trades: {performance_data.get('losing_trades', 0)}

Gross Profit: ${performance_data.get('gross_profit', 0):.2f}
Gross Loss: ${performance_data.get('gross_loss', 0):.2f}

ROI: {performance_data.get('roi_percent', 0):.2f}%
Max Consecutive Wins: {performance_data.get('max_consecutive_wins', 0)}
Max Consecutive Losses: {performance_data.get('max_consecutive_losses', 0)}"""
        
            if hasattr(self, 'performance_chart_text') and self.performance_chart_text:
                self.performance_chart_text.config(state="normal")
                self.performance_chart_text.delete(1.0, tk.END)
                self.performance_chart_text.insert(tk.END, chart_text)
                self.performance_chart_text.config(state="disabled")
            elif hasattr(self, 'performance_metrics_text') and self.performance_metrics_text:
                # ถ้าไม่มี performance_chart_text ใช้ performance_metrics_text แทน
                self.performance_metrics_text.config(state="normal")
                self.performance_metrics_text.delete(1.0, tk.END)
                self.performance_metrics_text.insert(tk.END, chart_text)
                self.performance_metrics_text.config(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Performance panel update error: {e}")
            # Debug information
            if hasattr(self, 'performance_tracker') and self.performance_tracker:
                available_methods = [method for method in dir(self.performance_tracker) if not method.startswith('_')]
                self.log(f"Available methods in performance_tracker: {available_methods[:10]}...")  # แสดงแค่ 10 ตัวแรก

    # ==========================================
    # 🔍 MT5 CONNECTION METHODS (Streamlined)
    # ==========================================
    
    def scan_mt5_terminals(self):
        """🔍 สแกน MT5 Terminals - FIXED"""
        try:
            self.log("🔍 Scanning for MT5 terminals...")
            self.update_system_status("🔍 Scanning...")
            
            # ใช้ threading เพื่อไม่ให้ GUI แขวน
            def scan_thread():
                try:
                    # ✅ แก้ไข: ใช้ method ที่มีจริง
                    terminals = self.mt5_connector.find_running_mt5_installations()
                    
                    # อัพเดท GUI ใน main thread
                    self.root.after(0, lambda: self._update_terminals_list(terminals))
                    
                except Exception as e:
                    self.log(f"❌ Terminal scan error: {e}")
                    self.root.after(0, lambda: self.update_system_status("❌ Scan Failed"))
            
            threading.Thread(target=scan_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Scan terminals error: {e}")
            
    def _update_terminals_list(self, installations: List):
        """📝 อัพเดทรายการ terminals"""
        try:
            if installations:
                self.log(f"✅ Found {len(installations)} MT5 terminals")
                self.update_system_status(f"✅ Found {len(installations)} Terminals")
                
                # เก็บรายการ installations
                self.available_terminals = installations
                
                # แสดง Terminal Selection Dialog
                self._show_terminal_selection_dialog(installations)
                
            else:
                self.log("❌ No MT5 terminals found")
                self.update_system_status("❌ No Terminals Found")
                
                # แสดง Help Message
                messagebox.showinfo(
                    "No Terminals Found", 
                    "ไม่พบ MT5 Terminals ที่ทำงานอยู่\n\n" +
                    "วิธีแก้ไข:\n" +
                    "1. เปิด MetaTrader 5 และ Login\n" +
                    "2. รอสักครู่ให้โปรแกรมเสถียร\n" +
                    "3. กด Scan อีกครั้ง"
                )
                
        except Exception as e:
            self.log(f"❌ Terminal list update error: {e}")
    
    def _show_terminal_selection_dialog(self, installations: List):
        """🖥️ แสดง Dialog เลือก MT5 Terminal"""
        try:
            # สร้างหน้าต่างเลือก Terminal
            selection_window = tk.Toplevel(self.root)
            selection_window.title("🔍 Select MT5 Terminal")
            selection_window.geometry("600x400")
            selection_window.configure(bg="#1a1a2e")
            selection_window.resizable(False, False)
            
            # ทำให้อยู่ด้านหน้า
            selection_window.transient(self.root)
            selection_window.grab_set()
            
            # Header
            header_frame = tk.Frame(selection_window, bg="#1a1a2e")
            header_frame.pack(fill="x", padx=10, pady=10)
            
            tk.Label(
                header_frame,
                text=f"🔍 Found {len(installations)} MT5 Terminals",
                font=("Arial", 16, "bold"), fg="#00d4aa", bg="#1a1a2e"
            ).pack()
            
            tk.Label(
                header_frame,
                text="Please select the terminal you want to connect to:",
                font=("Arial", 10), fg="#ffffff", bg="#1a1a2e"
            ).pack(pady=(5, 0))
            
            # Terminal List Frame
            list_frame = tk.Frame(selection_window, bg="#1a1a2e")
            list_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Listbox with Scrollbar
            listbox_frame = tk.Frame(list_frame, bg="#1a1a2e")
            listbox_frame.pack(fill="both", expand=True)
            
            scrollbar = tk.Scrollbar(listbox_frame)
            scrollbar.pack(side="right", fill="y")
            
            self.terminal_listbox = tk.Listbox(
                listbox_frame,
                font=("Consolas", 11),
                bg="#0f0f0f", fg="#ffffff",
                selectbackground="#3498db", selectforeground="#ffffff",
                yscrollcommand=scrollbar.set,
                height=12
            )
            self.terminal_listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=self.terminal_listbox.yview)
            
            # เพิ่มรายการ terminals
            for i, installation in enumerate(installations):
                broker = installation.broker
                exe_type = "64-bit" if "64" in installation.executable_type else "32-bit"
                status = "🟢 Running" if installation.is_running else "🔴 Stopped"
                path_short = "..." + installation.path[-50:] if len(installation.path) > 50 else installation.path
                
                display_text = f"[{i+1:2d}] {broker} ({exe_type}) - {status}"
                detail_text = f"      Path: {path_short}"
                
                self.terminal_listbox.insert(tk.END, display_text)
                self.terminal_listbox.insert(tk.END, detail_text)
                self.terminal_listbox.insert(tk.END, "")  # Empty line for spacing
            
            # Buttons Frame
            button_frame = tk.Frame(selection_window, bg="#1a1a2e")
            button_frame.pack(fill="x", padx=10, pady=10)
            
            # Select Button
            def on_select():
                try:
                    selection = self.terminal_listbox.curselection()
                    if not selection:
                        messagebox.showwarning("No Selection", "Please select a terminal first!")
                        return
                    
                    # คำนวณ index จริง (เพราะมี empty lines)
                    selected_line = selection[0]
                    terminal_index = selected_line // 3  # 3 lines per terminal
                    
                    if terminal_index < len(installations):
                        selected_terminal = installations[terminal_index]
                        
                        # เก็บการเลือก
                        self.selected_terminal = selected_terminal
                        self.mt5_connector.selected_mt5 = selected_terminal
                        
                        self.log(f"✅ Selected: {selected_terminal.broker}")
                        
                        # เปิดใช้งาน Connect button
                        self.connect_button.config(state="normal", text="🔗 Connect")
                        self.update_system_status(f"✅ Terminal Selected")
                        
                        # ปิดหน้าต่าง
                        selection_window.destroy()
                    
                except Exception as e:
                    self.log(f"❌ Terminal selection error: {e}")
            
            tk.Button(
                button_frame, text="🔗 Select & Continue", 
                command=on_select,
                bg="#00d4aa", fg="white", font=("Arial", 12, "bold"),
                width=20, height=1
            ).pack(side="left", padx=5)
            
            # Cancel Button
            def on_cancel():
                selection_window.destroy()
                self.update_system_status("❌ Selection cancelled")
            
            tk.Button(
                button_frame, text="❌ Cancel", 
                command=on_cancel,
                bg="#e74c3c", fg="white", font=("Arial", 12),
                width=10, height=1
            ).pack(side="right", padx=5)
            
            # Center the window
            selection_window.update_idletasks()
            x = (selection_window.winfo_screenwidth() // 2) - (selection_window.winfo_width() // 2)
            y = (selection_window.winfo_screenheight() // 2) - (selection_window.winfo_height() // 2)
            selection_window.geometry(f"+{x}+{y}")
            
            # Focus on first item
            if installations:
                self.terminal_listbox.selection_set(0)
                self.terminal_listbox.focus_set()
            
        except Exception as e:
            self.log(f"❌ Terminal selection dialog error: {e}")

# ==========================================
# 🔧 แทนที่ method scan_mt5_terminals ใน main.py
# ==========================================

    def scan_mt5_terminals(self):
        """🔍 สแกน MT5 Terminals - CORRECTED"""
        try:
            self.log("🔍 Scanning for MT5 terminals...")
            self.update_system_status("🔍 Scanning...")
            
            # ใช้ threading เพื่อไม่ให้ GUI แขวน
            def scan_thread():
                try:
                    # ✅ ใช้ method ที่มีจริงใน MT5Connector
                    installations = self.mt5_connector.find_running_mt5_installations()
                    
                    # อัพเดท GUI ใน main thread
                    self.root.after(0, lambda: self._update_terminals_list(installations))
                    
                except Exception as e:
                    self.log(f"❌ Terminal scan error: {e}")
                    self.root.after(0, lambda: self.update_system_status("❌ Scan Failed"))
            
            threading.Thread(target=scan_thread, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Scan terminals error: {e}")

    def _update_terminals_list(self, terminals):
        """📝 อัพเดทรายการ terminals - ENHANCED"""
        try:
            if terminals:
                self.log(f"✅ Found {len(terminals)} MT5 terminals")
                self.update_system_status(f"✅ Found {len(terminals)} Terminals")
                
                # เก็บรายการ installations
                self.available_terminals = terminals
                
                # แสดง Terminal Selection Dialog
                self._show_terminal_selection_dialog(terminals)
                
            else:
                self.log("❌ No MT5 terminals found")
                self.update_system_status("❌ No Terminals Found")
                
                # แสดง Help Message
                messagebox.showinfo(
                    "No Terminals Found", 
                    "ไม่พบ MT5 Terminals ที่ทำงานอยู่\n\n" +
                    "วิธีแก้ไข:\n" +
                    "1. เปิด MetaTrader 5 และ Login\n" +
                    "2. รอสักครู่ให้โปรแกรมเสถียร\n" +
                    "3. กด Scan อีกครั้ง"
                )
                
        except Exception as e:
            self.log(f"❌ Terminal list update error: {e}")

    def _show_terminal_selection_dialog(self, installations):
        """🖥️ แสดง Dialog เลือก MT5 Terminal - เพิ่มใหม่"""
        try:
            # สร้างหน้าต่างเลือก Terminal
            selection_window = tk.Toplevel(self.root)
            selection_window.title("🔍 Select MT5 Terminal")
            selection_window.geometry("600x400")
            selection_window.configure(bg="#1a1a2e")
            selection_window.resizable(False, False)
            
            # ทำให้อยู่ด้านหน้า
            selection_window.transient(self.root)
            selection_window.grab_set()
            
            # Header
            header_frame = tk.Frame(selection_window, bg="#1a1a2e")
            header_frame.pack(fill="x", padx=10, pady=10)
            
            tk.Label(
                header_frame,
                text=f"🔍 Found {len(installations)} MT5 Terminals",
                font=("Arial", 16, "bold"), fg="#00d4aa", bg="#1a1a2e"
            ).pack()
            
            tk.Label(
                header_frame,
                text="Please select the terminal you want to connect to:",
                font=("Arial", 10), fg="#ffffff", bg="#1a1a2e"
            ).pack(pady=(5, 0))
            
            # Terminal List Frame
            list_frame = tk.Frame(selection_window, bg="#1a1a2e")
            list_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Listbox with Scrollbar
            listbox_frame = tk.Frame(list_frame, bg="#1a1a2e")
            listbox_frame.pack(fill="both", expand=True)
            
            scrollbar = tk.Scrollbar(listbox_frame)
            scrollbar.pack(side="right", fill="y")
            
            self.terminal_listbox = tk.Listbox(
                listbox_frame,
                font=("Consolas", 11),
                bg="#0f0f0f", fg="#ffffff",
                selectbackground="#3498db", selectforeground="#ffffff",
                yscrollcommand=scrollbar.set,
                height=12
            )
            self.terminal_listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=self.terminal_listbox.yview)
            
            # เพิ่มรายการ terminals
            for i, installation in enumerate(installations):
                broker = installation.broker
                exe_type = "64-bit" if "64" in installation.executable_type else "32-bit"
                status = "🟢 Running" if installation.is_running else "🔴 Stopped"
                path_short = "..." + installation.path[-50:] if len(installation.path) > 50 else installation.path
                
                display_text = f"[{i+1:2d}] {broker} ({exe_type}) - {status}"
                detail_text = f"      Path: {path_short}"
                
                self.terminal_listbox.insert(tk.END, display_text)
                self.terminal_listbox.insert(tk.END, detail_text)
                self.terminal_listbox.insert(tk.END, "")  # Empty line for spacing
            
            # Buttons Frame
            button_frame = tk.Frame(selection_window, bg="#1a1a2e")
            button_frame.pack(fill="x", padx=10, pady=10)
            
            # Select Button
            def on_select():
                try:
                    selection = self.terminal_listbox.curselection()
                    if not selection:
                        messagebox.showwarning("No Selection", "Please select a terminal first!")
                        return
                    
                    # คำนวณ index จริง (เพราะมี empty lines)
                    selected_line = selection[0]
                    terminal_index = selected_line // 3  # 3 lines per terminal
                    
                    if terminal_index < len(installations):
                        selected_terminal = installations[terminal_index]
                        
                        # เก็บการเลือก
                        self.selected_terminal = selected_terminal
                        self.mt5_connector.selected_mt5 = selected_terminal
                        
                        self.log(f"✅ Selected: {selected_terminal.broker}")
                        
                        # เปิดใช้งาน Connect button
                        self.connect_button.config(state="normal", text="🔗 Connect")
                        self.update_system_status(f"✅ Terminal Selected")
                        
                        # ปิดหน้าต่าง
                        selection_window.destroy()
                    
                except Exception as e:
                    self.log(f"❌ Terminal selection error: {e}")
            
            tk.Button(
                button_frame, text="🔗 Select & Continue", 
                command=on_select,
                bg="#00d4aa", fg="white", font=("Arial", 12, "bold"),
                width=20, height=1
            ).pack(side="left", padx=5)
            
            # Cancel Button
            def on_cancel():
                selection_window.destroy()
                self.update_system_status("❌ Selection cancelled")
            
            tk.Button(
                button_frame, text="❌ Cancel", 
                command=on_cancel,
                bg="#e74c3c", fg="white", font=("Arial", 12),
                width=10, height=1
            ).pack(side="right", padx=5)
            
            # Center the window
            selection_window.update_idletasks()
            x = (selection_window.winfo_screenwidth() // 2) - (selection_window.winfo_width() // 2)
            y = (selection_window.winfo_screenheight() // 2) - (selection_window.winfo_height() // 2)
            selection_window.geometry(f"+{x}+{y}")
            
            # Focus on first item
            if installations:
                self.terminal_listbox.selection_set(0)
                self.terminal_listbox.focus_set()
            
        except Exception as e:
            self.log(f"❌ Terminal selection dialog error: {e}")

    def connect_mt5(self):
        """🔗 เชื่อมต่อ MT5 - ENHANCED"""
        try:
            # ตรวจสอบว่าเลือก terminal แล้วหรือยัง
            if not hasattr(self, 'selected_terminal') or not self.selected_terminal:
                messagebox.showwarning(
                    "No Terminal Selected", 
                    "Please scan and select a terminal first!\n\n" +
                    "Steps:\n" +
                    "1. Click 'Scan' button\n" +
                    "2. Select a terminal from the list\n" +
                    "3. Click 'Connect'"
                )
                return
            
            terminal = self.selected_terminal
            self.log(f"🔗 Connecting to: {terminal.broker}")
            self.update_system_status("🔗 Connecting...")
            
            def connect_thread():
                try:
                    # เชื่อมต่อกับ terminal ที่เลือก
                    success = self.mt5_connector.connect_to_selected_terminal(terminal)
                    
                    if success:
                        # อัพเดท GUI
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
        """🚀 เริ่ม Enhanced Trading System - เวอร์ชั่นสุดท้าย"""
        try:
            if not self.mt5_connector.is_connected:
                messagebox.showerror("Error", "กรุณาเชื่อมต่อ MT5 ก่อน")
                return
            
            if not self.enhanced_risk_manager:
                messagebox.showerror("Error", "Enhanced Risk Manager ไม่พร้อม")
                return
            
            # ตรวจสอบ risk ก่อนเริ่ม
            risk_status = {}
            
            try:
                # ลอง method หลักก่อน
                if hasattr(self.enhanced_risk_manager, 'check_risk_levels'):
                    risk_status = self.enhanced_risk_manager.check_risk_levels()
                elif hasattr(self.enhanced_risk_manager, 'assess_comprehensive_risk'):
                    risk_status = self.enhanced_risk_manager.assess_comprehensive_risk()
                elif hasattr(self.enhanced_risk_manager, 'get_risk_status'):
                    risk_status = self.enhanced_risk_manager.get_risk_status()
                else:
                    # ถ้าไม่มี method ใดๆ ใช้ข้อมูล default
                    self.log("⚠️ Risk Manager methods not available - using default risk check")
                    risk_status = {
                        'can_trade': True,
                        'emergency_stop': False,
                        'overall_risk': 'medium',
                        'warnings': ['Risk Manager method not available'],
                        'restrictions': []
                    }
                    
            except Exception as risk_error:
                self.log(f"❌ Risk check error: {risk_error}")
                # ถาม user ว่าจะเริ่มหรือไม่
                result = messagebox.askyesno(
                    "Risk Check Error", 
                    f"ไม่สามารถตรวจสอบ risk ได้: {risk_error}\n\nต้องการเริ่มเทรดต่อไปหรือไม่?"
                )
                
                if not result:
                    return
                    
                risk_status = {
                    'can_trade': True,
                    'emergency_stop': False,
                    'overall_risk': 'unknown',
                    'warnings': [f'Risk check failed: {risk_error}'],
                    'restrictions': []
                }
            
            # ตรวจสอบผลการ risk check
            if risk_status.get('emergency_stop', False):
                messagebox.showerror("Risk Warning", "ไม่สามารถเทรดได้: Emergency stop active")
                self.log("🚨 Trading blocked: Emergency stop")
                return
            
            if not risk_status.get('can_trade', True):
                # แสดง warnings ให้ user เห็น
                warnings = risk_status.get('warnings', [])
                warning_text = "\n".join(warnings[:3]) if warnings else "Risk level high"
                
                result = messagebox.askyesno(
                    "Risk Warning", 
                    f"Risk warnings detected:\n\n{warning_text}\n\nต้องการเริ่มเทรดหรือไม่?"
                )
                
                if not result:
                    self.log("🛑 Trading cancelled by user (risk warnings)")
                    return
            
            # ตรวจสอบ system readiness (ใช้ชื่อตามโค้ดของคุณ)
            if not hasattr(self, 'enhanced_signal_generator') or not self.enhanced_signal_generator:
                messagebox.showwarning("Warning", "Enhanced Signal Generator ไม่พร้อม - จะใช้ fallback mode")
                
            if not self.order_manager:
                messagebox.showerror("Error", "Order Manager ไม่พร้อม")
                return
            
            # เริ่มเทรด
            self.is_trading = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # อัพเดท status
            risk_level = risk_status.get('overall_risk', 'unknown').upper()
            self.update_system_status(f"🚀 Trading Active (Risk: {risk_level})")
            
            # Log risk summary
            warnings_count = len(risk_status.get('warnings', []))
            restrictions_count = len(risk_status.get('restrictions', []))
            self.log(f"🚀 Trading started with {warnings_count} warnings, {restrictions_count} restrictions")
            
            # แสดง risk warnings ถ้ามี
            if warnings_count > 0:
                for warning in risk_status.get('warnings', [])[:3]:
                    self.log(f"⚠️ {warning}")
            
            # เริ่ม trading thread โดยเรียกใช้ trading_loop ที่มีอยู่
            self.trading_thread = threading.Thread(target=self.trading_loop, daemon=True)
            self.trading_thread.start()
            
            self.log("✅ Enhanced AI Trading System started successfully")
            
        except Exception as e:
            self.log(f"❌ Start trading error: {e}")
            
            # Debug information
            if hasattr(self, 'enhanced_risk_manager') and self.enhanced_risk_manager:
                available_methods = [method for method in dir(self.enhanced_risk_manager) 
                                if not method.startswith('_') and callable(getattr(self.enhanced_risk_manager, method))]
                self.log(f"Debug: Available risk manager methods: {available_methods[:5]}...")
            
            messagebox.showerror("Start Error", f"ไม่สามารถเริ่มเทรดได้: {e}")
            
            # Reset buttons on error
            self.is_trading = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.update_system_status("❌ Trading Start Failed")

    def stop_trading(self):
        """🛑 หยุด Trading System"""
        try:
            if not self.is_trading:
                return
            
            self.log("🛑 Stopping Enhanced AI Trading System...")
            
            self.is_trading = False
            
            # รอให้ trading thread หยุด
            if self.trading_thread and self.trading_thread.is_alive():
                self.trading_thread.join(timeout=3.0)
            
            # Reset buttons
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            # อัพเดท status
            self.update_system_status("🛑 Trading Stopped")
            
            # แสดงสรุปผลการเทรด
            if self.performance_tracker:
                try:
                    if hasattr(self.performance_tracker, 'get_current_metrics'):
                        metrics = self.performance_tracker.get_current_metrics()
                        total_trades = metrics.get('total_trades', 0)
                        net_profit = metrics.get('net_profit', 0)
                        self.log(f"📊 Session summary: {total_trades} trades, ${net_profit:.2f} net")
                except:
                    pass
            
            self.log("✅ Trading stopped successfully")
            
        except Exception as e:
            self.log(f"❌ Stop trading error: {e}")

    
    def trading_loop(self):
        """🎯 Main trading loop ที่ใช้ Central Order Manager v4.0"""
        try:
            self.log("🎯 Enhanced Trading Loop v4.0 started")
            self.log("🔄 Using Central Order Management System")
            
            while self.is_trading:
                loop_start_time = time.time()
                
                try:
                    # 1. ตรวจสอบการเชื่อมต่อ
                    if not self.mt5_connector or not self.mt5_connector.is_connected:
                        self.log("⚠️ MT5 connection lost - attempting reconnect...")
                        time.sleep(10)
                        continue
                    
                    # 2. อัพเดท Capital Status
                    if self.capital_manager:
                        self.capital_manager.update_capital_status()
                        capital_status = self.capital_manager.get_capital_status()
                        
                        # เช็ค emergency mode
                        if capital_status.get('trading_mode') == 'emergency':
                            self.log("🚨 Emergency mode active - trading limited")
                            time.sleep(30)  # หน่วงนานขึ้นใน emergency
                            continue
                    
                    # 3. อัพเดท Role Manager (cleanup closed positions)
                    if self.role_manager and self.enhanced_position_monitor:
                        current_positions = self.enhanced_position_monitor.get_current_positions()
                        active_position_ids = [str(pos.get('ticket', pos.get('id', ''))) for pos in current_positions]
                        self.role_manager.cleanup_closed_positions(active_position_ids)
                    
                    # 4. Generate Trading Signal
                    if self.enhanced_signal_generator:
                        signal_data = self.enhanced_signal_generator.generate_signal()
                        
                        if signal_data and signal_data.get('action') in ['BUY', 'SELL']:
                            self.log(f"📊 New signal: {signal_data['action']} (Strength: {signal_data.get('strength', 0):.2f})")
                            
                            # 🆕 5. Process Signal ผ่าน Central Order Manager
                            if self.order_manager:
                                processing_result = self.order_manager.process_trading_signal(signal_data)
                                
                                if processing_result:
                                    if processing_result.get('success'):
                                        self.log(f"✅ Order executed successfully")
                                        order_details = processing_result.get('order_details', {})
                                        self.log(f"   Action: {order_details.get('action')}")
                                        self.log(f"   Lot: {order_details.get('lot_size')}")
                                        self.log(f"   Role: {order_details.get('role')}")
                                        self.log(f"   Zone: {order_details.get('capital_zone')}")
                                        
                                        # อัพเดท performance tracking
                                        if self.performance_tracker:
                                            self.performance_tracker.record_execution(
                                                processing_result.get('execution_result', {}),
                                                signal_data
                                            )
                                    else:
                                        # Log rejection reason
                                        reason = processing_result.get('reason', processing_result.get('error', 'Unknown'))
                                        stage = processing_result.get('stage', 'unknown')
                                        
                                        if processing_result.get('blocked'):
                                            self.log(f"🚫 Signal blocked at {stage}: {reason}")
                                        elif processing_result.get('delayed'):
                                            wait_time = processing_result.get('wait_seconds', 0)
                                            self.log(f"⏰ Signal delayed {wait_time}s: {reason}")
                                        else:
                                            self.log(f"❌ Signal failed at {stage}: {reason}")
                            else:
                                # Fallback to direct order executor (ถ้า order manager ไม่พร้อม)
                                self.log("⚠️ Using fallback execution (no order manager)")
                                if self.order_executor:
                                    result = self.order_executor.execute_signal(signal_data)
                                    if result and result.get('success'):
                                        self.log("✅ Order executed (fallback mode)")
                    
                    # 6. Monitor Positions
                    if self.enhanced_position_monitor:
                        self.enhanced_position_monitor.monitor_positions()
                    
                    # 7. Update Performance Metrics
                    if self.performance_tracker:
                        self.performance_tracker.update_session_metrics()
                    
                    # 8. Adaptive Loop Timing
                    loop_duration = time.time() - loop_start_time
                    
                    # ปรับ sleep time ตาม trading mode
                    if self.capital_manager:
                        trading_mode = capital_status.get('trading_mode', 'normal')
                        if trading_mode == 'emergency':
                            sleep_time = 30  # ช้าลงใน emergency
                        elif trading_mode == 'conservative':
                            sleep_time = 20  # ช้าลงใน conservative
                        elif trading_mode == 'recovery':
                            sleep_time = 10  # เร็วขึ้นใน recovery
                        else:
                            sleep_time = 15  # normal mode
                    else:
                        sleep_time = 15  # default
                    
                    # ลบเวลาที่ใช้ประมวลผลออก
                    actual_sleep = max(1, sleep_time - loop_duration)
                    time.sleep(actual_sleep)
                    
                except Exception as loop_error:
                    self.log(f"❌ Trading loop error: {loop_error}")
                    time.sleep(30)  # พักนานขึ้นเมื่อเกิดข้อผิดพลาด
                    
        except Exception as e:
            self.log(f"❌ Trading loop critical error: {e}")
            import traceback
            self.log(f"📋 Error traceback: {traceback.format_exc()}")
        finally:
            self.log("🛑 Enhanced Trading Loop v4.0 stopped")
    
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
        """🔒 Enhanced Shutdown Procedure - แก้ไข method calls"""
        try:
            self.log("🔒 Shutting down Enhanced AI Trading System...")
            
            # หยุด GUI updates
            self.gui_update_active = False
            
            # หยุด trading
            if self.is_trading:
                self.stop_trading()
                time.sleep(2)
            
            # Save enhanced session data - ✅ ตรวจสอบ methods ก่อนเรียกใช้
            
            # 1. Capital Manager - ตรวจสอบว่ามี method save อะไรบ้าง
            if self.capital_manager:
                try:
                    # ลองหา method ที่เกี่ยวกับ save
                    if hasattr(self.capital_manager, 'save_session_data'):
                        self.capital_manager.save_session_data()
                    elif hasattr(self.capital_manager, 'save_capital_data'):
                        self.capital_manager.save_capital_data()
                    elif hasattr(self.capital_manager, 'save_to_persistence'):
                        self.capital_manager.save_to_persistence()
                    else:
                        # ไม่มี save method - แค่ log ว่าข้าม
                        self.log("💰 Capital Manager: No save method available (data in memory only)")
                        
                    self.log("💰 Capital session data processed")
                    
                except Exception as e:
                    self.log(f"❌ Capital Manager save error: {e}")
            
            # 2. Role Manager - ตรวจสอบ methods
            if self.role_manager:
                try:
                    if hasattr(self.role_manager, 'save_role_history'):
                        self.role_manager.save_role_history()
                    elif hasattr(self.role_manager, 'save_role_data'):
                        self.role_manager.save_role_data()
                    elif hasattr(self.role_manager, 'cleanup_closed_positions'):
                        # ใช้ cleanup แทน save
                        active_positions = self._get_current_position_ids()
                        self.role_manager.cleanup_closed_positions(active_positions)
                        self.log("🎭 Role data cleaned up")
                    else:
                        self.log("🎭 Role Manager: No save method available (data in memory only)")
                        
                    self.log("🎭 Role history processed")
                    
                except Exception as e:
                    self.log(f"❌ Role Manager save error: {e}")
            
            # 3. Performance Tracker - ตรวจสอบ methods
            if self.performance_tracker:
                try:
                    if hasattr(self.performance_tracker, 'save_session_stats'):
                        self.performance_tracker.save_session_stats()
                    elif hasattr(self.performance_tracker, 'save_to_persistence'):
                        self.performance_tracker.save_to_persistence()
                    elif hasattr(self.performance_tracker, 'export_session_data'):
                        self.performance_tracker.export_session_data()
                    else:
                        # ไม่มี save method - แสดงสรุปผลงาน
                        if hasattr(self.performance_tracker, 'get_current_metrics'):
                            metrics = self.performance_tracker.get_current_metrics()
                            total_trades = metrics.get('total_trades', 0)
                            net_profit = metrics.get('net_profit', 0)
                            self.log(f"📈 Session Summary: {total_trades} trades, ${net_profit:.2f} profit")
                        else:
                            self.log("📈 Performance Tracker: Session completed")
                            
                    self.log("📈 Performance data processed")
                    
                except Exception as e:
                    self.log(f"❌ Performance Tracker save error: {e}")
            
            # 4. Enhanced Risk Manager - ตรวจสอบ methods
            if self.enhanced_risk_manager:
                try:
                    if hasattr(self.enhanced_risk_manager, 'save_risk_data'):
                        self.enhanced_risk_manager.save_risk_data()
                    elif hasattr(self.enhanced_risk_manager, 'export_risk_summary'):
                        self.enhanced_risk_manager.export_risk_summary()
                    else:
                        self.log("🛡️ Risk Manager: Session completed")
                        
                except Exception as e:
                    self.log(f"❌ Risk Manager save error: {e}")
            
            # 5. Order Manager - ตรวจสอบ methods
            if self.order_manager:
                try:
                    if hasattr(self.order_manager, 'cleanup_old_history'):
                        self.order_manager.cleanup_old_history()
                        self.log("📦 Order history cleaned up")
                    elif hasattr(self.order_manager, 'save_order_history'):
                        self.order_manager.save_order_history()
                        self.log("📦 Order history saved")
                    else:
                        self.log("📦 Order Manager: Session completed")
                        
                except Exception as e:
                    self.log(f"❌ Order Manager cleanup error: {e}")
            
            # 6. Position Monitor - ตรวจสอบ methods  
            if self.position_monitor:
                try:
                    if hasattr(self.position_monitor, 'save_monitor_data'):
                        self.position_monitor.save_monitor_data()
                    elif hasattr(self.position_monitor, 'cleanup_cache'):
                        self.position_monitor.cleanup_cache()
                        self.log("📊 Position cache cleaned up")
                    else:
                        self.log("📊 Position Monitor: Session completed")
                        
                except Exception as e:
                    self.log(f"❌ Position Monitor cleanup error: {e}")
            
            # Disconnect MT5
            try:
                if self.mt5_connector and self.mt5_connector.is_connected:
                    self.mt5_connector.disconnect()
                    self.log("🔌 MT5 disconnected")
            except Exception as e:
                self.log(f"❌ MT5 disconnect error: {e}")
            
            self.log("✅ Enhanced system shutdown completed")
            
            # ปิดโปรแกรม
            self.root.destroy()
            
        except Exception as e:
            print(f"❌ Shutdown error: {e}")
            try:
                self.root.destroy()
            except:
                pass

    def _get_current_position_ids(self) -> List[str]:
        """🔍 ดึง position IDs ปัจจุบันสำหรับ cleanup"""
        try:
            if not self.mt5_connector or not self.mt5_connector.is_connected:
                return []
            
            # ลองใช้ method ที่มีอยู่
            if hasattr(self.mt5_connector, 'get_positions'):
                positions = self.mt5_connector.get_positions()
                return [str(pos.get('ticket', '')) for pos in positions if pos.get('ticket')]
            else:
                # ใช้ MT5 library โดยตรง
                import MetaTrader5 as mt5
                positions = mt5.positions_get()
                if positions:
                    return [str(pos.ticket) for pos in positions]
                return []
                
        except Exception as e:
            print(f"❌ Get position IDs error: {e}")
            return []

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