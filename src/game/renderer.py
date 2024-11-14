class BoardRenderer:
    def get_board_html(self, board_state):
        html = "<table>"
        for row in board_state:
            html += "<tr>"
            for cell in row:
                cell_class = ""
                if cell == 'X':
                    cell_class = "hit"
                elif cell == 'O':
                    cell_class = "miss"
                html += f'<td class="{cell_class}">{cell if cell != " " else "&nbsp;"}</td>'
            html += "</tr>"
        html += "</table>"
        return html

    def get_guess_history_html(self, guess_history):
        html = "<ul>"
        for move in guess_history:
            html += f"<li>{move}</li>"
        html += "</ul>"
        return html