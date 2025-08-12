import { buildBoard } from "./builders";
import config from "./config";
import mountGameHandlers from "./mountGameHandlers";
import SnakePool from "./SnakePool";
import type { SnapshotType } from "./types";

class GameLoop {
  snakePool: SnakePool | null;
  offset: number | null;
  constructor() {
    this.snakePool = null;
    this.offset = null;
  }
  init(snapshot: SnapshotType) {
    buildBoard(snapshot);
    mountGameHandlers();
    this.snakePool = new SnakePool();
    this.offset = snapshot.offset;
  }
  run(): void {
    let iteration: number = 1;
    const move = (): void => {
      if (Date.now() - (this.offset as number) - iteration * config.CYCLE_FREQUENCY >= 0) {
        console.log('Error', Date.now() - (this.offset as number) - iteration * config.CYCLE_FREQUENCY);
        (this.snakePool as SnakePool).move((this.offset as number) + iteration * config.CYCLE_FREQUENCY);
        iteration += 1;
      }
      requestAnimationFrame(move);
    }
    requestAnimationFrame(move);
  }
}

const gameLoop: GameLoop = new GameLoop();

export default gameLoop;


