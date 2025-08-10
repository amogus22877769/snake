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
import SnakePool from "./SnakePool.ts";
import mountGameHandlers from "./mountGameHandlers.ts";
import gameLoop from "./GameLoop.ts";

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
      console.log(snapshot);
      gameLoop.init(snapshot);
      gameLoop.run();
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
