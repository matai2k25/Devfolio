from manim import *

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Question text
        question = Text("Solve the linear equation", font_size=25)
        question.to_edge(UP, buff=0.5)
        self.play(FadeIn(question, shift=UP))
        self.wait(0.5)

        question2 = Text("2x + 5 = 0 for the variable x.", font_size=25)
        question2.next_to(question, DOWN, buff=0.2)
        self.play(FadeIn(question2, shift=UP))
        self.wait(0.5)

        question3 = Text("Given data: 2x + 5 = 0.", font_size=25)
        question3.next_to(question2, DOWN, buff=0.2)
        self.play(FadeIn(question3, shift=UP))
        self.wait(0.5)

        question4 = Text("What needs to be solved: find the value of x that satisfies the equation.", font_size=25)
        question4.next_to(question3, DOWN, buff=0.2)
        self.play(FadeIn(question4, shift=UP))
        self.wait(2)

        self.play(FadeOut(VGroup(question, question2, question3, question4), shift=UP))

        # Number line
        number_line = NumberLine(x_range=[-3, 0, 1], length=10, include_tip=True)
        number_line.move_to(ORIGIN)
        self.play(Create(number_line))

        # Point and label
        point = Dot(point=(-2.5, 0, 0), radius=0.05)
        point_label = Text("-2.5", font_size=25)
        point_label.next_to(point, DOWN)
        self.play(Create(point), Create(point_label))

        # Red "X" marker
        x_marker = Text("X", font_size=25, color=RED)
        x_marker.next_to(point, UP)
        self.play(Create(x_marker))

        # Equation box
        equation_box = Rectangle(width=4, height=2, fill_opacity=0.5, fill_color=WHITE)
        equation_box.move_to(ORIGIN)
        equation = Text("2x + 5 = 0", font_size=25)
        equation.move_to(equation_box.get_center())
        self.play(Create(equation_box), Create(equation))

        # Solution
        solution = Text("x = -2.5", font_size=25)
        solution.to_edge(UP, buff=0.5)
        self.play(FadeIn(solution, shift=UP))
        self.wait(2)

        self.play(FadeOut(VGroup(number_line, point, point_label, x_marker, equation_box, equation, solution), shift=DOWN))