import { buildBoard } from "./builders";
import Snake from "./Snake";
import SnakePool from "./SnakePool";
// import { socket } from "./socket";
import "./style.css";
import type { DirectionType } from "./types";

document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
  <div>
    <div>
      Snake
    </div>
    <div id="game-board">
    </div>
  </div>
`;

function generateAsciiUnderscoreString(length = 10) {
  const chars = "abcdefghijklmnopqrstuvwxyz_";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// const snakeName = generateAsciiUnderscoreString();

// localStorage.setItem("snakeName", snakeName);

// console.log('Snake created at ', Date.now());

// socket.emit("new_snake", {
//   name: snakeName,
// });

// document.addEventListener("keydown", (event: KeyboardEvent) => {
//   const snake: Snake = new Snake(localStorage.getItem("snakeName") as string);
//   let newDirection: DirectionType = "up";
//   switch (event.key.toLowerCase()) {
//     case "w":
//       newDirection = "up";
//       break;
//     case "a":
//       newDirection = "left";
//       break;
//     case "s":
//       newDirection = "down";
//       break;
//     case "d":
//       newDirection = "right";
//       break;
//   }
//   snake.changeDirection(newDirection);
//   socket.emit("change_direction", newDirection);
// });

// setInterval((): void => {
//   new SnakePool().move();
// }, 100);

buildBoard(
{"snakes":[{"name":"maxim","blocks":[{"left":280,"top":720},{"left":220,"top":720},{"left":260,"top":720},{"left":240,"top":720}],"direction":"right"}],"apples":[]}
)