import os
from graphviz import Digraph


class GraphGenerator:
    @staticmethod
    def generate(path="assets/turing_graph"):
        os.makedirs("assets", exist_ok=True)

        dot = Digraph("Maquina_Turing_Suma_Binaria", format="png")
        dot.attr(rankdir="LR", bgcolor="#101014")
        dot.attr("node", shape="circle", style="filled", color="white",
                 fontcolor="white", fillcolor="#20202a")
        dot.attr("edge", color="white", fontcolor="white")

        dot.node("inicio", shape="point", fillcolor="white")
        dot.node("q_seek_end", "q_seek_end\nBuscar fin")
        dot.node("q_check_right", "q_check_right\nRevisar B")
        dot.node("q_check_found_one", "q_check_found_one\nB > 0")
        dot.node("q_check_zero", "q_check_zero\nB = 0")
        dot.node("q_dec_borrow", "q_dec_borrow\nB = B - 1")
        dot.node("q_seek_plus", "q_seek_plus\nBuscar +")
        dot.node("q_inc_carry", "q_inc_carry\nA = A + 1")
        dot.node("q_cleanup", "q_cleanup\nLimpiar cinta")
        dot.node("qf", "qf\nAcepta", shape="doublecircle", fillcolor="#003d1f")
        dot.node("qr", "qr\nRechaza", shape="doublecircle", fillcolor="#4a0000")

        dot.edge("inicio", "q_seek_end")
        dot.edge("q_seek_end", "q_seek_end", label="0,1,+ / mismo,R")
        dot.edge("q_seek_end", "q_check_right", label="□/□,L")

        dot.edge("q_check_right", "q_check_right", label="0/0,L")
        dot.edge("q_check_right", "q_check_found_one", label="1/1,N")
        dot.edge("q_check_right", "q_check_zero", label="+/+,N")

        dot.edge("q_check_found_one", "q_dec_borrow", label="Ir al final y decrementar B")
        dot.edge("q_dec_borrow", "q_dec_borrow", label="0/1,L")
        dot.edge("q_dec_borrow", "q_seek_plus", label="1/0,N")

        dot.edge("q_seek_plus", "q_seek_plus", label="0,1 / mismo,L")
        dot.edge("q_seek_plus", "q_inc_carry", label="+/+,L")

        dot.edge("q_inc_carry", "q_inc_carry", label="1/0,L")
        dot.edge("q_inc_carry", "q_seek_end", label="0/1,N")
        dot.edge("q_inc_carry", "q_seek_end", label="□/1,N")

        dot.edge("q_check_zero", "q_cleanup", label="Limpiar +000")
        dot.edge("q_cleanup", "q_cleanup", label="+,0 / □,R")
        dot.edge("q_cleanup", "qf", label="□/□,N")

        dot.edge("inicio", "qr", label="Entrada inválida")

        return dot.render(path, cleanup=True)