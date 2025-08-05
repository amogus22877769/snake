import { type SnapshotType } from "./types";
import type { AppleType, SnakeType } from "./types";

function buildBoard(snapshot: SnapshotType) {
  for (const snake of snapshot.snakes) {
    buildSnake(snake);
  }
  for (const apple of snapshot.apples) {
    buildApple(apple);
  }
}

function buildApple(apple: AppleType) {
  const appleElement = document.createElement<"div">("div");
  appleElement.setAttribute("id", "apple");
  appleElement.setAttribute(
    "style",
    `
                position: absolute;
                top: ${apple.top}px;
                left: ${apple.left}px;
            `,
  );
  (
    document.querySelector<HTMLDivElement>("#game-board") as HTMLDivElement
  ).appendChild(appleElement);
}

function buildSnake(snake: SnakeType) {
  for (const [blockIndex, block] of snake.blocks.entries()) {
    const newBlock: HTMLDivElement = document.createElement<"div">("div");
    newBlock.setAttribute("id", "snake-block");
    newBlock.setAttribute("data-name", snake.name);
    newBlock.setAttribute("data-number", `${blockIndex + 1}`);
    newBlock.setAttribute(
      "style",
      `
                    position: absolute;
                    top: ${block.top}px;
                    left: ${block.left}px;
                `,
    );
    let newBlockClass: string = "";
    if (blockIndex === 0) {
      newBlock.setAttribute("data-direction", snake.direction);
      newBlockClass += " first";
    }
    if (blockIndex === snake.blocks.length - 1) {
      newBlockClass += " last";
    }
    newBlock.setAttribute("class", newBlockClass);
    (
      document.querySelector<HTMLDivElement>("#game-board") as HTMLDivElement
    ).appendChild(newBlock);
  }
}

export { buildBoard, buildApple, buildSnake };
