from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QTextEdit, QMessageBox, QScrollArea, QTabWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from turing_machine import TuringMachine
from binary_validator import BinaryValidator
from graph_generator import GraphGenerator
from evidence_exporter import EvidenceExporter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.machine = TuringMachine()
        self.current_step = 0

        self.setWindowTitle("Proyecto Final - Máquina de Turing para Suma y Resta Binaria")
        self.setMinimumSize(1250, 780)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #101014;
                color: #e8e8e8;
            }

            QLabel {
                color: #e8e8e8;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #1d1d24;
                color: white;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
            }

            QPushButton {
                background-color: #20202a;
                color: white;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #30303d;
                border: 1px solid #888;
            }

            QTableWidget {
                background-color: #17171d;
                color: white;
                gridline-color: #444;
                border: 1px solid #333;
            }

            QHeaderView::section {
                background-color: #22222c;
                color: white;
                padding: 6px;
                border: 1px solid #444;
            }

            QTextEdit {
                background-color: #17171d;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }

            QTabWidget::pane {
                border: 1px solid #333;
            }

            QTabBar::tab {
                background: #20202a;
                color: white;
                padding: 10px;
                border: 1px solid #444;
            }

            QTabBar::tab:selected {
                background: #30303d;
                border-bottom: 2px solid #00e676;
            }
        """)

        self.build_ui()

    def build_ui(self):
        central = QWidget()
        root_layout = QVBoxLayout()

        title = QLabel("Simulador de Máquina de Turing para Suma y Resta Binaria")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root_layout.addWidget(title)

        subtitle = QLabel("Proyecto Final - Teoría Matemática de la Computación")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 15px; color: #bbbbbb;")
        root_layout.addWidget(subtitle)

        input_layout = QHBoxLayout()

        self.input_expression = QLineEdit()
        self.input_expression.setPlaceholderText("Ejemplo: 101+11 o 101-10")

        btn_run = QPushButton("Ejecutar completo")
        btn_run.clicked.connect(self.run_full)

        btn_step = QPushButton("Paso a paso")
        btn_step.clicked.connect(self.run_step)

        btn_reset = QPushButton("Reiniciar")
        btn_reset.clicked.connect(self.reset_view)

        input_layout.addWidget(QLabel("Entrada:"))
        input_layout.addWidget(self.input_expression)
        input_layout.addWidget(btn_run)
        input_layout.addWidget(btn_step)
        input_layout.addWidget(btn_reset)

        root_layout.addLayout(input_layout)

        self.stats_label = QLabel(
            "Pasos: 0 | Movimientos: 0 | Estado final: --- | Aceptada: ---"
        )
        self.stats_label.setStyleSheet("font-size: 15px; color: #ffcc00;")
        root_layout.addWidget(self.stats_label)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.simulation_tab(), "Simulación")
        self.tabs.addTab(self.grammar_tab(), "Gramática y lenguaje")
        self.tabs.addTab(self.transitions_tab(), "Tabla y δ")
        self.tabs.addTab(self.graph_tab(), "Grafo")
        self.tabs.addTab(self.evidence_tab(), "Evidencia")

        root_layout.addWidget(self.tabs)

        central.setLayout(root_layout)
        self.setCentralWidget(central)

    def simulation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel("Resultado: ---")
        self.result_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00e676;")
        layout.addWidget(self.result_label)

        self.state_label = QLabel("Estado actual: ---")
        self.state_label.setStyleSheet("font-size: 16px; color: #ffcc00;")
        layout.addWidget(self.state_label)

        tape_title = QLabel("Cinta de la Máquina de Turing")
        tape_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(tape_title)

        self.tape_container = QHBoxLayout()
        self.tape_widget = QWidget()
        self.tape_widget.setLayout(self.tape_container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.tape_widget)
        scroll.setFixedHeight(120)
        layout.addWidget(scroll)

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)
        self.detail_box.setFixedHeight(150)
        layout.addWidget(self.detail_box)

        self.steps_table = QTableWidget()
        self.steps_table.setColumnCount(7)
        self.steps_table.setHorizontalHeaderLabels([
            "Paso", "Estado", "Lee", "Escribe", "Movimiento", "Cinta", "Descripción"
        ])
        self.steps_table.horizontalHeader().setStretchLastSection(True)
        self.steps_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.steps_table)

        tab.setLayout(layout)
        return tab

    def grammar_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.grammar_box = QTextEdit()
        self.grammar_box.setReadOnly(True)
        self.grammar_box.setText(BinaryValidator.grammar_text())

        layout.addWidget(self.grammar_box)
        tab.setLayout(layout)
        return tab

    def transitions_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.transitions_box = QTextEdit()
        self.transitions_box.setReadOnly(True)
        self.transitions_box.setText(self.build_transition_text())

        layout.addWidget(self.transitions_box)
        tab.setLayout(layout)
        return tab

    def graph_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        btn_generate = QPushButton("Generar grafo de estados")
        btn_generate.clicked.connect(self.show_graph)

        self.graph_label = QLabel("Presiona el botón para generar el grafo.")
        self.graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(btn_generate)
        layout.addWidget(self.graph_label)

        tab.setLayout(layout)
        return tab

    def evidence_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        btn_export = QPushButton("Exportar evidencia de la ejecución actual")
        btn_export.clicked.connect(self.export_evidence)

        self.evidence_box = QTextEdit()
        self.evidence_box.setReadOnly(True)
        self.evidence_box.setText(
            "Ejecuta primero una simulación y después exporta la evidencia."
        )

        layout.addWidget(btn_export)
        layout.addWidget(self.evidence_box)

        tab.setLayout(layout)
        return tab

    def prepare_machine(self):
        expression = self.input_expression.text().strip()

        if not expression:
            QMessageBox.warning(self, "Advertencia", "Escribe una operación binaria.")
            return False

        self.machine.load(expression)
        self.machine.run()

        self.current_step = 0
        self.steps_table.setRowCount(0)
        return True

    def run_full(self):
        if not self.prepare_machine():
            return

        self.steps_table.setRowCount(0)

        for step in self.machine.steps:
            self.insert_step(step)

        self.show_step(self.machine.steps[-1])
        self.update_stats()
        self.update_result()
        self.tabs.setCurrentIndex(0)

    def run_step(self):
        if not self.machine.steps or self.current_step >= len(self.machine.steps):
            if not self.prepare_machine():
                return
            self.steps_table.setRowCount(0)

        if self.current_step < len(self.machine.steps):
            step = self.machine.steps[self.current_step]
            self.insert_step(step)
            self.show_step(step)
            self.current_step += 1

        if self.current_step == len(self.machine.steps):
            self.update_result()

        self.update_stats()
        self.tabs.setCurrentIndex(0)

    def insert_step(self, step):
        row = self.steps_table.rowCount()
        self.steps_table.insertRow(row)

        values = [
            str(step.number),
            step.state,
            step.read,
            step.write,
            step.move,
            " ".join(step.tape),
            step.description
        ]

        for col, value in enumerate(values):
            self.steps_table.setItem(row, col, QTableWidgetItem(value))

    def show_step(self, step):
        self.state_label.setText(f"Estado actual: {step.state}")

        self.detail_box.setText(f"""
Paso: {step.number}
Estado: {step.state}
Símbolo leído: {step.read}
Símbolo escrito: {step.write}
Movimiento: {step.move}

Descripción:
{step.description}
""")

        self.render_tape(step.tape, step.head)

    def render_tape(self, tape, head):
        while self.tape_container.count():
            item = self.tape_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for index, symbol in enumerate(tape):
            cell = QLabel(symbol)
            cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell.setFixedSize(55, 55)

            if index == head:
                cell.setStyleSheet("""
                    QLabel {
                        background-color: #ffcc00;
                        color: black;
                        border: 3px solid white;
                        font-size: 22px;
                        font-weight: bold;
                    }
                """)
            else:
                cell.setStyleSheet("""
                    QLabel {
                        background-color: #22222a;
                        color: white;
                        border: 1px solid #555;
                        font-size: 22px;
                        font-weight: bold;
                    }
                """)

            self.tape_container.addWidget(cell)

        self.tape_container.addStretch()

    def update_result(self):
        if self.machine.accepted:
            self.result_label.setText(f"Resultado: {self.machine.result}")
        else:
            self.result_label.setText("Resultado: ERROR")

    def update_stats(self):
        stats = self.machine.stats()
        self.stats_label.setText(
            f"Pasos: {stats['pasos']} | "
            f"Movimientos: {stats['movimientos']} | "
            f"Estado final: {stats['estado_final']} | "
            f"Aceptada: {stats['aceptada']}"
        )

    def reset_view(self):
        self.machine.reset()
        self.current_step = 0
        self.result_label.setText("Resultado: ---")
        self.state_label.setText("Estado actual: ---")
        self.stats_label.setText("Pasos: 0 | Movimientos: 0 | Estado final: --- | Aceptada: ---")
        self.detail_box.clear()
        self.steps_table.setRowCount(0)
        self.render_tape(["□", "□", "□"], 1)

    def build_transition_text(self):
        text = "TABLA DE TRANSICIONES\n\n"
        text += "Estado | Lee | Escribe | Movimiento | Siguiente\n"
        text += "-" * 70 + "\n"

        for row in TuringMachine.transition_table():
            text += f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n"

        text += "\n\n"
        text += TuringMachine.formal_delta_text()
        return text

    def show_graph(self):
        try:
            graph_path = GraphGenerator.generate()
            pixmap = QPixmap(graph_path)

            if pixmap.isNull():
                self.graph_label.setText("No se pudo cargar el grafo.")
                return

            self.graph_label.setPixmap(
                pixmap.scaled(
                    1050,
                    520,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudo generar el grafo:\n{error}")

    def export_evidence(self):
        if not self.machine.steps:
            QMessageBox.warning(self, "Advertencia", "Primero ejecuta una simulación.")
            return

        stats = self.machine.stats()

        path = EvidenceExporter.export(
            self.input_expression.text().strip(),
            stats["resultado"],
            self.machine.steps,
            stats
        )

        self.evidence_box.setText(
            f"Evidencia exportada correctamente.\n\nArchivo creado:\n{path}"
        )

        QMessageBox.information(self, "Evidencia exportada", f"Archivo creado:\n{path}")