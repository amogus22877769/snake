import { io } from "socket.io-client";
import {
  AppleSchema,
  NewDirectionSchema,
  SnakeSchema,
  SnapshotSchema,
} from "./zodSchemas";
import z from "zod";
import { buildApple, buildBoard, buildSnake } from "./builders";
import Snake from "./Snake";

export const socket = io("ws://localhost:5000");

console.log("Initializing socket");

socket.on("connect", (): void => {
  console.log("Connected ", socket.id);
});

socket.on("disconnect", (): void => {
  console.log("Disconnected");
});

socket.on("error", (data: unknown) => {
  console.log("Server error: ", data);
});

socket.on("snapshot", (data: unknown) => {
  console.log("Recieved snapshot");
  try {
    if (typeof data == "string") {
      const jsonSnaphot = JSON.parse(data);
      const snapshot = SnapshotSchema.parse(jsonSnaphot);
      console.log("Snapshot data: ", snapshot);
      buildBoard(snapshot);
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
      new Snake(newDirection.name).changeDirection(newDirection.direction);
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
  console.log("New snake recieved at ", Date.now());
  try {
    if (typeof data == "string") {
      const jsonNewSnake = JSON.parse(data);
      const newSnake = SnakeSchema.parse(jsonNewSnake);
      buildSnake(newSnake);
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
