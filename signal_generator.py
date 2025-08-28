"""
🎯 Advanced Signal Generator v4.0 - Capital & Role Intelligence
signal_generator.py

🚀 NEW v4.0 FEATURES:
✅ Capital-Aware Signal Strength
✅ Role-based Signal Filtering  
✅ Recovery Opportunity Detection
✅ Relaxed Entry Rules (ไม่เข้มงวดเกินไป)
✅ Portfolio State Intelligence
✅ Integration with Capital Manager
✅ Dynamic Zone-based Signals

🔧 ENHANCED FROM v3.0:
✅ Mini Trend Analysis (2 ใน 3 แท่ง)
✅ Portfolio Balance Intelligence  
✅ Dynamic Signal Strength + Lot Sizing
✅ Quality Filters + Session Adjustment

📋 BUY Signal Rules v4.0:
- แท่งเขียว 2 ใน 3 แท่งล่าสุด
- Body ratio >= 3% (ลดจาก 5%)
- การเคลื่อนไหว >= 0.15 points (ลดจาก 0.2)
- Capital zone consideration
- Role opportunity detection

📋 SELL Signal Rules v4.0:  
- แท่งแดง 2 ใน 3 แท่งล่าสุด
- Body ratio >= 3% (ลดจาก 5%)
- การเคลื่อนไหว >= 0.15 points (ลดจาก 0.2)
- Capital zone consideration
- Role opportunity detection
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time
import MetaTrader5 as mt5

class SignalGenerator:
    """
    🎯 Advanced Signal Generator v4.0
    
    สร้างสัญญาณ BUY/SELL แบบ Capital & Role Intelligence
    พร้อม Mini Trend Analysis + Portfolio Balance
    """
    
    def __init__(self, candlestick_analyzer, config: Dict):
        """
        🔧 เริ่มต้น Advanced Signal Generator v4.0
        
        Args:
            candlestick_analyzer: Candlestick analyzer instance  
            config: การตั้งค่าระบบ v4.0
        """
        self.candlestick_analyzer = candlestick_analyzer
        self.config = config
        
        # การตั้งค่า signal generation (อัพเดท v4.0)
        self.smart_rules = config.get("smart_entry_rules", {})
        self.mini_trend_config = self.smart_rules.get("mini_trend", {})
        self.balance_config = self.smart_rules.get("portfolio_balance", {})
        self.lot_config = self.smart_rules.get("dynamic_lot_sizing", {})
        self.filter_config = config.get("entry_filters", {})
        
        # 🆕 v4.0: Capital & Role integration
        self.capital_config = config.get("capital_management", {})
        self.role_config = config.get("order_roles", {})
        self.capital_manager = None  # จะถูกตั้งค่าภายหลัง
        self.role_manager = None     # จะถูกตั้งค่าภายหลัง
        
        # Signal rate limiting (relaxed v4.0)
        trading_config = config.get("trading", {})
        self.cooldown_seconds = trading_config.get("signal_cooldown_seconds", 45)  # ลดจาก 60
        self.max_signals_per_hour = trading_config.get("max_signals_per_hour", 50)  # เพิ่มจาก 40
        self.high_frequency_mode = trading_config.get("high_frequency_mode", True)
        
        # Signal tracking (เดิม)
        self.last_signal_time = datetime.min
        self.signal_history = []
        self.total_signals_today = 0
        self.last_reset_date = datetime.now().date()
        
        # Performance tracking (เดิม)
        self.signals_generated = {'BUY': 0, 'SELL': 0, 'WAIT': 0}
        self.signal_quality_scores = []
        
        # Signal locking (เดิม)
        self.last_signal_signature = None
        self.signal_signatures = set()
        self.max_signal_history = 100
        
        # Portfolio tracking (enhanced v4.0)
        self.portfolio_stats = {
            'buy_positions': 0,
            'sell_positions': 0,
            'total_volume': 0.0,
            'imbalance_ratio': 0.0,
            'drawdown': 0.0,
            'trading_mode': 'normal',
            'last_update': datetime.min
        }
        
        # 🆕 v4.0: Capital zone tracking
        self.capital_zones_stats = {
            'safe_utilization': 0.0,
            'growth_utilization': 0.0, 
            'aggressive_utilization': 0.0
        }
        
        # Mini trend tracking (เดิม)
        self.trend_history = []
        self.max_trend_history = 10
        
        print(f"🎯 Advanced Signal Generator v4.0 initialized")
        print(f"   Mode: Capital & Role Intelligence")
        print(f"   Cooldown: {self.cooldown_seconds}s (relaxed)")
        print(f"   Max signals/hour: {self.max_signals_per_hour}")
        print(f"   Min body ratio: {self.mini_trend_config.get('min_body_ratio', 0.03)*100:.1f}% (relaxed)")
        print(f"   Min movement: {self.filter_config.get('price_movement_filter', {}).get('min_price_change_points', 0.15)} points (relaxed)")

    # ==========================================
    # 🆕 v4.0: CAPITAL & ROLE INTEGRATION
    # ==========================================
    
    def set_capital_manager(self, capital_manager):
        """🔗 เชื่อมต่อ Capital Manager"""
        self.capital_manager = capital_manager
        print("🔗 Capital Manager integrated with Signal Generator")
    
    def set_role_manager(self, role_manager):
        """🔗 เชื่อมต่อ Role Manager"""
        self.role_manager = role_manager
        print("🔗 Role Manager integrated with Signal Generator")

    def _update_capital_context(self) -> Dict:
        """💰 อัพเดทบริบททุนสำหรับการสร้าง signal"""
        try:
            if not self.capital_manager:
                return {'zone': 'safe', 'mode': 'normal', 'drawdown': 0.0, 'efficiency': 1.0}
            
            capital_status = self.capital_manager.update_capital_status()
            
            context = {
                'current_capital': capital_status.get('current_capital', 5000),
                'drawdown': capital_status.get('current_drawdown', 0.0),
                'trading_mode': capital_status.get('trading_mode', 'normal'),
                'zones': capital_status.get('capital_zones', {}),
                'efficiency': capital_status.get('current_capital', 5000) / capital_status.get('initial_capital', 5000)
            }
            
            # อัพเดท portfolio stats
            self.portfolio_stats.update({
                'drawdown': context['drawdown'],
                'trading_mode': context['trading_mode']
            })
            
            return context
            
        except Exception as e:
            print(f"❌ Capital context update error: {e}")
            return {'zone': 'safe', 'mode': 'normal', 'drawdown': 0.0, 'efficiency': 1.0}

    def _determine_recommended_zone(self, signal_data: Dict, capital_context: Dict) -> str:
        """🎯 กำหนด Capital Zone ที่แนะนำสำหรับ signal นี้"""
        try:
            signal_strength = signal_data.get('strength', 0.5)
            trading_mode = capital_context.get('trading_mode', 'normal')
            drawdown = capital_context.get('drawdown', 0.0)
            
            # Zone recommendation logic
            if trading_mode == 'emergency':
                return 'safe'  # Emergency mode = Safe zone only
            
            elif trading_mode == 'conservative':
                if signal_strength >= 0.8:
                    return 'growth'  # High strength signals can use growth zone
                else:
                    return 'safe'
            
            elif trading_mode == 'recovery':
                if signal_strength >= 0.9:
                    return 'aggressive'  # Recovery mode with very strong signals
                elif signal_strength >= 0.7:
                    return 'growth'
                else:
                    return 'safe'
            
            else:  # normal mode
                if signal_strength >= 0.85:
                    return 'aggressive'  # Very strong signals
                elif signal_strength >= 0.6:
                    return 'growth'      # Medium strength signals  
                else:
                    return 'safe'        # Weak signals
            
        except Exception as e:
            print(f"❌ Zone determination error: {e}")
            return 'safe'

    def _detect_role_opportunities(self, signal_data: Dict, capital_context: Dict) -> List[str]:
        """🎭 ตรวจหาโอกาสสำหรับ roles ต่างๆ"""
        try:
            opportunities = []
            
            signal_strength = signal_data.get('strength', 0.5)
            drawdown = capital_context.get('drawdown', 0.0)
            trading_mode = capital_context.get('trading_mode', 'normal')
            imbalance = self.portfolio_stats.get('imbalance_ratio', 0.0)
            
            # HG (Hedge Guard) opportunities
            if drawdown > 15.0 or imbalance > 0.65:
                opportunities.append('HG')
            
            # PW (Profit Walker) opportunities  
            if 0.4 <= signal_strength <= 0.8 and trading_mode in ['normal', 'recovery']:
                opportunities.append('PW')
            
            # RH (Recovery Hunter) opportunities
            if trading_mode == 'recovery' or (drawdown > 20.0 and signal_strength > 0.7):
                opportunities.append('RH')
            
            # SC (Scalp Capture) opportunities
            if signal_strength > 0.8 and self._is_high_volatility_time() and drawdown < 10.0:
                opportunities.append('SC')
            
            return opportunities
            
        except Exception as e:
            print(f"❌ Role opportunities detection error: {e}")
            return ['PW']  # Default to Profit Walker

    # ==========================================
    # 🎯 MAIN SIGNAL GENERATION (enhanced v4.0)
    # ==========================================
    
    def generate_signal(self, candlestick_data: Dict) -> Optional[Dict]:
        """
        🎯 สร้าง Signal แบบ Capital & Role Intelligence v4.0
        
        คงชื่อ method เดิมไว้ แต่เพิ่ม Capital & Role intelligence
        """
        try:
            if not candlestick_data:
                return self._create_wait_signal("No data")
            
            # 🆕 v4.0: อัพเดทบริบททุนก่อน
            capital_context = self._update_capital_context()
            
            # ตรวจสอบ rate limiting (relaxed v4.0)
            if not self._check_rate_limits():
                return self._create_wait_signal("Rate limit exceeded")
            
            # ดึง timestamp และ signature check (เดิม)
            candle_timestamp = candlestick_data.get('candle_timestamp')
            if not candle_timestamp:
                return self._create_wait_signal("No timestamp")
            
            signature = f"Smart_{candle_timestamp}"
            if self._is_signal_sent_for_signature(signature):
                return self._create_wait_signal("Already processed")
            
            # 🔍 Mini Trend Analysis (เดิม)
            recent_candles = self._get_recent_candles_data(candlestick_data)
            if not recent_candles:
                return self._create_wait_signal("Cannot get candles data")
            
            mini_trend_result = self._analyze_mini_trend(recent_candles)
            if not mini_trend_result:
                return self._create_wait_signal("No mini trend detected")
            
            # 🆕 v4.0: ปรับ signal strength ด้วย capital factors
            enhanced_signal = self._enhance_signal_with_capital_intelligence(
                mini_trend_result, 
                capital_context
            )
            
            if not enhanced_signal:
                return self._create_wait_signal("Capital filters rejected signal")
            
            # 🔍 Quality Filters (relaxed v4.0)
            if not self._pass_relaxed_quality_filters(candlestick_data, enhanced_signal):
                return self._create_wait_signal("Quality filters failed")
            
            # 📊 Portfolio Balance (enhanced v4.0)
            balance_adjusted_signal = self._apply_capital_aware_portfolio_balance(enhanced_signal)
            
            # 📏 Dynamic Lot Sizing (enhanced v4.0)
            recommended_zone = self._determine_recommended_zone(balance_adjusted_signal, capital_context)
            role_opportunities = self._detect_role_opportunities(balance_adjusted_signal, capital_context)
            
            # 🆕 v4.0: คำนวณ lot size แบบ capital + role aware
            dynamic_lot = self._calculate_capital_role_aware_lot_size(
                balance_adjusted_signal, 
                recommended_zone,
                role_opportunities[0] if role_opportunities else 'PW'
            )
            
            # 🚫 Emergency mode signal restriction
            if capital_context.get('trading_mode') == 'emergency' and balance_adjusted_signal['strength'] < 0.7:
                return self._create_wait_signal("Emergency mode: insufficient signal strength")
            
            # 🎯 สร้าง Final Signal
            signal = {
                'action': balance_adjusted_signal['action'],
                'strength': balance_adjusted_signal['strength'],
                'confidence': balance_adjusted_signal['confidence'],
                'timestamp': datetime.now(),
                'signal_id': f"{balance_adjusted_signal['action']}_{datetime.now().strftime('%H%M%S')}",
                
                # 🆕 v4.0: Capital intelligence data
                'capital_zone': recommended_zone,
                'trading_mode': capital_context.get('trading_mode'),
                'current_drawdown': capital_context.get('drawdown'),
                'capital_efficiency': capital_context.get('efficiency'),
                
                # 🆕 v4.0: Role intelligence data
                'role_opportunities': role_opportunities,
                'recommended_role': role_opportunities[0] if role_opportunities else 'PW',
                
                # Enhanced data (from v3.0)
                'trend_pattern': balance_adjusted_signal.get('trend_pattern'),
                'trend_strength': balance_adjusted_signal.get('trend_strength'),
                'portfolio_balance_factor': balance_adjusted_signal.get('portfolio_balance_factor', 1.0),
                'dynamic_lot_size': dynamic_lot,
                
                # Quality metrics
                'signal_quality_score': self._calculate_signal_quality_score(balance_adjusted_signal, capital_context),
                'filters_passed': True,
                'candles_analyzed': len(recent_candles)
            }
            
            # บันทึก signature (เดิม)
            self._mark_signal_sent_for_signature(signature)
            
            # บันทึก signal (เดิม)
            self._record_signal(signal)
            
            print(f"🎯 CAPITAL-SMART SIGNAL: {signal['action']} (Strength: {signal['strength']:.2f})")
            print(f"   💰 Zone: {recommended_zone} | Mode: {capital_context.get('trading_mode')} | DD: {capital_context.get('drawdown'):.1f}%")
            print(f"   🎭 Role: {signal['recommended_role']} | Opportunities: {role_opportunities}")
            print(f"   📏 Lot: {dynamic_lot:.3f} | Quality: {signal['signal_quality_score']:.2f}")
            
            return signal
            
        except Exception as e:
            print(f"❌ Signal generation error: {e}")
            return self._create_wait_signal(f"Error: {str(e)}")

    def _enhance_signal_with_capital_intelligence(self, base_signal: Dict, capital_context: Dict) -> Optional[Dict]:
        """💡 เพิ่มปัญญาด้านทุนให้กับ signal"""
        try:
            enhanced_signal = base_signal.copy()
            
            original_strength = enhanced_signal.get('strength', 0.5)
            
            # Capital efficiency multiplier
            efficiency = capital_context.get('efficiency', 1.0)
            efficiency_multiplier = min(1.2, max(0.8, efficiency))
            
            # Trading mode multiplier
            mode = capital_context.get('trading_mode', 'normal')
            mode_multipliers = {
                'normal': 1.0,
                'conservative': 0.8,    # ลดความแรงเมื่อระมัดระวัง
                'emergency': 0.6,      # ลดความแรงเมื่อฉุกเฉิน
                'recovery': 1.3        # เพิ่มความแรงเมื่อฟื้นตัว
            }
            mode_multiplier = mode_multipliers.get(mode, 1.0)
            
            # Drawdown adjustment
            drawdown = capital_context.get('drawdown', 0.0)
            if drawdown > 25.0:
                drawdown_multiplier = 0.7  # ลดความแรงเมื่อ drawdown สูงมาก
            elif drawdown > 15.0:
                drawdown_multiplier = 0.85 # ลดความแรงเมื่อ drawdown สูง
            else:
                drawdown_multiplier = 1.0
            
            # คำนวณความแรงใหม่
            new_strength = original_strength * efficiency_multiplier * mode_multiplier * drawdown_multiplier
            new_strength = max(0.1, min(0.95, new_strength))  # จำกัดช่วง
            
            enhanced_signal['strength'] = round(new_strength, 3)
            enhanced_signal['capital_enhancement'] = {
                'original_strength': original_strength,
                'efficiency_multiplier': efficiency_multiplier,
                'mode_multiplier': mode_multiplier,
                'drawdown_multiplier': drawdown_multiplier,
                'final_strength': new_strength
            }
            
            # ตรวจสอบ minimum strength
            min_strength_threshold = 0.3 if mode == 'recovery' else 0.4
            if new_strength < min_strength_threshold:
                print(f"   ❌ Signal strength too low: {new_strength:.3f} < {min_strength_threshold}")
                return None
            
            print(f"   💡 Capital enhancement: {original_strength:.3f} → {new_strength:.3f} (Mode: {mode})")
            return enhanced_signal
            
        except Exception as e:
            print(f"❌ Capital intelligence enhancement error: {e}")
            return base_signal

    def _calculate_capital_role_aware_lot_size(self, signal_data: Dict, zone: str, role: str) -> float:
        """📏 คำนวณ Lot Size แบบ Capital + Role Aware"""
        try:
            if self.capital_manager:
                # ใช้ Capital Manager คำนวณ
                signal_strength = signal_data.get('strength', 0.5)
                lot_size = self.capital_manager.calculate_position_size(zone, signal_strength, role)
                return lot_size
            else:
                # Fallback calculation
                base_lot = 0.01
                strength_multiplier = 1 + signal_data.get('strength', 0.5)
                
                zone_multipliers = {'safe': 0.8, 'growth': 1.0, 'aggressive': 1.5}
                role_multipliers = {'HG': 0.8, 'PW': 1.0, 'RH': 1.5, 'SC': 1.2}
                
                lot = base_lot * strength_multiplier * zone_multipliers.get(zone, 1.0) * role_multipliers.get(role, 1.0)
                return max(0.01, min(0.20, round(lot, 2)))
                
        except Exception as e:
            print(f"❌ Capital role aware lot calculation error: {e}")
            return 0.01

    def _pass_relaxed_quality_filters(self, candlestick_data: Dict, signal_data: Dict) -> bool:
        """🔍 Quality Filters แบบ Relaxed v4.0"""
        try:
            # Price movement filter (relaxed)
            movement_filter = self.filter_config.get("price_movement_filter", {})
            if movement_filter.get("enabled", False):
                price_change = abs(candlestick_data.get('high', 0) - candlestick_data.get('low', 0))
                min_movement = movement_filter.get("min_price_change_points", 0.15)  # ลดจาก 0.20
                if price_change < min_movement:
                    print(f"   ❌ Movement too small: {price_change:.3f} < {min_movement}")
                    return False
            
            # Session activity filter (relaxed)
            session_filter = self.filter_config.get("session_activity_filter", {})
            if session_filter.get("enabled", False):
                activity_score = self._get_session_activity_score()
                if activity_score < 0.3:  # ลดจาก 0.5
                    print(f"   ❌ Low session activity: {activity_score:.2f}")
                    return False
            
            # Capital zone filter (new v4.0)
            capital_zone_filter = self.filter_config.get("capital_zone_filter", {})
            if capital_zone_filter.get("enabled", False):
                # อนุญาต signals ในทุก zones (relaxed)
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ Quality filters error: {e}")
            return True  # อนุญาตเมื่อเกิดข้อผิดพลาด

    def _calculate_signal_quality_score(self, signal_data: Dict, capital_context: Dict) -> float:
        """📊 คำนวณคะแนนคุณภาพ signal"""
        try:
            score = 0.0
            
            # Signal strength component (40%)
            strength = signal_data.get('strength', 0.5)
            score += (strength * 0.4)
            
            # Trend quality component (30%)
            trend_strength = signal_data.get('trend_strength', 0.5)
            score += (trend_strength * 0.3)
            
            # Capital context component (20%)
            efficiency = capital_context.get('efficiency', 1.0)
            drawdown = capital_context.get('drawdown', 0.0)
            capital_score = max(0, efficiency - (drawdown / 100))
            score += (capital_score * 0.2)
            
            # Portfolio balance component (10%)
            balance_factor = signal_data.get('portfolio_balance_factor', 1.0)
            balance_score = min(1.0, balance_factor / 2.0)  # normalize
            score += (balance_score * 0.1)
            
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            return 0.5

    # ==========================================
    # 🔍 MINI TREND ANALYSIS (เดิม + ปรับแก้เล็กน้อย)
    # ==========================================
    
    def _get_recent_candles_data(self, current_candlestick_data: Dict) -> List[Dict]:
        """🔍 ดึงข้อมูล candles หลายแท่งสำหรับ mini trend analysis"""
        try:
            # ดึงข้อมูลจาก MT5 โดยตรง
            symbol = current_candlestick_data.get('symbol', 'XAUUSD.v')
            timeframe = mt5.TIMEFRAME_M5
            
            # ดึง 5 แท่งล่าสุด (ใช้ 3 แท่ง, เผื่อไว้ 2 แท่ง)
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 5)
            
            if rates is None or len(rates) < 3:
                print(f"❌ ไม่สามารถดึง rates data ได้")
                return []
            
            # แปลงเป็น format ที่ใช้งาน
            candles = []
            for i, rate in enumerate(rates[-3:]):  # ใช้ 3 แท่งล่าสุด
                candle = {
                    'open': float(rate[1]),
                    'high': float(rate[2]),
                    'low': float(rate[3]),
                    'close': float(rate[4]),
                    'volume': int(rate[5]) if len(rate) > 5 else 0,
                    'timestamp': int(rate[0])
                }
                
                # คำนวณ derived data
                candle['body_size'] = abs(candle['close'] - candle['open'])
                candle['range_size'] = candle['high'] - candle['low'] 
                candle['body_ratio'] = candle['body_size'] / candle['range_size'] if candle['range_size'] > 0 else 0
                candle['candle_color'] = 'green' if candle['close'] > candle['open'] else 'red'
                
                candles.append(candle)
            
            return candles
            
        except Exception as e:
            print(f"❌ Get recent candles error: {e}")
            return []

    def _analyze_mini_trend(self, candles: List[Dict]) -> Optional[Dict]:
        """🔍 วิเคราะห์ Mini Trend จาก 3 แท่งล่าสุด (relaxed v4.0)"""
        try:
            if len(candles) < 3:
                return None
            
            # วิเคราะห์ 3 แท่งล่าสุด
            colors = [candle['candle_color'] for candle in candles]
            green_count = colors.count('green')
            red_count = colors.count('red')
            
            # แท่งปัจจุบัน (แท่งสุดท้าย)
            current_candle = candles[-1]
            current_body_ratio = current_candle['body_ratio']
            current_color = current_candle['candle_color']
            
            # ตรวจสอบ body ratio ขั้นต่ำ (relaxed v4.0)
            min_body_ratio = self.mini_trend_config.get('min_body_ratio', 0.03)  # ลดจาก 0.05
            if current_body_ratio < min_body_ratio:
                return None
            
            # 🎯 BUY Signal: เขียว 2 ใน 3 + แท่งปัจจุบันเขียว
            if green_count >= 2 and current_color == 'green':
                trend_strength = self._calculate_trend_strength(candles, 'bullish')
                
                signal = {
                    'action': 'BUY',
                    'strength': trend_strength,
                    'confidence': min(0.6 + (green_count - 2) * 0.2, 0.9),
                    'trend_pattern': f"GREEN_{green_count}_of_3",
                    'trend_strength': trend_strength,
                    'candles_analyzed': len(candles)
                }
                
                return signal
            
            # 🎯 SELL Signal: แดง 2 ใน 3 + แท่งปัจจุบันแดง  
            if red_count >= 2 and current_color == 'red':
                trend_strength = self._calculate_trend_strength(candles, 'bearish')
                
                signal = {
                    'action': 'SELL',
                    'strength': trend_strength,
                    'confidence': min(0.6 + (red_count - 2) * 0.2, 0.9),
                    'trend_pattern': f"RED_{red_count}_of_3",
                    'trend_strength': trend_strength,
                    'candles_analyzed': len(candles)
                }
                
                return signal
            
            return None  # ไม่เจอ pattern ที่ต้องการ
            
        except Exception as e:
            print(f"❌ Mini trend analysis error: {e}")
            return None

    def _calculate_trend_strength(self, candles: List[Dict], direction: str) -> float:
        """📊 คำนวณความแรงของ trend (enhanced v4.0)"""
        try:
            if len(candles) < 3:
                return 0.5
            
            base_strength = 0.4  # เริ่มต้น
            
            # ความสม่ำเสมอของสี
            target_color = 'green' if direction == 'bullish' else 'red'
            color_consistency = sum(1 for c in candles if c['candle_color'] == target_color) / len(candles)
            base_strength += color_consistency * 0.3
            
            # ขนาดของ body
            avg_body_ratio = sum(c['body_ratio'] for c in candles) / len(candles)
            base_strength += min(avg_body_ratio * 2, 0.3)  # max 0.3 จาก body
            
            # ปริมาณการเคลื่อนไหว
            total_range = sum(c['range_size'] for c in candles)
            if total_range > 2.0:  # movements มาก
                base_strength += 0.1
            elif total_range > 1.0:  # movements ปานกลาง
                base_strength += 0.05
            
            # จำกัดขอบเขต
            final_strength = max(0.3, min(0.9, base_strength))  # ผ่อนผันขอบเขต
            
            return round(final_strength, 3)
            
        except Exception as e:
            return 0.5

    # ==========================================
    # 📊 PORTFOLIO BALANCE (enhanced v4.0)
    # ==========================================
    
    def _apply_capital_aware_portfolio_balance(self, signal: Dict) -> Dict:
        """⚖️ ปรับ Signal ด้วย Capital-aware Portfolio Balance"""
        try:
            # อัพเดท portfolio stats
            self._update_portfolio_stats()
            
            action = signal['action']
            imbalance_ratio = self.portfolio_stats.get('imbalance_ratio', 0.0)
            
            # Balance adjustment logic (relaxed v4.0)
            balance_factor = 1.0
            
            if action == 'BUY':
                if imbalance_ratio > 0.70:  # BUY มากเกินไป (relaxed จาก 0.65)
                    balance_factor = 0.7  # ลดความแรง
                elif imbalance_ratio < 0.30:  # BUY น้อยเกินไป
                    balance_factor = 1.4  # เพิ่มความแรง
            
            elif action == 'SELL':
                if imbalance_ratio < 0.30:  # SELL มากเกินไป
                    balance_factor = 0.7  # ลดความแรง
                elif imbalance_ratio > 0.70:  # SELL น้อยเกินไป
                    balance_factor = 1.4  # เพิ่มความแรง
            
            # ปรับความแรง signal
            original_strength = signal['strength']
            new_strength = min(0.95, original_strength * balance_factor)
            
            adjusted_signal = signal.copy()
            adjusted_signal['strength'] = round(new_strength, 3)
            adjusted_signal['portfolio_balance_factor'] = balance_factor
            adjusted_signal['portfolio_imbalance'] = imbalance_ratio
            
            if balance_factor != 1.0:
                print(f"   ⚖️ Balance adjustment: {original_strength:.3f} → {new_strength:.3f} (factor: {balance_factor:.2f})")
            
            return adjusted_signal
            
        except Exception as e:
            print(f"❌ Portfolio balance error: {e}")
            return signal

    def _update_portfolio_stats(self):
        """📊 อัพเดทสถิติ portfolio (enhanced v4.0)"""
        try:
            # ดึงข้อมูล positions จาก MT5
            symbol = self.config.get("trading", {}).get("symbol", "XAUUSD.v")
            positions = mt5.positions_get(symbol=symbol)
            
            if positions is None:
                positions = []
            
            # นับ positions แยกตาม type
            buy_positions = sum(1 for p in positions if p.type == mt5.ORDER_TYPE_BUY)
            sell_positions = sum(1 for p in positions if p.type == mt5.ORDER_TYPE_SELL)
            total_positions = buy_positions + sell_positions
            total_volume = sum(p.volume for p in positions)
            
            # คำนวณ imbalance ratio
            if total_positions > 0:
                imbalance_ratio = buy_positions / total_positions
            else:
                imbalance_ratio = 0.5  # neutral เมื่อไม่มี positions
            
            # อัพเดท stats
            self.portfolio_stats.update({
                'buy_positions': buy_positions,
                'sell_positions': sell_positions,
                'total_volume': total_volume,
                'imbalance_ratio': imbalance_ratio,
                'last_update': datetime.now()
            })
            
        except Exception as e:
            print(f"❌ Portfolio stats update error: {e}")

    # ==========================================
    # 🔧 UTILITY METHODS (เดิม + เพิ่ม v4.0)
    # ==========================================
    
    def _check_rate_limits(self) -> bool:
        """⏰ ตรวจสอบ rate limiting (relaxed v4.0)"""
        try:
            now = datetime.now()
            
            # ตรวจสอบ cooldown (relaxed)
            time_since_last = (now - self.last_signal_time).total_seconds()
            if time_since_last < self.cooldown_seconds:
                return False
            
            # ตรวจสอบสัญญาณต่อชั่วโมง (relaxed)  
            hour_ago = now - timedelta(hours=1)
            recent_signals = [s for s in self.signal_history if s.get('timestamp', datetime.min) > hour_ago]
            
            if len(recent_signals) >= self.max_signals_per_hour:
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Rate limit check error: {e}")
            return False

    def _is_high_volatility_time(self) -> bool:
        """⚡ ตรวจสอบช่วงเวลา high volatility"""
        try:
            now = datetime.now()
            hour = now.hour
            
            # London session (8-12 GMT+7) หรือ NY session (21-01 GMT+7)
            return (8 <= hour <= 12) or (21 <= hour <= 23) or (0 <= hour <= 1)
            
        except Exception as e:
            return False

    def _get_session_activity_score(self) -> float:
        """📊 คะแนนความคึกคักของ session"""
        try:
            hour = datetime.now().hour
            
            # London + NY overlap (เช้า)
            if 8 <= hour <= 12:
                return 1.0
            # NY session (ค่ำ-กลางคืน)  
            elif 21 <= hour <= 23 or 0 <= hour <= 2:
                return 0.9
            # Asia session
            elif 13 <= hour <= 18:
                return 0.7
            # Low activity periods
            else:
                return 0.4
                
        except Exception as e:
            return 0.5

    def _create_wait_signal(self, reason: str) -> Dict:
        """สร้าง WAIT signal (เดิม)"""
        return {
            'action': 'WAIT',
            'strength': 0.0,
            'confidence': 0.0,
            'timestamp': datetime.now(),
            'reason': reason,
            'signal_id': f"WAIT_{datetime.now().strftime('%H%M%S')}"
        }

    def _is_signal_sent_for_signature(self, signature: str) -> bool:
        """🔒 เช็คว่าส่ง signal แล้วหรือยัง (เดิม)"""
        try:
            if not hasattr(self, 'signal_signatures'):
                self.signal_signatures = set()
            
            return signature in self.signal_signatures
            
        except Exception as e:
            return False

    def _mark_signal_sent_for_signature(self, signature: str):
        """🔒 บันทึกว่าส่ง signal แล้ว (เดิม)"""
        try:
            if not hasattr(self, 'signal_signatures'):
                self.signal_signatures = set()
            
            self.signal_signatures.add(signature)
            
            # เก็บแค่ 100 signatures ล่าสุด
            if len(self.signal_signatures) > 100:
                signatures_list = list(self.signal_signatures)
                self.signal_signatures = set(signatures_list[-50:])
            
        except Exception as e:
            print(f"❌ Mark signature error: {e}")

    def _record_signal(self, signal_data: Dict):
        """📝 บันทึก Signal History (เดิม)"""
        try:
            if not hasattr(self, 'signals_generated'):
                self.signals_generated = {'BUY': 0, 'SELL': 0, 'WAIT': 0}
            if not hasattr(self, 'signal_history'):
                self.signal_history = []
            if not hasattr(self, 'last_signal_time'):
                self.last_signal_time = datetime.min
                
            action = signal_data.get('action')
            if action in ['BUY', 'SELL']:
                self.signals_generated[action] += 1
                self.signal_history.append({
                    'action': action,
                    'strength': signal_data.get('strength', 0),
                    'timestamp': datetime.now(),
                    'signal_id': signal_data.get('signal_id'),
                    'capital_zone': signal_data.get('capital_zone'),
                    'role': signal_data.get('recommended_role')
                })
                self.last_signal_time = datetime.now()
                
            # บันทึกคะแนนคุณภาพ
            quality_score = signal_data.get('signal_quality_score', 0.5)
            self.signal_quality_scores.append(quality_score)
            
            # เก็บแค่ 100 scores ล่าสุด
            if len(self.signal_quality_scores) > 100:
                self.signal_quality_scores = self.signal_quality_scores[-50:]
                
        except Exception as e:
            print(f"❌ Record signal error: {e}")

    # ==========================================
    # 🔧 DEBUGGING & MAINTENANCE METHODS (เดิม)
    # ==========================================
    
    def clear_signal_locks(self):
        """🗑️ ล้างการล็อก signal ทั้งหมด (เดิม)"""
        try:
            if hasattr(self, 'signal_signatures'):
                old_count = len(self.signal_signatures)
                self.signal_signatures.clear()
                print(f"🗑️ Cleared {old_count} signal signature locks")
            
            return True
            
        except Exception as e:
            print(f"❌ Clear signal locks error: {e}")
            return False

    def get_signal_lock_info(self) -> Dict:
        """📊 ข้อมูลการล็อก signal (เดิม)"""
        try:
            if not hasattr(self, 'signal_signatures'):
                self.signal_signatures = set()
            
            return {
                'total_locked_signatures': len(self.signal_signatures),
                'recent_signatures': list(self.signal_signatures)[-5:] if self.signal_signatures else [],
                'max_signature_history': 100,
                'lock_method': 'candle_timestamp_based'
            }
            
        except Exception as e:
            return {'error': str(e)}

    def get_portfolio_stats(self) -> Dict:
        """📊 ส่งออกสถิติ portfolio (enhanced v4.0)"""
        stats = self.portfolio_stats.copy()
        stats['capital_zones_stats'] = self.capital_zones_stats.copy()
        return stats

    def get_performance_summary(self) -> Dict:
        """📈 สรุปผลงาน signal generation (enhanced v4.0)"""
        try:
            total_signals = sum(self.signals_generated.values())
            
            summary = {
                'total_signals_generated': total_signals,
                'buy_signals': self.signals_generated.get('BUY', 0),
                'sell_signals': self.signals_generated.get('SELL', 0),
                'wait_signals': self.signals_generated.get('WAIT', 0),
                'buy_sell_ratio': self.signals_generated.get('BUY', 0) / max(self.signals_generated.get('SELL', 1), 1),
                'avg_signal_quality': sum(self.signal_quality_scores) / max(len(self.signal_quality_scores), 1),
                'portfolio_stats': self.portfolio_stats,
                'last_signal_time': self.last_signal_time.isoformat() if self.last_signal_time != datetime.min else None,
                
                # 🆕 v4.0: Enhanced metrics
                'capital_intelligence': {
                    'capital_manager_connected': self.capital_manager is not None,
                    'role_manager_connected': self.role_manager is not None,
                    'capital_zones_utilization': self.capital_zones_stats
                }
            }
            
            return summary
            
        except Exception as e:
            return {'error': str(e)}