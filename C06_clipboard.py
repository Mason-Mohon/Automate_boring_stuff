TEXT = {
    'agree':"""Yes, I agree. That sounds fine to me.""",
    'busy':"""Sorry, can we do this later this week or next week?""",
    'excuse':"""Apologies for the delay—our project's scalar waveform orthogonality index\n encountered an unforeseen phase-transient recursion within the hyperconductive mesh buffer,\n causing a cascade of stochastic eigenvalue realignments\n across the core multiplexing fabric. This led to a temporal desynchronization in\n the quantum-inverted feedback loop, which, despite extensive entropic normalization,\n failed to converge before system level watchdog protocols\n initiated a full-spectrum recalibration. We're currently rerouting the nanosecond-scale\n flux coefficients through a secondary subraster to restore nominal throughput."""
}

import sys, pyperclip
if len(sys.argv) < 2:
    print('Usage: py mclip.py [keyphrase] - copy phrase text')
    sys.exit()

keyphrase = sys.argv[1]

if keyphrase in TEXT:
    pyperclip.copy(TEXT[keyphrase])
    print(f'Text for {keyphrase} copied to clipboard.')
else:
    print('There is no text for ' + keyphrase)