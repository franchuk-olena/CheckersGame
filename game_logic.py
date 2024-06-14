def is_valid_move(board, old_pos, new_pos, turn):
    old_row, old_col = old_pos
    new_row, new_col = new_pos
    piece = board.get_piece(old_row, old_col)
    is_king = board.is_king(piece)

    if not is_king:
        direction = 1 if turn == 'red' else -1

        if abs(new_row - old_row) == 1 and abs(new_col - old_col) == 1:
            return board.get_piece(new_row, new_col) is None and (new_row - old_row == direction)

        if abs(new_row - old_row) == 2 and abs(new_col - old_col) == 2:
            mid_row, mid_col = (old_row + new_row) // 2, (old_col + new_col) // 2
            return (board.get_piece(mid_row, mid_col) is not None and
                    board.get_piece_color(mid_row, mid_col) != turn and
                    board.get_piece(new_row, new_col) is None)

    else:
        if abs(new_row - old_row) == abs(new_col - old_col):
            delta_row = (new_row - old_row) // abs(new_row - old_row)
            delta_col = (new_col - old_col) // abs(new_col - old_col)
            row, col = old_row + delta_row, old_col + delta_col
            captured = False
            while row != new_row and col != new_col:
                if board.get_piece(row, col) is not None:
                    if board.get_piece_color(row, col) == turn:
                        return False
                    elif not captured:
                        captured = True
                    else:
                        return False
                row += delta_row
                col += delta_col
            return True

    return False

def is_valid_capture_move(board, old_pos, new_pos, turn):
    old_row, old_col = old_pos
    new_row, new_col = new_pos
    piece = board.get_piece(old_row, old_col)
    is_king = board.is_king(piece)

    if not is_king:
        direction = 1 if turn == 'red' else -1

        if abs(new_row - old_row) == 2 and abs(new_col - old_col) == 2:
            mid_row, mid_col = (old_row + new_row) // 2, (old_col + new_col) // 2
            return (board.get_piece(mid_row, mid_col) is not None and
                    board.get_piece_color(mid_row, mid_col) != turn and
                    board.get_piece(new_row, new_col) is None)

    else:
        if abs(new_row - old_row) == abs(new_col - old_col):
            delta_row = (new_row - old_row) // abs(new_row - old_row)
            delta_col = (new_col - old_col) // abs(new_col - old_col)
            row, col = old_row + delta_row, old_col + delta_col
            captured = False
            while row != new_row and col != new_col:
                if board.get_piece(row, col) is not None:
                    if board.get_piece_color(row, col) == turn:
                        return False
                    elif not captured:
                        captured = True
                    else:
                        return False
                row += delta_row
                col += delta_col
            return captured and board.get_piece(new_row, new_col) is None

    return False

def has_mandatory_capture(board, turn):
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and board.get_piece_color(row, col) == turn:
                if has_capture_move(board, row, col, turn):
                    return True
    return False

def has_mandatory_capture_for_piece(board, row, col):
    piece = board.get_piece(row, col)
    if piece and board.get_piece_color(row, col) == turn:
        return has_capture_move(board, row, col, turn)
    return False

def has_capture_move(board, row, col, turn):
    piece = board.get_piece(row, col)
    is_king = board.is_king(piece)
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for direction in directions:
        if is_king:
            for i in range(1, 8):
                new_row = row + direction[0] * i
                new_col = col + direction[1] * i
                if 0 <= new_row < 8 and 0 <= new_col < 8 and is_valid_capture_move(board, (row, col), (new_row, new_col), turn):
                    return True
        else:
            new_row = row + direction[0] * 2
            new_col = col + direction[1] * 2
            if 0 <= new_row < 8 and 0 <= new_col < 8 and is_valid_capture_move(board, (row, col), (new_row, new_col), turn):
                return True
    return False
