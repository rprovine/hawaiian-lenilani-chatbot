import { format, formatInTimeZone, toDate } from 'date-fns-tz';
import { addDays, setHours, setMinutes } from 'date-fns';

const HAWAII_TIMEZONE = 'Pacific/Honolulu';

export const hawaiianTimeUtils = {
  // Get current time in Hawaii
  getCurrentHawaiiTime: (): Date => {
    return toDate(new Date(), { timeZone: HAWAII_TIMEZONE });
  },

  // Format time for display
  formatHawaiiTime: (date: Date, formatStr: string = 'h:mm a zzz'): string => {
    return formatInTimeZone(date, HAWAII_TIMEZONE, formatStr);
  },

  // Get time of day period
  getTimeOfDay: (): 'morning' | 'afternoon' | 'evening' | 'night' => {
    const hour = parseInt(formatInTimeZone(new Date(), HAWAII_TIMEZONE, 'H'));
    
    if (hour >= 5 && hour < 10) return 'morning';
    if (hour >= 10 && hour < 17) return 'afternoon';
    if (hour >= 17 && hour < 20) return 'evening';
    return 'night';
  },

  // Get appropriate greeting
  getGreeting: (): { hawaiian: string; english: string; pidgin: string } => {
    const timeOfDay = hawaiianTimeUtils.getTimeOfDay();
    
    const greetings = {
      morning: {
        hawaiian: 'Aloha kakahiaka',
        english: 'Good morning',
        pidgin: 'Howzit! Early yeah?'
      },
      afternoon: {
        hawaiian: 'Aloha awakea',
        english: 'Good afternoon',
        pidgin: 'Howzit! Hot one today!'
      },
      evening: {
        hawaiian: 'Aloha ahiahi',
        english: 'Good evening',
        pidgin: 'Pau hana time!'
      },
      night: {
        hawaiian: 'Aloha pō',
        english: 'Good night',
        pidgin: 'Late night, yeah?'
      }
    };
    
    return greetings[timeOfDay];
  },

  // Check if business hours
  isBusinessHours: (): boolean => {
    const hour = parseInt(formatInTimeZone(new Date(), HAWAII_TIMEZONE, 'H'));
    const day = parseInt(formatInTimeZone(new Date(), HAWAII_TIMEZONE, 'i')); // 1-7, Monday is 1
    
    // Monday-Friday, 8 AM - 5 PM
    return day >= 1 && day <= 5 && hour >= 8 && hour < 17;
  },

  // Get next business day
  getNextBusinessDay: (): Date => {
    let nextDay = addDays(new Date(), 1);
    const day = parseInt(formatInTimeZone(nextDay, HAWAII_TIMEZONE, 'i'));
    
    // If Saturday (6), add 2 days to get to Monday
    // If Sunday (7), add 1 day to get to Monday
    if (day === 6) nextDay = addDays(nextDay, 2);
    else if (day === 7) nextDay = addDays(nextDay, 1);
    
    // Set to 9 AM Hawaii time
    return setMinutes(setHours(nextDay, 9), 0);
  },

  // Hawaiian holidays
  isHawaiianHoliday: (date: Date): { isHoliday: boolean; name?: string } => {
    const monthDay = format(date, 'MM-dd');
    const holidays: Record<string, string> = {
      '03-26': 'Prince Kuhio Day',
      '06-11': 'King Kamehameha Day',
      '05-01': 'Lei Day',
    };
    
    if (holidays[monthDay]) {
      return { isHoliday: true, name: holidays[monthDay] };
    }
    
    // Check for Statehood Day (3rd Friday in August)
    const month = date.getMonth();
    const dayOfWeek = date.getDay();
    const dayOfMonth = date.getDate();
    
    if (month === 7 && dayOfWeek === 5 && dayOfMonth >= 15 && dayOfMonth <= 21) {
      return { isHoliday: true, name: 'Statehood Day' };
    }
    
    return { isHoliday: false };
  },

  // Format relative time
  getRelativeTimeString: (date: Date): string => {
    const now = new Date();
    const diffInHours = Math.floor((date.getTime() - now.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 0) {
      return 'past';
    } else if (diffInHours === 0) {
      return 'within the hour';
    } else if (diffInHours < 24) {
      return `in ${diffInHours} hour${diffInHours !== 1 ? 's' : ''}`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `in ${diffInDays} day${diffInDays !== 1 ? 's' : ''}`;
    }
  },

  // Get cultural time context
  getCulturalTimeContext: (): string => {
    const timeOfDay = hawaiianTimeUtils.getTimeOfDay();
    const isBusinessHours = hawaiianTimeUtils.isBusinessHours();
    
    const contexts = {
      morning: {
        business: 'Perfect time to start fresh with new opportunities!',
        nonBusiness: 'Early bird gets the worm! Great time for planning.',
      },
      afternoon: {
        business: 'Productive afternoon! Let\'s make progress together.',
        nonBusiness: 'Afternoon is perfect for big decisions.',
      },
      evening: {
        business: 'Wrapping up the day? Let\'s plan for tomorrow\'s success!',
        nonBusiness: 'Evening reflection time - perfect for strategic thinking.',
      },
      night: {
        business: 'Burning the midnight oil? Respect the hustle!',
        nonBusiness: 'Late night planning session - dedication!',
      },
    };
    
    return contexts[timeOfDay][isBusinessHours ? 'business' : 'nonBusiness'];
  },
};

export default hawaiianTimeUtils;