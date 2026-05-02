from src.detectors.redundant_sload import detect as detect_redundant_sload
from src.detectors.unoptimized_loop import detect as detect_unoptimized_loop
from src.detectors.string_vs_bytes32 import detect as detect_string_vs_bytes32
from src.detectors.public_vs_external import detect as detect_public_vs_external
from src.detectors.unchecked_arithmetic import detect as detect_unchecked_arithmetic
from src.detectors.dead_code import detect as detect_dead_code

ALL_DETECTORS = [
    ('redundant_sload',       detect_redundant_sload),
    ('unoptimized_loop',      detect_unoptimized_loop),
    ('string_vs_bytes32',     detect_string_vs_bytes32),
    ('public_vs_external',    detect_public_vs_external),
    ('unchecked_arithmetic',  detect_unchecked_arithmetic),
    ('dead_code',             detect_dead_code),
]
