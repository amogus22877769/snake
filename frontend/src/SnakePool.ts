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
  move(): void {
    this.snakes.forEach((snake: Snake) => {
      snake.move();
    });
  }
}
