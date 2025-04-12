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
 
 kX chnget "x"
 if kX > 0 then
  kWavetable = portk(kX, 0.1)
 endif
 
 kVib init 0
 kNewVib chnget "vib"
 if kNewVib > 0 then
    kVib = portk(kNewVib, 0.1)
 endif
 
 kLFO poscil kVib, kVib* 10
 kModPitch = mtof(iPch) + (kLFO * mtof(iPch) * 0.5)
 aTone poscil .2, kModPitch
 aSaw vco2 .2, kModPitch
 aOut = aTone * (1-kWavetable) + aSaw * (kWavetable)
 aOutL, aOutR = pan2(aOut, kLFO/2*kVib + 0.5)
 out aOutL, aOutR
endin

</CsInstruments>
<CsScore>
i 1 0 60000
</CsScore>
</CsoundSynthesizer>