#!/usr/bin/env python3
"""
Script to help analyze Render logs for rate limit and error patterns
Run this script after downloading logs from Render dashboard
"""
import re
import json
from collections import Counter, defaultdict
from datetime import datetime
import sys

def analyze_log_file(log_file_path):
    """Analyze log file for error patterns"""
    
    # Patterns to look for
    patterns = {
        'rate_limit_429': r'429|rate.?limit',
        'overloaded_529': r'529|overloaded',
        'api_error': r'Error.*Claude|Error.*Anthropic|Error routing to Claude',
        'timeout': r'timeout|timed out',
        'connection_error': r'connection.*error|refused|ECONNREFUSED',
        'fallback_response': r'fallback_response|technical difficulties',
        'claude_init_error': r'Failed to initialize Claude client',
        'no_api_key': r'ANTHROPIC_API_KEY not found',
        'busy_message': r'stay busy|system stay busy',
        'non_retryable': r'Non-retryable error',
        'max_retries': r'Max retries exceeded',
        'token_limit': r'token.*limit|daily.*limit'
    }
    
    # Time patterns
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    
    # Initialize counters
    error_counts = Counter()
    error_times = defaultdict(list)
    error_examples = defaultdict(list)
    total_lines = 0
    
    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                
                # Extract timestamp if present
                time_match = re.search(time_pattern, line)
                timestamp = time_match.group(1) if time_match else None
                
                # Check each pattern
                for error_type, pattern in patterns.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        error_counts[error_type] += 1
                        if timestamp:
                            error_times[error_type].append(timestamp)
                        if len(error_examples[error_type]) < 3:  # Keep first 3 examples
                            error_examples[error_type].append(line.strip()[:200])
    
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found")
        return None
    
    # Analyze results
    results = {
        'total_lines': total_lines,
        'error_counts': dict(error_counts),
        'error_examples': dict(error_examples),
        'error_times': dict(error_times),
        'analysis': {}
    }
    
    # Calculate error rates
    if total_lines > 0:
        for error_type, count in error_counts.items():
            results['analysis'][error_type] = {
                'count': count,
                'percentage': round((count / total_lines) * 100, 2),
                'frequency': f"1 every {total_lines // count if count > 0 else 0} lines"
            }
    
    # Find peak error times
    all_error_times = []
    for times in error_times.values():
        all_error_times.extend(times)
    
    if all_error_times:
        # Group by hour
        hour_counts = Counter()
        for time_str in all_error_times:
            try:
                dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                hour_counts[dt.hour] += 1
            except:
                pass
        
        results['peak_hours'] = dict(hour_counts.most_common(5))
    
    return results


def print_analysis(results):
    """Print analysis results in a readable format"""
    print("\n" + "="*60)
    print("🌺 Hawaiian Chatbot Log Analysis Report")
    print("="*60)
    
    print(f"\n📊 Total lines analyzed: {results['total_lines']:,}")
    
    print("\n🚨 Error Summary:")
    print("-"*40)
    
    error_priorities = [
        ('rate_limit_429', '⚠️  Rate Limit (429)', 'Critical - Users getting blocked'),
        ('overloaded_529', '🔥 Overloaded (529)', 'Critical - API overloaded'),
        ('busy_message', '💬 Busy Messages', 'User-facing error messages'),
        ('api_error', '❌ API Errors', 'Claude API errors'),
        ('timeout', '⏱️  Timeouts', 'Request timeouts'),
        ('connection_error', '🔌 Connection Errors', 'Network issues'),
        ('claude_init_error', '🚫 Init Errors', 'Claude client initialization'),
        ('no_api_key', '🔑 No API Key', 'Missing API key'),
        ('fallback_response', '🔄 Fallbacks', 'Using fallback responses'),
        ('non_retryable', '❗ Non-retryable', 'Permanent errors'),
        ('max_retries', '🔁 Max Retries', 'Exhausted retry attempts'),
        ('token_limit', '🎯 Token Limits', 'Daily token limits')
    ]
    
    for error_key, display_name, description in error_priorities:
        if error_key in results['error_counts'] and results['error_counts'][error_key] > 0:
            count = results['error_counts'][error_key]
            analysis = results['analysis'].get(error_key, {})
            print(f"\n{display_name}: {count} occurrences ({analysis.get('percentage', 0)}%)")
            print(f"  └─ {description}")
            print(f"  └─ Frequency: {analysis.get('frequency', 'N/A')}")
            
            # Show examples
            if error_key in results['error_examples']:
                print("  └─ Examples:")
                for i, example in enumerate(results['error_examples'][error_key][:2], 1):
                    print(f"     {i}. {example}")
    
    # Peak hours analysis
    if 'peak_hours' in results and results['peak_hours']:
        print("\n⏰ Peak Error Hours (24-hour format):")
        print("-"*40)
        for hour, count in sorted(results['peak_hours'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {hour:02d}:00 - {count} errors")
    
    # Recommendations
    print("\n💡 Recommendations:")
    print("-"*40)
    
    recommendations = []
    
    if results['error_counts'].get('rate_limit_429', 0) > 10:
        recommendations.append("🔴 HIGH PRIORITY: Frequent rate limiting detected!")
        recommendations.append("   - Check current Anthropic tier and upgrade if needed")
        recommendations.append("   - Implement request queuing or throttling")
        recommendations.append("   - Add longer delays between requests")
    
    if results['error_counts'].get('overloaded_529', 0) > 5:
        recommendations.append("🔴 HIGH PRIORITY: API overload errors detected!")
        recommendations.append("   - Implement exponential backoff")
        recommendations.append("   - Consider using multiple API keys")
        recommendations.append("   - Add circuit breaker pattern")
    
    if results['error_counts'].get('timeout', 0) > 20:
        recommendations.append("🟡 MEDIUM: Timeout issues detected")
        recommendations.append("   - Increase timeout settings")
        recommendations.append("   - Optimize prompt length")
        recommendations.append("   - Consider response streaming")
    
    if results['error_counts'].get('no_api_key', 0) > 0:
        recommendations.append("🔴 CRITICAL: Missing API key detected!")
        recommendations.append("   - Verify ANTHROPIC_API_KEY is set in Render environment")
        recommendations.append("   - Check for typos in environment variable name")
    
    if results['error_counts'].get('token_limit', 0) > 0:
        recommendations.append("🟡 Token limits being hit")
        recommendations.append("   - Monitor daily token usage")
        recommendations.append("   - Implement token counting before requests")
        recommendations.append("   - Consider upgrading tier for more tokens")
    
    if not recommendations:
        recommendations.append("✅ No critical issues detected in the logs")
    
    for rec in recommendations:
        print(rec)
    
    # Summary
    total_errors = sum(results['error_counts'].values())
    error_rate = (total_errors / results['total_lines'] * 100) if results['total_lines'] > 0 else 0
    
    print(f"\n📈 Overall Error Rate: {error_rate:.2f}%")
    print(f"   Total Errors: {total_errors:,}")
    print(f"   Total Lines: {results['total_lines']:,}")
    
    print("\n" + "="*60)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python check_render_logs.py <log_file>")
        print("\nHow to get logs from Render:")
        print("1. Go to your Render dashboard")
        print("2. Click on your service (hawaiian-chatbot-api)")
        print("3. Click 'Logs' tab")
        print("4. Click 'Download logs' button")
        print("5. Save the file and run: python check_render_logs.py <downloaded_file>")
        return
    
    log_file = sys.argv[1]
    results = analyze_log_file(log_file)
    
    if results:
        print_analysis(results)
        
        # Save detailed results
        output_file = log_file.replace('.log', '_analysis.json').replace('.txt', '_analysis.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Detailed analysis saved to: {output_file}")


if __name__ == "__main__":
    main()