<CsoundSynthesizer>
<CsOptions>
-odac --nodisplays -m 128
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1
seed 0


gknoteLength init 0 

garvb  init     0
gadel  init     0

// from "Trapped" by Dr. B
instr 1                                      ; p4 = delay send factor
ifreq  =       mtof(p5 * 64 + 48)            ; p5 = freq
                                             ; p6 = amp
k1     expseg  1, p3 * .5, 40, p3 * .5, 2    ; p7 = reverb send factor
k2     expseg  10, p3 * .72, 35, p3 * .28, 6
k3     linen   p6, p3* .333, p3, p3 * .333
k4     randh   k1, k2, .5
a4     oscil   k3, ifreq + (p5 * .05) + k4, 1, .1

k5     linseg  .4, p3 * .9, 26, p3 * .1, 0
k6     linseg  8, p3 * .24, 20, p3 * .76, 2
k7     linen   p6, p3 * .5, p3, p3 * .46
k8     randh   k5, k6, .4
a3     oscil   k7, ifreq + (p5 * .03) + k8, 14, .3

k9     expseg  1, p3 * .7, 50, p3 * .3, 2
k10    expseg  10, p3 * .3, 45, p3 * .7, 6
k11    linen   p6, p3 * .25, p3, p3 * .25
k12    randh   k9, k10, .5
a2     oscil   k11, ifreq + (p5 * .02) + k12, 1, .1

k13    linseg  .4, p3 * .6, 46, p3 * .4, 0
k14    linseg  18, p3 * .1, 50, p3 * .9, 2
k15    linen   p6, p3 * .2, p3, p3 * .3
k16    randh   k13, k14, .8
a1     oscil   k15, ifreq + (p5 * .01) + k16, 14, .3

amix   =       a1 + a2 + a3 + a4
gadel += amix * 0.1
       outs    a1 + a3, a2 + a4
endin

instr 2

ifreq  =       mtof(p5 * 64 + 12) 

ksampleAmp = expseg(1, p3 * 0.5, 50, p3 * 0.5, 5)
ksampleFreq = expseg(5, p3 * 0.88, 23, p3 * 0.12, 12)
kfreq = randh(ksampleAmp, ksampleFreq)
kamp = linen:k(p6, p3*0.33, p3, p3*0.67)
a1 oscil kamp, ifreq + kfreq, 13, .1

ksampleAmp1 = expseg(1, p3 * 0.6, 155, p3 * 0.4, 5)
ksampleFreq1 = expseg(5, p3 * 0.8, 23, p3 * 0.2, 12)
kfreq1 = randh(ksampleAmp1, ksampleFreq1)
kamp1 = linen:k(p6, p3*0.33, p3, p3*0.67)
a2 oscil kamp1, ifreq + kfreq1, 11, .5

ksampleAmp2 = expseg(1, p3 * 0.5, 65, p3 * 0.5, 5)
ksampleFreq2 = expseg(5, p3 * 0.88, 23, p3 * 0.12, 12)
kfreq2 = randh(ksampleAmp2, ksampleFreq2)
kamp2 = linen:k(p6, p3*0.33, p3, p3*0.67)
a3 oscil kamp2, ifreq + kfreq2, 13, .1

ksampleAmp3 = expseg(1, p3 * 0.6, 155, p3 * 0.4, 5)
ksampleFreq3 = expseg(5, p3 * 0.8, 23, p3 * 0.2, 12)
kfreq3 = randh(ksampleAmp3, ksampleFreq3)
kamp3 = linen:k(p6, p3*0.33, p3, p3*0.67)
a4 oscil kamp3, ifreq + kfreq3, 11, .5

amix   =       a1 + a2 + a3 + a4
garvb += amix * 0.1
outs a1 + a3, a2 + a4
endin


instr 3
ifreq   =      mtof(p5 * 124 + 12)                    ; p5 = freq
                                             ; p6 = amp
k2      randh  p4, p7, .1                    ; p7 = reverb send factor
k3      randh  p4 * .98, p7 * .91, .2        ; p8 = rand amp
k4      randh  p4 * 1.2, p7 * .96, .3        ; p9 = rand freq
k5      randh  p4 * .9, p7 * 1.3

kenv    linen  p6, p3 *.1, p3, p3 * .8

a1      oscil  kenv, ifreq + k2, 1, .2
a2      oscil  kenv * .91, (ifreq + .004) + k3, 2, .3
a3      oscil  kenv * .85, (ifreq + .006) + k4, 3, .5
a4      oscil  kenv * .95, (ifreq + .009) + k5, 4, .8

amix    =      a1 + a2 + a3 + a4

        outs   a1 + a3, a2 + a4
garvb   +=      (amix * 0.3)
        endin

instr  4                           ; p5 = FilterSweep StartFreq
ifuncl  =      8                             ; p6 = FilterSweep EndFreq
                                             ; p9 = bandwidth
k1      phasor p4  * 2                       
k2      table  k1 * ifuncl, 19               ; p7 = amp
anoise  rand   2                      ; p4 = pitch
k3      expon  p5 * 10000, p3, 1  
a1      reson  anoise, k3 * k2, k3 / 5 + p7, 1

kenv    linen  p6, .01, p3, .05
asig    =      a1 * kenv

        outs   asig, asig
garvb   +=  (asig * 0.3)
        endin

       // i6   53.3   8.5     0.81   3000     17     10     0.6    1.6

// from "Trapped" by Dr. B
;============================================================================;
;==================================== SMEAR =================================;
;============================================================================;
        instr  98
asig    delay  gadel, .08
        outs   asig, asig
gadel   =      0
        endin
;============================================================================;
;==================================== SWIRL =================================;
;============================================================================;
       instr   99                            ; p4 = panrate
k1     oscil   .5, p4, 1
k2     =       .5 + k1
k3     =       k2 - 1
asig   reverb  garvb, 2.1
       outs    asig * k2, asig * k3
garvb  =       0
       endin

</CsInstruments>
<CsScore>
f1   0  8192  10   1
f2   0  512   10   10  8   0   6   0   4   0   1
f3   0  512   10   10  0   5   5   0   4   3   0   1
f4   0  2048  10   10  0   9   0   0   8   0   7   0  4  0  2  0  1
f5   0  2048  10   5   3   2   1   0
f6   0  2048  10   8   10  7   4   3   1
f7   0  2048  10   7   9   11  4   2   0   1   1
f8   0  2048  10   0   0   0   0   7   0   0   0   0  2  0  0  0  1  1
f9   0  2048  10   10  9   8   7   6   5   4   3   2  1
f10  0  2048  10   10  0   9   0   8   0   7   0   6  0  5
f11  0  2048  10   10  10  9   0   0   0   3   2   0  0  1
f12  0  2048  10   10  0   0   0   5   0   0   0   0  0  3
f13  0  2048  10   10  0   0   0   0   3   1
f14  0  512   9    1   3   0   3   1   0   9  .333   180
f15  0  8192  9    1   1   90
f16  0  2048  9    1   3   0   3   1   0   6   1   0
f17  0  9     5   .1   8   1
f18  0  17    5   .1   10  1   6  .4
f19  0  16    2    1   7   10  7   6   5   4   2   1   1  1  1  1  1  1  1
f20  0  16   -2    0   30  40  45  50  40  30  20  10  5  4  3  2  1  0  0  0
f21  0  16   -2    0   20  15  10  9   8   7   6   5   4  3  2  1  0  0
f22  0  9    -2   .001 .004 .007 .003 .002 .005 .009 .006

i 98 0 36000
i 99 0 36000 1
</CsScore>
</CsoundSynthesizer>