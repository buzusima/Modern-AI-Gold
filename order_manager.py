"""
⚡ Central Order Management System v4.0 - CAPITAL + ROLE INTELLIGENCE
order_manager.py

🚀 NEW FEATURES v4.0:
✅ Capital-aware Order Execution (check zones before execution)
✅ Role-based Order Management (HG/PW/RH/SC integration)
✅ Smart Order Flow (signal → validation → execution → monitoring)
✅ Advanced Order Coordination (prevent conflicts + optimize timing)
✅ Intelligent Position Sizing (capital + role + signal strength)
✅ Complete Integration Hub (connects all trading components)

🎯 Central Command Center สำหรับการจัดการออเดอร์ทั้งหมด
ประสานงานระหว่าง signal_generator, lot_calculator, order_executor, etc.
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import time
import json
from enum import Enum
import statistics

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
        
        # Role quotas (เป้าหมายสัดส่วน)
        self.role_quotas = self.role_config.get("role_quotas", {
            "HG": 25.0,  # Hedge Guard 25%
            "PW": 40.0,  # Profit Walker 40% 
            "RH": 20.0,  # Recovery Hunter 20%
            "SC": 15.0   # Scalp Capture 15%
        })
        
        # Role settings (การตั้งค่าสำหรับแต่ละ role)
        self.role_settings = self.role_config.get("role_settings", {
            "HG": {
                "max_age_hours": 48,        # hedge ยาวได้ 48 ชั่วโมง
                "min_profit_threshold": 4.0, # ปิดเมื่อกำไร $4+
                "max_loss_tolerance": -60.0, # ทนขาดทุนได้ $60
                "defensive": True,          # เน้นการป้องกัน
                "preferred_lot_range": (0.01, 0.05)
            },
            "PW": {
                "max_age_hours": 24,        # profit walker 24 ชั่วโมง
                "min_profit_threshold": 2.5, # ปิดเมื่อกำไร $2.5+
                "max_loss_tolerance": -35.0, # ทนขาดทุนได้ $35
                "profit_trailing": True,    # เดินตามกำไร
                "preferred_lot_range": (0.01, 0.10)
            },
            "RH": {
                "max_age_hours": 12,        # recovery 12 ชั่วโมง
                "min_profit_threshold": 1.0, # ปิดเมื่อกำไร $1+
                "max_loss_tolerance": -25.0, # ทนขาดทุนได้ $25
                "recovery_focused": True,   # เน้นการกู้คืน
                "preferred_lot_range": (0.01, 0.08)
            },
            "SC": {
                "max_age_hours": 2,         # scalp เร็ว 2 ชั่วโมง
                "min_profit_threshold": 0.5, # ปิดเมื่อกำไร $0.5+
                "max_loss_tolerance": -8.0,  # ทนขาดทุนได้ $8
                "quick_profit": True,       # เก็บกำไรเร็ว
                "preferred_lot_range": (0.01, 0.15)
            }
        })
        
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
            str: Role ที่กำหนดให้ (HG/PW/RH/SC)
        """
        try:
            if not self.auto_assignment:
                return "PW"  # Default เป็น Profit Walker
            
            # ประเมินสถานการณ์ portfolio
            drawdown_percent = portfolio_context.get('drawdown_percent', 0)
            trading_mode = portfolio_context.get('trading_mode', 'normal')
            current_positions = portfolio_context.get('current_positions', 0)
            signal_strength = portfolio_context.get('signal_strength', 0.5)
            
            # คำนวณ role distribution ปัจจุบัน
            current_distribution = self._calculate_current_distribution()
            
            # กฎการกำหนด role
            assigned_role = self._determine_optimal_role(
                position_info, portfolio_context, current_distribution
            )
            
            print(f"🎯 Role assigned: {assigned_role} (Signal: {signal_strength:.2f}, Drawdown: {drawdown_percent:.1f}%)")
            
            return assigned_role
            
        except Exception as e:
            print(f"❌ Role assignment error: {e}")
            return "PW"  # Default fallback
    
    def _determine_optimal_role(self, position_info: Dict, portfolio_context: Dict, current_distribution: Dict) -> str:
        """🧠 กำหนด Role ที่เหมาะสม"""
        try:
            drawdown_percent = portfolio_context.get('drawdown_percent', 0)
            trading_mode = portfolio_context.get('trading_mode', 'normal')
            signal_strength = portfolio_context.get('signal_strength', 0.5)
            
            # Emergency mode → เน้น Hedge Guard
            if trading_mode == 'emergency':
                if current_distribution.get('HG', 0) < self.role_quotas['HG']:
                    return "HG"
            
            # Recovery mode → เน้น Recovery Hunter
            if trading_mode == 'recovery':
                if current_distribution.get('RH', 0) < self.role_quotas['RH']:
                    return "RH"
            
            # High drawdown → เพิ่ม Hedge Guard
            if drawdown_percent > 15.0:
                if current_distribution.get('HG', 0) < self.role_quotas['HG']:
                    return "HG"
            
            # Strong signal → Profit Walker หรือ Scalp
            if signal_strength >= 0.75:
                if current_distribution.get('PW', 0) < self.role_quotas['PW']:
                    return "PW"
                elif current_distribution.get('SC', 0) < self.role_quotas['SC']:
                    return "SC"
            
            # Medium signal → Recovery Hunter หรือ Profit Walker
            if signal_strength >= 0.5:
                if current_distribution.get('RH', 0) < self.role_quotas['RH']:
                    return "RH"
                elif current_distribution.get('PW', 0) < self.role_quotas['PW']:
                    return "PW"
            
            # Default: ใช้ role ที่ขาดที่สุด
            return self._get_most_needed_role(current_distribution)
            
        except Exception as e:
            print(f"❌ Role determination error: {e}")
            return "PW"
    
    def _calculate_current_distribution(self) -> Dict:
        """📊 คำนวณการกระจาย role ปัจจุบัน"""
        try:
            if not self.position_roles:
                return {"HG": 0, "PW": 0, "RH": 0, "SC": 0}
            
            total_positions = len(self.position_roles)
            role_counts = {"HG": 0, "PW": 0, "RH": 0, "SC": 0}
            
            for position_data in self.position_roles.values():
                role = position_data.get('role', 'PW')
                if role in role_counts:
                    role_counts[role] += 1
            
            # แปลงเป็นเปอร์เซ็นต์
            role_percentages = {}
            for role, count in role_counts.items():
                role_percentages[role] = (count / total_positions * 100) if total_positions > 0 else 0
            
            return role_percentages
            
        except Exception as e:
            print(f"❌ Distribution calculation error: {e}")
            return {"HG": 0, "PW": 0, "RH": 0, "SC": 0}
    
    def _get_most_needed_role(self, current_distribution: Dict) -> str:
        """🎯 หา Role ที่ต้องการมากที่สุด"""
        try:
            max_deficit = 0
            most_needed_role = "PW"
            
            for role, quota in self.role_quotas.items():
                current_percent = current_distribution.get(role, 0)
                deficit = quota - current_percent
                
                if deficit > max_deficit:
                    max_deficit = deficit
                    most_needed_role = role
            
            return most_needed_role
            
        except Exception as e:
            print(f"❌ Most needed role calculation error: {e}")
            return "PW"

    # ==========================================
    # 📊 PORTFOLIO ANALYSIS
    # ==========================================
    
    def get_portfolio_role_distribution(self) -> Dict:
        """📊 ดู Role Distribution ของ Portfolio"""
        try:
            current_distribution = self._calculate_current_distribution()
            total_positions = len(self.position_roles)
            
            # สร้างรายงาน
            distribution_report = {
                'roles': {},
                'balance_status': 'balanced',
                'imbalances': [],
                'recommendations': [],
                'total_positions': total_positions,
                'timestamp': datetime.now()
            }
            
            # วิเคราะห์แต่ละ role
            for role in ["HG", "PW", "RH", "SC"]:
                current_percent = current_distribution.get(role, 0)
                target_percent = self.role_quotas.get(role, 0)
                difference = current_percent - target_percent
                
                distribution_report['roles'][role] = {
                    'count': sum(1 for p in self.position_roles.values() if p.get('role') == role),
                    'percentage': current_percent,
                    'target_percentage': target_percent,
                    'difference': difference,
                    'status': 'balanced' if abs(difference) <= 10 else ('over' if difference > 0 else 'under')
                }
                
                # เพิ่มข้อมูลความไม่สมดุล
                if abs(difference) > 15:
                    imbalance_msg = f"Role {role}: {current_percent:.1f}% (Target: {target_percent:.1f}%)"
                    distribution_report['imbalances'].append(imbalance_msg)
            
            # ประเมินสถานะความสมดุล
            major_imbalances = len([r for r in distribution_report['roles'].values() 
                                  if abs(r['difference']) > 15])
            
            if major_imbalances >= 2:
                distribution_report['balance_status'] = 'severely_imbalanced'
            elif major_imbalances == 1:
                distribution_report['balance_status'] = 'imbalanced'
            else:
                distribution_report['balance_status'] = 'balanced'
            
            return distribution_report
            
        except Exception as e:
            print(f"❌ Portfolio role distribution error: {e}")
            return {'error': str(e)}
    
    def track_new_position(self, position_id: str, role_data: Dict):
        """📝 ติดตาม Position ใหม่"""
        try:
            self.position_roles[position_id] = {
                'role': role_data.get('role', 'PW'),
                'assigned_time': datetime.now(),
                'assignment_reason': role_data.get('assignment_reason', ''),
                'portfolio_context': role_data.get('portfolio_context', {}),
                'performance_metrics': {
                    'profit_history': [],
                    'role_changes': [],
                    'close_reason': None
                }
            }
            
            print(f"📝 Position {position_id} registered as {role_data.get('role', 'PW')}")
            
        except Exception as e:
            print(f"❌ Position registration error: {e}")

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


class OrderManager:
    """
    ⚡ Central Order Management System v4.0
    
    🎯 Central Hub สำหรับการจัดการออเดอร์ทั้งหมด:
    - Capital Zone Validation
    - Role Assignment & Management  
    - Smart Order Execution
    - Position Coordination
    - Risk Integration
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """
        🔧 เริ่มต้น Central Order Manager v4.0
        
        Args:
            mt5_connector: MT5 connection object
            config: การตั้งค่าระบบ
        """
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Component references (will be set by integration)
        self.capital_manager = None
        self.role_manager = None
        self.lot_calculator = None
        self.order_executor = None
        self.risk_manager = None
        self.signal_generator = None
        
        # Order management configuration
        self.trading_config = config.get("trading", {})
        self.symbol = self.trading_config.get("symbol", "XAUUSD.v")
        self.max_positions = self.trading_config.get("max_positions", 60)
        
        # Order coordination
        self.pending_orders = {}  # {signal_id: order_info}
        self.execution_queue = []  # FIFO queue for orders
        self.order_history = []   # ประวัติการส่งออเดอร์
        
        # Performance tracking
        self.execution_stats = {
            'total_orders': 0,
            'successful_orders': 0,
            'failed_orders': 0,
            'blocked_orders': 0,
            'avg_execution_time_ms': 0.0,
            'last_execution_time': datetime.min
        }
        
        # Smart coordination features
        self.order_spacing_seconds = 15  # ห่างระหว่างออเดอร์
        self.batch_execution_enabled = True
        self.smart_timing_enabled = True
        
        print(f"⚡ Central Order Manager v4.0 initialized")
        print(f"   Symbol: {self.symbol}")
        print(f"   Max positions: {self.max_positions}")
        print(f"   Order spacing: {self.order_spacing_seconds}s")

    # ==========================================
    # 🔗 COMPONENT INTEGRATION
    # ==========================================
    
    def set_capital_manager(self, capital_manager):
        """💰 เชื่อมต่อ Capital Manager"""
        self.capital_manager = capital_manager
        print("💰 Capital Manager integrated with Order Manager")
    
    def set_role_manager(self, role_manager):
        """🎭 เชื่อมต่อ Role Manager"""
        self.role_manager = role_manager
        print("🎭 Role Manager integrated with Order Manager")
    
    def set_lot_calculator(self, lot_calculator):
        """📏 เชื่อมต่อ Lot Calculator"""
        self.lot_calculator = lot_calculator
        print("📏 Lot Calculator integrated with Order Manager")
        
    def set_order_executor(self, order_executor):
        """⚡ เชื่อมต่อ Order Executor"""
        self.order_executor = order_executor
        print("⚡ Order Executor integrated with Order Manager")
        
    def set_risk_manager(self, risk_manager):
        """🛡️ เชื่อมต่อ Risk Manager"""
        self.risk_manager = risk_manager
        print("🛡️ Risk Manager integrated with Order Manager")
        
    def set_signal_generator(self, signal_generator):
        """📊 เชื่อมต่อ Signal Generator"""
        self.signal_generator = signal_generator
        print("📊 Signal Generator integrated with Order Manager")

    def get_integration_status(self) -> Dict:
        """🔗 ตรวจสอบสถานะการเชื่อมต่อทุก components"""
        return {
            'capital_manager': '✅' if self.capital_manager else '❌',
            'role_manager': '✅' if self.role_manager else '❌',
            'lot_calculator': '✅' if self.lot_calculator else '❌',
            'order_executor': '✅' if self.order_executor else '❌',
            'risk_manager': '✅' if self.risk_manager else '❌',
            'signal_generator': '✅' if self.signal_generator else '❌',
            'mt5_connector': '✅' if self.mt5_connector and self.mt5_connector.is_connected else '❌',
            'system_ready': self._is_system_ready()
        }

    def _is_system_ready(self) -> bool:
        """✅ ตรวจสอบว่าระบบพร้อมเทรดหรือไม่"""
        required_components = [
            self.mt5_connector,
            self.order_executor,
            self.lot_calculator
        ]
        
        return all(comp is not None for comp in required_components) and \
               self.mt5_connector.is_connected

    # ==========================================
    # 🎯 MAIN ORDER PROCESSING
    # ==========================================
    
    def process_trading_signal(self, signal_data: Dict) -> Optional[Dict]:
        """
        🎯 ประมวลผล Trading Signal แบบ Complete Flow
        
        ขั้นตอน: Signal → Validation → Role Assignment → Execution → Monitoring
        
        Args:
            signal_data: ข้อมูล signal จาก SignalGenerator
            
        Returns:
            Dict: ผลการประมวลผล + execution result
        """
        try:
            signal_id = signal_data.get('signal_id', f"sig_{int(time.time())}")
            action = signal_data.get('action', 'WAIT')
            
            print(f"🎯 Processing signal {signal_id}: {action}")
            
            # ขั้นตอนที่ 1: ตรวจสอบระบบ
            if not self._is_system_ready():
                return {
                    'success': False,
                    'signal_id': signal_id,
                    'stage': 'system_check',
                    'error': 'System components not ready',
                    'integration_status': self.get_integration_status()
                }
            
            # ขั้นตอนที่ 2: ตรวจสอบ signal validity
            if action not in ['BUY', 'SELL']:
                print(f"ℹ️ Signal {signal_id}: No execution needed for {action}")
                return {
                    'success': True,
                    'signal_id': signal_id,
                    'stage': 'validation',
                    'action_taken': 'none',
                    'reason': f'Non-executable action: {action}'
                }
            
            # ขั้นตอนที่ 3: Capital Zone Validation
            capital_status = self._validate_capital_zone()
            if not capital_status['can_trade']:
                print(f"🚫 Signal {signal_id} blocked: {capital_status['reason']}")
                self.execution_stats['blocked_orders'] += 1
                return {
                    'success': False,
                    'signal_id': signal_id,
                    'stage': 'capital_validation',
                    'blocked': True,
                    'reason': capital_status['reason'],
                    'capital_info': capital_status
                }
            
            # ขั้นตอนที่ 4: Risk Management Validation
            risk_approval = self._validate_risk_constraints(signal_data, capital_status)
            if not risk_approval['approved']:
                print(f"🛡️ Signal {signal_id} blocked by risk management")
                self.execution_stats['blocked_orders'] += 1
                return {
                    'success': False,
                    'signal_id': signal_id,
                    'stage': 'risk_validation',
                    'blocked': True,
                    'reason': 'Risk management rejection',
                    'risk_info': risk_approval
                }
            
            # ขั้นตอนที่ 5: Smart Order Spacing
            spacing_check = self._check_order_spacing()
            if not spacing_check['can_execute']:
                print(f"⏰ Signal {signal_id} delayed for spacing: {spacing_check['wait_seconds']}s")
                # อาจจะเพิ่มเข้า queue แทนการ block
                return {
                    'success': False,
                    'signal_id': signal_id,
                    'stage': 'timing_validation',
                    'delayed': True,
                    'wait_seconds': spacing_check['wait_seconds']
                }
            
            # ขั้นตอนที่ 6: Calculate Optimal Lot Size
            lot_info = self._calculate_optimal_lot_size(signal_data, capital_status, risk_approval)
            if lot_info['lot_size'] <= 0:
                print(f"📏 Signal {signal_id} blocked: Invalid lot size")
                return {
                    'success': False,
                    'signal_id': signal_id,
                    'stage': 'lot_calculation',
                    'error': 'Invalid lot size calculated',
                    'lot_info': lot_info
                }
            
            # ขั้นตอนที่ 7: Role Assignment (if role manager available)
            role_info = self._assign_order_role(signal_data, capital_status, lot_info)
            
            # ขั้นตอนที่ 8: Execute Order
            execution_data = {
                **signal_data,
                'lot_size': lot_info['lot_size'],
                'capital_zone': capital_status['current_zone'],
                'assigned_role': role_info['role'],
                'risk_level': risk_approval['risk_level']
            }
            
            execution_result = self._execute_order(execution_data)
            
            # ขั้นตอนที่ 9: Post-execution Processing
            if execution_result and execution_result.get('success'):
                self._handle_successful_execution(signal_id, execution_data, execution_result, role_info)
                
                return {
                    'success': True,
                    'signal_id': signal_id,
                    'stage': 'completed',
                    'execution_result': execution_result,
                    'order_details': {
                        'action': action,
                        'lot_size': lot_info['lot_size'],
                        'role': role_info['role'],
                        'capital_zone': capital_status['current_zone'],
                        'execution_price': execution_result.get('execution_price'),
                        'order_id': execution_result.get('order_id')
                    }
                }
            else:
                self._handle_failed_execution(signal_id, execution_data, execution_result)
                
                return {
                    'success': False,
                    'signal_id': signal_id,
                    'stage': 'execution',
                    'error': 'Order execution failed',
                    'execution_result': execution_result
                }
                
        except Exception as e:
            print(f"❌ Signal processing error: {e}")
            return {
                'success': False,
                'signal_id': signal_data.get('signal_id', 'unknown'),
                'stage': 'exception',
                'error': str(e)
            }

    # ==========================================
    # 🔍 VALIDATION METHODS
    # ==========================================
    
    def _validate_capital_zone(self) -> Dict:
        """💰 ตรวจสอบ Capital Zone + สถานะการเทรด"""
        try:
            if not self.capital_manager:
                return {
                    'can_trade': True,
                    'current_zone': 'unknown',
                    'reason': 'No capital manager - using defaults'
                }
            
            capital_status = self.capital_manager.get_capital_status()
            trading_mode = capital_status.get('trading_mode', 'normal')
            
            # ตรวจสอบสถานะ emergency
            if trading_mode == 'emergency':
                return {
                    'can_trade': False,
                    'current_zone': capital_status.get('current_zone', 'unknown'),
                    'reason': 'Emergency trading mode active',
                    'drawdown_percent': capital_status.get('drawdown_percent', 0)
                }
            
            # ตรวจสอบ zone availability
            current_zone = capital_status.get('current_zone', 'safe')
            zone_available = capital_status.get('zones', {}).get(current_zone, {}).get('remaining_capital', 0) > 0
            
            if not zone_available:
                return {
                    'can_trade': False,
                    'current_zone': current_zone,
                    'reason': f'No remaining capital in {current_zone} zone'
                }
            
            return {
                'can_trade': True,
                'current_zone': current_zone,
                'trading_mode': trading_mode,
                'available_capital': capital_status.get('zones', {}).get(current_zone, {}).get('remaining_capital', 0),
                'reason': 'Capital validation passed'
            }
            
        except Exception as e:
            print(f"❌ Capital zone validation error: {e}")
            return {
                'can_trade': True,  # Fail-safe: allow trading
                'current_zone': 'unknown',
                'reason': f'Validation error: {e}'
            }
    
    def _validate_risk_constraints(self, signal_data: Dict, capital_status: Dict) -> Dict:
        """🛡️ ตรวจสอบข้อจำกัดความเสี่ยง"""
        try:
            if not self.risk_manager:
                return {
                    'approved': True,
                    'risk_level': 'unknown',
                    'reason': 'No risk manager - using defaults'
                }
            
            # ใช้ enhanced trade validation
            action = signal_data.get('action', 'BUY').lower()
            suggested_lot = signal_data.get('suggested_lot_size', 0.01)
            
            validation = self.risk_manager.validate_new_trade(
                order_type=action,
                volume=suggested_lot,
                role=None  # จะกำหนดทีหลัง
            )
            
            return {
                'approved': validation.get('approved', False),
                'risk_level': validation.get('risk_level', 'medium'),
                'recommended_volume': validation.get('recommended_volume', suggested_lot),
                'confidence_score': validation.get('confidence_score', 0.5),
                'adjustments': validation.get('adjustments', []),
                'reason': 'Risk manager validation'
            }
            
        except Exception as e:
            print(f"❌ Risk validation error: {e}")
            return {
                'approved': True,  # Fail-safe
                'risk_level': 'unknown',
                'reason': f'Validation error: {e}'
            }
    
    def _check_order_spacing(self) -> Dict:
        """⏰ ตรวจสอบระยะห่างระหว่างออเดอร์"""
        try:
            if not self.smart_timing_enabled:
                return {'can_execute': True, 'wait_seconds': 0}
            
            current_time = datetime.now()
            time_since_last = (current_time - self.execution_stats['last_execution_time']).total_seconds()
            
            if time_since_last >= self.order_spacing_seconds:
                return {'can_execute': True, 'wait_seconds': 0}
            else:
                wait_seconds = self.order_spacing_seconds - time_since_last
                return {'can_execute': False, 'wait_seconds': int(wait_seconds)}
                
        except Exception as e:
            return {'can_execute': True, 'wait_seconds': 0}  # Fail-safe

    # ==========================================
    # 📏 LOT CALCULATION & ROLE ASSIGNMENT
    # ==========================================
    
    def _calculate_optimal_lot_size(self, signal_data: Dict, capital_status: Dict, risk_approval: Dict) -> Dict:
        """📏 คำนวณ Lot Size ที่เหมาะสม"""
        try:
            if not self.lot_calculator:
                base_lot = 0.01
                return {
                    'lot_size': base_lot,
                    'method': 'fallback',
                    'reason': 'No lot calculator available'
                }
            
            # เตรียมข้อมูลสำหรับ lot calculation
            enhanced_signal_data = {
                **signal_data,
                'capital_zone': capital_status.get('current_zone', 'safe'),
                'trading_mode': capital_status.get('trading_mode', 'normal'),
                'risk_level': risk_approval.get('risk_level', 'medium'),
                'recommended_volume': risk_approval.get('recommended_volume')
            }
            
            # คำนวณ lot size
            calculated_lot = self.lot_calculator.calculate_lot_size(enhanced_signal_data)
            
            # ใช้ recommended volume จาก risk manager ถ้ามี
            if risk_approval.get('recommended_volume'):
                final_lot = min(calculated_lot, risk_approval['recommended_volume'])
            else:
                final_lot = calculated_lot
            
            return {
                'lot_size': final_lot,
                'calculated_lot': calculated_lot,
                'risk_adjusted_lot': risk_approval.get('recommended_volume'),
                'method': 'integrated_calculation',
                'capital_zone': capital_status.get('current_zone'),
                'reason': 'Calculated using capital + risk integration'
            }
            
        except Exception as e:
            print(f"❌ Lot calculation error: {e}")
            return {
                'lot_size': 0.01,  # Fallback
                'method': 'error_fallback',
                'reason': f'Calculation error: {e}'
            }
    
    def _assign_order_role(self, signal_data: Dict, capital_status: Dict, lot_info: Dict) -> Dict:
        """🎭 กำหนด Role ให้ออเดอร์"""
        try:
            if not self.role_manager:
                return {
                    'role': 'PW',  # Default role
                    'method': 'fallback',
                    'reason': 'No role manager available'
                }
            
            # เตรียมข้อมูล portfolio context
            portfolio_context = {
                'capital_zone': capital_status.get('current_zone', 'safe'),
                'trading_mode': capital_status.get('trading_mode', 'normal'),
                'drawdown_percent': capital_status.get('drawdown_percent', 0),
                'current_positions': len(self._get_current_positions()),
                'signal_strength': signal_data.get('strength', 0.5)
            }
            
            # เตรียมข้อมูล position info
            position_info = {
                'type': signal_data.get('action', 'BUY').lower(),
                'volume': lot_info['lot_size'],
                'entry_price': signal_data.get('current_price', 0),
                'signal_id': signal_data.get('signal_id')
            }
            
            # กำหนด role
            assigned_role = self.role_manager.assign_role_to_new_position(
                position_info, 
                portfolio_context
            )
            
            return {
                'role': assigned_role,
                'method': 'intelligent_assignment',
                'portfolio_context': portfolio_context,
                'reason': f'Assigned by role manager based on portfolio state'
            }
            
        except Exception as e:
            print(f"❌ Role assignment error: {e}")
            return {
                'role': 'PW',  # Fallback
                'method': 'error_fallback',
                'reason': f'Assignment error: {e}'
            }

    # ==========================================
    # ⚡ ORDER EXECUTION
    # ==========================================
    
    def _execute_order(self, execution_data: Dict) -> Optional[Dict]:
        """⚡ ส่งออเดอร์จริง"""
        try:
            if not self.order_executor:
                print(f"❌ No order executor available")
                return None
            
            print(f"⚡ Executing {execution_data.get('action')} order...")
            print(f"   Lot: {execution_data.get('lot_size')}")
            print(f"   Role: {execution_data.get('assigned_role')}")
            print(f"   Zone: {execution_data.get('capital_zone')}")
            
            # บันทึกเวลาก่อนส่ง
            execution_start = time.time()
            
            # ส่งออเดอร์ผ่าน order executor
            result = self.order_executor.execute_signal(execution_data)
            
            # คำนวณเวลาการส่ง
            execution_time = time.time() - execution_start
            
            # อัพเดท statistics
            self.execution_stats['total_orders'] += 1
            self.execution_stats['last_execution_time'] = datetime.now()
            
            # อัพเดท average execution time
            current_avg = self.execution_stats['avg_execution_time_ms']
            total_orders = self.execution_stats['total_orders']
            new_time_ms = execution_time * 1000
            
            self.execution_stats['avg_execution_time_ms'] = (
                (current_avg * (total_orders - 1) + new_time_ms) / total_orders
            )
            
            if result and result.get('success'):
                self.execution_stats['successful_orders'] += 1
                print(f"✅ Order executed successfully in {new_time_ms:.1f}ms")
            else:
                self.execution_stats['failed_orders'] += 1
                print(f"❌ Order execution failed")
            
            return result
            
        except Exception as e:
            print(f"❌ Order execution error: {e}")
            self.execution_stats['failed_orders'] += 1
            return None

    # ==========================================
    # 📋 POST-EXECUTION PROCESSING
    # ==========================================
    
    def _handle_successful_execution(self, signal_id: str, execution_data: Dict, execution_result: Dict, role_info: Dict):
        """✅ จัดการหลังส่งออเดอร์สำเร็จ"""
        try:
            order_id = execution_result.get('order_id')
            
            # บันทึกประวัติ
            order_record = {
                'timestamp': datetime.now(),
                'signal_id': signal_id,
                'order_id': order_id,
                'action': execution_data.get('action'),
                'lot_size': execution_data.get('lot_size'),
                'execution_price': execution_result.get('execution_price'),
                'role': role_info.get('role'),
                'capital_zone': execution_data.get('capital_zone'),
                'status': 'executed'
            }
            
            self.order_history.append(order_record)
            
            # อัพเดท role manager ถ้ามี
            if self.role_manager and order_id:
                role_data = {
                    'role': role_info.get('role'),
                    'assignment_reason': role_info.get('reason', ''),
                    'portfolio_context': role_info.get('portfolio_context', {}),
                    'order_details': order_record
                }
                
                self.role_manager.track_new_position(str(order_id), role_data)
            
            # อัพเดท capital manager ถ้ามี
            if self.capital_manager:
                used_capital = execution_data.get('lot_size', 0) * 100  # ประมาณการ margin used
                self.capital_manager.allocate_capital(
                    execution_data.get('capital_zone', 'safe'),
                    used_capital
                )
            
            print(f"✅ Post-execution processing completed for order {order_id}")
            
        except Exception as e:
            print(f"❌ Post-execution processing error: {e}")
    
    def _handle_failed_execution(self, signal_id: str, execution_data: Dict, execution_result: Dict):
        """❌ จัดการหลังส่งออเดอร์ไม่สำเร็จ"""
        try:
            # บันทึกประวัติความล้มเหลว
            failure_record = {
                'timestamp': datetime.now(),
                'signal_id': signal_id,
                'action': execution_data.get('action'),
                'lot_size': execution_data.get('lot_size'),
                'role': execution_data.get('assigned_role'),
                'error': execution_result.get('error', 'Unknown error') if execution_result else 'No execution result',
                'status': 'failed'
            }
            
            self.order_history.append(failure_record)
            
            print(f"❌ Failed execution recorded for signal {signal_id}")
            
        except Exception as e:
            print(f"❌ Failed execution processing error: {e}")

    # ==========================================
    # 📊 MONITORING & UTILITIES
    # ==========================================
    
    def _get_current_positions(self) -> List[Dict]:
        """📋 ดึงรายการ positions ปัจจุบัน"""
        try:
            if not self.mt5_connector or not self.mt5_connector.is_connected:
                return []
            
            positions = mt5.positions_get(symbol=self.symbol)
            if positions is None:
                return []
            
            return [{'ticket': pos.ticket, 'type': pos.type, 'volume': pos.volume, 
                    'profit': pos.profit} for pos in positions]
            
        except Exception as e:
            print(f"❌ Get positions error: {e}")
            return []
    
    def get_order_manager_status(self) -> Dict:
        """📊 สถานะ Order Manager"""
        try:
            current_positions = self._get_current_positions()
            
            return {
                'system_ready': self._is_system_ready(),
                'integration_status': self.get_integration_status(),
                'current_positions': len(current_positions),
                'max_positions': self.max_positions,
                'positions_available': self.max_positions - len(current_positions),
                'execution_stats': self.execution_stats,
                'order_history_count': len(self.order_history),
                'pending_orders': len(self.pending_orders),
                'last_update': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e), 'system_ready': False}
    
    def get_recent_order_history(self, limit: int = 10) -> List[Dict]:
        """📜 ประวัติออเดอร์ล่าสุด"""
        try:
            sorted_history = sorted(
                self.order_history, 
                key=lambda x: x.get('timestamp', datetime.min), 
                reverse=True
            )
            
            return sorted_history[:limit]
            
        except Exception as e:
            print(f"❌ Get order history error: {e}")
            return []
    
    def cleanup_old_history(self, max_age_hours: int = 24):
        """🧹 ล้างประวัติเก่า"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            self.order_history = [
                order for order in self.order_history
                if order.get('timestamp', datetime.now()) > cutoff_time
            ]
            
            print(f"🧹 Cleaned order history older than {max_age_hours} hours")
            
        except Exception as e:
            print(f"❌ History cleanup error: {e}")


# ==========================================
# 🔧 FACTORY & INTEGRATION FUNCTIONS
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
        # ตรวจสอบ config
        if not config:
            print("❌ No configuration provided for OrderRoleManager")
            return None
            
        # สร้าง OrderRoleManager
        print("🏭 Creating Order Role Manager...")
        role_manager = OrderRoleManager(config)
        
        # ตรวจสอบว่าสร้างสำเร็จ
        if role_manager:
            print("✅ Order Role Manager created successfully")
            print(f"   Auto assignment: {role_manager.auto_assignment}")
            print(f"   Role evolution: {role_manager.role_evolution}")
            print(f"   Portfolio balancing: {role_manager.portfolio_balancing}")
            return role_manager
        else:
            print("❌ Failed to create OrderRoleManager")
            return None
        
    except Exception as e:
        print(f"❌ Order Role Manager creation error: {e}")
        return None

def create_order_manager(mt5_connector, config: Dict) -> 'OrderManager':
    """
    🏭 Factory function สำหรับสร้าง OrderManager (Central)
    
    Args:
        mt5_connector: MT5 connector instance
        config: การตั้งค่าระบบ
        
    Returns:
        OrderManager: configured instance
    """
    try:
        # ตรวจสอบ parameters
        if not mt5_connector:
            print("❌ No MT5 connector provided for OrderManager")
            return None
            
        if not config:
            print("❌ No configuration provided for OrderManager")
            return None
            
        # สร้าง OrderManager
        print("🏭 Creating Central Order Manager...")
        order_manager = OrderManager(mt5_connector, config)
        
        # ตรวจสอบว่าสร้างสำเร็จ
        if order_manager:
            print("✅ Central Order Manager created successfully")
            
            # แสดงข้อมูลการตั้งค่า
            symbol = config.get("trading", {}).get("symbol", "XAUUSD.v")
            max_positions = config.get("trading", {}).get("max_positions", 60)
            
            print(f"   Symbol: {symbol}")
            print(f"   Max positions: {max_positions}")
            print(f"   Smart timing: enabled")
            print(f"   Batch execution: enabled")
            
            return order_manager
        else:
            print("❌ Failed to create OrderManager")
            return None
        
    except Exception as e:
        print(f"❌ Order Manager creation error: {e}")
        return None
    
# เพิ่มฟังก์ชัน factory อื่นๆ ด้วยถ้าต้องการ
def integrate_order_manager_with_system(order_manager, components: Dict):
    """
    🔗 ผูก Order Manager เข้ากับระบบทั้งหมด
    
    Args:
        order_manager: OrderManager instance
        components: dictionary ของ components ต่างๆ
    """
    try:
        print("🔗 Integrating Order Manager with system components...")
        
        # เชื่อมต่อ components ทีละตัว
        if components.get('capital_manager'):
            order_manager.set_capital_manager(components['capital_manager'])
            
        if components.get('role_manager'):
            order_manager.set_role_manager(components['role_manager'])
            
        if components.get('lot_calculator'):
            order_manager.set_lot_calculator(components['lot_calculator'])
            
        if components.get('order_executor'):
            order_manager.set_order_executor(components['order_executor'])
            
        if components.get('risk_manager'):
            order_manager.set_risk_manager(components['risk_manager'])
            
        if components.get('signal_generator'):
            order_manager.set_signal_generator(components['signal_generator'])
        
        print("✅ Order Manager integration completed")
        return order_manager.get_integration_status()
        
    except Exception as e:
        print(f"❌ Order Manager integration error: {e}")
        return None

# ==========================================
# 🧪 TESTING FUNCTIONS
# ==========================================

# def test_order_manager():
#     """🧪 ทดสอบ Order Manager v4.0"""
#     print("\n🧪 Testing Central Order Manager v4.0...")
    
#     # Mock configuration
#     test_config = {
#         "trading": {
#             "symbol": "XAUUSD.v",
#             "max_positions": 60
#         },
#         "capital_management": {
#             "initial_capital": 7500.0
#         },
#         "order_roles": {
#             "auto_assignment": True
#         }
#     }
    
#     # Mock connector
#     class MockConnector:
#         def __init__(self):
#             self.is_connected = True
    
#     # สร้าง Order Manager
#     mock_connector = MockConnector()
#     order_manager = create_order_role_manager(mock_connector, test_config)
    
#     # ทดสอบ integration status
#     print("\n1️⃣ Integration Status:")
#     status = order_manager.get_integration_status()
#     for component, status_icon in status.items():
#         print(f"   {component}: {status_icon}")
    
#     # ทดสอบ system readiness
#     print(f"\n2️⃣ System Ready: {'✅' if order_manager._is_system_ready() else '❌'}")
    
#     # ทดสอบ mock signal processing
#     print(f"\n3️⃣ Mock Signal Processing:")
#     mock_signal = {
#         'signal_id': 'test_001',
#         'action': 'BUY',
#         'strength': 0.65,
#         'current_price': 2650.50,
#         'suggested_lot_size': 0.02
#     }
    
#     result = order_manager.process_trading_signal(mock_signal)
#     print(f"   Result: {result.get('success')}")
#     print(f"   Stage: {result.get('stage')}")
#     print(f"   Reason: {result.get('reason', result.get('error', 'N/A'))}")
    
#     print("\n✅ Order Manager v4.0 testing completed!")
#     print("🚀 Ready for full system integration")

# if __name__ == "__main__":
#     test_order_manager()