import { buildBoard } from "./builders";
import Snake from "./Snake";
import SnakePool from "./SnakePool";
import { socket } from "./socket";
import "./style.css";
import type { DirectionType } from "./types";

document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
  <div>
    <div>
      Snake
    </div>
    <div id="game-board">
    </div>
    <input id="snake-name" required></input><button id="play" disabled>PLAY!</button><br/>
    <p id="input-error" style="color: #ff0000"></p>
  </div>
`;

let name: string = ''

document.getElementById('snake-name')?.addEventListener('input', (e: Event): void => {
  const inputElement = e.target as HTMLInputElement;
  name = inputElement.value;
  if (!/^[a-z_]+$/.test(name)) {
    document.getElementById('input-error')!.innerText = 'Snake name must only contain lowercase english letters and underscores';
    (document.getElementById('play') as HTMLButtonElement).disabled = true;
  } else {
    document.getElementById('input-error')!.innerText = '';
    (document.getElementById('play') as HTMLButtonElement).disabled = false;
  }
});

document.getElementById('play')?.addEventListener('click', (): void => {
  console.log('Play!')
  socket.emit('new_snake', {name: name});
  localStorage.setItem('snakeName', name);
})

// socket.emit("new_snake", {
//   name: snakeName,
// });

document.addEventListener("keydown", (event: KeyboardEvent) => {
  const snake: Snake = new Snake(localStorage.getItem("snakeName") as string);
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
});

// setInterval((): void => {
//   new SnakePool().move();
// }, 100);