import Snake from "./Snake";

export default class SnakePool {
  snakes: Snake[];
  constructor() {
    this.snakes = [];
    const firstBlocks: NodeListOf<HTMLDivElement> =
      document.querySelectorAll<HTMLDivElement>("#snake-block.first");
    for (const firstBlock of firstBlocks) {
      this.snakes.push(new Snake(firstBlock.dataset.name as string));
    }
  }
  getSnake(name: string): Snake {
    for (const snake of this.snakes) {
      if (snake.snakeFirstBlock.dataset.name === name) {
        return snake;
      }
    }
    throw Error("There is no snake with such name");
  }
  clear(): void {
    this.snakes = this.snakes.filter((snake) => !snake.deleted);
  }
  move(offset: number): void {
    this.clear();
    this.snakes.forEach((snake: Snake) => {
      snake.freezeFor ? snake.freezeFor -= 1 : snake.move(offset);
    });
  }
}
