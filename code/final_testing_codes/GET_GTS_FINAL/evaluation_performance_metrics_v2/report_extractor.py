"""
Module to extract report content from response.md files.
"""
import json
from pathlib import Path
from typing import Dict, Optional


def extract_report_text(report_file: Path) -> Optional[str]:
    """
    Extract report text from response.md file.
    
    Args:
        report_file: Path to response.md file
    
    Returns:
        Report text string if found, None otherwise
    """
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report_text = f.read()
        
        if not report_text or len(report_text.strip()) == 0:
            print(f"Warning: Empty report in {report_file.name}")
            return None
        
        return report_text
        
    except Exception as e:
        print(f"Error reading {report_file.name}: {e}")
        return None


def extract_all_reports(report_files: Dict[str, Optional[Path]]) -> Dict[str, Optional[str]]:
    """
    Extract original_report text for all report files.
    
    Args:
        report_files: Dict mapping {unique_id: report_file_path}
    
    Returns:
        Dict mapping {unique_id: report_text} (text is None if extraction failed)
    """
    reports = {}
    
    for unique_id, report_file in report_files.items():
        if report_file is None:
            reports[unique_id] = None
            continue
        
        report_text = extract_report_text(report_file)
        reports[unique_id] = report_text
    
    # Print summary
    extracted_count = sum(1 for text in reports.values() if text is not None)
    total_count = len(reports)
    print(f"Extracted reports for {extracted_count}/{total_count} questions")
    
    return reports
