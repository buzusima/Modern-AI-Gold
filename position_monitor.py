"""
💰 Enhanced Position Monitor v4.0 - Capital & Role Intelligence
position_monitor.py (CAPITAL & ROLE ENHANCED)

🚀 NEW v4.0 FEATURES:
✅ Role-based Closing Logic (HG/PW/RH/SC)
✅ Capital-sensitive Thresholds
✅ Integration with Capital Manager & Role Manager
✅ Advanced Multi-level Profit Taking
✅ Smart Recovery Combinations
✅ Capital Zone Awareness

🔧 ENHANCED FROM v3.0:
✅ Lot-Aware Analysis (profit per lot, volume efficiency)
✅ Margin Impact Optimization 
✅ Volume-Weighted Portfolio Balance
✅ Partial Position Closing
✅ Dynamic Efficiency Thresholds

🎯 Position Management Strategy v4.0:
- แต่ละ role มี logic การปิดที่ต่างกัน
- Profit targets ปรับตาม capital zone + role
- Recovery combinations แบบ intelligent
- Capital preservation เป็นความสำคัญสูงสุด
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import statistics
import time

class PositionMonitor:
    """
    💰 Enhanced Position Monitor v4.0 - Capital & Role Intelligence
    
    🎯 เน้น Capital Preservation + Role-based Management
    ติดตามออเดอร์และจัดการแบบอัจฉริยะตามทุน + บทบาท
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """
        🔧 เริ่มต้น Enhanced Position Monitor v4.0
        """
        self.mt5_connector = mt5_connector
        self.config = config
        
        # การตั้งค่า position management (v3.0)
        self.position_config = config.get("position_management", {})
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD.v")
        
        # LOT-AWARE SETTINGS (v3.0)
        self.min_efficiency_threshold = self.position_config.get("min_efficiency_per_lot", 40.0)  # ลดจาก 50
        self.volume_balance_tolerance = self.position_config.get("volume_balance_tolerance", 0.35)  # เพิ่มจาก 0.3
        self.partial_close_enabled = self.position_config.get("partial_close_enabled", True)
        self.min_partial_volume = self.position_config.get("min_partial_volume", 0.01)
        
        # 🆕 v4.0: Capital & Role integration
        self.capital_config = config.get("capital_management", {})
        self.role_config = config.get("order_roles", {})
        self.capital_manager = None  # จะถูกตั้งค่าภายหลัง
        self.role_manager = None     # จะถูกตั้งค่าภายหลัง
        
        # 🆕 v4.0: Role-based closing settings
        self.role_close_settings = self.position_config.get("smart_close_settings", {}).get("role_based_closing", {})
        self.profit_taking_config = self.position_config.get("profit_taking", {})
        self.recovery_config = self.position_config.get("recovery_combinations", {})
        
        # Smart close settings (relaxed v4.0)
        smart_close = self.position_config.get("smart_close_settings", {})
        self.max_losing_age_hours = smart_close.get("max_losing_age_hours", 12)  # เพิ่มจาก 8
        self.min_net_profit_to_close = smart_close.get("min_net_profit_to_close", 1.5)  # ลดจาก 2.0
        self.portfolio_balance_threshold = smart_close.get("portfolio_balance_threshold", 0.70)  # เพิ่มจาก 0.65
        
        # MARGIN OPTIMIZATION SETTINGS (v3.0)
        self.margin_efficiency_weight = 0.4
        self.profit_efficiency_weight = 0.6
        self.high_margin_usage_threshold = 70.0
        
        # Emergency settings (v3.0)
        self.max_total_loss = -200.0
        self.emergency_close_enabled = True
        
        # 🆕 v4.0: Capital-sensitive thresholds
        self.capital_thresholds = {
            'safe_zone_min_profit': 1.0,      # Safe zone ปิดเมื่อกำไร $1+
            'growth_zone_min_profit': 2.0,    # Growth zone ปิดเมื่อกำไร $2+
            'aggressive_zone_min_profit': 3.0 # Aggressive zone ปิดเมื่อกำไร $3+
        }
        
        # Performance tracking (enhanced v4.0)
        self.position_cache = {}
        self.last_update_time = datetime.min
        self.update_interval = 5  # วินาที
        
        # 🆕 v4.0: Role performance tracking
        self.role_close_stats = {
            'HG': {'closed': 0, 'avg_profit': 0.0, 'avg_hold_time': 0.0},
            'PW': {'closed': 0, 'avg_profit': 0.0, 'avg_hold_time': 0.0},
            'RH': {'closed': 0, 'avg_profit': 0.0, 'avg_hold_time': 0.0},
            'SC': {'closed': 0, 'avg_profit': 0.0, 'avg_hold_time': 0.0}
        }
        
        # Lot statistics (v3.0)
        self.lot_stats = {
            'total_buy_volume': 0.0,
            'total_sell_volume': 0.0,
            'avg_profit_per_lot_buy': 0.0,
            'avg_profit_per_lot_sell': 0.0,
            'volume_imbalance_ratio': 0.0,
            'margin_efficiency_score': 0.0
        }
        
        print(f"💰 Enhanced Position Monitor v4.0 initialized")
        print(f"   Capital & Role Intelligence: Enabled")
        print(f"   Min efficiency: ${self.min_efficiency_threshold}/lot")
        print(f"   Balance tolerance: {self.volume_balance_tolerance:.1%}")
        print(f"   Role-based closing: {self.role_close_settings.get('enabled', True)}")

    # ==========================================
    # 🆕 v4.0: CAPITAL & ROLE INTEGRATION
    # ==========================================
    
    def set_capital_manager(self, capital_manager):
        """🔗 เชื่อมต่อ Capital Manager"""
        self.capital_manager = capital_manager
        print("🔗 Capital Manager integrated with Position Monitor")

    def set_role_manager(self, role_manager):
        """🔗 เชื่อมต่อ Role Manager"""
        self.role_manager = role_manager
        print("🔗 Role Manager integrated with Position Monitor")

    def _get_capital_context(self) -> Dict:
        """💰 ดึงบริบททุนสำหรับ position management"""
        try:
            if self.capital_manager:
                return self.capital_manager.update_capital_status()
            else:
                return {
                    'trading_mode': 'normal',
                    'current_drawdown': 0.0,
                    'capital_zones': {'safe_zone': 2500, 'growth_zone': 1750, 'aggressive_zone': 750}
                }
        except Exception as e:
            return {'trading_mode': 'normal', 'current_drawdown': 0.0}

    def _get_position_role(self, position_id: str) -> str:
        """🎭 ดึง role ของ position"""
        try:
            if self.role_manager and hasattr(self.role_manager, 'position_roles'):
                return self.role_manager.position_roles.get(position_id, {}).get('role', 'PW')
            else:
                return 'PW'  # Default role
        except Exception as e:
            return 'PW'

    # ==========================================
    # 🎯 MAIN MONITORING METHODS (enhanced v4.0)
    # ==========================================
    
    def check_smart_close_opportunities(self) -> List[Dict]:
        """
        🧠 ตรวจสอบโอกาสปิดออเดอร์อัจฉริยะ v4.0
        
        🆕 v4.0 enhancements:
        - Role-based closing logic
        - Capital-sensitive thresholds
        - Advanced profit taking
        - Smart recovery combinations
        
        Returns:
            List[Dict]: รายการ action recommendations
        """
        try:
            positions = self.get_all_positions()
            if not positions:
                return []
            
            print(f"🧠 Enhanced Smart Close Analysis v4.0: {len(positions)} positions")
            
            # 🆕 v4.0: ดึงบริบททุนและ role
            capital_context = self._get_capital_context()
            
            close_opportunities = []
            
            # 🆕 1. Role-based Close Analysis (สำคัญสูงสุด v4.0)
            if self.role_close_settings.get("enabled", True):
                role_actions = self._find_role_based_close_opportunities(positions, capital_context)
                close_opportunities.extend(role_actions)
            
            # 2. Advanced Multi-level Profit Taking (v4.0)
            profit_actions = self._find_multi_level_profit_opportunities(positions, capital_context)
            close_opportunities.extend(profit_actions)
            
            # 3. Capital-sensitive Recovery Opportunities (v4.0)
            recovery_actions = self._find_capital_aware_recovery_opportunities(positions, capital_context)
            close_opportunities.extend(recovery_actions)
            
            # 4. Enhanced Margin Optimization (v3.0)
            margin_actions = self._find_margin_optimization_opportunities(positions)
            close_opportunities.extend(margin_actions)
            
            # 5. Volume Balance Opportunities (v3.0)
            balance_actions = self._find_volume_balance_opportunities(positions)
            close_opportunities.extend(balance_actions)
            
            # เรียงตาม priority (ต่ำ = สำคัญกว่า)
            close_opportunities.sort(key=lambda x: x.get('priority', 10))
            
            # จำกัดจำนวน recommendations
            close_opportunities = close_opportunities[:10]
            
            if close_opportunities:
                print(f"🧠 Found {len(close_opportunities)} enhanced close opportunities")
                for i, action in enumerate(close_opportunities[:3]):
                    print(f"   {i+1}. {action.get('action_type', 'unknown')} (Priority: {action.get('priority', 'N/A')})")
                    print(f"      {action.get('reason', 'No reason')}")
            
            return close_opportunities
            
        except Exception as e:
            print(f"❌ Smart close opportunities error: {e}")
            return []

    # ==========================================
    # 🆕 v4.0: ROLE-BASED CLOSE ANALYSIS
    # ==========================================
    
    def _find_role_based_close_opportunities(self, positions: List[Dict], capital_context: Dict) -> List[Dict]:
        """🎭 หาโอกาสปิดตาม Role Logic (NEW v4.0)"""
        try:
            role_actions = []
            
            if not self.role_manager:
                return role_actions
            
            # ดึง role recommendations สำหรับแต่ละ position
            for pos in positions:
                position_id = pos.get('id', '')
                position_role = self._get_position_role(position_id)
                
                # ขอ action recommendation จาก role manager
                if hasattr(self.role_manager, 'get_role_based_action_for_position'):
                    role_action = self.role_manager.get_role_based_action_for_position(position_id, pos)
                    
                    if role_action.get('action') == 'close':
                        # แปลงเป็น format ของ position monitor
                        close_action = {
                            'action_type': 'role_based_close',
                            'position_id': position_id,
                            'order_role': position_role,
                            'priority': role_action.get('priority', 3),
                            'reason': f"Role {position_role}: {role_action.get('reason', '')}",
                            'profit': pos.get('total_pnl', 0),
                            'volume': pos.get('volume', 0),
                            'age_hours': pos.get('age_hours', 0)
                        }
                        role_actions.append(close_action)
            
            # เรียงตาม role priority (HG, SC, RH, PW)
            role_priority_order = {'HG': 1, 'SC': 2, 'RH': 3, 'PW': 4}
            role_actions.sort(key=lambda x: (
                x.get('priority', 5),
                role_priority_order.get(x.get('order_role', 'PW'), 5)
            ))
            
            print(f"🎭 Role-based close analysis: {len(role_actions)} actions")
            return role_actions
            
        except Exception as e:
            print(f"❌ Role-based close analysis error: {e}")
            return []

    # ==========================================
    # 🆕 v4.0: MULTI-LEVEL PROFIT TAKING
    # ==========================================
    
    def _find_multi_level_profit_opportunities(self, positions: List[Dict], capital_context: Dict) -> List[Dict]:
        """💰 Multi-level Profit Taking System (NEW v4.0)"""
        try:
            profit_actions = []
            
            if not self.profit_taking_config.get("multi_level_enabled", True):
                return profit_actions
            
            # Profit level definitions
            micro_profits = self.profit_taking_config.get("micro_profits", {"min": 0.5, "max": 2.0})
            standard_profits = self.profit_taking_config.get("standard_profits", {"min": 2.0, "max": 8.0})
            momentum_profits = self.profit_taking_config.get("momentum_profits", {"min": 8.0, "max": 50.0})
            
            trading_mode = capital_context.get('trading_mode', 'normal')
            current_drawdown = capital_context.get('current_drawdown', 0.0)
            
            for pos in positions:
                profit = pos.get('total_pnl', 0)
                volume = pos.get('volume', 0)
                age_hours = pos.get('age_hours', 0)
                position_id = pos.get('id', '')
                role = self._get_position_role(position_id)
                
                # กำหนด profit target ตาม role + capital context
                profit_target = self._calculate_dynamic_profit_target(role, volume, capital_context)
                
                close_profit = False
                priority = 5
                reason = ""
                profit_level = ""
                
                # 💰 Momentum Profits (high priority)
                if profit >= momentum_profits["min"]:
                    close_profit = True
                    priority = 1
                    profit_level = "momentum"
                    reason = f"Momentum profit: ${profit:.2f} ({role})"
                
                # 💰 Standard Profits 
                elif profit >= standard_profits["min"]:
                    # ปรับ threshold ตาม trading mode
                    if trading_mode in ['emergency', 'conservative']:
                        close_profit = True  # รีบเก็บในสถานการณ์ยาก
                        priority = 2
                    elif profit >= profit_target:
                        close_profit = True
                        priority = 2
                    
                    profit_level = "standard"
                    reason = f"Standard profit: ${profit:.2f} (Target: ${profit_target:.2f}, {role})"
                
                # 💰 Micro Profits (conditional)
                elif profit >= micro_profits["min"]:
                    # Micro profits ขึ้นอยู่กับ role + สถานการณ์
                    if role == 'SC':  # Scalp Capture รับ micro profits
                        close_profit = True
                        priority = 2
                    elif trading_mode in ['emergency', 'conservative'] and profit >= profit_target * 0.8:
                        close_profit = True  # ยอมรับ micro profits ในสถานการณ์ยาก
                        priority = 3
                    elif age_hours >= 24 and profit >= 0.8:  # เก่าแล้ว + มีกำไรเล็กน้อย
                        close_profit = True
                        priority = 4
                    
                    profit_level = "micro"
                    reason = f"Micro profit: ${profit:.2f} ({role}, {trading_mode} mode)"
                
                if close_profit:
                    profit_actions.append({
                        'action_type': 'multi_level_profit',
                        'position_id': position_id,
                        'profit_level': profit_level,
                        'order_role': role,
                        'priority': priority,
                        'reason': reason,
                        'profit': profit,
                        'volume': volume,
                        'target_achieved': profit >= profit_target
                    })
            
            print(f"💰 Multi-level profit analysis: {len(profit_actions)} opportunities")
            return profit_actions
            
        except Exception as e:
            print(f"❌ Multi-level profit analysis error: {e}")
            return []

    def _calculate_dynamic_profit_target(self, role: str, volume: float, capital_context: Dict) -> float:
        """🎯 คำนวณ Profit Target แบบ Dynamic"""
        try:
            # Base targets ตาม role
            base_targets = {
                'HG': 4.0,   # Hedge Guard - target สูงกว่า
                'PW': 2.5,   # Profit Walker - target ปกติ  
                'RH': 1.0,   # Recovery Hunter - target ต่ำ เร่งฟื้นตัว
                'SC': 0.5    # Scalp Capture - target ต่ำสุด
            }
            
            base_target = base_targets.get(role, 2.0)
            
            # ปรับตาม volume
            volume_multiplier = min(1.5, 0.8 + (volume * 2))  # volume มาก = target สูงขึ้น
            
            # ปรับตาม trading mode
            trading_mode = capital_context.get('trading_mode', 'normal')
            mode_adjustments = {
                'normal': 1.0,
                'conservative': 0.7,      # ลด target ในโหมดระมัดระวัง
                'emergency': 0.5,         # ลด target มากในโหมดฉุกเฉิน
                'recovery': 0.8           # ลด target เล็กน้อยในโหมดฟื้นตัว
            }
            mode_multiplier = mode_adjustments.get(trading_mode, 1.0)
            
            # คำนวณ final target
            final_target = base_target * volume_multiplier * mode_multiplier
            
            return max(0.5, final_target)  # minimum $0.5 target
            
        except Exception as e:
            return 2.0  # fallback

    # ==========================================
    # 🆕 v4.0: CAPITAL-AWARE RECOVERY
    # ==========================================
    
    def _find_capital_aware_recovery_opportunities(self, positions: List[Dict], capital_context: Dict) -> List[Dict]:
        """🚀 หาโอกาส Recovery แบบ Capital-aware (NEW v4.0)"""
        try:
            recovery_actions = []
            
            if not self.recovery_config.get("enabled", True):
                return recovery_actions
            
            trading_mode = capital_context.get('trading_mode', 'normal')
            current_drawdown = capital_context.get('current_drawdown', 0.0)
            
            # เน้น recovery มากขึ้นเมื่อ drawdown สูง
            if current_drawdown < 10.0 and trading_mode not in ['recovery', 'conservative']:
                return recovery_actions  # ไม่ต้อง aggressive recovery
            
            # หา losing positions ที่ต้อง recovery
            losing_positions = [p for p in positions if p.get('total_pnl', 0) < -10.0]
            profitable_positions = [p for p in positions if p.get('total_pnl', 0) > 2.0]
            
            if not losing_positions or not profitable_positions:
                return recovery_actions
            
            print(f"🚀 Capital-aware recovery: {len(losing_positions)} losing vs {len(profitable_positions)} profitable")
            
            # หา recovery combinations ที่เหมาะสม
            for losing_pos in losing_positions:
                losing_role = self._get_position_role(losing_pos.get('id', ''))
                
                # ถ้าเป็น RH role ให้ aggressive recovery มากขึ้น
                is_recovery_role = losing_role == 'RH'
                
                recovery_combination = self._find_optimal_capital_aware_recovery(
                    losing_pos, profitable_positions, capital_context, is_recovery_role
                )
                
                if recovery_combination:
                    net_result = recovery_combination['net_profit']
                    risk_adjusted_score = recovery_combination['risk_adjusted_score']
                    
                    # เงื่อนไขการ recovery ปรับตาม capital context
                    min_net_profit = self._get_recovery_min_profit(capital_context, is_recovery_role)
                    
                    if net_result >= min_net_profit and risk_adjusted_score >= 0.4:
                        recovery_action = {
                            'action_type': 'capital_aware_recovery',
                            'target_position': losing_pos['id'],
                            'recovery_positions': recovery_combination['position_ids'],
                            'net_profit': net_result,
                            'risk_score': risk_adjusted_score,
                            'capital_context': trading_mode,
                            'is_recovery_role': is_recovery_role,
                            'priority': 1 if is_recovery_role else 2,
                            'reason': f"Capital recovery: ${net_result:.2f}, {trading_mode} mode"
                        }
                        recovery_actions.append(recovery_action)
            
            return recovery_actions
            
        except Exception as e:
            print(f"❌ Capital-aware recovery analysis error: {e}")
            return []

    def _get_recovery_min_profit(self, capital_context: Dict, is_recovery_role: bool) -> float:
        """🎯 กำหนด minimum profit สำหรับ recovery"""
        try:
            trading_mode = capital_context.get('trading_mode', 'normal')
            drawdown = capital_context.get('current_drawdown', 0.0)
            
            # Base requirements
            if is_recovery_role:  # RH role ยอมรับ recovery ที่ขาดทุนเล็กน้อยได้
                base_min = -5.0
            else:
                base_min = -2.0
            
            # ปรับตาม trading mode
            if trading_mode == 'emergency':
                return base_min - 3.0  # ยอมรับขาดทุนมากขึ้นใน emergency
            elif trading_mode == 'recovery':
                return base_min - 2.0  # ยอมรับขาดทุนมากขึ้นใน recovery mode
            elif drawdown > 25.0:
                return base_min - 2.0  # drawdown สูงมาก = ยอมรับขาดทุน
            else:
                return base_min
                
        except Exception as e:
            return -2.0

    def _find_optimal_capital_aware_recovery(self, target_pos: Dict, candidate_positions: List[Dict], 
                                           capital_context: Dict, is_recovery_role: bool) -> Optional[Dict]:
        """🔍 หา Recovery Combination แบบ Capital-aware"""
        try:
            target_volume = target_pos.get('volume', 0)
            target_pnl = target_pos.get('total_pnl', 0)
            
            best_combination = None
            best_score = -999999
            
            max_combination_size = self.recovery_config.get("max_combination_size", 5)
            
            # ลองหา combinations ขนาดต่างๆ
            for combo_size in range(1, min(len(candidate_positions) + 1, max_combination_size + 1)):
                
                # ลองทุก combination ในขนาดนี้ (simplified - ใช้แค่ top candidates)
                sorted_candidates = sorted(candidate_positions, 
                                         key=lambda x: x.get('profit_per_lot', 0), reverse=True)
                
                for i in range(min(10, len(sorted_candidates) - combo_size + 1)):  # ลอง 10 combinations แรก
                    combination = sorted_candidates[i:i+combo_size]
                    
                    recovery_score = self._evaluate_capital_aware_recovery_combination(
                        combination, target_pos, capital_context, is_recovery_role
                    )
                    
                    if recovery_score['score'] > best_score:
                        best_combination = recovery_score
                        best_score = recovery_score['score']
            
            return best_combination if best_score > 0.3 else None
            
        except Exception as e:
            print(f"❌ Capital-aware recovery combination error: {e}")
            return None

    def _evaluate_capital_aware_recovery_combination(self, recovery_positions: List[Dict], target_pos: Dict, 
                                                   capital_context: Dict, is_recovery_role: bool) -> Dict:
        """📊 ประเมิน Recovery Combination แบบ Capital-aware"""
        try:
            # คำนวณผลรวม
            recovery_volume = sum(p.get('volume', 0) for p in recovery_positions)
            recovery_profit = sum(p.get('total_pnl', 0) for p in recovery_positions)
            
            target_volume = target_pos.get('volume', 0)
            target_profit = target_pos.get('total_pnl', 0)
            
            net_profit = recovery_profit + target_profit
            volume_match_ratio = min(recovery_volume, target_volume) / max(recovery_volume, target_volume) if max(recovery_volume, target_volume) > 0 else 0
            
            # Capital context adjustments
            trading_mode = capital_context.get('trading_mode', 'normal')
            drawdown = capital_context.get('current_drawdown', 0.0)
            
            # คำนวณ risk-adjusted score
            profit_score = self._calculate_recovery_profit_score(net_profit, trading_mode, drawdown, is_recovery_role)
            volume_score = volume_match_ratio
            capital_score = self._calculate_capital_recovery_score(capital_context, is_recovery_role)
            
            # รวมคะแนน
            total_score = (profit_score * 0.5) + (volume_score * 0.3) + (capital_score * 0.2)
            
            return {
                'position_ids': [p['id'] for p in recovery_positions],
                'total_volume': recovery_volume,
                'net_profit': net_profit,
                'volume_match_ratio': volume_match_ratio,
                'risk_adjusted_score': total_score,
                'score': total_score
            }
            
        except Exception as e:
            return {'score': 0}

    def _calculate_recovery_profit_score(self, net_profit: float, trading_mode: str, drawdown: float, is_recovery_role: bool) -> float:
        """💰 คำนวณคะแนนกำไรสำหรับ recovery"""
        try:
            # Base scoring
            if net_profit >= 5.0:
                base_score = 1.0
            elif net_profit >= 0.0:
                base_score = 0.7
            elif net_profit >= -5.0:
                base_score = 0.5
            else:
                base_score = 0.2
            
            # Trading mode adjustments
            if trading_mode == 'emergency':
                base_score += 0.3  # ยอมรับ recovery ง่ายขึ้นใน emergency
            elif trading_mode == 'recovery':
                base_score += 0.2  # ยอมรับ recovery ง่ายขึ้นใน recovery mode
            
            # Recovery role adjustment
            if is_recovery_role:
                base_score += 0.2  # RH role ยอมรับ recovery ง่ายขึ้น
            
            # Drawdown adjustment
            if drawdown > 25.0:
                base_score += 0.3  # drawdown สูงมาก = ยอมรับ recovery ง่ายขึ้น
            elif drawdown > 20.0:
                base_score += 0.2
            
            return max(0.0, min(1.0, base_score))
            
        except Exception as e:
            return 0.5

    def _calculate_capital_recovery_score(self, capital_context: Dict, is_recovery_role: bool) -> float:
        """💰 คำนวณคะแนน capital สำหรับ recovery"""
        try:
            efficiency = capital_context.get('efficiency', 1.0)
            drawdown = capital_context.get('current_drawdown', 0.0)
            
            # Capital efficiency score
            if efficiency > 1.2:
                capital_score = 0.3  # ทุนเพิ่ม = ไม่ต้อง recovery aggressive
            elif efficiency > 1.0:
                capital_score = 0.5
            elif efficiency > 0.8:
                capital_score = 0.7
            else:
                capital_score = 1.0  # ทุนลด = ต้อง recovery
            
            # Drawdown urgency
            if drawdown > 25.0:
                capital_score += 0.4  # urgent recovery needed
            elif drawdown > 20.0:
                capital_score += 0.3
            elif drawdown > 15.0:
                capital_score += 0.2
            
            # Recovery role bonus
            if is_recovery_role:
                capital_score += 0.1
            
            return max(0.0, min(1.0, capital_score))
            
        except Exception as e:
            return 0.5

    # ==========================================
    # 📊 ENHANCED POSITION ANALYSIS (v3.0 + v4.0)
    # ==========================================
    
    def get_all_positions(self) -> List[Dict]:
        """💼 ดึงข้อมูล positions ทั้งหมด พร้อม enhanced analysis v4.0"""
        try:
            # เช็ค cache ก่อน (v3.0)
            now = datetime.now()
            if (now - self.last_update_time).total_seconds() < self.update_interval and self.position_cache:
                return list(self.position_cache.values())
            
            # ดึงข้อมูลจาก MT5
            symbol = self.symbol
            positions = mt5.positions_get(symbol=symbol)
            
            if positions is None:
                positions = []
            
            # แปลงเป็น enhanced format
            enhanced_positions = []
            for pos in positions:
                enhanced_pos = self._enhance_position_with_capital_role_data(pos)
                enhanced_positions.append(enhanced_pos)
            
            # อัพเดท cache
            self.position_cache = {pos['id']: pos for pos in enhanced_positions}
            self.last_update_time = now
            
            # อัพเดทสถิติ portfolio (v3.0)
            self._update_portfolio_lot_stats(enhanced_positions)
            
            # 🆕 v4.0: อัพเดทสถิติ role
            self._update_role_distribution_stats(enhanced_positions)
            
            return enhanced_positions
            
        except Exception as e:
            print(f"❌ Get all positions error: {e}")
            return []

    def _enhance_position_with_capital_role_data(self, pos) -> Dict:
        """🆕 v4.0: เพิ่มข้อมูล Capital & Role ให้ position"""
        try:
            # Basic position data (v3.0)
            position_data = {
                'id': str(pos.ticket),
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == mt5.ORDER_TYPE_BUY else 'SELL',
                'volume': pos.volume,
                'open_price': pos.price_open,
                'current_price': pos.price_current,
                'total_pnl': pos.profit + pos.swap,
                'swap': pos.swap,
                'commission': getattr(pos, 'commission', 0),
                'open_time': datetime.fromtimestamp(pos.time)
            }
            
            # Enhanced calculations (v3.0)
            age_timedelta = datetime.now() - position_data['open_time']
            age_hours = age_timedelta.total_seconds() / 3600
            profit_per_lot = position_data['total_pnl'] / position_data['volume'] if position_data['volume'] > 0 else 0
            
            # 🆕 v4.0: Role information
            position_id = position_data['id']
            position_role = self._get_position_role(position_id)
            
            # 🆕 v4.0: Capital zone determination
            capital_context = self._get_capital_context()
            position_zone = self._determine_position_capital_zone(position_data, capital_context)
            
            # Enhanced data
            position_data.update({
                'age_hours': round(age_hours, 1),
                'age': f"{int(age_hours)}h {int((age_hours % 1) * 60)}m",
                'profit_per_lot': round(profit_per_lot, 1),
                
                # 🆕 v4.0: Role & Capital data
                'order_role': position_role,
                'capital_zone': position_zone,
                'trading_mode': capital_context.get('trading_mode', 'normal'),
                
                # Analysis categories (v3.0 + v4.0)
                'efficiency_category': self._classify_efficiency_category_v4(position_data, position_role),
                'risk_category': self._classify_risk_category_v4(position_data, position_role, capital_context),
                'close_priority': self._calculate_role_aware_close_priority(position_data, position_role, capital_context),
                
                # Technical data
                'estimated_margin': self._estimate_position_margin(position_data),
                'margin_efficiency': profit_per_lot / max(self._estimate_position_margin(position_data), 1) if self._estimate_position_margin(position_data) > 0 else 0
            })
            
            return position_data
            
        except Exception as e:
            print(f"❌ Position enhancement error: {e}")
            return {'id': 'error', 'error': str(e)}

    def _determine_position_capital_zone(self, position_data: Dict, capital_context: Dict) -> str:
        """💰 กำหนด Capital Zone ของ position (ประมาณ)"""
        try:
            volume = position_data.get('volume', 0.01)
            
            # ประมาณจาก lot size (simple heuristic)
            if volume <= 0.03:
                return 'safe'
            elif volume <= 0.10:
                return 'growth'  
            else:
                return 'aggressive'
                
        except Exception as e:
            return 'safe'

    def _classify_efficiency_category_v4(self, position_data: Dict, role: str) -> str:
        """📊 จำแนกหมวดหมู่ Efficiency v4.0 (role-aware)"""
        try:
            profit_per_lot = position_data.get('profit_per_lot', 0)
            
            # Role-specific efficiency thresholds
            if role == 'SC':  # Scalp Capture - เกณฑ์ต่ำ
                thresholds = {'excellent': 20, 'good': 10, 'fair': 0, 'poor': -20}
            elif role == 'RH':  # Recovery Hunter - เกณฑ์ต่ำ
                thresholds = {'excellent': 30, 'good': 15, 'fair': 0, 'poor': -30}
            elif role == 'HG':  # Hedge Guard - เกณฑ์สูง
                thresholds = {'excellent': 80, 'good': 40, 'fair': 0, 'poor': -60}
            else:  # PW - Profit Walker - เกณฑ์ปกติ
                thresholds = {'excellent': 60, 'good': 30, 'fair': 0, 'poor': -40}
            
            if profit_per_lot >= thresholds['excellent']:
                return 'excellent'
            elif profit_per_lot >= thresholds['good']:
                return 'good'
            elif profit_per_lot >= thresholds['fair']:
                return 'fair'
            elif profit_per_lot >= thresholds['poor']:
                return 'poor'
            else:
                return 'terrible'
                
        except Exception as e:
            return 'unknown'

    def _classify_risk_category_v4(self, position_data: Dict, role: str, capital_context: Dict) -> str:
        """🛡️ จำแนกหมวดหมู่ Risk v4.0 (capital-aware)"""
        try:
            total_pnl = position_data.get('total_pnl', 0)
            age_hours = position_data.get('age_hours', 0)
            volume = position_data.get('volume', 0)
            
            # Capital context
            drawdown = capital_context.get('current_drawdown', 0.0)
            trading_mode = capital_context.get('trading_mode', 'normal')
            
            # Role-specific risk tolerance
            if role == 'HG':  # Hedge Guard - ทนได้มาก
                high_risk_loss = -60.0
                medium_risk_loss = -30.0
                max_age = 48
            elif role == 'RH':  # Recovery Hunter - ทนได้ปานกลาง
                high_risk_loss = -25.0
                medium_risk_loss = -15.0  
                max_age = 12
            elif role == 'SC':  # Scalp Capture - ทนได้น้อย
                high_risk_loss = -8.0
                medium_risk_loss = -4.0
                max_age = 3
            else:  # PW - Profit Walker
                high_risk_loss = -35.0
                medium_risk_loss = -20.0
                max_age = 24
            
            # Capital mode adjustments
            if trading_mode == 'emergency':
                high_risk_loss *= 0.7  # เข้มงวดมากขึ้น
                max_age *= 0.5
            elif trading_mode == 'recovery':
                high_risk_loss *= 1.3  # ผ่อนปรนขึ้น
                max_age *= 1.2
            
            # จำแนกความเสี่ยง
            if total_pnl <= high_risk_loss or age_hours >= max_age:
                return 'high'
            elif total_pnl <= medium_risk_loss or age_hours >= max_age * 0.7:
                return 'medium'
            elif total_pnl < 0:
                return 'low'
            else:
                return 'minimal'
                
        except Exception as e:
            return 'unknown'

    def _calculate_role_aware_close_priority(self, position_data: Dict, role: str, capital_context: Dict) -> float:
        """🎯 คำนวณ Priority การปิดแบบ Role-aware"""
        try:
            profit_per_lot = position_data.get('profit_per_lot', 0)
            age_hours = position_data.get('age_hours', 0)
            volume = position_data.get('volume', 0)
            total_profit = position_data.get('total_pnl', 0)
            
            # Role-specific priority calculation
            if role == 'SC':  # Scalp Capture - ปิดเร็วสุด
                priority = min(1.0, (total_profit + 5) / 10)  # normalize -5 to +5
                if age_hours > 2:  # เกินเวลา = priority สูง
                    priority += 0.3
                    
            elif role == 'RH':  # Recovery Hunter - ปิดเมื่อ recovery สำเร็จ
                if total_profit > 0:
                    priority = 0.9  # recovery สำเร็จ = ปิดทันที
                else:
                    priority = max(0.3, age_hours / 12)  # ปิดตาม age
                    
            elif role == 'HG':  # Hedge Guard - ค้ำได้นาน
                if total_profit > 5.0:
                    priority = 0.8  # กำไรดีแล้ว
                else:
                    priority = max(0.2, age_hours / 48)  # ค้ำได้นาน
                    
            else:  # PW - Profit Walker
                priority = (total_profit + 10) / 30  # normalize -10 to +20
                priority += age_hours / 48  # factor ของ age
            
            # Capital context adjustment
            trading_mode = capital_context.get('trading_mode', 'normal')
            if trading_mode == 'emergency':
                priority += 0.2  # เร่งปิดใน emergency
            elif trading_mode == 'recovery' and total_profit > 0:
                priority += 0.1  # เร่งเก็บกำไรใน recovery mode
            
            return max(0.0, min(1.0, priority))
            
        except Exception as e:
            return 0.5

    def _update_role_distribution_stats(self, positions: List[Dict]):
        """🆕 v4.0: อัพเดทสถิติการกระจาย role"""
        try:
            if not self.role_manager:
                return
            
            role_distribution = self.role_manager.get_portfolio_role_distribution(positions)
            
            # บันทึกสถิติ role performance
            for pos in positions:
                role = pos.get('order_role', 'PW')
                profit = pos.get('total_pnl', 0)
                age_hours = pos.get('age_hours', 0)
                
                if role in self.role_close_stats:
                    # อัพเดท running averages (simplified)
                    current_count = self.role_close_stats[role]['closed']
                    self.role_close_stats[role]['avg_profit'] = (
                        (self.role_close_stats[role]['avg_profit'] * current_count + profit) / (current_count + 1)
                    ) if current_count > 0 else profit
                    
                    self.role_close_stats[role]['avg_hold_time'] = (
                        (self.role_close_stats[role]['avg_hold_time'] * current_count + age_hours) / (current_count + 1)
                    ) if current_count > 0 else age_hours
            
        except Exception as e:
            print(f"❌ Role distribution stats update error: {e}")

    # ==========================================
    # 📊 REPORTING & ANALYTICS (enhanced v4.0)
    # ==========================================
    
    def get_enhanced_position_report_v4(self) -> Dict:
        """📊 รายงาน Position แบบ Capital & Role Enhanced v4.0"""
        try:
            positions = self.get_all_positions()
            capital_context = self._get_capital_context()
            
            # Basic stats
            total_positions = len(positions)
            total_profit = sum(p.get('total_pnl', 0) for p in positions)
            total_volume = sum(p.get('volume', 0) for p in positions)
            
            # 🆕 v4.0: Role distribution analysis
            role_distribution = {}
            role_performance = {}
            
            if self.role_manager:
                role_data = self.role_manager.get_portfolio_role_distribution(positions)
                role_distribution = role_data.get('distribution', {})
                role_performance = role_data.get('profits', {})
            
            # 🆕 v4.0: Capital zone analysis
            zone_distribution = {}
            for pos in positions:
                zone = pos.get('capital_zone', 'safe')
                if zone not in zone_distribution:
                    zone_distribution[zone] = {'count': 0, 'volume': 0.0, 'profit': 0.0}
                zone_distribution[zone]['count'] += 1
                zone_distribution[zone]['volume'] += pos.get('volume', 0)
                zone_distribution[zone]['profit'] += pos.get('total_pnl', 0)
            
            # Close opportunities analysis
            opportunities = self.check_smart_close_opportunities()
            
            report = {
                'summary': {
                    'total_positions': total_positions,
                    'total_profit': round(total_profit, 2),
                    'total_volume': round(total_volume, 2),
                    'avg_profit_per_lot': round(total_profit / total_volume, 1) if total_volume > 0 else 0,
                    'portfolio_health': self._calculate_portfolio_health_score(positions)
                },
                
                # 🆕 v4.0: Capital analysis
                'capital_analysis': {
                    'trading_mode': capital_context.get('trading_mode', 'normal'),
                    'current_drawdown': capital_context.get('current_drawdown', 0.0),
                    'zone_distribution': zone_distribution,
                    'capital_efficiency': capital_context.get('efficiency', 1.0)
                },
                
                # 🆕 v4.0: Role analysis  
                'role_analysis': {
                    'distribution': role_distribution,
                    'performance': role_performance,
                    'close_stats': self.role_close_stats.copy()
                },
                
                # Enhanced opportunities (v3.0 + v4.0)
                'opportunities': {
                    'total_found': len(opportunities),
                    'high_priority': len([o for o in opportunities if o.get('priority', 5) <= 2]),
                    'by_type': self._categorize_opportunities(opportunities),
                    'top_recommendations': opportunities[:5]
                },
                
                # Lot statistics (v3.0)
                'lot_statistics': self.lot_stats.copy(),
                
                'last_updated': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Enhanced position report error: {e}")
            return {'error': str(e)}

    def _calculate_portfolio_health_score(self, positions: List[Dict]) -> float:
        """🏥 คำนวณคะแนนสุขภาพ portfolio (enhanced v4.0)"""
        try:
            if not positions:
                return 1.0
            
            total_profit = sum(p.get('total_pnl', 0) for p in positions)
            total_volume = sum(p.get('volume', 0) for p in positions)
            
            # Profit health (40%)
            avg_profit_per_lot = total_profit / total_volume if total_volume > 0 else 0
            profit_health = max(0, min(1, (avg_profit_per_lot + 50) / 100))
            
            # Position age health (20%)
            avg_age = sum(p.get('age_hours', 0) for p in positions) / len(positions)
            age_health = max(0, 1 - (avg_age / 48))  # ยิ่งเก่า = สุขภาพแย่
            
            # Volume balance health (20%)
            buy_volume = sum(p.get('volume', 0) for p in positions if p.get('type') == 'BUY')
            sell_volume = sum(p.get('volume', 0) for p in positions if p.get('type') == 'SELL')
            balance_ratio = buy_volume / (buy_volume + sell_volume) if (buy_volume + sell_volume) > 0 else 0.5
            balance_health = 1 - abs(balance_ratio - 0.5) * 2  # ยิ่งสมดุล = สุขภาพดี
            
            # 🆕 v4.0: Role balance health (20%)
            role_health = self._calculate_role_balance_health(positions)
            
            # รวมคะแนน
            overall_health = (profit_health * 0.4) + (age_health * 0.2) + (balance_health * 0.2) + (role_health * 0.2)
            
            return round(max(0.0, min(1.0, overall_health)), 2)
            
        except Exception as e:
            return 0.5

    def _calculate_role_balance_health(self, positions: List[Dict]) -> float:
        """🎭 คำนวณสุขภาพการกระจาย role"""
        try:
            if not positions or not self.role_manager:
                return 1.0
            
            role_distribution = {}
            for pos in positions:
                role = pos.get('order_role', 'PW')
                role_distribution[role] = role_distribution.get(role, 0) + 1
            
            total_positions = len(positions)
            target_quotas = self.role_manager.role_quotas
            
            # คำนวณ deviation จาก target quotas
            deviation_score = 0.0
            for role, target_percent in target_quotas.items():
                current_count = role_distribution.get(role, 0)
                current_percent = (current_count / total_positions) * 100
                deviation = abs(current_percent - target_percent)
                deviation_score += deviation
            
            # แปลงเป็น health score (ยิ่ง deviation น้อย = health ดี)
            max_possible_deviation = 100.0  # theoretical max
            health_score = max(0, 1 - (deviation_score / max_possible_deviation))
            
            return health_score
            
        except Exception as e:
            return 1.0

    def _categorize_opportunities(self, opportunities: List[Dict]) -> Dict:
        """📊 จำแนกประเภทโอกาส"""
        try:
            categories = {}
            for opp in opportunities:
                action_type = opp.get('action_type', 'unknown')
                if action_type not in categories:
                    categories[action_type] = 0
                categories[action_type] += 1
            
            return categories
            
        except Exception as e:
            return {}

    # ==========================================
    # 🔧 LEGACY METHODS (v3.0 - เก็บไว้เพื่อ compatibility)
    # ==========================================
    
    def get_lot_efficiency_report(self) -> Dict:
        """📊 รายงาน Lot Efficiency (v3.0)"""
        try:
            positions = self.get_all_positions()
            
            if not positions:
                return {'message': 'No positions to analyze'}
            
            # Efficiency breakdown
            efficiency_breakdown = {}
            categories = ['excellent', 'good', 'fair', 'poor', 'terrible']
            
            for category in categories:
                positions_in_category = [p for p in positions if p.get('efficiency_category') == category]
                
                if positions_in_category:
                    total_volume = sum(p.get('volume', 0) for p in positions_in_category)
                    total_profit = sum(p.get('total_pnl', 0) for p in positions_in_category)
                    avg_efficiency = sum(p.get('profit_per_lot', 0) for p in positions_in_category) / len(positions_in_category)
                    
                    efficiency_breakdown[category] = {
                        'count': len(positions_in_category),
                        'total_volume': round(total_volume, 2),
                        'total_profit': round(total_profit, 2),
                        'avg_efficiency': round(avg_efficiency, 1),
                        'volume_percentage': round((total_volume / sum(p.get('volume', 0) for p in positions)) * 100, 1)
                    }
            
            # Recommendations
            recommendations = self._generate_lot_efficiency_recommendations(efficiency_breakdown)
            
            return {
                'efficiency_breakdown': efficiency_breakdown,
                'portfolio_stats': self.lot_stats.copy(),
                'recommendations': recommendations
            }
            
        except Exception as e:
            print(f"❌ Lot efficiency report error: {e}")
            return {'error': str(e)}

    def _generate_lot_efficiency_recommendations(self, breakdown: Dict) -> List[str]:
        """💡 สร้างคำแนะนำจาก lot efficiency analysis"""
        recommendations = []
        
        try:
            total_positions = sum(data['count'] for data in breakdown.values() if isinstance(data, dict))
            
            if total_positions == 0:
                return ["📊 No positions to analyze"]
            
            # แนะนำตาม efficiency distribution
            poor_terrible_count = breakdown.get('poor', {}).get('count', 0) + breakdown.get('terrible', {}).get('count', 0)
            if poor_terrible_count > total_positions * 0.3:
                recommendations.append(f"🚨 มี {poor_terrible_count} positions efficiency แย่มาก - หา hedge partners")
            
            excellent_count = breakdown.get('excellent', {}).get('count', 0)
            if excellent_count > total_positions * 0.3:
                recommendations.append(f"🌟 มี {excellent_count} positions efficiency ดีมาก - พิจารณาปิดเก็บกำไร")
            
            # Volume distribution recommendations
            total_volume = sum(data.get('total_volume', 0) for data in breakdown.values() if isinstance(data, dict))
            terrible_volume_pct = breakdown.get('terrible', {}).get('volume_percentage', 0)
            
            if terrible_volume_pct > 30:
                recommendations.append(f"⚠️ Volume ใน terrible category สูง {terrible_volume_pct:.1f}% - ลด lot sizes")
                
            if not recommendations:
                recommendations.append("✅ Portfolio efficiency ดูดี - ติดตามต่อไป")
            
            return recommendations
            
        except Exception as e:
            return [f"❌ Recommendation error: {e}"]

    def get_lot_distribution_analysis(self) -> Dict:
        """📊 วิเคราะห์การกระจายตัวของ Lot Size (v3.0)"""
        try:
            positions = self.get_all_positions()
            
            if not positions:
                return {'message': 'No positions to analyze'}
            
            # จัดกลุ่มตาม lot size ranges
            lot_ranges = {
                'micro': [],    # 0.01-0.03
                'small': [],    # 0.04-0.10  
                'medium': [],   # 0.11-0.50
                'large': [],    # 0.51-1.00
                'huge': []      # > 1.00
            }
            
            for pos in positions:
                volume = pos.get('volume', 0)
                
                if volume <= 0.03:
                    lot_ranges['micro'].append(pos)
                elif volume <= 0.10:
                    lot_ranges['small'].append(pos)
                elif volume <= 0.50:
                    lot_ranges['medium'].append(pos)
                elif volume <= 1.00:
                    lot_ranges['large'].append(pos)
                else:
                    lot_ranges['huge'].append(pos)
            
            # สรุปแต่ละ range
            analysis = {}
            for range_name, range_positions in lot_ranges.items():
                if range_positions:
                    total_volume = sum(p.get('volume', 0) for p in range_positions)
                    total_profit = sum(p.get('total_pnl', 0) for p in range_positions)
                    avg_efficiency = sum(p.get('profit_per_lot', 0) for p in range_positions) / len(range_positions)
                    
                    analysis[range_name] = {
                        'count': len(range_positions),
                        'total_volume': round(total_volume, 2),
                        'total_profit': round(total_profit, 2),
                        'avg_profit_per_lot': round(avg_efficiency, 1),
                        'percentage_of_portfolio': round((len(range_positions) / len(positions)) * 100, 1)
                    }
            
            return analysis
            
        except Exception as e:
            print(f"❌ Lot distribution analysis error: {e}")
            return {'error': str(e)}

    def calculate_volume_adjusted_threshold(self, volume: float) -> float:
        """📊 คำนวณ threshold ที่ปรับตาม volume (v3.0)"""
        try:
            # Base threshold ที่ปรับตาม volume
            if volume <= 0.01:
                return 1.0    # micro lots
            elif volume <= 0.05:
                return 2.5    # small lots
            elif volume <= 0.10:
                return 4.0    # medium lots
            elif volume <= 0.20:
                return 6.0    # large lots
            else:
                return 8.0    # huge lots
                
        except Exception as e:
            return 2.0

    # ==========================================
    # 🔧 LEGACY OPPORTUNITY METHODS (v3.0)
    # ==========================================
    
    def _find_margin_optimization_opportunities(self, positions: List[Dict]) -> List[Dict]:
        """🔧 หาโอกาส Margin Optimization (v3.0)"""
        try:
            margin_actions = []
            
            # ตรวจสอบ margin usage
            account_info = self.mt5_connector.get_account_info()
            if not account_info:
                return margin_actions
            
            margin_level = account_info.get('margin_level', 1000)
            
            # ถ้า margin level ต่ำ ให้หาโอกาส optimize
            if margin_level < 300:  # margin pressure
                print(f"⚠️ Margin pressure detected: {margin_level:.1f}%")
                
                # หา positions ที่ efficiency ต่ำเพื่อปิด
                low_efficiency_positions = [p for p in positions if p.get('efficiency_category') in ['poor', 'terrible']]
                
                # เรียงตาม margin impact (volume * current price)
                low_efficiency_positions.sort(key=lambda x: x.get('volume', 0) * x.get('current_price', 2000), reverse=True)
                
                for pos in low_efficiency_positions[:3]:  # ปิดสูงสุด 3 positions
                    margin_freed = pos.get('estimated_margin', 0)
                    profit_impact = pos.get('total_pnl', 0)
                    
                    if margin_freed > 50:  # margin ที่จะได้กลับมาก
                        margin_action = {
                            'action_type': 'margin_optimization',
                            'position_id': pos['id'],
                            'margin_freed': margin_freed,
                            'profit_impact': profit_impact,
                            'priority': 1,
                            'reason': f"Free ${margin_freed:.0f} margin, Impact: ${profit_impact:.2f}"
                        }
                        margin_actions.append(margin_action)
            
            return margin_actions
            
        except Exception as e:
            print(f"❌ Margin optimization error: {e}")
            return []

    def _find_volume_balance_opportunities(self, positions: List[Dict]) -> List[Dict]:
        """⚖️ หาโอกาส Volume Balance (v3.0)"""
        try:
            balance_actions = []
            
            # คำนวณ volume imbalance
            buy_positions = [p for p in positions if p.get('type') == 'BUY']
            sell_positions = [p for p in positions if p.get('type') == 'SELL']
            
            total_buy_volume = sum(p.get('volume', 0) for p in buy_positions)
            total_sell_volume = sum(p.get('volume', 0) for p in sell_positions)
            total_volume = total_buy_volume + total_sell_volume
            
            if total_volume < 0.1:
                return balance_actions
            
            buy_ratio = total_buy_volume / total_volume
            imbalance = abs(buy_ratio - 0.5)
            
            # ถ้า imbalance เกิน threshold
            if imbalance > self.volume_balance_tolerance:
                
                # หาว่าฝั่งไหนมากเกินไป
                if buy_ratio > 0.5 + self.volume_balance_tolerance:  # BUY มากเกินไป
                    excess_type = 'BUY'
                    excess_positions = buy_positions
                else:  # SELL มากเกินไป
                    excess_type = 'SELL'
                    excess_positions = sell_positions
                
                # หา positions ที่ควรปิดเพื่อ balance
                # เรียงตาม close priority (สูง = ปิดก่อน)
                excess_positions.sort(key=lambda x: x.get('close_priority', 0), reverse=True)
                
                # เลือก positions เพื่อลด imbalance
                target_volume_to_close = (total_volume * imbalance) / 2  # ลด imbalance ครึ่งหนึ่ง
                selected_for_balance = self._select_volume_close_set(excess_positions, target_volume_to_close)
                
                if selected_for_balance:
                    total_profit_impact = sum(p.get('total_pnl', 0) for p in selected_for_balance)
                    total_volume_to_close = sum(p.get('volume', 0) for p in selected_for_balance)
                    
                    balance_action = {
                        'action_type': 'volume_balance',
                        'position_ids': [p['id'] for p in selected_for_balance],
                        'excess_type': excess_type,
                        'volume_to_close': total_volume_to_close,
                        'profit_impact': total_profit_impact,
                        'current_imbalance': imbalance,
                        'priority': 2,
                        'reason': f"Balance {excess_type} excess: {imbalance:.1%} imbalance"
                    }
                    balance_actions.append(balance_action)
            
            return balance_actions
            
        except Exception as e:
            print(f"❌ Volume balance opportunities error: {e}")
            return []

    def _select_volume_close_set(self, positions: List[Dict], target_volume: float) -> List[Dict]:
        """📊 เลือกชุด positions เพื่อปิดตาม volume target"""
        try:
            selected_positions = []
            accumulated_volume = 0.0
            accumulated_profit = 0.0
            
            for pos in positions:
                pos_volume = pos.get('volume', 0)
                pos_profit = pos.get('total_pnl', 0)
                
                # เช็คว่าการเพิ่ม position นี้คุ้มค่าหรือไม่
                if accumulated_volume + pos_volume <= target_volume * 1.2:  # ไม่เกิน 120% ของเป้าหมาย
                    
                    projected_profit = accumulated_profit + pos_profit
                    
                    # เพิ่มเข้าไปถ้าไม่ทำให้ขาดทุนมากเกินไป
                    if projected_profit >= accumulated_profit - 10.0:  # ไม่ให้แย่ลงเกิน $10
                        selected_positions.append(pos)
                        accumulated_volume += pos_volume
                        accumulated_profit += pos_profit
                        
                        # ถ้าถึงเป้าหมายแล้ว หยุด
                        if accumulated_volume >= target_volume * 0.8:  # 80% ของเป้าหมาย
                            break
            
            return selected_positions
            
        except Exception as e:
            print(f"❌ Volume close set selection error: {e}")
            return []

    def _find_enhanced_profit_opportunities(self, positions: List[Dict]) -> List[Dict]:
        """💰 หาโอกาสปิดเพื่อกำไร - ENHANCED WITH DYNAMIC LOT EFFICIENCY (v3.0)"""
        try:
            profit_actions = []
            
            # วนตรวจสอบทุก position
            for pos in positions:
                volume = pos.get('volume', 0)
                total_profit = pos.get('total_pnl', 0)
                profit_per_lot = pos.get('profit_per_lot', 0)
                age_hours = pos.get('age_hours', 0)
                
                # คำนวณ dynamic threshold สำหรับ position นี้
                volume_threshold = self.calculate_volume_adjusted_threshold(volume)
                
                close_profit = False
                priority = 5
                reason = ""
                
                # เกณฑ์การปิดแบบ volume-adjusted
                if total_profit >= volume_threshold * 2:  # efficiency สูงมาก
                    close_profit = True
                    priority = 1
                    reason = f"Very high efficiency: ${total_profit:.1f} vs ${volume_threshold * 2:.1f} target ({volume:.2f}L)"
                    
                elif total_profit >= volume_threshold:  # efficiency ดี
                    close_profit = True  
                    priority = 2
                    reason = f"Good efficiency: ${total_profit:.1f} vs ${volume_threshold:.1f} target ({volume:.2f}L)"
                    
                elif total_profit >= volume_threshold * 0.8 and age_hours >= 12:  # efficiency พอได้ + เก่า
                    close_profit = True
                    priority = 3
                    reason = f"OK efficiency + old: ${total_profit:.1f} vs ${volume_threshold * 0.8:.1f} target ({age_hours:.1f}h)"
                
                elif total_profit >= volume_threshold * 0.6 and volume >= 0.1:  # volume ใหญ่ + กำไรพอได้
                    close_profit = True
                    priority = 4
                    reason = f"Large volume profit: ${total_profit:.1f} with {volume:.2f}L"
                
                if close_profit:
                    profit_actions.append({
                        'action_type': 'enhanced_profit',
                        'position_id': pos['id'],
                        'volume': volume,
                        'profit': total_profit,
                        'profit_per_lot': profit_per_lot,
                        'threshold_used': volume_threshold,
                        'age_hours': age_hours,
                        'priority': priority,
                        'reason': reason
                    })
            
            print(f"💰 Enhanced profit analysis: {len(profit_actions)} opportunities")
            return profit_actions
            
        except Exception as e:
            print(f"❌ Enhanced profit opportunities error: {e}")
            return []

    # ==========================================
    # 🔄 POSITION CLOSING EXECUTION (v3.0 + v4.0)
    # ==========================================
    
    def execute_close_action(self, action_data: Dict) -> bool:
        """🔄 ดำเนินการปิด Position (enhanced v4.0)"""
        try:
            action_type = action_data.get('action_type')
            
            if action_type == 'role_based_close':
                return self._execute_role_based_close(action_data)
            elif action_type == 'multi_level_profit':
                return self._execute_multi_level_profit_close(action_data)
            elif action_type == 'capital_aware_recovery':
                return self._execute_capital_aware_recovery(action_data)
            else:
                # Fallback to v3.0 methods
                return self._execute_legacy_close_action(action_data)
                
        except Exception as e:
            print(f"❌ Execute close action error: {e}")
            return False

    def _execute_role_based_close(self, action_data: Dict) -> bool:
        """🎭 ปิด position ตาม role logic"""
        try:
            position_id = action_data.get('position_id')
            if not position_id:
                return False
            
            success = self._close_position_by_id(position_id)
            
            if success and self.role_manager:
                # บันทึกสถิติ role
                role = action_data.get('order_role', 'PW')
                profit = action_data.get('profit', 0)
                
                if role in self.role_close_stats:
                    self.role_close_stats[role]['closed'] += 1
                    # อัพเดท avg_profit (simplified)
                    current_count = self.role_close_stats[role]['closed']
                    current_avg = self.role_close_stats[role]['avg_profit']
                    new_avg = ((current_avg * (current_count - 1)) + profit) / current_count
                    self.role_close_stats[role]['avg_profit'] = round(new_avg, 2)
            
            print(f"✅ Role-based close executed: {action_data.get('order_role')} ${action_data.get('profit', 0):.2f}")
            return success
            
        except Exception as e:
            print(f"❌ Role-based close error: {e}")
            return False

    def _execute_multi_level_profit_close(self, action_data: Dict) -> bool:
        """💰 ปิด position สำหรับ multi-level profit"""
        try:
            position_id = action_data.get('position_id')
            profit_level = action_data.get('profit_level', 'standard')
            
            success = self._close_position_by_id(position_id)
            
            if success:
                print(f"✅ Multi-level profit close: {profit_level} level ${action_data.get('profit', 0):.2f}")
            
            return success
            
        except Exception as e:
            return False

    def _execute_capital_aware_recovery(self, action_data: Dict) -> bool:
        """🚀 ปิด positions สำหรับ capital-aware recovery"""
        try:
            target_id = action_data.get('target_position')
            recovery_ids = action_data.get('recovery_positions', [])
            
            success_count = 0
            total_to_close = 1 + len(recovery_ids)
            
            # ปิด target position
            if self._close_position_by_id(target_id):
                success_count += 1
            
            # ปิด recovery positions
            for recovery_id in recovery_ids:
                if self._close_position_by_id(recovery_id):
                    success_count += 1
            
            success = success_count == total_to_close
            
            if success:
                net_profit = action_data.get('net_profit', 0)
                print(f"✅ Capital-aware recovery executed: ${net_profit:.2f} net result")
            else:
                print(f"⚠️ Partial recovery: {success_count}/{total_to_close} positions closed")
            
            return success
            
        except Exception as e:
            print(f"❌ Capital-aware recovery error: {e}")
            return False

    def _execute_legacy_close_action(self, action_data: Dict) -> bool:
        """🔄 ปิด position แบบ legacy (v3.0)"""
        try:
            action_type = action_data.get('action_type')
            
            if action_type == 'single_profit':
                position_id = action_data.get('position_id')
                return self._close_position_by_id(position_id)
                
            elif action_type in ['margin_optimization', 'volume_balance', 'lot_aware_recovery']:
                # ปิดหลาย positions
                position_ids = action_data.get('position_ids', [])
                target_id = action_data.get('target_position')
                recovery_ids = action_data.get('recovery_positions', [])
                
                all_ids = []
                if target_id:
                    all_ids.append(target_id)
                all_ids.extend(position_ids)
                all_ids.extend(recovery_ids)
                
                success_count = 0
                for pos_id in all_ids:
                    if self._close_position_by_id(pos_id):
                        success_count += 1
                
                return success_count > 0
            
            return False
            
        except Exception as e:
            print(f"❌ Legacy close action error: {e}")
            return False

    def _close_position_by_id(self, position_id: str) -> bool:
        """🔄 ปิด position ด้วย ID (v3.0)"""
        try:
            if not position_id:
                return False
            
            # ดึงข้อมูล position
            positions = mt5.positions_get(symbol=self.symbol)
            target_position = None
            
            for pos in positions:
                if str(pos.ticket) == str(position_id):
                    target_position = pos
                    break
            
            if not target_position:
                print(f"❌ Position {position_id} not found")
                return False
            
            # สร้าง close request
            close_request = {
                'action': mt5.TRADE_ACTION_DEAL,
                'symbol': target_position.symbol,
                'volume': target_position.volume,
                'type': mt5.ORDER_TYPE_SELL if target_position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                'position': target_position.ticket,
                'deviation': 20,
                'magic': 0,
                'comment': f"Smart close by Position Monitor v4.0"
            }
            
            # ส่งคำสั่งปิด
            result = mt5.order_send(close_request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"✅ Position {position_id} closed successfully")
                return True
            else:
                print(f"❌ Failed to close position {position_id}: {result.retcode}")
                return False
                
        except Exception as e:
            print(f"❌ Close position by ID error: {e}")
            return False

    def close_multiple_positions(self, position_ids: List[str]) -> Dict:
        """🔄 ปิดหลาย positions พร้อมกัน (v3.0)"""
        try:
            results = {
                'total_requested': len(position_ids),
                'successful': 0,
                'failed': 0,
                'errors': []
            }
            
            for position_id in position_ids:
                try:
                    success = self._close_position_by_id(position_id)
                    if success:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(f"Position {position_id}: Close failed")
                        
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Position {position_id}: {str(e)}")
            
            print(f"🔄 Multiple close result: {results['successful']}/{results['total_requested']} successful")
            return results
            
        except Exception as e:
            print(f"❌ Multiple close error: {e}")
            return {'error': str(e)}

    def emergency_close_all_positions(self) -> Dict:
        """🚨 ปิด positions ทั้งหมดฉุกเฉิน (v3.0)"""
        try:
            positions = self.get_all_positions()
            
            if not positions:
                return {'message': 'No positions to close'}
            
            position_ids = [p['id'] for p in positions]
            
            print(f"🚨 EMERGENCY: Closing all {len(positions)} positions")
            
            result = self.close_multiple_positions(position_ids)
            
            if result.get('successful', 0) > 0:
                print(f"✅ Emergency close completed: {result['successful']} positions closed")
            
            return result
            
        except Exception as e:
            print(f"❌ Emergency close error: {e}")
            return {'error': str(e)}

    def get_position_summary(self) -> Dict:
        """📋 สรุปข้อมูล positions (v3.0 + v4.0)"""
        try:
            positions = self.get_all_positions()
            
            if not positions:
                return {'total_positions': 0, 'message': 'No active positions'}
            
            # Basic summary
            summary = {
                'total_positions': len(positions),
                'total_profit': sum(p.get('total_pnl', 0) for p in positions),
                'total_volume': sum(p.get('volume', 0) for p in positions),
                'buy_positions': len([p for p in positions if p.get('type') == 'BUY']),
                'sell_positions': len([p for p in positions if p.get('type') == 'SELL'])
            }
            
            # 🆕 v4.0: Role summary
            role_summary = {}
            for pos in positions:
                role = pos.get('order_role', 'Unknown')
                if role not in role_summary:
                    role_summary[role] = {'count': 0, 'profit': 0.0, 'volume': 0.0}
                role_summary[role]['count'] += 1
                role_summary[role]['profit'] += pos.get('total_pnl', 0)
                role_summary[role]['volume'] += pos.get('volume', 0)
            
            summary['role_summary'] = role_summary
            summary['avg_profit_per_lot'] = round(summary['total_profit'] / summary['total_volume'], 1) if summary['total_volume'] > 0 else 0
            summary['portfolio_health'] = self._calculate_portfolio_health_score(positions)
            
            return summary
            
        except Exception as e:
            print(f"❌ Position summary error: {e}")
            return {'error': str(e)}

    # ==========================================
    # 📊 LOT STATISTICS (v3.0)
    # ==========================================
    
    def _update_portfolio_lot_stats(self, positions: List[Dict]):
        """📊 อัพเดทสถิติ portfolio - lot aware (v3.0)"""
        try:
            if not positions:
                self.lot_stats = {
                    'total_buy_volume': 0.0,
                    'total_sell_volume': 0.0,
                    'avg_profit_per_lot_buy': 0.0,
                    'avg_profit_per_lot_sell': 0.0,
                    'volume_imbalance_ratio': 0.0,
                    'margin_efficiency_score': 0.0
                }
                return
            
            # คำนวณ volume และ profit โดยแยก type
            buy_positions = [p for p in positions if p.get('type') == 'BUY']
            sell_positions = [p for p in positions if p.get('type') == 'SELL']
            
            total_buy_volume = sum(p.get('volume', 0) for p in buy_positions)
            total_sell_volume = sum(p.get('volume', 0) for p in sell_positions)
            
            # คำนวณ average profit per lot
            if total_buy_volume > 0:
                total_buy_profit = sum(p.get('total_pnl', 0) for p in buy_positions)
                avg_profit_buy = total_buy_profit / total_buy_volume
            else:
                avg_profit_buy = 0.0
            
            if total_sell_volume > 0:
                total_sell_profit = sum(p.get('total_pnl', 0) for p in sell_positions)
                avg_profit_sell = total_sell_profit / total_sell_volume
            else:
                avg_profit_sell = 0.0
            
            # คำนวณ volume imbalance
            total_volume = total_buy_volume + total_sell_volume
            if total_volume > 0:
                imbalance = abs(total_buy_volume - total_sell_volume) / total_volume
            else:
                imbalance = 0.0
            
            # คำนวณ margin efficiency
            total_profit = sum(p.get('total_pnl', 0) for p in positions)
            estimated_margin = sum(p.get('estimated_margin', 0) for p in positions)
            margin_efficiency = total_profit / estimated_margin if estimated_margin > 0 else 0
            
            # อัพเดท lot stats
            self.lot_stats = {
                'total_buy_volume': round(total_buy_volume, 2),
                'total_sell_volume': round(total_sell_volume, 2),
                'avg_profit_per_lot_buy': round(avg_profit_buy, 1),
                'avg_profit_per_lot_sell': round(avg_profit_sell, 1),
                'volume_imbalance_ratio': round(imbalance, 2),
                'margin_efficiency_score': round(margin_efficiency, 3)
            }
            
        except Exception as e:
            print(f"❌ Portfolio lot stats update error: {e}")

    def _estimate_position_margin(self, position_data: Dict) -> float:
        """📊 ประมาณการใช้ margin ของ position (v3.0)"""
        try:
            volume = position_data.get('volume', 0.01)
            current_price = position_data.get('current_price', 2000)
            
            # ประมาณการ margin สำหรับ gold (leverage 1:100 โดยประมาณ)
            estimated_margin = (volume * current_price * 100) / 100  # simplified
            return estimated_margin
            
        except Exception as e:
            return 0.0

    # ==========================================
    # 🧹 CLEANUP & MAINTENANCE (v3.0 + v4.0)
    # ==========================================
    
    def cleanup_closed_positions(self):
        """🧹 ล้างข้อมูล positions ที่ปิดแล้ว"""
        try:
            current_positions = mt5.positions_get(symbol=self.symbol)
            if current_positions is None:
                current_positions = []
            
            active_ids = {str(pos.ticket) for pos in current_positions}
            cached_ids = set(self.position_cache.keys())
            
            closed_ids = cached_ids - active_ids
            
            for closed_id in closed_ids:
                if closed_id in self.position_cache:
                    del self.position_cache[closed_id]
            
            # 🆕 v4.0: ล้าง role data ด้วย
            if self.role_manager and hasattr(self.role_manager, 'cleanup_closed_positions'):
                self.role_manager.cleanup_closed_positions(list(active_ids))
            
            if closed_ids:
                print(f"🧹 Cleaned up {len(closed_ids)} closed positions")
                
        except Exception as e:
            print(f"❌ Position cleanup error: {e}")

    def force_lot_aware_analysis(self) -> Dict:
        """🔧 บังคับทำ Analysis ทันที v4.0"""
        try:
            print(f"🔧 FORCE ENHANCED ANALYSIS v4.0...")
            
            # Clear cache
            self.position_cache = {}
            self.last_update_time = datetime.min
            
            # ดึงข้อมูลใหม่
            positions = self.get_all_positions()
            capital_context = self._get_capital_context()
            
            # วิเคราะห์ opportunities
            opportunities = self.check_smart_close_opportunities()
            
            # สรุปผล v4.0
            analysis_result = {
                'total_positions': len(positions),
                'capital_context': {
                    'trading_mode': capital_context.get('trading_mode'),
                    'drawdown': capital_context.get('current_drawdown'),
                    'capital_efficiency': capital_context.get('efficiency', 1.0)
                },
                'role_distribution': self._get_current_role_distribution(positions),
                'close_opportunities': len(opportunities),
                'top_opportunities': [
                    {
                        'type': opp.get('action_type'),
                        'priority': opp.get('priority'),
                        'reason': opp.get('reason', '')[:60]
                    }
                    for opp in opportunities[:5]
                ],
                'portfolio_health': self._calculate_portfolio_health_score(positions),
                'lot_statistics': self.lot_stats.copy(),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Enhanced analysis v4.0 completed")
            print(f"   Trading mode: {capital_context.get('trading_mode')}")
            print(f"   Drawdown: {capital_context.get('current_drawdown', 0):.1f}%") 
            print(f"   Portfolio health: {analysis_result['portfolio_health']:.2f}")
            print(f"   Opportunities: {len(opportunities)}")
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Force enhanced analysis error: {e}")
            return {'error': str(e)}

    def _get_current_role_distribution(self, positions: List[Dict]) -> Dict:
        """🎭 ดึงการกระจาย role ปัจจุบัน"""
        try:
            distribution = {'HG': 0, 'PW': 0, 'RH': 0, 'SC': 0, 'Unknown': 0}
            
            for pos in positions:
                role = pos.get('order_role', 'Unknown')
                if role in distribution:
                    distribution[role] += 1
                else:
                    distribution['Unknown'] += 1
            
            return distribution
            
        except Exception as e:
            return {}


# ==========================================
# 🔧 INTEGRATION HELPER FUNCTIONS
# ==========================================

def create_enhanced_position_monitor(mt5_connector, config: Dict):
    """🏭 Factory function สำหรับสร้าง Enhanced Position Monitor v4.0"""
    try:
        monitor = PositionMonitor(mt5_connector, config)
        print("🏭 Enhanced Position Monitor v4.0 created successfully")
        return monitor
        
    except Exception as e:
        print(f"❌ Enhanced Position Monitor creation error: {e}")
        return None

def integrate_position_monitor_with_managers(monitor, capital_manager, role_manager):
    """🔗 ผูก Position Monitor เข้ากับ managers"""
    try:
        print("🔗 Integrating Position Monitor with Capital & Role Managers...")
        
        if capital_manager:
            monitor.set_capital_manager(capital_manager)
        
        if role_manager:
            monitor.set_role_manager(role_manager)
        
        print("✅ Position Monitor integration completed")
        
    except Exception as e:
        print(f"❌ Position Monitor integration error: {e}")