from multiprocessing import Process

from backend.src.services.run_move_loop_service import run_move_loop_service

if __name__ == '__main__':
    Process(target=run_move_loop_service).start()
