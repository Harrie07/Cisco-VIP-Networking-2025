def generate_summary_report(data):
    """Generate summary statistics from analysis data"""
    return {
        'total_devices': len(data.get('devices', {})),
        'analysis_timestamp': data.get('timestamp', 'Unknown'),
        'health_score': data.get('validation_summary', {}).get('overall_score', 0)
    }
