import {socket} from "./socket.ts";

type Direction = "up" | "down" | "left" | "right";

export default class Snake {
  snakeFirstBlock: HTMLDivElement;
  snakeLastBlock: HTMLDivElement;
  name: string;
  constructor(name: string) {
    this.name = name;
    this.snakeFirstBlock = document.querySelector<HTMLDivElement>(
      `#snake-block.first[data-name="${name}"]`,
    ) as HTMLDivElement;
    this.snakeLastBlock = document.querySelector<HTMLDivElement>(
      `#snake-block.last[data-name="${name}"]`,
    ) as HTMLDivElement;
  }
  move(offset: number): void {
    if (this.snakeFirstBlock.dataset.scheduledDirection !== undefined) {
      this.changeDirection(this.snakeFirstBlock.dataset.scheduledDirection as Direction);
      socket.emit("change_direction", {direction: this.snakeFirstBlock.dataset.scheduledDirection, offset: offset});
      this.snakeFirstBlock.removeAttribute('data-scheduledDirection');
    }
    const oldLastBlockTop: string = this.snakeLastBlock.style.top;
    const oldLastBlockLeft: string = this.snakeLastBlock.style.left;
    switch (this.snakeFirstBlock.dataset.direction) {
      case "up":
        this.snakeLastBlock.style.top = `${parseInt(this.snakeFirstBlock.style.top) - 20}px`;
        this.snakeLastBlock.style.left = this.snakeFirstBlock.style.left;
        break;
      case "down":
        this.snakeLastBlock.style.top = `${parseInt(this.snakeFirstBlock.style.top) + 20}px`;
        this.snakeLastBlock.style.left = this.snakeFirstBlock.style.left;
        break;
      case "right":
        this.snakeLastBlock.style.top = this.snakeFirstBlock.style.top;
        this.snakeLastBlock.style.left = `${parseInt(this.snakeFirstBlock.style.left) + 20}px`;
        break;
      case "left":
        this.snakeLastBlock.style.top = this.snakeFirstBlock.style.top;
        this.snakeLastBlock.style.left = `${parseInt(this.snakeFirstBlock.style.left) - 20}px`;
        break;
    }
    if (this.snakeFirstBlock != this.snakeLastBlock) {
      this.snakeFirstBlock.className = this.snakeFirstBlock.className.replace(
        " first",
        "",
      );
      this.snakeLastBlock.className = this.snakeLastBlock.className.replace(
        " last",
        " first",
      );
      const pred: HTMLDivElement = document.querySelector<HTMLDivElement>(
        `[data-number="${parseInt(this.snakeLastBlock.dataset.number as string) - 1}"][data-name="${this.name}"]`,
      ) as HTMLDivElement;
      pred.className += " last";
      document
        .querySelectorAll<HTMLDivElement>(
          `#snake-block:not(.first)[data-name="${this.name}"]`,
        )
        .forEach((snakeBlock: HTMLDivElement): void => {
          snakeBlock.dataset.number = (
            parseInt(snakeBlock.dataset.number as string) + 1
          ).toString();
        });
      this.snakeLastBlock.dataset.number = "1";
      this.snakeLastBlock.setAttribute(
        "data-direction",
        this.snakeFirstBlock.dataset.direction as string,
      );
      this.snakeFirstBlock.removeAttribute("data-direction");
      this.snakeFirstBlock = this.snakeLastBlock;
      this.snakeLastBlock = pred;
    }
    const apples: NodeListOf<HTMLDivElement> =
      document.querySelectorAll<HTMLDivElement>("#apple");
    for (const apple of apples) {
      if (
        this.snakeFirstBlock.style.top == apple.style.top &&
        this.snakeFirstBlock.style.left == apple.style.left
      ) {
        apple.remove();
        const newSnakeLastBlock = document.createElement<"div">("div");
        newSnakeLastBlock.setAttribute("class", " last");
        newSnakeLastBlock.setAttribute("id", "snake-block");
        newSnakeLastBlock.setAttribute(
          "style",
          `
                      position: absolute;
                      top: ${oldLastBlockTop};
                      left: ${oldLastBlockLeft};
              `,
        );
        newSnakeLastBlock.setAttribute(
          "data-number",
          (
            parseInt(this.snakeLastBlock.dataset.number as string) + 1
          ).toString(),
        );
        newSnakeLastBlock.setAttribute("data-name", this.name);
        this.snakeLastBlock.after(newSnakeLastBlock);
        this.snakeLastBlock.className = this.snakeLastBlock.className.replace(
          " last",
          "",
        );
        this.snakeLastBlock = newSnakeLastBlock;
      }
    }
    if (this.isDead()) {
      this.delete();
    }
  }
  scheduleChangeDirection(direction: Direction): void {
    switch (this.snakeFirstBlock.dataset.direction) {
      case "up":
        if (direction == "down") return;
        break;
      case "down":
        if (direction == "up") return;
        break;
      case "left":
        if (direction == "right") return;
        break;
      case "right":
        if (direction == "left") return;
        break;
    }
    this.snakeFirstBlock.dataset.scheduledDirection = direction;
  }
  changeDirection(direction: Direction): void {
    switch (this.snakeFirstBlock.dataset.direction) {
      case "up":
        if (direction == "down") return;
        break;
      case "down":
        if (direction == "up") return;
        break;
      case "left":
        if (direction == "right") return;
        break;
      case "right":
        if (direction == "left") return;
        break;
    }
    this.snakeFirstBlock.dataset.direction = direction;
  }
  private isDead(): boolean {
    if (
      parseInt(this.snakeFirstBlock.style.top) < 0 ||
      parseInt(this.snakeFirstBlock.style.top) > 1780 ||
      parseInt(this.snakeFirstBlock.style.left) < 0 ||
      parseInt(this.snakeFirstBlock.style.left) > 1920
    ) {
      return true;
    }
    let isDead: boolean = false;
    document
      .querySelectorAll<HTMLDivElement>(
        `#snake-block:not(.first[data-name="${this.name}"])`,
      )
      .forEach((snakeBlock: HTMLDivElement): void => {
        if (
          snakeBlock.style.top == this.snakeFirstBlock.style.top &&
          snakeBlock.style.left == this.snakeFirstBlock.style.left
        ) {
          isDead = true;
        }
      });
    return isDead;
  }
  private delete(): void {
    document
      .querySelectorAll<HTMLDivElement>(`[data-name="${this.name}"]`)
      .forEach((block: HTMLDivElement) => {
        block.remove();
      });
  }
}
