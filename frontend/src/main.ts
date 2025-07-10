import Apple from './Apple';
import Snake from './Snake';
import './style.css'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <div
      Snake
    </div>
    <div id="game-board">
      <div id="snake-block" class=" first" data-direction="right" data-number="1" style="position: absolute;top: 0px;left: 20px;"></div>
      <div id="snake-block" class=" last" data-number="2" style="position: absolute;top: 0px;left: 0px;"></div>
    </div>
  </div>
`

    // <div id="snake-block" class=" first" data-direction="right" data-number="1" style="position: absolute;top: 0px;left: 200px;" />
    // <div id="snake-block" class=" last" data-number="2" style="position: absolute;top: 0px;left: 0px;" />

document.addEventListener('keydown', (event: KeyboardEvent) => {
  const snake: Snake = new Snake()
  switch (event.key.toLowerCase()) {
    case 'w':
      snake.changeDirection('up');
      break;
    case 'a':
      snake.changeDirection('left');
      break;
    case 's':
      snake.changeDirection('down');
      break;
    case 'd':
      snake.changeDirection('right');
      break;
  }
});

new Apple()

setInterval(() => {
  new Snake().move()
}, 100)