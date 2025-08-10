import gameLoop from "./GameLoop";
import type Snake from "./Snake";
import type SnakePool from "./SnakePool";
import type { DirectionType } from "./types";

export default function handleWASD(event: KeyboardEvent) {
  const snakeName = localStorage.getItem("snakeName");
  if (snakeName === null) {
    console.log("Not found snake name in storage");
    return;
  }
  let snake: Snake;
  try {
    snake = (gameLoop.snakePool as SnakePool).getSnake(snakeName);
  } catch (error) {
    console.log(error);
    return;
  }
  let newDirection: DirectionType = "up";
  switch (event.key.toLowerCase()) {
    case "w":
      newDirection = "up";
      break;
    case "a":
      newDirection = "left";
      break;
    case "s":
      newDirection = "down";
      break;
    case "d":
      newDirection = "right";
      break;
  }
  snake.scheduleChangeDirection(newDirection);
}
