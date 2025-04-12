from manim import *
from scipy.integrate import solve_ivp
import numpy as np
import ctcsound

# CALCULATING LORENZ EQUATION
def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

# MANIM ANIMATION
class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            x_length=12,
            y_length=12,
            z_length=5,
        )
        # axes.set_width(pixel_width)
        axes.center()
        # axes.shift(OUT)

        # self.camera.reorient(43, 76, 1, IN, 10)
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        # self.camera.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
        self.add(axes)

        # Add the equations
        equations = MathTex(
            R"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & =\sigma(y-x) \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & =x(\rho-z)-y \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & =x y-\beta z
            \end{aligned}
            """,
            # TODO: fix color mapping on latex
            # tex_to_color_map={
            #     "x": RED,
            #     "y": GREEN,
            #     "z": BLUE,
            # },
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(equations)
        equations.to_corner(UL)
        # equations.set_backstroke()
        self.play(Write(equations), run_time = 1)

        # # Compute a set of solutions
        epsilon = 1e-5
        evolution_time = 30
        n_points = 1
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([PURPLE_A, BLUE_A], len(states)) # gradient color of each state

        # save point values to send to csound
        all_trajectories = []
        
        curves = VGroup()
        
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            all_trajectories.append(points)
            curve = VMobject().set_points_smoothly(axes.c2p(points))#axes.c2p(*points.T))
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)
        
        self.generateAudio(all_trajectories, "output.wav", evolution_time)

        curves.set_stroke(width=2, opacity=1)

        # Display dots moving along those trajectories
        # NOT GLOW DOTS LIKE IN EXAMPLE SO IMPOSSIBLE TO SEE
        dots = Group(*[Dot(color=color) for color in colors])

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)
        self.add(dots)

        tail = VGroup(
            TracedPath(dot.get_center, dissipating_time=1.5).match_color(dot)
            for dot in dots
        )

        self.add(tail)
        curves.set_opacity(0)
        self.play(
            *(
                Create(curve, rate_func=linear)
                for curve in curves
            ),
            run_time=evolution_time,
        )
        
    # CSOUND AUDIO OUTPUT
    def generateAudio(self, all_points, outputFile, evoTime):
        cs = ctcsound.Csound()
        csd = f'''
        <CsoundSynthesizer>
        <CsOptions>
        -ooutput.wav -W
        </CsOptions>
        <CsInstruments>
        sr = 44100
        ksmps = 64
        nchnls = 2
        0dbfs = 1
        seed 0

        gkx[] init 10
        gky[] init 10
        gkz[] init 10

        instr 1
        ; Convert point data to audio parameters
        gkx[p4] = port:k(p5, 0.01, -1)
        gky[p4] = port:k(p6, 0.01, -1)
        gkz[p4] = port:k(p7, 0.01, -1)
        endin

        instr 2
        ; Map coordinates to frequency (x), amplitude (y), and filter (z)
        kfreq = gkz[p4] * 440 * 5
        kamp = abs(gky[p4])/2 + 0.5
        kcutoff = abs(gkx[p4]) * 22000
        
        ; Generate sound
        asig = vco2(kamp, kfreq)
        asig = moogladder(asig, kcutoff, 0.5)
        outs asig, asig
        endin

        </CsInstruments>
        <CsScore>
        i2 0 31 0
        '''
        
        # Calculate time step between points
        dt = evoTime / len(all_points[0])
        
        # Add note events for each point in each trajectory
        for i, points in enumerate(all_points):
            for t, (x, y, z) in enumerate(points):
                if(t%1 != 0):
                    pass
                # Scale coordinates to reasonable audio ranges
                scaled_x = x / 50.0
                scaled_y = y / 50.0
                scaled_z = z / 50.0
                        #   time     len  pnt# x-val      y-val       z-val
                csd += f"i1 {t*dt+1} {dt} {i} {scaled_x} {scaled_y} {scaled_z}\n"
        
        csd += f"e {evoTime}\n"
        csd += "</CsScore>\n</CsoundSynthesizer>"
        with open("lorenz.csd", "w") as f:
            f.write(csd)
        
        # Compile and render Csound
        cs.compile_csd(csd, 1)
        res = cs.start()
        # compute audio blocks
        while res == ctcsound.CSOUND_SUCCESS:
            res = cs.perform_ksmps()
        return
        
# After rendering the animation, combine with audio:
# manim -ql -i lorenzCsound.py LorenzAttractor
# Then use ffmpeg to combine video and audio:
# ffmpeg -i media/videos/lorenzCsound/480p15/LorenzAttractor.mp4 -i output.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4