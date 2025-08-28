"""
📏 Capital & Role Aware Lot Calculator v4.0
lot_calculator.py

🚀 NEW v4.0 FEATURES:
✅ Capital Zone Integration
✅ Role-based Lot Sizing
✅ Drawdown-sensitive Scaling
✅ Recovery Boost Logic
✅ Trading Mode Adjustments
✅ Portfolio Balance Consideration
✅ Advanced Risk Scaling

🔧 ENHANCED FROM v3.0:
✅ Dynamic Lot Sizing based on Signal Strength
✅ Balance-based Scaling
✅ Multi-factor Lot Calculation
✅ Risk Management Integration

🎯 Lot Sizing Strategy v4.0:
- Capital zones กำหนด base lot และ max lot
- Role multipliers ปรับ lot ตามหน้าที่ออเดอร์
- Trading mode adjustments ปรับตามสถานการณ์
- Drawdown protection ลด lot เมื่อ drawdown สูง
- Recovery boost เพิ่ม lot เมื่อฟื้นตัว
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import statistics

class LotCalculator:
    """
    📏 Capital & Role Aware Lot Calculator v4.0
    
    คำนวณ lot size อัจฉริยะตามทุน + บทบาท + ความเสี่ยง
    ปรับตัวตามสถานการณ์ portfolio แบบ real-time
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """
        🔧 เริ่มต้น Lot Calculator v4.0
        
        Args:
            mt5_connector: MT5 connection object
            config: การตั้งค่าระบบ v4.0
        """
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Basic lot configuration (v3.0)
        self.lot_config = config.get("smart_entry_rules", {}).get("dynamic_lot_sizing", {})
        self.base_lot = self.lot_config.get("base_lot", 0.01)
        self.min_lot = self.lot_config.get("min_lot", 0.01)
        self.max_lot = self.lot_config.get("max_lot", 0.25)
        
        # 🆕 v4.0: Capital management integration
        self.capital_config = config.get("capital_management", {})
        self.zone_limits = self.capital_config.get("zone_risk_limits", {})
        self.mode_adjustments = self.capital_config.get("trading_mode_adjustments", {})
        self.capital_manager = None  # จะถูกตั้งค่าภายหลัง
        
        # 🆕 v4.0: Role-based multipliers
        self.role_config = config.get("order_roles", {})
        self.role_settings = self.role_config.get("role_settings", {})
        self.role_multipliers = {
            "HG": 0.8,   # Hedge Guard - conservative
            "PW": 1.0,   # Profit Walker - normal
            "RH": 1.5,   # Recovery Hunter - aggressive
            "SC": 1.2    # Scalp Capture - slightly higher
        }
        
        # Factor configurations (enhanced v4.0)
        self.signal_strength_factor = self.lot_config.get("signal_strength_factor", {})
        self.trend_strength_factor = self.lot_config.get("trend_strength_factor", {})
        self.balance_factor = self.lot_config.get("balance_factor", {})
        self.movement_factor = self.lot_config.get("movement_factor", {})
        
        # 🆕 v4.0: New factors
        self.capital_factor = self.lot_config.get("capital_factor", {})
        self.role_factor = self.lot_config.get("role_factor", {})
        
        # Performance tracking
        self.lot_history = []
        self.performance_stats = {
            'total_calculations': 0,
            'avg_lot_size': 0.0,
            'lot_size_distribution': {},
            'role_distribution': {},
            'zone_distribution': {}
        }
        
        print(f"📏 Capital & Role Aware Lot Calculator v4.0 initialized")
        print(f"   Base lot: {self.base_lot} | Min: {self.min_lot} | Max: {self.max_lot}")
        print(f"   Role multipliers: HG={self.role_multipliers['HG']} PW={self.role_multipliers['PW']} RH={self.role_multipliers['RH']} SC={self.role_multipliers['SC']}")
        print(f"   Capital zones: {len(self.zone_limits)} zones configured")

    # ==========================================
    # 🆕 v4.0: CAPITAL MANAGER INTEGRATION
    # ==========================================
    
    def set_capital_manager(self, capital_manager):
        """🔗 เชื่อมต่อ Capital Manager"""
        self.capital_manager = capital_manager
        print("🔗 Capital Manager integrated with Lot Calculator")

    def _get_capital_context(self) -> Dict:
        """💰 ดึงบริบททุนสำหรับการคำนวณ lot"""
        try:
            if self.capital_manager:
                return self.capital_manager.update_capital_status()
            else:
                # Fallback context
                return {
                    'current_capital': 5000.0,
                    'trading_mode': 'normal',
                    'current_drawdown': 0.0,
                    'capital_zones': {
                        'safe_zone': 2500.0,
                        'growth_zone': 1750.0,
                        'aggressive_zone': 750.0
                    }
                }
                
        except Exception as e:
            print(f"❌ Capital context error: {e}")
            return {
                'current_capital': 5000.0,
                'trading_mode': 'normal', 
                'current_drawdown': 0.0,
                'capital_zones': {'safe_zone': 2500.0, 'growth_zone': 1750.0, 'aggressive_zone': 750.0}
            }

    # ==========================================
    # 🎯 MAIN LOT CALCULATION (enhanced v4.0)
    # ==========================================
    
    def calculate_lot_size(self, signal_data: Dict, capital_zone: str = "safe", order_role: str = "PW") -> float:
        """
        📏 คำนวณ Lot Size แบบ Capital & Role Intelligence v4.0
        
        Args:
            signal_data: ข้อมูล signal
            capital_zone: โซนทุน ("safe", "growth", "aggressive")
            order_role: บทบาทออเดอร์ ("HG", "PW", "RH", "SC")
            
        Returns:
            float: ขนาด lot ที่คำนวณแล้ว
        """
        try:
            # ดึงบริบททุน
            capital_context = self._get_capital_context()
            
            # 🎯 Base lot ตาม capital zone
            base_lot = self._get_zone_base_lot(capital_zone)
            max_lot_for_zone = self._get_zone_max_lot(capital_zone)
            
            print(f"📏 Lot calculation: Zone={capital_zone} Role={order_role}")
            print(f"   Base lot: {base_lot} | Max for zone: {max_lot_for_zone}")
            
            # 🔢 คำนวณ multipliers ทั้งหมด
            multipliers = self._calculate_all_multipliers(signal_data, capital_context, capital_zone, order_role)
            
            # 🧮 คำนวณ lot ขั้นสุดท้าย
            calculated_lot = base_lot
            
            for factor_name, multiplier in multipliers.items():
                calculated_lot *= multiplier
                print(f"   {factor_name}: x{multiplier:.2f} → {calculated_lot:.3f}")
            
            # 🚧 ปรับขอบเขตและ validation
            final_lot = self._apply_lot_constraints(calculated_lot, max_lot_for_zone, capital_context, order_role)
            
            # 📊 บันทึกสถิติ
            self._record_lot_calculation(final_lot, capital_zone, order_role, multipliers)
            
            print(f"   📏 FINAL LOT: {final_lot:.3f}")
            return final_lot
            
        except Exception as e:
            print(f"❌ Lot calculation error: {e}")
            return self._get_fallback_lot_size(capital_zone, order_role)

    def _get_zone_base_lot(self, zone: str) -> float:
        """🎯 Base lot ตาม capital zone"""
        try:
            zone_settings = self.zone_limits.get(zone, {})
            return zone_settings.get("base_lot", 0.01)
        except Exception as e:
            return 0.01

    def _get_zone_max_lot(self, zone: str) -> float:
        """🎯 Max lot ตาม capital zone"""
        try:
            zone_settings = self.zone_limits.get(zone, {})
            return zone_settings.get("max_lot", 0.05)
        except Exception as e:
            return 0.05

    def _calculate_all_multipliers(self, signal_data: Dict, capital_context: Dict, zone: str, role: str) -> Dict:
        """🔢 คำนวณ multipliers ทั้งหมด v4.0"""
        try:
            multipliers = {}
            
            # 1. Signal Strength Multiplier (v3.0)
            if self.signal_strength_factor.get("enabled", True):
                multipliers['signal_strength'] = self._calculate_signal_strength_multiplier(signal_data)
            
            # 2. Trend Strength Multiplier (v3.0)
            if self.trend_strength_factor.get("enabled", True):
                multipliers['trend_strength'] = self._calculate_trend_strength_multiplier(signal_data)
            
            # 3. Portfolio Balance Multiplier (v3.0)
            if self.balance_factor.get("enabled", True):
                multipliers['portfolio_balance'] = self._calculate_balance_multiplier(signal_data)
            
            # 4. Movement Factor Multiplier (v3.0)
            if self.movement_factor.get("enabled", True):
                multipliers['price_movement'] = self._calculate_movement_multiplier(signal_data)
            
            # 🆕 5. Capital Factor Multiplier (v4.0)
            if self.capital_factor.get("enabled", True):
                multipliers['capital_efficiency'] = self._calculate_capital_multiplier(capital_context)
            
            # 🆕 6. Role Factor Multiplier (v4.0)
            if self.role_factor.get("enabled", True):
                multipliers['order_role'] = self._calculate_role_multiplier(role)
            
            # 🆕 7. Trading Mode Multiplier (v4.0)
            multipliers['trading_mode'] = self._calculate_trading_mode_multiplier(capital_context)
            
            # 🆕 8. Drawdown Protection Multiplier (v4.0)
            multipliers['drawdown_protection'] = self._calculate_drawdown_multiplier(capital_context)
            
            # 🆕 9. Recovery Boost Multiplier (v4.0)
            if capital_context.get('trading_mode') == 'recovery':
                multipliers['recovery_boost'] = self._calculate_recovery_boost_multiplier(capital_context, signal_data)
            
            return multipliers
            
        except Exception as e:
            print(f"❌ Multipliers calculation error: {e}")
            return {'fallback': 1.0}

    # ==========================================
    # 🔢 MULTIPLIER CALCULATION METHODS
    # ==========================================
    
    def _calculate_signal_strength_multiplier(self, signal_data: Dict) -> float:
        """💪 Signal Strength Multiplier (v3.0)"""
        try:
            strength = signal_data.get('strength', 0.5)
            
            min_multiplier = self.signal_strength_factor.get("min_multiplier", 0.6)
            max_multiplier = self.signal_strength_factor.get("max_multiplier", 3.5)
            sensitivity = self.signal_strength_factor.get("strength_sensitivity", 1.0)
            
            # แปลง strength (0.0-1.0) เป็น multiplier
            normalized_strength = max(0, min(1, strength)) ** sensitivity
            multiplier = min_multiplier + (normalized_strength * (max_multiplier - min_multiplier))
            
            return round(multiplier, 2)
            
        except Exception as e:
            return 1.0

    def _calculate_trend_strength_multiplier(self, signal_data: Dict) -> float:
        """📈 Trend Strength Multiplier (v3.0)"""
        try:
            trend_strength = signal_data.get('trend_strength', 0.5)
            threshold = self.trend_strength_factor.get("trend_threshold", 0.5)
            
            if trend_strength >= threshold:
                return self.trend_strength_factor.get("strong_trend_multiplier", 1.8)
            else:
                return self.trend_strength_factor.get("weak_trend_multiplier", 0.8)
                
        except Exception as e:
            return 1.0

    def _calculate_balance_multiplier(self, signal_data: Dict) -> float:
        """⚖️ Portfolio Balance Multiplier (v3.0)"""
        try:
            balance_factor = signal_data.get('portfolio_balance_factor', 1.0)
            
            if balance_factor > 1.2:  # เพิ่มจาก imbalance correction
                return self.balance_factor.get("imbalance_boost", 1.4)
            elif balance_factor < 0.8:  # ลดจาก oversupply
                return self.balance_factor.get("oversupply_reduction", 0.7)
            else:
                return 1.0
                
        except Exception as e:
            return 1.0

    def _calculate_movement_multiplier(self, signal_data: Dict) -> float:
        """🏃 Price Movement Multiplier (v3.0)"""
        try:
            # สามารถดึงจาก signal_data หรือคำนวณจาก current price action
            movement_points = signal_data.get('price_movement_points', 0.5)
            
            min_movement = self.movement_factor.get("min_movement_points", 0.15)
            max_movement = self.movement_factor.get("max_movement_points", 2.50)
            max_multiplier = self.movement_factor.get("movement_multiplier_max", 1.6)
            
            if movement_points <= min_movement:
                return 0.8
            elif movement_points >= max_movement:
                return max_multiplier
            else:
                # Linear interpolation
                ratio = (movement_points - min_movement) / (max_movement - min_movement)
                return 0.8 + (ratio * (max_multiplier - 0.8))
                
        except Exception as e:
            return 1.0

    # ==========================================
    # 🆕 v4.0: NEW MULTIPLIER METHODS
    # ==========================================
    
    def _calculate_capital_multiplier(self, capital_context: Dict) -> float:
        """💰 Capital Efficiency Multiplier (NEW v4.0)"""
        try:
            current_capital = capital_context.get('current_capital', 5000)
            initial_capital = capital_context.get('initial_capital', 5000)
            
            efficiency = current_capital / initial_capital
            
            if efficiency >= 1.5:        # เพิ่มทุน 50%+
                return 1.4
            elif efficiency >= 1.2:      # เพิ่มทุน 20-50%
                return 1.2
            elif efficiency >= 1.0:      # เพิ่มทุนเล็กน้อย
                return 1.0
            elif efficiency >= 0.8:      # ลดทุน 20% ขึ้นไป
                return 0.8
            else:                         # ลดทุนมาก 20%+
                return 0.6
                
        except Exception as e:
            return 1.0

    def _calculate_role_multiplier(self, role: str) -> float:
        """🎭 Order Role Multiplier (NEW v4.0)"""
        try:
            role_multiplier = self.role_multipliers.get(role, 1.0)
            
            # อาจปรับเพิ่มจาก role settings
            role_settings = self.role_settings.get(role, {})
            if role_settings.get("aggressive_sizing", False):  # สำหรับ RH
                role_multiplier *= 1.2
            elif role_settings.get("quick_profit", False):     # สำหรับ SC
                role_multiplier *= 1.1
            
            return role_multiplier
            
        except Exception as e:
            return 1.0

    def _calculate_trading_mode_multiplier(self, capital_context: Dict) -> float:
        """🎨 Trading Mode Multiplier (NEW v4.0)"""
        try:
            trading_mode = capital_context.get('trading_mode', 'normal')
            mode_adjustment = self.mode_adjustments.get(trading_mode, {})
            
            return mode_adjustment.get("lot_multiplier", 1.0)
            
        except Exception as e:
            return 1.0

    def _calculate_drawdown_multiplier(self, capital_context: Dict) -> float:
        """🛡️ Drawdown Protection Multiplier (NEW v4.0)"""
        try:
            drawdown = capital_context.get('current_drawdown', 0.0)
            
            if drawdown >= 25.0:         # Drawdown สูงมาก
                return 0.4
            elif drawdown >= 20.0:       # Drawdown สูง
                return 0.6
            elif drawdown >= 15.0:       # Drawdown ปานกลาง
                return 0.8
            elif drawdown >= 10.0:       # Drawdown เล็กน้อย
                return 0.9
            else:                        # Drawdown ต่ำ
                return 1.0
                
        except Exception as e:
            return 1.0

    def _calculate_recovery_boost_multiplier(self, capital_context: Dict, signal_data: Dict) -> float:
        """🚀 Recovery Boost Multiplier (NEW v4.0)"""
        try:
            if not self.capital_config.get("recovery_boost_enabled", True):
                return 1.0
            
            signal_strength = signal_data.get('strength', 0.5)
            drawdown = capital_context.get('current_drawdown', 0.0)
            
            # Recovery boost logic
            if signal_strength >= 0.8 and drawdown >= 15.0:
                return 1.6  # Strong signal + high drawdown = aggressive recovery
            elif signal_strength >= 0.7 and drawdown >= 10.0:
                return 1.4  # Good signal + medium drawdown = moderate recovery
            elif signal_strength >= 0.6:
                return 1.2  # Decent signal = slight recovery boost
            else:
                return 1.0  # No boost for weak signals
                
        except Exception as e:
            return 1.0

    # ==========================================
    # 🚧 LOT CONSTRAINTS & VALIDATION
    # ==========================================
    
    def _apply_lot_constraints(self, calculated_lot: float, max_lot_for_zone: float, capital_context: Dict, role: str) -> float:
        """🚧 ปรับขอบเขตและตรวจสอบ lot size"""
        try:
            # ขอบเขตพื้นฐาน
            constrained_lot = max(self.min_lot, min(calculated_lot, max_lot_for_zone, self.max_lot))
            
            # ตรวจสอบ emergency mode
            trading_mode = capital_context.get('trading_mode', 'normal')
            if trading_mode == 'emergency':
                emergency_max = max_lot_for_zone * 0.5  # ลดลงครึ่งหนึ่งใน emergency
                constrained_lot = min(constrained_lot, emergency_max)
            
            # ตรวจสอบ capital availability
            current_capital = capital_context.get('current_capital', 5000)
            if current_capital < 1000:  # ทุนน้อยมาก
                constrained_lot = min(constrained_lot, 0.01)
            
            # รอบ lot size ให้เป็น 0.01 เท่านั้น
            final_lot = round(constrained_lot, 2)
            
            # Final validation
            if final_lot < self.min_lot:
                final_lot = self.min_lot
            elif final_lot > self.max_lot:
                final_lot = self.max_lot
            
            return final_lot
            
        except Exception as e:
            print(f"❌ Lot constraints error: {e}")
            return self.min_lot

    def _get_fallback_lot_size(self, zone: str, role: str) -> float:
        """🆘 Fallback lot size เมื่อเกิดข้อผิดพลาด"""
        try:
            # เลือก lot ตาม zone
            if zone == "aggressive":
                base = 0.02
            elif zone == "growth":
                base = 0.01
            else:  # safe
                base = 0.01
            
            # ปรับตาม role
            if role == "RH":     # Recovery Hunter
                return min(base * 1.5, 0.03)
            elif role == "SC":   # Scalp Capture
                return min(base * 1.2, 0.02)
            elif role == "HG":   # Hedge Guard
                return min(base * 0.8, 0.01)
            else:                # Profit Walker
                return base
                
        except Exception as e:
            return self.min_lot

    # ==========================================
    # 📊 PERFORMANCE TRACKING & ANALYTICS
    # ==========================================
    
    def _record_lot_calculation(self, lot_size: float, zone: str, role: str, multipliers: Dict):
        """📊 บันทึกการคำนวณ lot"""
        try:
            record = {
                'timestamp': datetime.now(),
                'lot_size': lot_size,
                'capital_zone': zone,
                'order_role': role,
                'multipliers': multipliers.copy()
            }
            
            self.lot_history.append(record)
            
            # เก็บแค่ 500 records ล่าสุด
            if len(self.lot_history) > 500:
                self.lot_history = self.lot_history[-250:]
            
            # อัพเดทสถิติ
            self._update_performance_stats(lot_size, zone, role)
            
        except Exception as e:
            print(f"❌ Lot recording error: {e}")

    def _update_performance_stats(self, lot_size: float, zone: str, role: str):
        """📈 อัพเดทสถิติผลงาน"""
        try:
            self.performance_stats['total_calculations'] += 1
            
            # อัพเดท average lot size
            current_avg = self.performance_stats['avg_lot_size']
            total_calc = self.performance_stats['total_calculations']
            new_avg = ((current_avg * (total_calc - 1)) + lot_size) / total_calc
            self.performance_stats['avg_lot_size'] = round(new_avg, 3)
            
            # อัพเดท lot size distribution
            lot_range = self._get_lot_range_category(lot_size)
            if lot_range not in self.performance_stats['lot_size_distribution']:
                self.performance_stats['lot_size_distribution'][lot_range] = 0
            self.performance_stats['lot_size_distribution'][lot_range] += 1
            
            # อัพเดท role distribution
            if role not in self.performance_stats['role_distribution']:
                self.performance_stats['role_distribution'][role] = 0
            self.performance_stats['role_distribution'][role] += 1
            
            # อัพเดท zone distribution
            if zone not in self.performance_stats['zone_distribution']:
                self.performance_stats['zone_distribution'][zone] = 0
            self.performance_stats['zone_distribution'][zone] += 1
            
        except Exception as e:
            print(f"❌ Performance stats update error: {e}")

    def _get_lot_range_category(self, lot_size: float) -> str:
        """📊 หมวดหมู่ lot size"""
        if lot_size <= 0.01:
            return "micro"
        elif lot_size <= 0.03:
            return "small"
        elif lot_size <= 0.10:
            return "medium"
        elif lot_size <= 0.20:
            return "large"
        else:
            return "huge"

    # ==========================================
    # 📈 REPORTING & ANALYTICS
    # ==========================================
    
    def get_lot_calculation_report(self) -> Dict:
        """📊 รายงานการคำนวณ lot"""
        try:
            if not self.lot_history:
                return {'message': 'No lot calculations recorded yet'}
            
            # สถิติพื้นฐาน
            recent_lots = [record['lot_size'] for record in self.lot_history[-50:]]  # 50 ล่าสุด
            
            report = {
                'summary': {
                    'total_calculations': self.performance_stats['total_calculations'],
                    'avg_lot_size': self.performance_stats['avg_lot_size'],
                    'min_lot_calculated': min(recent_lots),
                    'max_lot_calculated': max(recent_lots),
                    'median_lot_size': statistics.median(recent_lots) if recent_lots else 0
                },
                'distributions': {
                    'lot_size_ranges': self.performance_stats['lot_size_distribution'].copy(),
                    'capital_zones': self.performance_stats['zone_distribution'].copy(),
                    'order_roles': self.performance_stats['role_distribution'].copy()
                },
                'recent_activity': self._get_recent_activity_summary(),
                'multiplier_analysis': self._analyze_multiplier_effectiveness(),
                'recommendations': self._generate_lot_recommendations()
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Lot calculation report error: {e}")
            return {'error': str(e)}

    def _get_recent_activity_summary(self) -> Dict:
        """📊 สรุปกิจกรรมล่าสุด"""
        try:
            recent_records = self.lot_history[-20:] if len(self.lot_history) >= 20 else self.lot_history
            
            if not recent_records:
                return {'message': 'No recent activity'}
            
            # วิเคราะห์ล่าสุด
            recent_zones = [r['capital_zone'] for r in recent_records]
            recent_roles = [r['order_role'] for r in recent_records]
            recent_lots = [r['lot_size'] for r in recent_records]
            
            return {
                'records_analyzed': len(recent_records),
                'most_used_zone': max(set(recent_zones), key=recent_zones.count),
                'most_used_role': max(set(recent_roles), key=recent_roles.count),
                'avg_recent_lot': round(sum(recent_lots) / len(recent_lots), 3),
                'lot_trend': self._determine_lot_trend(recent_lots)
            }
            
        except Exception as e:
            return {'error': str(e)}

    def _analyze_multiplier_effectiveness(self) -> Dict:
        """🔍 วิเคราะห์ประสิทธิภาพ multipliers"""
        try:
            if len(self.lot_history) < 10:
                return {'message': 'Insufficient data for analysis'}
            
            # วิเคราะห์ multipliers ที่ใช้บ่อย
            all_multipliers = {}
            
            for record in self.lot_history[-50:]:  # 50 ล่าสุด
                multipliers = record.get('multipliers', {})
                for factor, value in multipliers.items():
                    if factor not in all_multipliers:
                        all_multipliers[factor] = []
                    all_multipliers[factor].append(value)
            
            # คำนวณสถิติสำหรับแต่ละ multiplier
            multiplier_stats = {}
            for factor, values in all_multipliers.items():
                multiplier_stats[factor] = {
                    'avg': round(statistics.mean(values), 2),
                    'min': round(min(values), 2),
                    'max': round(max(values), 2),
                    'usage_frequency': len(values)
                }
            
            return {
                'multiplier_statistics': multiplier_stats,
                'most_impactful_factor': max(multiplier_stats.keys(), 
                                           key=lambda x: abs(multiplier_stats[x]['avg'] - 1.0)),
                'most_stable_factor': min(multiplier_stats.keys(),
                                        key=lambda x: multiplier_stats[x]['max'] - multiplier_stats[x]['min'])
            }
            
        except Exception as e:
            return {'error': str(e)}

    def _generate_lot_recommendations(self) -> List[str]:
        """💡 สร้างคำแนะนำการปรับปรุง lot calculation"""
        try:
            recommendations = []
            
            # วิเคราะห์ recent performance
            if self.performance_stats['total_calculations'] > 20:
                avg_lot = self.performance_stats['avg_lot_size']
                
                if avg_lot < 0.015:
                    recommendations.append("📉 Average lot size ต่ำมาก - พิจารณาเพิ่ม base lot")
                elif avg_lot > 0.08:
                    recommendations.append("📈 Average lot size สูงมาก - ตรวจสอบ risk management")
            
            # วิเคราะห์ zone distribution
            zone_dist = self.performance_stats['zone_distribution']
            if zone_dist:
                safe_ratio = zone_dist.get('safe', 0) / sum(zone_dist.values())
                if safe_ratio > 0.8:
                    recommendations.append("🛡️ ใช้ Safe zone มากเกินไป - พิจารณาใช้ Growth zone มากขึ้น")
                elif safe_ratio < 0.3:
                    recommendations.append("⚠️ ใช้ Safe zone น้อยเกินไป - เพิ่มความระมัดระวัง")
            
            # วิเคราะห์ role distribution
            role_dist = self.performance_stats['role_distribution']
            if role_dist:
                rh_ratio = role_dist.get('RH', 0) / sum(role_dist.values())
                if rh_ratio > 0.4:
                    recommendations.append("🏹 ใช้ Recovery Hunter มากเกินไป - อาจมีปัญหา portfolio")
            
            if not recommendations:
                recommendations.append("✅ Lot calculation working well - keep monitoring")
            
            return recommendations
            
        except Exception as e:
            return [f"❌ Recommendation generation error: {e}"]

    def _determine_lot_trend(self, lot_sizes: List[float]) -> str:
        """📊 กำหนด trend ของ lot sizes"""
        try:
            if len(lot_sizes) < 5:
                return "insufficient_data"
            
            recent_5 = lot_sizes[-5:]
            first_half = statistics.mean(recent_5[:2])
            second_half = statistics.mean(recent_5[-2:])
            
            difference = second_half - first_half
            
            if difference > 0.005:
                return "increasing"
            elif difference < -0.005:
                return "decreasing"
            else:
                return "stable"
                
        except Exception as e:
            return "unknown"

    # ==========================================
    # 🔧 UTILITY & HELPER METHODS
    # ==========================================
    
    def reset_performance_stats(self):
        """🔄 รีเซ็ตสถิติผลงาน"""
        try:
            self.performance_stats = {
                'total_calculations': 0,
                'avg_lot_size': 0.0,
                'lot_size_distribution': {},
                'role_distribution': {},
                'zone_distribution': {}
            }
            print("🔄 Lot calculator performance stats reset")
            
        except Exception as e:
            print(f"❌ Stats reset error: {e}")

    def get_calculator_info(self) -> Dict:
        """ℹ️ ข้อมูล Lot Calculator"""
        return {
            'name': 'Capital & Role Aware Lot Calculator',
            'version': '4.0.0',
            'base_lot': self.base_lot,
            'min_lot': self.min_lot,
            'max_lot': self.max_lot,
            'capital_manager_connected': self.capital_manager is not None,
            'total_calculations': self.performance_stats['total_calculations'],
            'avg_lot_size': self.performance_stats['avg_lot_size'],
            'supported_zones': list(self.zone_limits.keys()),
            'supported_roles': list(self.role_multipliers.keys())
        }

# ==========================================
# 🔧 INTEGRATION HELPER FUNCTIONS
# ==========================================

def create_lot_calculator(mt5_connector, config: Dict) -> LotCalculator:
    """
    🏭 Factory function สำหรับสร้าง LotCalculator
    
    Args:
        mt5_connector: MT5 connector instance
        config: การตั้งค่าระบบ
        
    Returns:
        LotCalculator: configured instance
    """
    try:
        calculator = LotCalculator(mt5_connector, config)
        print("🏭 Capital & Role Aware Lot Calculator created successfully")
        return calculator
        
    except Exception as e:
        print(f"❌ Lot Calculator creation error: {e}")
        return None

def integrate_lot_calculator_with_system(calculator, capital_manager, signal_generator, order_executor):
    """
    🔗 ผูก Lot Calculator เข้ากับระบบอื่น
    
    Args:
        calculator: LotCalculator instance
        capital_manager: CapitalManager instance
        signal_generator: SignalGenerator instance
        order_executor: OrderExecutor instance
    """
    try:
        print("🔗 Integrating Lot Calculator with system components...")
        
        # ผูกกับ Capital Manager
        if capital_manager:
            calculator.set_capital_manager(capital_manager)
        
        # ผูกกับ Signal Generator
        if hasattr(signal_generator, 'set_lot_calculator'):
            signal_generator.set_lot_calculator(calculator)
        
        # ผูกกับ Order Executor
        if hasattr(order_executor, 'set_lot_calculator'):
            order_executor.set_lot_calculator(calculator)
        
        print("✅ Lot Calculator integration completed")
        
    except Exception as e:
        print(f"❌ Lot Calculator integration error: {e}")