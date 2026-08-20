import chess
import chess.engine
import random
board = chess.Board()
engine = None
engines = [["/usr/local/bin/patricia", "Patricia"], ["/home/linuxbrew/.linuxbrew/bin/stockfish", "Stockfish"], ["/usr/local/bin/dragon", "Dragon"]]
def set_random_skill(engine, engine_name):
    skill_params = {"Stockfish": "Skill Level", "Patricia": "Skill_Level", "Dragon": "Skill"}
    skill_floor = None
    skill_ceiling = None
    skill_test = -30
    while True:
        try:
            engine.configure({skill_params[engine_name]: skill_test})
            if skill_floor == None:
                skill_floor = skill_test
        except chess.engine.EngineError:
            if skill_floor != None:
                skill_ceiling = skill_test-1
        skill_test += 1
        if skill_ceiling != None:
            break
    skill_level = random.randint(skill_floor, skill_ceiling)
    engine.configure({skill_params[engine_name]: skill_level})
    print(f"SKILL LEVEL: {skill_level}!")
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
        if engine != None:
            engine.quit()
        break
    elif line[0] == "ucinewgame":
        if engine != None:
            engine.quit()
        current_engine = random.choice(engines)
        engine = chess.engine.SimpleEngine.popen_uci(current_engine[0])
        print(f"ENGINE: {current_engine[1]}!")
        set_random_skill(engine, current_engine[1])
