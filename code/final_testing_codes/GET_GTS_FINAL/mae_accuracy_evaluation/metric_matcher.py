"""Metric name matching utilities"""
from .normalizer import normalize_metric_name
from .config import METRIC_EQUIVALENTS


def are_metrics_similar(metric1: str, metric2: str) -> bool:
    """Check if two metric names are similar.
    
    Similarity criteria:
    1. Exact match after normalization
    2. One is substring of the other
    3. Both belong to same equivalence group
    
    Args:
        metric1: First metric name
        metric2: Second metric name
        
    Returns:
        True if metrics are similar
    """
    if not metric1 or not metric2:
        return False
    
    norm1 = normalize_metric_name(metric1)
    norm2 = normalize_metric_name(metric2)
    
    # Exact match
    if norm1 == norm2:
        return True
    
    # Substring match (bidirectional)
    if norm1 in norm2 or norm2 in norm1:
        return True
    
    # Check equivalence groups
    for canonical, variants in METRIC_EQUIVALENTS.items():
        norm_variants = [normalize_metric_name(v) for v in variants]
        norm_variants.append(canonical)
        
        if norm1 in norm_variants and norm2 in norm_variants:
            return True
    
    return False


def find_matching_metric(target_metric: str, available_metrics: list) -> str:
    """Find matching metric from available list.
    
    Args:
        target_metric: Metric to find match for
        available_metrics: List of available metric names
        
    Returns:
        Matching metric name or None
    """
    for available in available_metrics:
        if are_metrics_similar(target_metric, available):
            return available
    
    return None
