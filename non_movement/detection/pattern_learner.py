"""
Pattern learning system

Learns normal activity patterns over time to reduce false positives
and personalize thresholds for each individual.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import os


class PatternLearner:
    """
    Learns and stores normal movement patterns.
    
    This helps the system:
    1. Understand normal activity levels
    2. Adjust thresholds based on individual patterns
    3. Identify unusual activity (which might indicate issues)
    4. Reduce false positives
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the pattern learner.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        monitoring_config = config.get('monitoring', {})
        
        self.enable_learning = monitoring_config.get('enable_pattern_learning', True)
        self.learning_period_days = monitoring_config.get('learning_period_days', 7)
        self.baseline_establishment_days = monitoring_config.get('baseline_establishment_days', 3)
        
        # Data storage
        system_config = config.get('system', {})
        self.data_directory = system_config.get('data_directory', 'data')
        self.patterns_file = system_config.get('movement_patterns_file', 'data/patterns.json')
        
        # Pattern storage
        self.patterns: Dict[str, Any] = {
            'hourly_activity': {},  # Activity level by hour of day
            'daily_patterns': {},  # Patterns by day of week
            'baseline_established': False,
            'baseline_date': None,
            'movement_events': [],  # Recent movement events
        }
        
        # Ensure data directory exists
        os.makedirs(self.data_directory, exist_ok=True)
        
        # Load existing patterns if available
        self.load_patterns()
    
    def record_movement_event(self, timestamp: datetime, sensor_name: str, value: Any):
        """
        Record a movement event for pattern learning.
        
        Args:
            timestamp: When movement occurred
            sensor_name: Which sensor detected it
            value: Sensor value
        """
        if not self.enable_learning:
            return
        
        event = {
            'timestamp': timestamp.isoformat(),
            'sensor': sensor_name,
            'value': value,
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),  # 0=Monday, 6=Sunday
        }
        
        self.patterns['movement_events'].append(event)
        
        # Keep only recent events (last 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        self.patterns['movement_events'] = [
            e for e in self.patterns['movement_events']
            if datetime.fromisoformat(e['timestamp']) > cutoff_date
        ]
        
        # Update hourly activity
        hour = timestamp.hour
        if hour not in self.patterns['hourly_activity']:
            self.patterns['hourly_activity'][hour] = {'count': 0, 'total': 0}
        
        self.patterns['hourly_activity'][hour]['count'] += 1
        self.patterns['hourly_activity'][hour]['total'] += 1
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """
        Analyze recorded patterns and generate insights.
        
        Returns:
            Dictionary with pattern analysis
        """
        if not self.enable_learning or len(self.patterns['movement_events']) < 10:
            return {'status': 'insufficient_data'}
        
        # Calculate average activity by hour
        hourly_avg = {}
        for hour in range(24):
            if hour in self.patterns['hourly_activity']:
                data = self.patterns['hourly_activity'][hour]
                # Calculate average (simplified - in reality would use time windows)
                hourly_avg[hour] = data['count'] / max(1, len(self.patterns['movement_events']) / 24)
            else:
                hourly_avg[hour] = 0.0
        
        # Identify most active hours
        most_active_hour = max(hourly_avg.items(), key=lambda x: x[1])[0] if hourly_avg else None
        least_active_hour = min(hourly_avg.items(), key=lambda x: x[1])[0] if hourly_avg else None
        
        # Check if baseline is established
        events_age_days = 0
        if self.patterns['movement_events']:
            oldest_event = min(
                datetime.fromisoformat(e['timestamp'])
                for e in self.patterns['movement_events']
            )
            events_age_days = (datetime.now() - oldest_event).days
        
        baseline_established = events_age_days >= self.baseline_establishment_days
        
        if baseline_established and not self.patterns['baseline_established']:
            self.patterns['baseline_established'] = True
            self.patterns['baseline_date'] = datetime.now().isoformat()
            self.save_patterns()
        
        return {
            'status': 'analyzed',
            'baseline_established': baseline_established,
            'events_recorded': len(self.patterns['movement_events']),
            'events_age_days': events_age_days,
            'hourly_activity': hourly_avg,
            'most_active_hour': most_active_hour,
            'least_active_hour': least_active_hour,
        }
    
    def get_expected_activity_level(self, hour: int) -> float:
        """
        Get expected activity level for a given hour.
        
        Args:
            hour: Hour of day (0-23)
        
        Returns:
            Expected activity level (0.0 to 1.0)
        """
        if not self.patterns['baseline_established']:
            return 0.5  # Default moderate activity
        
        analysis = self.analyze_patterns()
        hourly_activity = analysis.get('hourly_activity', {})
        
        if hour in hourly_activity:
            # Normalize to 0-1 scale
            max_activity = max(hourly_activity.values()) if hourly_activity else 1.0
            return min(1.0, hourly_activity[hour] / max_activity) if max_activity > 0 else 0.5
        
        return 0.5
    
    def is_unusual_activity(self, current_hour: int, has_movement: bool) -> bool:
        """
        Check if current activity is unusual based on learned patterns.
        
        Args:
            current_hour: Current hour of day
            has_movement: Whether movement is currently detected
        
        Returns:
            True if activity is unusual
        """
        if not self.patterns['baseline_established']:
            return False  # Can't determine unusual if no baseline
        
        expected_level = self.get_expected_activity_level(current_hour)
        
        # If we expect high activity but see none, that's unusual
        if expected_level > 0.7 and not has_movement:
            return True
        
        # If we expect low activity but see high, that's also unusual (but less concerning)
        # This could indicate someone else in the home, etc.
        
        return False
    
    def save_patterns(self):
        """Save patterns to file."""
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def load_patterns(self):
        """Load patterns from file."""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    self.patterns = json.load(f)
            except Exception as e:
                print(f"Error loading patterns: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of pattern learner."""
        analysis = self.analyze_patterns()
        
        return {
            'learning_enabled': self.enable_learning,
            'baseline_established': self.patterns.get('baseline_established', False),
            'baseline_date': self.patterns.get('baseline_date'),
            'events_recorded': len(self.patterns.get('movement_events', [])),
            'analysis': analysis,
        }
