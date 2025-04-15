from manim import *
from scipy.integrate import solve_ivp

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
        self.play(Write(equations))

        # # Compute a set of solutions
        epsilon = 1e-5
        evolution_time = 60
        n_points = 10
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([PURPLE_E, BLUE_E], len(states)) # gradient color of each state

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(axes.c2p(points))#axes.c2p(*points.T))
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)

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