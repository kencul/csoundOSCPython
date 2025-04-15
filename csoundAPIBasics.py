import ctcsound
import sys

# Step 1: Create csound instance
cs = ctcsound.Csound()

# Step 2: Compile CSD from text or file
csd ='''
<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1
seed 0

instr 1
 kFreq chnget "pitch"
 aTone poscil .2, kFreq
 out aTone, aTone
endin

</CsInstruments>
<CsScore>
</CsScore>
</CsoundSynthesizer>'''
result = cs.compile_csd(csd, 1)

if result != ctcsound.CSOUND_SUCCESS:
    print(f"Error compiling csd!", file=sys.stderr)
    sys.exit(1)

# Step 3: Start the engine    
result = cs.start()

if result != ctcsound.CSOUND_SUCCESS:
    print(f"Error starting Csound!", file=sys.stderr)
    sys.exit(1)

# Step 4: interact with Csound
# Sending events (score statements)
cs.event_string("i1 0 2")
cs.event_string("e 2")
# Controlling channels
cs.set_control_channel("pitch", 880)
# Get audio buffers
inBuff = cs.spin()
outBuff = cs.spout()
# Get ftable
table = cs.table(1)

# Step 5: Compute audio blocks
while cs.perform_ksmps() == ctcsound.CSOUND_SUCCESS:
    continue

sys.exit()