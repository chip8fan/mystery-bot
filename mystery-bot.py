import chess
import chess.engine
import random
board = chess.Board()
engine = None
engines = ["/usr/games/stockfish", "/usr/games/fairy-stockfish", "/home/linuxbrew/.linuxbrew/bin/stockfish"]
def set_random_skill(engine):
    skill_floor = None
    skill_ceiling = None
    skill_test = -30
    while True:
        try:
            engine.configure({"Skill Level": skill_test})
            if skill_floor == None:
                skill_floor = skill_test
        except chess.engine.EngineError:
            if skill_floor != None:
                skill_ceiling = skill_test-1
        skill_test += 1
        if skill_ceiling != None:
            break
    engine.configure({"Skill Level": random.randint(skill_floor, skill_ceiling)})
while True:
    line = input().split()
    if line[0] == "uci":
        print("id name Mystery Bot")
        print("uciok")
    elif line[0] == "isready":
        print("readyok")
    elif line[0] == "position":
        if "fen" in line:
            board = chess.Board(fen=" ".join(line[2:]).split(" moves")[0])
        elif "startpos" in line:
            board = chess.Board()
        if "moves" in line:
            move_list = line[3:]
            for move in move_list:
                board.push_uci(move)
    elif line[0] == "go":
        if line[1] == "wtime" and line[3] == "btime" and line[5] == "winc" and line[7] == "binc":
            white_clock = int(line[2])/1000
            black_clock = int(line[4])/1000
            white_inc = int(line[6])/1000
            black_inc = int(line[8])/1000
            limit = chess.engine.Limit(white_clock=white_clock, black_clock=black_clock, white_inc=white_inc, black_inc=black_inc)
        elif line[1] == "movetime":
            move_time = int(line[2])/1000
            limit = chess.engine.Limit(time=move_time)
        best_move = engine.play(board, limit).move
        print(f"bestmove {best_move.uci()}")
    elif line[0] == "quit":
        break
    elif line[0] == "ucinewgame":
        if engine != None:
            engine.quit()
        engine = chess.engine.SimpleEngine.popen_uci(random.choice(engines))
        set_random_skill(engine)
