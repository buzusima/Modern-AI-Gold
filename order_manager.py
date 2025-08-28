"""
🎭 Order Role Intelligence System v4.0
order_role_manager.py

🚀 NEW FEATURES:
✅ Auto Role Assignment (HG/PW/RH/SC)
✅ Role Evolution Logic (dynamic role changes)
✅ Role-based Action Logic 
✅ Portfolio Role Balance Management
✅ Smart Role Recommendations
✅ Role Performance Analytics

🎯 ให้ระบบรู้หน้าที่ของแต่ละออเดอร์
จัดการออเดอร์แต่ละตัวตามบทบาทที่เหมาะสม
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import statistics
from enum import Enum

class OrderRole(Enum):
    """🎭 Order Role Definitions"""
    HG = "HG"  # Hedge Guard - ค้ำพอร์ต ป้องกัน major losses
    PW = "PW"  # Profit Walker - เดินตามกำไร รอจังหวะปิด  
    RH = "RH"  # Recovery Hunter - ช่วยฟื้นตัว hedge กับออเดอร์ติดลบ
    SC = "SC"  # Scalp Capture - เก็บกำไรเร็ว short-term opportunities

class OrderRoleManager:
    """
    🎭 Order Role Intelligence System
    
    จัดการบทบาทของแต่ละออเดอร์แบบอัจฉริยะ
    ปรับ role ตามสถานการณ์ + portfolio state
    """
    
    def __init__(self, config: Dict):
        """
        🔧 เริ่มต้น Order Role Manager
        
        Args:
            config: การตั้งค่าระบบ
        """
        self.config = config
        
        # Role configuration
        self.role_config = config.get("order_roles", {})
        
        # Role assignment rules
        self.auto_assignment = self.role_config.get("auto_assignment", True)
        self.role_evolution = self.role_config.get("role_evolution", True)
        self.portfolio_balancing = self.role_config.get("portfolio_balancing", True)
        
        # Role quotas (% of total positions)
        self.role_quotas = self.role_config.get("role_quotas", {
            "HG": 25.0,  # 25% Hedge Guard
            "PW": 40.0,  # 40% Profit Walker  
            "RH": 20.0,  # 20% Recovery Hunter
            "SC": 15.0   # 15% Scalp Capture
        })
        
        # Role-specific settings
        self.role_settings = {
            "HG": {
                "max_age_hours": 48,        # ค้ำได้นานสุด 48 ชั่วโมง
                "min_profit_threshold": 5.0, # ปิดเมื่อกำไร $5+
                "max_loss_tolerance": -50.0, # ทนขาดทุนได้ $50
                "hedge_priority": 1.0,      # priority สูงสุดในการ hedge
                "preferred_lot_range": (0.01, 0.05)
            },
            "PW": {
                "max_age_hours": 24,        # เดินตามกำไรนาน 24 ชั่วโมง
                "min_profit_threshold": 3.0, # ปิดเมื่อกำไร $3+ 
                "max_loss_tolerance": -30.0, # ทนขาดทุนได้ $30
                "trail_profit": True,       # ใช้ trailing profit
                "preferred_lot_range": (0.01, 0.10)
            },
            "RH": {
                "max_age_hours": 12,        # recovery เร็ว 12 ชั่วโมง
                "min_profit_threshold": 1.0, # ปิดเมื่อกำไร $1+
                "max_loss_tolerance": -20.0, # ทนขาดทุนได้ $20
                "aggressive_sizing": True,  # ใช้ lot size ใหญ่กว่า
                "preferred_lot_range": (0.02, 0.20)
            },
            "SC": {
                "max_age_hours": 2,         # scalp เร็ว 2 ชั่วโมง
                "min_profit_threshold": 0.5, # ปิดเมื่อกำไร $0.5+
                "max_loss_tolerance": -5.0,  # ทนขาดทุนได้ $5
                "quick_profit": True,       # เก็บกำไรเร็ว
                "preferred_lot_range": (0.01, 0.15)
            }
        }
        
        # Role tracking
        self.position_roles = {}  # {position_id: role_info}
        self.role_history = []    # ประวัติการเปลี่ยน role
        self.role_performance = {role.value: {'count': 0, 'profit': 0.0, 'success_rate': 0.0} 
                               for role in OrderRole}
        
        # Portfolio state
        self.portfolio_state = "balanced"  # balanced, imbalanced, recovery, protective
        self.last_balance_check = datetime.now()
        
        print(f"🎭 Order Role Manager initialized")
        print(f"   Role Quotas: HG {self.role_quotas['HG']}% | PW {self.role_quotas['PW']}% | RH {self.role_quotas['RH']}% | SC {self.role_quotas['SC']}%")
        print(f"   Auto Assignment: {self.auto_assignment}")
        print(f"   Role Evolution: {self.role_evolution}")

    # ==========================================
    # 🎯 ROLE ASSIGNMENT LOGIC
    # ==========================================
    
    def assign_role_to_new_position(self, position_info: Dict, portfolio_context: Dict) -> str:
        """
        🎯 กำหนด Role ให้ Position ใหม่
        
        Args:
            position_info: ข้อมูล position (type, volume, entry_price, etc.)
            portfolio_context: บริบท portfolio (drawdown, imbalance, etc.)
            
        Returns:
            str: Role ที่กำหนด ("HG", "PW", "RH", "SC")
        """
        try:
            if not self.auto_assignment:
                return "PW"  # default role
            
            # ดึงข้อมูลสำคัญ
            position_type = position_info.get('type', 'BUY')
            volume = position_info.get('volume', 0.01)
            signal_strength = position_info.get('signal_strength', 0.5)
            capital_zone = position_info.get('capital_zone', 'safe')
            
            # Portfolio context
            drawdown = portfolio_context.get('drawdown', 0.0)
            imbalance_ratio = portfolio_context.get('imbalance_ratio', 0.0)
            losing_positions = portfolio_context.get('losing_positions', 0)
            current_roles = portfolio_context.get('current_roles', {})
            
            # คำนวณ role scores
            role_scores = {}
            
            # HG (Hedge Guard) Score
            hg_score = 0.0
            if drawdown > 15.0:  # drawdown สูง ต้องการ hedge
                hg_score += 0.4
            if imbalance_ratio > 0.6:  # portfolio ไม่สมดุล
                hg_score += 0.3
            if losing_positions > 10:  # มี positions ติดลบเยอะ
                hg_score += 0.3
            if volume <= 0.05:  # lot เล็ก เหมาะสำหรับ hedge
                hg_score += 0.2
            
            # PW (Profit Walker) Score  
            pw_score = 0.5  # base score สูง (default role)
            if 0.6 <= signal_strength <= 0.8:  # signal strength ปานกลาง
                pw_score += 0.3
            if capital_zone in ['safe', 'growth']:  # zones ปกติ
                pw_score += 0.2
            if drawdown < 10.0:  # portfolio สุขภาพดี
                pw_score += 0.2
                
            # RH (Recovery Hunter) Score
            rh_score = 0.0
            if drawdown > 20.0:  # ต้องการ recovery
                rh_score += 0.5
            if losing_positions > 15:  # positions ติดลบเยอะ
                rh_score += 0.3
            if signal_strength > 0.8:  # signal แรง เหมาะสำหรับ recovery
                rh_score += 0.3
            if capital_zone == 'aggressive':  # aggressive zone
                rh_score += 0.2
                
            # SC (Scalp Capture) Score
            sc_score = 0.0
            if signal_strength > 0.7:  # signal แรง เหมาะสำหรับ scalp
                sc_score += 0.4
            if volume <= 0.08:  # lot เล็ก-กลาง เหมาะสำหรับ scalp
                sc_score += 0.2
            if drawdown < 5.0:  # portfolio สุขภาพดีมาก
                sc_score += 0.2
            if self._is_high_volatility_time():  # เวลาที่ market เคลื่อนไหวเร็ว
                sc_score += 0.3
            
            role_scores = {"HG": hg_score, "PW": pw_score, "RH": rh_score, "SC": sc_score}
            
            # ปรับ score ตาม portfolio role balance
            role_scores = self._adjust_scores_for_balance(role_scores, current_roles)
            
            # เลือก role ที่มี score สูงสุด
            assigned_role = max(role_scores, key=role_scores.get)
            
            print(f"🎯 Role assignment for {position_type} {volume:.2f}L:")
            print(f"   Scores: HG={hg_score:.2f} PW={pw_score:.2f} RH={rh_score:.2f} SC={sc_score:.2f}")
            print(f"   → Assigned: {assigned_role}")
            
            return assigned_role
            
        except Exception as e:
            print(f"❌ Role assignment error: {e}")
            return "PW"  # fallback to default

    def _adjust_scores_for_balance(self, role_scores: Dict, current_roles: Dict) -> Dict:
        """⚖️ ปรับ scores เพื่อรักษาสมดุล portfolio"""
        try:
            total_positions = sum(current_roles.values()) + 1  # +1 สำหรับ position ใหม่
            
            for role in role_scores:
                current_count = current_roles.get(role, 0)
                current_percent = (current_count / total_positions) * 100
                target_percent = self.role_quotas.get(role, 25.0)
                
                # ถ้า role นี้มีน้อยเกินไป ให้ boost score
                if current_percent < target_percent * 0.8:
                    role_scores[role] += 0.3
                # ถ้า role นี้มีมากเกินไป ให้ลด score  
                elif current_percent > target_percent * 1.2:
                    role_scores[role] -= 0.3
                    
            return role_scores
            
        except Exception as e:
            return role_scores

    def register_new_position(self, position_id: str, position_info: Dict, assigned_role: str):
        """
        📝 ลงทะเบียน Position ใหม่พร้อม Role
        
        Args:
            position_id: ID ของ position
            position_info: ข้อมูล position
            assigned_role: Role ที่กำหนด
        """
        try:
            self.position_roles[position_id] = {
                'role': assigned_role,
                'assigned_time': datetime.now(),
                'original_role': assigned_role,
                'evolution_count': 0,
                'position_info': position_info.copy(),
                'performance_metrics': {
                    'max_profit': 0.0,
                    'max_loss': 0.0,
                    'role_changes': []
                }
            }
            
            print(f"📝 Position {position_id} registered as {assigned_role}")
            
        except Exception as e:
            print(f"❌ Position registration error: {e}")

    # ==========================================
    # 🔄 ROLE EVOLUTION LOGIC  
    # ==========================================
    
    def check_role_evolution(self, positions: List[Dict]) -> List[Dict]:
        """
        🔄 ตรวจสอบและปรับ Role ตามสถานการณ์
        
        Args:
            positions: รายการ positions ปัจจุบัน
            
        Returns:
            List[Dict]: รายการ role changes ที่แนะนำ
        """
        try:
            if not self.role_evolution:
                return []
            
            evolution_recommendations = []
            
            for pos in positions:
                position_id = pos.get('id', '')
                if position_id not in self.position_roles:
                    continue
                    
                current_role = self.position_roles[position_id]['role']
                current_profit = pos.get('total_pnl', 0.0)
                age_hours = pos.get('age_hours', 0.0)
                
                # ตรวจสอบเงื่อนไข evolution สำหรับแต่ละ role
                new_role = self._evaluate_role_evolution(position_id, pos, current_role)
                
                if new_role and new_role != current_role:
                    evolution_recommendations.append({
                        'position_id': position_id,
                        'from_role': current_role,
                        'to_role': new_role,
                        'reason': self._get_evolution_reason(pos, current_role, new_role),
                        'priority': self._get_evolution_priority(current_role, new_role)
                    })
            
            return evolution_recommendations
            
        except Exception as e:
            print(f"❌ Role evolution check error: {e}")
            return []

    def _evaluate_role_evolution(self, position_id: str, position_data: Dict, current_role: str) -> Optional[str]:
        """🧠 ประเมิน Role Evolution สำหรับ Position หนึ่ง"""
        try:
            profit = position_data.get('total_pnl', 0.0)
            age_hours = position_data.get('age_hours', 0.0)
            volume = position_data.get('volume', 0.01)
            
            role_info = self.position_roles[position_id]
            
            # กฎการเปลี่ยน role ตามสถานการณ์
            if current_role == "HG":  # Hedge Guard
                # HG → PW เมื่อ portfolio ปลอดภัยแล้วและมีกำไร
                if profit > 3.0 and age_hours > 4:
                    return "PW"
                # HG → SC เมื่อมีกำไรน้อยแต่อยากปิดเร็ว
                elif 0.5 <= profit <= 2.0 and age_hours > 12:
                    return "SC"
                    
            elif current_role == "PW":  # Profit Walker  
                # PW → SC เมื่อมีกำไรแล้วแต่ไม่เยอะ อยากปิดเร็ว
                if 1.0 <= profit <= 4.0 and age_hours > 8:
                    return "SC"
                # PW → HG เมื่อขาดทุนและต้องการใช้เป็น hedge
                elif profit < -10.0 and age_hours > 6:
                    return "HG"
                # PW → RH เมื่อต้องการ recovery aggressive
                elif profit < -20.0 and volume >= 0.05:
                    return "RH"
                    
            elif current_role == "RH":  # Recovery Hunter
                # RH → PW เมื่อ recovery สำเร็จแล้ว
                if profit > 2.0:
                    return "PW"  
                # RH → SC เมื่อ recovery เล็กน้อยแต่อยากปิด
                elif 0.0 <= profit <= 1.5 and age_hours > 4:
                    return "SC"
                # RH → HG เมื่อ recovery ไม่สำเร็จ ให้ไปเป็น hedge
                elif profit < -30.0 and age_hours > 8:
                    return "HG"
                    
            elif current_role == "SC":  # Scalp Capture
                # SC → PW เมื่อกำไรเยอะเกินไป ควร hold ต่อ
                if profit > 5.0:
                    return "PW"
                # SC → HG เมื่อขาดทุนมาก ให้ไปเป็น hedge
                elif profit < -8.0:
                    return "HG"
            
            return None  # ไม่ต้องเปลี่ยน role
            
        except Exception as e:
            print(f"❌ Role evolution evaluation error: {e}")
            return None

    def apply_role_evolution(self, position_id: str, new_role: str, reason: str = ""):
        """
        🔄 ใช้การเปลี่ยน Role
        
        Args:
            position_id: ID ของ position
            new_role: Role ใหม่
            reason: เหตุผลการเปลี่ยน
        """
        try:
            if position_id not in self.position_roles:
                return False
            
            old_role = self.position_roles[position_id]['role']
            
            # อัพเดท role
            self.position_roles[position_id]['role'] = new_role
            self.position_roles[position_id]['evolution_count'] += 1
            
            # บันทึกประวัติ
            evolution_record = {
                'timestamp': datetime.now(),
                'position_id': position_id,
                'from_role': old_role,
                'to_role': new_role,
                'reason': reason
            }
            
            self.position_roles[position_id]['performance_metrics']['role_changes'].append(evolution_record)
            self.role_history.append(evolution_record)
            
            print(f"🔄 Role evolution: Position {position_id} {old_role} → {new_role} ({reason})")
            return True
            
        except Exception as e:
            print(f"❌ Role evolution application error: {e}")
            return False

    # ==========================================
    # 🎯 ROLE-BASED ACTION LOGIC
    # ==========================================
    
    def get_role_based_action_for_position(self, position_id: str, position_data: Dict) -> Dict:
        """
        🎯 ได้รับ Action แนะนำตาม Role
        
        Args:
            position_id: ID ของ position
            position_data: ข้อมูล position ปัจจุบัน
            
        Returns:
            Dict: Action recommendation
        """
        try:
            if position_id not in self.position_roles:
                return {'action': 'hold', 'reason': 'Unknown role'}
            
            role = self.position_roles[position_id]['role']
            profit = position_data.get('total_pnl', 0.0)
            age_hours = position_data.get('age_hours', 0.0)
            
            role_settings = self.role_settings.get(role, {})
            
            # Action logic แยกตาม role
            if role == "HG":  # Hedge Guard
                return self._get_hedge_guard_action(position_data, role_settings)
            elif role == "PW":  # Profit Walker
                return self._get_profit_walker_action(position_data, role_settings)
            elif role == "RH":  # Recovery Hunter  
                return self._get_recovery_hunter_action(position_data, role_settings)
            elif role == "SC":  # Scalp Capture
                return self._get_scalp_capture_action(position_data, role_settings)
            else:
                return {'action': 'hold', 'reason': f'Unknown role: {role}'}
                
        except Exception as e:
            print(f"❌ Role-based action error: {e}")
            return {'action': 'hold', 'reason': 'Error occurred'}

    def _get_hedge_guard_action(self, pos_data: Dict, settings: Dict) -> Dict:
        """🛡️ Hedge Guard Action Logic"""
        profit = pos_data.get('total_pnl', 0.0)
        age_hours = pos_data.get('age_hours', 0.0)
        
        if profit >= settings.get('min_profit_threshold', 5.0):
            return {'action': 'close', 'reason': f'HG profit target reached: ${profit:.2f}', 'priority': 2}
        elif profit <= settings.get('max_loss_tolerance', -50.0):
            return {'action': 'close', 'reason': f'HG loss limit hit: ${profit:.2f}', 'priority': 1}
        elif age_hours >= settings.get('max_age_hours', 48):
            return {'action': 'close', 'reason': f'HG max age reached: {age_hours:.1f}h', 'priority': 3}
        else:
            return {'action': 'hold', 'reason': f'HG protecting portfolio (${profit:.2f})', 'priority': 5}

    def _get_profit_walker_action(self, pos_data: Dict, settings: Dict) -> Dict:
        """🚶 Profit Walker Action Logic"""
        profit = pos_data.get('total_pnl', 0.0)
        age_hours = pos_data.get('age_hours', 0.0)
        
        if profit >= settings.get('min_profit_threshold', 3.0):
            return {'action': 'close', 'reason': f'PW profit target: ${profit:.2f}', 'priority': 2}
        elif profit <= settings.get('max_loss_tolerance', -30.0):
            return {'action': 'close', 'reason': f'PW loss limit: ${profit:.2f}', 'priority': 1}
        elif age_hours >= settings.get('max_age_hours', 24):
            return {'action': 'close', 'reason': f'PW max age: {age_hours:.1f}h', 'priority': 3}
        else:
            return {'action': 'hold', 'reason': f'PW walking for profit (${profit:.2f})', 'priority': 5}

    def _get_recovery_hunter_action(self, pos_data: Dict, settings: Dict) -> Dict:
        """🏹 Recovery Hunter Action Logic"""  
        profit = pos_data.get('total_pnl', 0.0)
        age_hours = pos_data.get('age_hours', 0.0)
        
        if profit >= settings.get('min_profit_threshold', 1.0):
            return {'action': 'close', 'reason': f'RH recovery success: ${profit:.2f}', 'priority': 1}
        elif profit <= settings.get('max_loss_tolerance', -20.0):
            return {'action': 'close', 'reason': f'RH loss limit: ${profit:.2f}', 'priority': 2}
        elif age_hours >= settings.get('max_age_hours', 12):
            return {'action': 'close', 'reason': f'RH timeout: {age_hours:.1f}h', 'priority': 2}
        else:
            return {'action': 'hold', 'reason': f'RH hunting recovery (${profit:.2f})', 'priority': 5}

    def _get_scalp_capture_action(self, pos_data: Dict, settings: Dict) -> Dict:
        """⚡ Scalp Capture Action Logic"""
        profit = pos_data.get('total_pnl', 0.0)
        age_hours = pos_data.get('age_hours', 0.0)
        
        if profit >= settings.get('min_profit_threshold', 0.5):
            return {'action': 'close', 'reason': f'SC quick profit: ${profit:.2f}', 'priority': 1}
        elif profit <= settings.get('max_loss_tolerance', -5.0):
            return {'action': 'close', 'reason': f'SC quick cut: ${profit:.2f}', 'priority': 1}
        elif age_hours >= settings.get('max_age_hours', 2):
            return {'action': 'close', 'reason': f'SC time up: {age_hours:.1f}h', 'priority': 2}
        else:
            return {'action': 'hold', 'reason': f'SC scalping (${profit:.2f})', 'priority': 5}

    # ==========================================
    # 📊 PORTFOLIO ROLE ANALYTICS
    # ==========================================
    
    def get_portfolio_role_distribution(self, positions: List[Dict]) -> Dict:
        """📊 การกระจาย Role ใน Portfolio"""
        try:
            role_distribution = {"HG": 0, "PW": 0, "RH": 0, "SC": 0, "Unknown": 0}
            role_profits = {"HG": 0.0, "PW": 0.0, "RH": 0.0, "SC": 0.0, "Unknown": 0.0}
            role_volumes = {"HG": 0.0, "PW": 0.0, "RH": 0.0, "SC": 0.0, "Unknown": 0.0}
            
            for pos in positions:
                position_id = pos.get('id', '')
                profit = pos.get('total_pnl', 0.0)
                volume = pos.get('volume', 0.0)
                
                if position_id in self.position_roles:
                    role = self.position_roles[position_id]['role']
                else:
                    role = "Unknown"
                
                role_distribution[role] += 1
                role_profits[role] += profit
                role_volumes[role] += volume
            
            total_positions = len(positions)
            
            return {
                'distribution': role_distribution,
                'percentages': {role: (count/total_positions)*100 if total_positions > 0 else 0 
                              for role, count in role_distribution.items()},
                'profits': role_profits,
                'volumes': role_volumes,
                'total_positions': total_positions,
                'balance_status': self._assess_role_balance(role_distribution, total_positions)
            }
            
        except Exception as e:
            print(f"❌ Portfolio role distribution error: {e}")
            return {}

    def _assess_role_balance(self, distribution: Dict, total: int) -> str:
        """⚖️ ประเมินความสมดุลของ roles"""
        try:
            if total == 0:
                return "empty"
            
            imbalance_score = 0.0
            for role in ["HG", "PW", "RH", "SC"]:
                current_percent = (distribution.get(role, 0) / total) * 100
                target_percent = self.role_quotas.get(role, 25.0)
                deviation = abs(current_percent - target_percent)
                imbalance_score += deviation
            
            if imbalance_score <= 20.0:
                return "balanced"
            elif imbalance_score <= 40.0:
                return "slightly_imbalanced"
            elif imbalance_score <= 60.0:
                return "imbalanced"
            else:
                return "severely_imbalanced"
                
        except Exception as e:
            return "unknown"

    def get_role_performance_summary(self) -> Dict:
        """📈 สรุปผลงานแต่ละ Role"""
        try:
            return {
                'performance_by_role': self.role_performance.copy(),
                'evolution_stats': {
                    'total_evolutions': len(self.role_history),
                    'evolutions_today': len([h for h in self.role_history 
                                           if h['timestamp'].date() == datetime.now().date()]),
                    'most_common_evolution': self._get_most_common_evolution()
                },
                'recommendations': self._generate_role_recommendations()
            }
            
        except Exception as e:
            return {'error': str(e)}

    def _is_high_volatility_time(self) -> bool:
        """⚡ ตรวจสอบว่าเป็นช่วงเวลา high volatility หรือไม่"""
        try:
            now = datetime.now()
            hour = now.hour
            
            # London session (8-12 GMT+7) หรือ NY session (21-01 GMT+7)
            return (8 <= hour <= 12) or (21 <= hour <= 23) or (0 <= hour <= 1)
            
        except Exception as e:
            return False

    def _get_evolution_reason(self, pos_data: Dict, from_role: str, to_role: str) -> str:
        """📝 สร้างเหตุผลการเปลี่ยน role"""
        profit = pos_data.get('total_pnl', 0.0)
        age = pos_data.get('age_hours', 0.0)
        
        return f"${profit:.1f} profit, {age:.1f}h age"

    def _get_evolution_priority(self, from_role: str, to_role: str) -> int:
        """🎯 ความสำคัญของการเปลี่ยน role"""
        priority_matrix = {
            ("HG", "PW"): 3,  # ปกติ
            ("HG", "SC"): 2,  # ค่อนข้างด่วน
            ("PW", "SC"): 2,  # ค่อนข้างด่วน
            ("PW", "HG"): 1,  # ด่วน
            ("RH", "PW"): 2,  # ค่อนข้างด่วน
            ("RH", "SC"): 1,  # ด่วน
        }
        return priority_matrix.get((from_role, to_role), 3)

    def _get_most_common_evolution(self) -> str:
        """📊 Evolution ที่เกิดขึ้นบ่อยที่สุด"""
        try:
            if not self.role_history:
                return "No evolutions yet"
            
            evolutions = [f"{h['from_role']}→{h['to_role']}" for h in self.role_history]
            from collections import Counter
            most_common = Counter(evolutions).most_common(1)
            
            return most_common[0][0] if most_common else "No pattern"
            
        except Exception as e:
            return "Error calculating"

    def _generate_role_recommendations(self) -> List[str]:
        """💡 สร้างคำแนะนำเกี่ยวกับ roles"""
        recommendations = []
        
        try:
            # Role balance recommendations
            if hasattr(self, 'last_distribution'):
                balance = self.last_distribution.get('balance_status', '')
                if balance == "severely_imbalanced":
                    recommendations.append("🚨 Portfolio roles ไม่สมดุลมาก - ควรปรับสัดส่วน")
                elif balance == "imbalanced":
                    recommendations.append("⚠️ Portfolio roles ไม่สมดุล - พิจารณาปรับ")
            
            # Performance recommendations
            for role, perf in self.role_performance.items():
                if perf['count'] > 10 and perf['success_rate'] < 0.4:
                    recommendations.append(f"📉 Role {role} performance ต่ำ - ปรับกลยุทธ์")
            
            return recommendations
            
        except Exception as e:
            return [f"❌ Recommendation error: {e}"]

    def cleanup_closed_positions(self, active_position_ids: List[str]):
        """🧹 ล้างข้อมูล positions ที่ปิดแล้ว"""
        try:
            closed_positions = [pid for pid in self.position_roles.keys() 
                              if pid not in active_position_ids]
            
            for pid in closed_positions:
                if pid in self.position_roles:
                    del self.position_roles[pid]
            
            if closed_positions:
                print(f"🧹 Cleaned up {len(closed_positions)} closed position roles")
                
        except Exception as e:
            print(f"❌ Position cleanup error: {e}")

# ==========================================
# 🔧 HELPER FUNCTIONS
# ==========================================

def create_order_role_manager(config: Dict) -> OrderRoleManager:
    """
    🏭 Factory function สำหรับสร้าง OrderRoleManager
    
    Args:
        config: การตั้งค่าระบบ
        
    Returns:
        OrderRoleManager: configured instance
    """
    try:
        role_manager = OrderRoleManager(config)
        print("🏭 Order Role Manager created successfully")
        return role_manager
        
    except Exception as e:
        print(f"❌ Order Role Manager creation error: {e}")
        return None