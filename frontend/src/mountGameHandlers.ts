import {
  AppleSchema,
  NewClientSnakeSchema,
  NewDirectionSchema,
  SnakeSchema,
} from "./zodSchemas.ts";
import { buildApple, buildSnake } from "./builders.ts";
import z from "zod";
import Snake from "./Snake.ts";
import { socket } from "./socket.ts";
import type { DirectionType } from "./types.ts";
import gameLoop from "./GameLoop.ts";
import type SnakePool from "./SnakePool.ts";
import handleWASD from "./handleWASD.ts";

export default function mountGameHandlers(): void {
  socket.on("new_apple", (data: unknown): void => {
    console.log("New apple recieved");
    try {
      if (typeof data == "string") {
        const jsonApple = JSON.parse(data);
        const apple = AppleSchema.parse(jsonApple);
        buildApple(apple);
      } else {
        console.log("Recieved data is not type string");
      }
    } catch (error) {
      if (error instanceof z.ZodError) {
        console.log("Zod error: ", error.issues);
      } else if (error instanceof SyntaxError) {
        console.log("JSON failed parsing =(, error: ", error.message);
      }
    }
  });

  socket.on("change_direction", (data: unknown): void => {
    console.log("New direction change recieved");
    try {
      if (typeof data == "string") {
        const jsonNewDirection = JSON.parse(data);
        const newDirection = NewDirectionSchema.parse(jsonNewDirection);
        gameLoop.snakePool?.getSnake(newDirection.name).changeDirection(newDirection.direction);
      } else {
        console.log("Recieved data is not type string");
      }
    } catch (error) {
      if (error instanceof z.ZodError) {
        console.log("Zod error: ", error.issues);
      } else if (error instanceof SyntaxError) {
        console.log("JSON failed parsing =(, error: ", error.message);
      }
    }
  });

  socket.on("new_snake", (data: unknown): void => {
    console.log("New snake recieved");
    try {
      if (typeof data == "string") {
        const jsonNewSnake = JSON.parse(data);
        const newSnake = NewClientSnakeSchema.parse(jsonNewSnake);
        console.log('Snake:', newSnake);
        console.log('Latency is', Date.now() - newSnake.offset);
        buildSnake(newSnake);
        gameLoop.snakePool?.snakes.push(new Snake(newSnake.name, 2));
      } else {
        console.log("Recieved data is not type string");
      }
    } catch (error) {
      if (error instanceof z.ZodError) {
        console.log("Zod error: ", error.issues);
      } else if (error instanceof SyntaxError) {
        console.log("JSON failed parsing =(, error: ", error.message);
      }
    }
  });
  document.addEventListener("keydown", handleWASD);
}
