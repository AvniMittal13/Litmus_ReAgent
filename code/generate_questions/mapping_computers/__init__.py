"""
Mapping computers for each scenario.
Each scenario has different logic for computing language-model mappings.
"""
from .scenario1 import compute_scenario1_mapping
from .scenario2 import compute_scenario2_mapping
from .scenario3 import compute_scenario3_mapping
from .scenario4 import compute_scenario4_mapping
from .scenario5 import compute_scenario5_mapping

__all__ = [
    'compute_scenario1_mapping',
    'compute_scenario2_mapping',
    'compute_scenario3_mapping',
    'compute_scenario4_mapping',
    'compute_scenario5_mapping',
]
