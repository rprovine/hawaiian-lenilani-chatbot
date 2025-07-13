"""
Hawaiian Timezone Handler - Manages Hawaii-specific time operations
"""
import logging
from typing import Dict, Optional, Any, List
from datetime import datetime, time, timedelta
import pytz
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


class HawaiianTimezoneHandler:
    """Handles all Hawaii timezone-specific operations"""
    
    def __init__(self):
        # Hawaii timezone (HST - Hawaii Standard Time)
        # Hawaii does not observe daylight saving time
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        self.hawaii_zoneinfo = ZoneInfo('Pacific/Honolulu')
        
        # Business hours in Hawaii (typical)
        self.business_hours = {
            "standard": {
                "open": time(8, 0),  # 8:00 AM
                "close": time(17, 0)  # 5:00 PM
            },
            "retail": {
                "open": time(9, 0),  # 9:00 AM
                "close": time(21, 0)  # 9:00 PM
            },
            "restaurant": {
                "open": time(6, 0),  # 6:00 AM
                "close": time(22, 0)  # 10:00 PM
            },
            "tourism": {
                "open": time(7, 0),  # 7:00 AM
                "close": time(19, 0)  # 7:00 PM
            }
        }
        
        # Hawaiian holidays and special dates
        self.hawaiian_holidays = {
            "Prince Kuhio Day": "March 26",
            "King Kamehameha Day": "June 11",
            "Statehood Day": "Third Friday in August",
            "Lei Day": "May 1",
            "Duke Kahanamoku Day": "August 24"
        }
        
        # Time-based greetings
        self.time_greetings = {
            "early_morning": {
                "start": time(5, 0),
                "end": time(8, 0),
                "hawaiian": "Aloha kakahiaka",
                "english": "Good early morning",
                "pidgin": "Howzit! Up early yeah?"
            },
            "morning": {
                "start": time(8, 0),
                "end": time(12, 0),
                "hawaiian": "Aloha kakahiaka",
                "english": "Good morning",
                "pidgin": "Morning! How you stay?"
            },
            "afternoon": {
                "start": time(12, 0),
                "end": time(17, 0),
                "hawaiian": "Aloha awakea",
                "english": "Good afternoon",
                "pidgin": "Howzit! Hot one today!"
            },
            "evening": {
                "start": time(17, 0),
                "end": time(20, 0),
                "hawaiian": "Aloha ahiahi",
                "english": "Good evening",
                "pidgin": "Pau hana time!"
            },
            "night": {
                "start": time(20, 0),
                "end": time(5, 0),
                "hawaiian": "Aloha po",
                "english": "Good night",
                "pidgin": "Late night, yeah?"
            }
        }
        
        logger.info("Hawaiian Timezone Handler initialized")
    
    def get_current_hawaii_time(self) -> Dict[str, Any]:
        """Get current time in Hawaii with full context"""
        hawaii_now = datetime.now(self.hawaii_tz)
        
        # Get time period
        time_period = self._get_time_period(hawaii_now.time())
        
        # Check if it's a Hawaiian holiday
        is_holiday, holiday_name = self._check_hawaiian_holiday(hawaii_now)
        
        # Check business hours
        is_business_hours = self._is_business_hours(
            hawaii_now.time(),
            "standard"
        )
        
        return {
            "datetime": hawaii_now,
            "formatted": hawaii_now.strftime("%Y-%m-%d %I:%M %p HST"),
            "time": hawaii_now.time(),
            "date": hawaii_now.date(),
            "day_of_week": hawaii_now.strftime("%A"),
            "time_period": time_period,
            "is_business_hours": is_business_hours,
            "is_holiday": is_holiday,
            "holiday_name": holiday_name,
            "timezone": "HST",
            "utc_offset": "-10:00"
        }
    
    def get_time_based_greeting(
        self,
        language: str = "mixed",
        business_context: bool = True
    ) -> str:
        """Get appropriate greeting based on current Hawaii time"""
        
        current_time = self.get_current_hawaii_time()
        time_period = current_time["time_period"]
        greeting_info = self.time_greetings[time_period]
        
        # Base greeting
        if language == "hawaiian":
            greeting = greeting_info["hawaiian"]
        elif language == "pidgin":
            greeting = greeting_info["pidgin"]
        elif language == "english":
            greeting = greeting_info["english"]
        else:  # mixed
            greeting = f"{greeting_info['hawaiian']}! {greeting_info['pidgin']}"
        
        # Add business context
        if business_context:
            if current_time["is_business_hours"]:
                greeting += " Ready for help with your business!"
            elif time_period == "evening":
                greeting += " Working late? We stay here for you!"
            elif time_period == "early_morning":
                greeting += " Early bird gets da worm! How can we help?"
        
        # Add holiday greeting
        if current_time["is_holiday"]:
            greeting += f" Happy {current_time['holiday_name']}! 🌺"
        
        return greeting
    
    def _get_time_period(self, current_time: time) -> str:
        """Determine which time period we're in"""
        
        for period, info in self.time_greetings.items():
            start = info["start"]
            end = info["end"]
            
            # Handle overnight period
            if start > end:  # Night period crosses midnight
                if current_time >= start or current_time < end:
                    return period
            else:
                if start <= current_time < end:
                    return period
        
        return "morning"  # Default
    
    def _is_business_hours(
        self,
        current_time: time,
        business_type: str = "standard"
    ) -> bool:
        """Check if current time is within business hours"""
        
        hours = self.business_hours.get(business_type, self.business_hours["standard"])
        open_time = hours["open"]
        close_time = hours["close"]
        
        return open_time <= current_time <= close_time
    
    def _check_hawaiian_holiday(
        self,
        current_date: datetime
    ) -> tuple[bool, Optional[str]]:
        """Check if today is a Hawaiian holiday"""
        
        # Check fixed date holidays
        current_month_day = current_date.strftime("%B %d")
        for holiday, date_str in self.hawaiian_holidays.items():
            if date_str == current_month_day:
                return True, holiday
        
        # Check Statehood Day (third Friday in August)
        if current_date.month == 8 and current_date.weekday() == 4:  # Friday
            # Check if it's the third Friday
            day = current_date.day
            if 15 <= day <= 21:
                return True, "Statehood Day"
        
        return False, None
    
    def convert_mainland_to_hawaii(
        self,
        mainland_time: datetime,
        mainland_tz: str = "US/Pacific"
    ) -> datetime:
        """Convert mainland US time to Hawaii time"""
        
        # Create timezone-aware datetime
        mainland_timezone = pytz.timezone(mainland_tz)
        if mainland_time.tzinfo is None:
            mainland_aware = mainland_timezone.localize(mainland_time)
        else:
            mainland_aware = mainland_time
        
        # Convert to Hawaii time
        hawaii_time = mainland_aware.astimezone(self.hawaii_tz)
        
        return hawaii_time
    
    def get_business_hours_status(
        self,
        business_type: str = "standard"
    ) -> Dict[str, Any]:
        """Get detailed business hours status"""
        
        current_time = self.get_current_hawaii_time()
        hours = self.business_hours.get(business_type, self.business_hours["standard"])
        
        is_open = self._is_business_hours(current_time["time"], business_type)
        
        # Calculate time until open/close
        current_minutes = current_time["time"].hour * 60 + current_time["time"].minute
        open_minutes = hours["open"].hour * 60 + hours["open"].minute
        close_minutes = hours["close"].hour * 60 + hours["close"].minute
        
        if is_open:
            minutes_until_close = close_minutes - current_minutes
            status_message = f"Open for {minutes_until_close // 60} hours {minutes_until_close % 60} minutes"
        else:
            if current_minutes < open_minutes:
                minutes_until_open = open_minutes - current_minutes
            else:
                # After closing, calculate time until tomorrow's opening
                minutes_until_open = (24 * 60 - current_minutes) + open_minutes
            
            status_message = f"Closed. Opens in {minutes_until_open // 60} hours {minutes_until_open % 60} minutes"
        
        return {
            "is_open": is_open,
            "current_time": current_time["formatted"],
            "open_time": hours["open"].strftime("%I:%M %p"),
            "close_time": hours["close"].strftime("%I:%M %p"),
            "status_message": status_message,
            "business_type": business_type
        }
    
    def suggest_meeting_times(
        self,
        duration_minutes: int = 30,
        business_type: str = "standard",
        days_ahead: int = 7
    ) -> List[Dict[str, Any]]:
        """Suggest available meeting times in Hawaii timezone"""
        
        suggestions = []
        current_hawaii = datetime.now(self.hawaii_tz)
        hours = self.business_hours.get(business_type, self.business_hours["standard"])
        
        # Standard meeting slots
        meeting_slots = [
            time(9, 0), time(10, 0), time(11, 0),
            time(13, 0), time(14, 0), time(15, 0), time(16, 0)
        ]
        
        # Generate suggestions for next N days
        for day_offset in range(days_ahead):
            check_date = current_hawaii + timedelta(days=day_offset)
            
            # Skip weekends for standard business
            if business_type == "standard" and check_date.weekday() >= 5:
                continue
            
            # Check if it's a holiday
            is_holiday, holiday_name = self._check_hawaiian_holiday(check_date)
            if is_holiday:
                continue
            
            # Add available slots
            for slot in meeting_slots:
                # Ensure slot is within business hours
                if hours["open"] <= slot <= hours["close"]:
                    # For today, only suggest future times
                    if day_offset == 0 and slot <= current_hawaii.time():
                        continue
                    
                    slot_datetime = self.hawaii_tz.localize(
                        datetime.combine(check_date.date(), slot)
                    )
                    
                    suggestions.append({
                        "datetime": slot_datetime,
                        "formatted": slot_datetime.strftime("%A, %B %d at %I:%M %p HST"),
                        "day": slot_datetime.strftime("%A"),
                        "date": slot_datetime.strftime("%Y-%m-%d"),
                        "time": slot_datetime.strftime("%I:%M %p"),
                        "available": True
                    })
        
        return suggestions[:10]  # Return max 10 suggestions
    
    def format_for_display(
        self,
        dt: datetime,
        include_timezone: bool = True,
        relative: bool = False
    ) -> str:
        """Format datetime for display in Hawaiian context"""
        
        # Ensure datetime is in Hawaii timezone
        if dt.tzinfo is None:
            hawaii_dt = self.hawaii_tz.localize(dt)
        else:
            hawaii_dt = dt.astimezone(self.hawaii_tz)
        
        # Base format
        formatted = hawaii_dt.strftime("%B %d, %Y at %I:%M %p")
        
        # Add timezone if requested
        if include_timezone:
            formatted += " HST"
        
        # Add relative time if requested
        if relative:
            now = datetime.now(self.hawaii_tz)
            diff = hawaii_dt - now
            
            if diff.days == 0:
                formatted += " (today)"
            elif diff.days == 1:
                formatted += " (tomorrow)"
            elif diff.days == -1:
                formatted += " (yesterday)"
            elif 0 < diff.days <= 7:
                formatted += f" (in {diff.days} days)"
            elif -7 <= diff.days < 0:
                formatted += f" ({abs(diff.days)} days ago)"
        
        return formatted