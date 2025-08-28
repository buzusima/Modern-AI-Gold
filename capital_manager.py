"""
💰 Capital-Based Portfolio Manager v4.0
capital_manager.py

🚀 NEW FEATURES:
✅ Capital Zone Allocation (Safe/Growth/Aggressive) 
✅ Drawdown-based Protection (30% max)
✅ Progressive Risk Scaling
✅ Recovery Mode Logic
✅ Dynamic Capital Tracking
✅ Live Capital Dashboard Integration

🎯 บริหารทุนอัจฉริยะตามจำนวนเงินจริง
ป้องกันพอร์ตแตก + เพิ่มประสิทธิภาพการใช้ทุน
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json

class CapitalManager:
    """
    💰 Capital-Based Portfolio Manager
    
    จัดการทุนแบบ Zone-based + Drawdown Protection
    ปรับ lot size และ risk ตามสถานะทุน
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """
        🔧 เริ่มต้น Capital Manager
        
        Args:
            mt5_connector: MT5 connection object
            config: การตั้งค่าระบบ
        """
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Capital configuration
        self.capital_config = config.get("capital_management", {})
        
        # Capital zones (% allocation)
        self.safe_zone_percent = self.capital_config.get("safe_zone_percent", 50.0)      # 50%
        self.growth_zone_percent = self.capital_config.get("growth_zone_percent", 35.0)  # 35% 
        self.aggressive_zone_percent = self.capital_config.get("aggressive_zone_percent", 15.0)  # 15%
        
        # Drawdown protection
        self.max_drawdown_percent = self.capital_config.get("max_drawdown_percent", 30.0)  # 30%
        self.conservative_trigger = self.capital_config.get("conservative_trigger", 20.0)  # 20%
        self.emergency_trigger = self.capital_config.get("emergency_trigger", 25.0)       # 25%
        
        # Capital tracking
        self.initial_capital = self.capital_config.get("initial_capital", 5000.0)  # $5K default
        self.current_capital = self.initial_capital
        self.peak_capital = self.initial_capital
        self.current_drawdown = 0.0
        
        # Trading modes
        self.current_mode = "normal"  # normal, conservative, emergency, recovery
        self.recovery_boost_enabled = self.capital_config.get("recovery_boost_enabled", True)
        self.progressive_scaling = self.capital_config.get("progressive_scaling", True)
        
        # Capital zones (dollar amounts)
        self.safe_zone_capital = 0.0
        self.growth_zone_capital = 0.0 
        self.aggressive_zone_capital = 0.0
        
        # Performance tracking
        self.capital_history = []
        self.mode_changes = []
        self.last_update = datetime.now()
        
        print(f"💰 Capital Manager initialized")
        print(f"   Initial Capital: ${self.initial_capital:,.2f}")
        print(f"   Zone Allocation: Safe {self.safe_zone_percent}% | Growth {self.growth_zone_percent}% | Aggressive {self.aggressive_zone_percent}%")
        print(f"   Max Drawdown: {self.max_drawdown_percent}%")
        
        self._update_capital_zones()

    # ==========================================
    # 🎯 CORE CAPITAL MANAGEMENT
    # ==========================================
    
    def update_capital_status(self) -> Dict:
        """
        📊 อัพเดทสถานะทุนปัจจุบัน
        
        Returns:
            Dict: ข้อมูลสถานะทุนและโซน
        """
        try:
            # ดึงข้อมูลบัญชีจาก MT5
            account_info = self.mt5_connector.get_account_info()
            if not account_info:
                return self._get_offline_capital_status()
            
            # อัพเดท current capital
            self.current_capital = account_info.get('equity', self.initial_capital)
            
            # คำนวณ drawdown
            if self.current_capital > self.peak_capital:
                self.peak_capital = self.current_capital
            
            self.current_drawdown = ((self.peak_capital - self.current_capital) / self.peak_capital) * 100
            
            # อัพเดท capital zones
            self._update_capital_zones()
            
            # กำหนด trading mode
            self._determine_trading_mode()
            
            # บันทึกประวัติ
            self._record_capital_history()
            
            # สร้าง status report
            status = {
                'current_capital': self.current_capital,
                'initial_capital': self.initial_capital,
                'peak_capital': self.peak_capital,
                'current_drawdown': self.current_drawdown,
                'trading_mode': self.current_mode,
                'capital_zones': {
                    'safe_zone': self.safe_zone_capital,
                    'growth_zone': self.growth_zone_capital,
                    'aggressive_zone': self.aggressive_zone_capital
                },
                'protection_status': self._get_protection_status(),
                'recommendations': self._generate_recommendations()
            }
            
            self.last_update = datetime.now()
            return status
            
        except Exception as e:
            print(f"❌ Capital status update error: {e}")
            return self._get_offline_capital_status()

    def _update_capital_zones(self):
        """🎯 อัพเดท Capital Zones ตามทุนปัจจุบัน"""
        try:
            self.safe_zone_capital = self.current_capital * (self.safe_zone_percent / 100)
            self.growth_zone_capital = self.current_capital * (self.growth_zone_percent / 100)
            self.aggressive_zone_capital = self.current_capital * (self.aggressive_zone_percent / 100)
            
        except Exception as e:
            print(f"❌ Capital zones update error: {e}")

    def _determine_trading_mode(self):
        """🎨 กำหนด Trading Mode ตาม Drawdown"""
        try:
            old_mode = self.current_mode
            
            if self.current_drawdown >= self.emergency_trigger:
                self.current_mode = "emergency"
            elif self.current_drawdown >= self.conservative_trigger:
                self.current_mode = "conservative"
            elif self.current_drawdown < 5.0 and self.current_capital > self.peak_capital * 0.95:
                self.current_mode = "recovery" if old_mode in ["conservative", "emergency"] else "normal"
            else:
                self.current_mode = "normal"
            
            # บันทึกการเปลี่ยน mode
            if old_mode != self.current_mode:
                self.mode_changes.append({
                    'timestamp': datetime.now(),
                    'from_mode': old_mode,
                    'to_mode': self.current_mode,
                    'drawdown': self.current_drawdown,
                    'capital': self.current_capital
                })
                
                print(f"🎨 Trading mode changed: {old_mode} → {self.current_mode} (DD: {self.current_drawdown:.1f}%)")
            
        except Exception as e:
            print(f"❌ Trading mode determination error: {e}")

    # ==========================================
    # 🎯 LOT SIZE & RISK CALCULATION
    # ==========================================
    
    def calculate_position_size(self, zone: str, signal_strength: float, order_role: str = "PW") -> float:
        """
        📏 คำนวณ Position Size ตาม Zone + Role
        
        Args:
            zone: "safe", "growth", หรือ "aggressive"
            signal_strength: ความแรงสัญญาณ (0.0-1.0)
            order_role: บทบาทของออเดอร์ (HG/PW/RH/SC)
            
        Returns:
            float: ขนาด lot ที่แนะนำ
        """
        try:
            # Base lot ตาม zone
            if zone == "safe":
                base_lot = 0.01
                max_lot = 0.05
                zone_capital = self.safe_zone_capital
            elif zone == "growth": 
                base_lot = 0.02
                max_lot = 0.10
                zone_capital = self.growth_zone_capital
            elif zone == "aggressive":
                base_lot = 0.03
                max_lot = 0.20
                zone_capital = self.aggressive_zone_capital
            else:
                base_lot = 0.01
                max_lot = 0.05
                zone_capital = self.safe_zone_capital
            
            # Role multiplier
            role_multipliers = {
                "HG": 0.8,   # Hedge Guard - conservative
                "PW": 1.0,   # Profit Walker - normal
                "RH": 1.5,   # Recovery Hunter - aggressive  
                "SC": 1.2    # Scalp Capture - slightly higher
            }
            role_multiplier = role_multipliers.get(order_role, 1.0)
            
            # Signal strength multiplier
            signal_multiplier = 0.5 + (signal_strength * 1.5)  # 0.5 - 2.0 range
            
            # Trading mode multiplier
            mode_multipliers = {
                "normal": 1.0,
                "conservative": 0.6,
                "emergency": 0.3,
                "recovery": 1.4
            }
            mode_multiplier = mode_multipliers.get(self.current_mode, 1.0)
            
            # Capital efficiency multiplier
            capital_efficiency = min(2.0, self.current_capital / self.initial_capital)
            
            # คำนวณ final lot
            calculated_lot = base_lot * signal_multiplier * role_multiplier * mode_multiplier * capital_efficiency
            
            # จำกัดขอบเขต
            final_lot = max(0.01, min(max_lot, calculated_lot))
            
            print(f"📏 Lot calculation: {zone} zone, {order_role} role")
            print(f"   Base: {base_lot} → Signal: {signal_multiplier:.2f} → Role: {role_multiplier} → Mode: {mode_multiplier} → Final: {final_lot:.2f}")
            
            return round(final_lot, 2)
            
        except Exception as e:
            print(f"❌ Position size calculation error: {e}")
            return 0.01

    def get_risk_allocation_for_zone(self, zone: str) -> Dict:
        """
        🎯 ได้รับ Risk Allocation สำหรับ Zone
        
        Args:
            zone: "safe", "growth", หรือ "aggressive"
            
        Returns:
            Dict: ข้อมูล risk allocation
        """
        try:
            if zone == "safe":
                return {
                    'max_risk_per_trade': 0.5,      # 0.5% ต่อ trade
                    'max_total_risk': 5.0,          # 5% ของ zone
                    'max_positions': 15,            # สูงสุด 15 positions
                    'preferred_roles': ['HG', 'PW'] # บทบาทที่เหมาะสม
                }
            elif zone == "growth":
                return {
                    'max_risk_per_trade': 1.0,      # 1% ต่อ trade
                    'max_total_risk': 10.0,         # 10% ของ zone  
                    'max_positions': 25,            # สูงสุด 25 positions
                    'preferred_roles': ['PW', 'SC'] # บทบาทที่เหมาะสม
                }
            elif zone == "aggressive":
                return {
                    'max_risk_per_trade': 2.0,      # 2% ต่อ trade
                    'max_total_risk': 15.0,         # 15% ของ zone
                    'max_positions': 10,            # สูงสุด 10 positions  
                    'preferred_roles': ['RH', 'SC'] # บทบาทที่เหมาะสม
                }
            else:
                # Default safe allocation
                return {
                    'max_risk_per_trade': 0.5,
                    'max_total_risk': 5.0,
                    'max_positions': 15,
                    'preferred_roles': ['HG', 'PW']
                }
                
        except Exception as e:
            print(f"❌ Risk allocation error: {e}")
            return {'max_risk_per_trade': 0.5, 'max_total_risk': 5.0, 'max_positions': 15, 'preferred_roles': ['HG']}

    # ==========================================
    # 🛡️ PROTECTION & EMERGENCY MANAGEMENT
    # ==========================================
    
    def _get_protection_status(self) -> Dict:
        """🛡️ สถานะการป้องกัน"""
        try:
            return {
                'drawdown_level': 'normal' if self.current_drawdown < 10 else 
                                'warning' if self.current_drawdown < 20 else
                                'critical' if self.current_drawdown < 25 else 'emergency',
                'protection_active': self.current_mode in ['conservative', 'emergency'],
                'recovery_mode': self.current_mode == 'recovery',
                'capital_efficiency': self.current_capital / self.initial_capital,
                'days_since_peak': (datetime.now() - self.last_update).days if hasattr(self, 'last_update') else 0
            }
            
        except Exception as e:
            return {'drawdown_level': 'unknown', 'protection_active': False}

    def _generate_recommendations(self) -> List[str]:
        """💡 สร้างคำแนะนำตามสถานการณ์"""
        try:
            recommendations = []
            
            if self.current_mode == "emergency":
                recommendations.extend([
                    f"🚨 Emergency Mode: Drawdown {self.current_drawdown:.1f}%",
                    "⚠️ ลด position size และเพิ่มความระมัดระวัง",
                    "🛡️ พิจารณาปิด positions ที่มี risk สูง",
                    "💰 เน้น Safe Zone trading เท่านั้น"
                ])
                
            elif self.current_mode == "conservative":
                recommendations.extend([
                    f"⚠️ Conservative Mode: Drawdown {self.current_drawdown:.1f}%", 
                    "📉 ลด lot size ลง 40%",
                    "🎯 เน้น high-probability setups เท่านั้น",
                    "⚖️ หา hedge opportunities"
                ])
                
            elif self.current_mode == "recovery":
                recommendations.extend([
                    "🚀 Recovery Mode: Performance กำลังฟื้นตัว",
                    "📈 สามารถเพิ่ม position size ได้เล็กน้อย", 
                    "🎯 หาโอกาส Growth Zone entries",
                    "💡 พิจารณา RH (Recovery Hunter) positions"
                ])
                
            else:  # normal mode
                recommendations.extend([
                    "✅ Normal Mode: Portfolio สุขภาพดี",
                    f"💰 Capital: ${self.current_capital:,.2f} (DD: {self.current_drawdown:.1f}%)",
                    "🎯 สามารถเทรดตามปกติได้",
                    "📊 ทุก zones พร้อมใช้งาน"
                ])
            
            # เพิ่มคำแนะนำตาม capital efficiency
            efficiency = self.current_capital / self.initial_capital
            if efficiency > 1.2:
                recommendations.append("🌟 Capital เพิ่มขึ้น 20%+ พิจารณาขยาย position sizes")
            elif efficiency < 0.8:
                recommendations.append("📉 Capital ลดลง 20%+ ควรระมัดระวังมากขึ้น")
            
            return recommendations
            
        except Exception as e:
            return [f"❌ Recommendation generation error: {e}"]

    # ==========================================
    # 📊 REPORTING & ANALYTICS
    # ==========================================
    
    def get_capital_dashboard_data(self) -> Dict:
        """📊 ข้อมูลสำหรับ Capital Dashboard"""
        try:
            return {
                'capital_overview': {
                    'current': self.current_capital,
                    'initial': self.initial_capital,
                    'peak': self.peak_capital,
                    'change_percent': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100,
                    'drawdown_percent': self.current_drawdown
                },
                'zone_allocation': {
                    'safe': {'amount': self.safe_zone_capital, 'percent': self.safe_zone_percent},
                    'growth': {'amount': self.growth_zone_capital, 'percent': self.growth_zone_percent}, 
                    'aggressive': {'amount': self.aggressive_zone_capital, 'percent': self.aggressive_zone_percent}
                },
                'trading_mode': {
                    'current': self.current_mode,
                    'protection_level': self._get_protection_status()['drawdown_level'],
                    'mode_changes_today': len([m for m in self.mode_changes if m['timestamp'].date() == datetime.now().date()])
                },
                'performance_metrics': {
                    'total_return_percent': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100,
                    'max_drawdown_percent': max([h.get('drawdown', 0) for h in self.capital_history] + [0]),
                    'capital_efficiency': self.current_capital / self.initial_capital,
                    'days_active': (datetime.now() - self.capital_history[0]['timestamp']).days if self.capital_history else 0
                }
            }
            
        except Exception as e:
            print(f"❌ Dashboard data error: {e}")
            return {'error': str(e)}

    def _record_capital_history(self):
        """📝 บันทึกประวัติ capital"""
        try:
            if not hasattr(self, 'capital_history'):
                self.capital_history = []
            
            self.capital_history.append({
                'timestamp': datetime.now(),
                'capital': self.current_capital,
                'drawdown': self.current_drawdown,
                'mode': self.current_mode,
                'peak': self.peak_capital
            })
            
            # เก็บแค่ 1000 records ล่าสุด
            if len(self.capital_history) > 1000:
                self.capital_history = self.capital_history[-500:]
                
        except Exception as e:
            print(f"❌ Capital history recording error: {e}")

    def _get_offline_capital_status(self) -> Dict:
        """📱 สถานะ offline เมื่อไม่ได้เชื่อมต่อ MT5"""
        return {
            'current_capital': self.current_capital,
            'initial_capital': self.initial_capital,
            'peak_capital': self.peak_capital,
            'current_drawdown': self.current_drawdown,
            'trading_mode': 'offline',
            'capital_zones': {
                'safe_zone': self.safe_zone_capital,
                'growth_zone': self.growth_zone_capital,
                'aggressive_zone': self.aggressive_zone_capital
            },
            'protection_status': {'drawdown_level': 'offline', 'protection_active': True},
            'recommendations': ['📱 ระบบ offline - รอการเชื่อมต่อ MT5']
        }

# ==========================================
# 🔧 INTEGRATION HELPER FUNCTIONS
# ==========================================

def integrate_capital_manager_with_system(capital_manager, signal_generator, lot_calculator, position_monitor, risk_manager):
    """
    🔗 ผูก Capital Manager เข้ากับระบบอื่น
    
    Args:
        capital_manager: CapitalManager instance
        signal_generator: SignalGenerator instance  
        lot_calculator: LotCalculator instance
        position_monitor: PositionMonitor instance
        risk_manager: RiskManager instance
    """
    try:
        print("🔗 Integrating Capital Manager with system components...")
        
        # ผูกกับ Signal Generator
        if hasattr(signal_generator, 'set_capital_manager'):
            signal_generator.set_capital_manager(capital_manager)
            
        # ผูกกับ Lot Calculator  
        if hasattr(lot_calculator, 'set_capital_manager'):
            lot_calculator.set_capital_manager(capital_manager)
            
        # ผูกกับ Position Monitor
        if hasattr(position_monitor, 'set_capital_manager'):
            position_monitor.set_capital_manager(capital_manager)
            
        # ผูกกับ Risk Manager
        if hasattr(risk_manager, 'set_capital_manager'):
            risk_manager.set_capital_manager(capital_manager)
            
        print("✅ Capital Manager integration completed")
        
    except Exception as e:
        print(f"❌ Capital Manager integration error: {e}")

def create_capital_manager(mt5_connector, config: Dict) -> CapitalManager:
    """
    🏭 Factory function สำหรับสร้าง CapitalManager
    
    Args:
        mt5_connector: MT5 connector instance
        config: การตั้งค่าระบบ
        
    Returns:
        CapitalManager: configured instance
    """
    try:
        capital_manager = CapitalManager(mt5_connector, config)
        capital_manager.update_capital_status()  # Update ครั้งแรก
        
        print("🏭 Capital Manager created and initialized")
        return capital_manager
        
    except Exception as e:
        print(f"❌ Capital Manager creation error: {e}")
        return None