from manim import *

class MyScene(Scene):
    def construct(self):
        question = Text("Solve the quadratic equation", font_size=25)
        question.to_edge(UP, buff=0.5)
        self.play(FadeIn(question, shift=UP))
        self.wait(2)

        if len(question.text) > 15:
            question2 = Text("3(x-2)^2 - 4(x+1) = 5x + 6 for x.", font_size=25)
            question2.next_to(question, DOWN)
            self.play(FadeIn(question2, shift=UP))
            self.wait(2)

        x_axis = NumberLine(x_range=[-5, 5], length=10, include_tip=False)
        x_axis.move_to(ORIGIN)
        self.play(Create(x_axis))

        x_point = Dot(point=x_axis.number_to_point(0), radius=0.05)
        x_point_label = Text("x", font_size=25)
        x_point_label.next_to(x_point, DOWN)
        self.play(Create(x_point), Create(x_point_label))

        quad_expr = MathTex("3(x-2)^2")
        quad_expr.next_to(x_axis, UP, buff=0.5)
        self.play(FadeIn(quad_expr, shift=UP))

        expanded_quad_expr = MathTex("3(x^2 - 4x + 4)")
        expanded_quad_expr.next_to(quad_expr, DOWN)
        self.play(Transform(quad_expr, expanded_quad_expr))

        simplified_expr = MathTex("3x^2 - 12x + 12 - 4x - 4")
        simplified_expr.next_to(expanded_quad_expr, DOWN)
        self.play(Transform(expanded_quad_expr, simplified_expr))

        lhs_expr = MathTex("3x^2 - 16x + 8")
        lhs_expr.next_to(simplified_expr, DOWN)
        self.play(Transform(simplified_expr, lhs_expr))

        rhs_expr = MathTex("5x + 6")
        rhs_expr.next_to(lhs_expr, RIGHT)
        self.play(FadeIn(rhs_expr, shift=RIGHT))

        rearranged_expr = MathTex("3x^2 - 21x - 2 = 0")
        rearranged_expr.next_to(lhs_expr, DOWN)
        self.play(Transform(lhs_expr, rearranged_expr), FadeOut(rhs_expr))

        factored_expr = MathTex("(3x + 1)(x - 2) = 0")
        factored_expr.next_to(rearranged_expr, DOWN)
        self.play(Transform(rearranged_expr, factored_expr))

        solution = Text("x = -1/3 or x = 2", font_size=25)
        solution.to_edge(UP, buff=0.5)
        self.play(FadeIn(solution, shift=UP))

        self.wait(2)
        self.play(FadeOut(question), FadeOut(question2) if 'question2' in locals() else None, FadeOut(x_axis), FadeOut(x_point), FadeOut(x_point_label), FadeOut(quad_expr), FadeOut(expanded_quad_expr), FadeOut(simplified_expr), FadeOut(lhs_expr), FadeOut(rhs_expr), FadeOut(rearranged_expr), FadeOut(factored_expr), FadeOut(solution))