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
 iPch random 60, 72
 chnset iPch, "pch"
 kPch init iPch
 kNewPch chnget "new_pitch"
 if kNewPch > 0 then
  kPch = kNewPch
 endif
 aTone poscil .2, mtof(kPch)
 out aTone, aTone
endin

</CsInstruments>
<CsScore>
i 1 0 600
</CsScore>
</CsoundSynthesizer>