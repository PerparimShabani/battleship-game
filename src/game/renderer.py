class BoardRenderer:
    def get_board_html(self, board_state, guesses):
        html = "<table>"
        for i in range(len(board_state)):
            html += "<tr>"
            for j in range(len(board_state[i])):
                cell_content = board_state[i][j]
                cell_class = ""
                if cell_content == 'X':
                    cell_class = "hit"
                elif cell_content == 'O':
                    cell_class = "miss"
                html += f'<td class="{cell_class}">{cell_content if cell_content != " " else "&nbsp;"}</td>'
            html += "</tr>"
        html += "</table>"
        return html

    def get_guess_history_html(self, guess_history):
        html = "<ul>"
        for move in reversed(guess_history[-50:]):  # Show only last 50 moves
            html += f"<li>{move}</li>"
        html += "</ul>"
        return html