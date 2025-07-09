import Apple from "./Apple";

type Direction = 
    | 'up'
    | 'down'
    | 'left'
    | 'right'

export default class Snake {
    snakeFirstBlock: HTMLDivElement;
    snakeLastBlock: HTMLDivElement;
    constructor(){
        this.snakeFirstBlock = document.querySelector<HTMLDivElement>('#snake-block.first') as HTMLDivElement;
        this.snakeLastBlock = document.querySelector<HTMLDivElement>('#snake-block.last') as HTMLDivElement;
    }
    move(): void { 
        const oldLastBlockTop: string = this.snakeLastBlock.style.top
        const oldLastBlockLeft: string = this.snakeLastBlock.style.left
        switch (this.snakeFirstBlock.dataset.direction) {
            case 'up':
                this.snakeLastBlock.style.top = `${parseInt(this.snakeFirstBlock.style.top) - 20}px`;
                this.snakeLastBlock.style.left = this.snakeFirstBlock.style.left;                
                break;
            case 'down':
                this.snakeLastBlock.style.top = `${parseInt(this.snakeFirstBlock.style.top) + 20}px`;
                this.snakeLastBlock.style.left = this.snakeFirstBlock.style.left;
                break;
            case 'right':
                this.snakeLastBlock.style.top = this.snakeFirstBlock.style.top;
                this.snakeLastBlock.style.left = `${parseInt(this.snakeFirstBlock.style.left) + 20}px`;
                break;
            case 'left':
                this.snakeLastBlock.style.top = this.snakeFirstBlock.style.top;
                this.snakeLastBlock.style.left = `${parseInt(this.snakeFirstBlock.style.left) - 20}px`;
                break;
        }
        if (this.snakeFirstBlock != this.snakeLastBlock) {            
            this.snakeFirstBlock.className = this.snakeFirstBlock.className.replace(' first', '');
            this.snakeLastBlock.className = this.snakeLastBlock.className.replace(' last', ' first');
            const pred: HTMLDivElement = document.querySelector<HTMLDivElement>(`[data-number="${parseInt(this.snakeLastBlock.dataset.number as string) - 1}"]`) as HTMLDivElement;            
            pred.className += ' last';
            document.querySelectorAll<HTMLDivElement>('#snake-block:not(.first)').forEach((snakeBlock: HTMLDivElement): void => {
                snakeBlock.dataset.number = (parseInt(snakeBlock.dataset.number as string) + 1).toString();
            });
            this.snakeLastBlock.dataset.number = '1';
            this.snakeLastBlock.setAttribute('data-direction', this.snakeFirstBlock.dataset.direction as string)
            this.snakeFirstBlock.removeAttribute('data-direction')
            this.snakeFirstBlock = this.snakeLastBlock;
            this.snakeLastBlock = pred;
        }
        const apple: HTMLDivElement = document.querySelector<HTMLDivElement>('#apple') as HTMLDivElement
        if (
            this.snakeFirstBlock.style.top == apple.style.top &&
            this.snakeFirstBlock.style.left == apple.style.left
        ) {
            apple.remove();
            new Apple();
            const newSnakeLastBlock = document.createElement<'div'>('div');
            newSnakeLastBlock.setAttribute('class', ' last');
            newSnakeLastBlock.setAttribute('id', 'snake-block');
            newSnakeLastBlock.setAttribute(
                'style',
                `
                    position: absolute;
                    top: ${oldLastBlockTop};
                    left: ${oldLastBlockLeft};
            `);
            newSnakeLastBlock.setAttribute('data-number', (parseInt(this.snakeLastBlock.dataset.number as string) + 1).toString())
            this.snakeLastBlock.after(newSnakeLastBlock);
            this.snakeLastBlock.className = this.snakeLastBlock.className.replace(' last', '');
            this.snakeLastBlock = newSnakeLastBlock;
        }
        if (this.isDead()) {
            alert('Вы умерли')
        }
    }
    changeDirection(direction: Direction): void {
        switch (this.snakeFirstBlock.dataset.direction) {
            case 'up':
                if (direction == 'down') return;
                break;
            case 'down':
                if (direction == 'up') return;
                break;
            case 'left':
                if (direction == 'right') return;
                break;
            case 'right':
                if (direction == 'left') return;
                break;
        }
        console.log(this.snakeFirstBlock);
        
        this.snakeFirstBlock.dataset.direction = direction;
    }
    private isDead(): boolean {
        let isDead: boolean = false;
        document.querySelectorAll<HTMLDivElement>('#snake-block:not(.first)').forEach((snakeBlock: HTMLDivElement): void => {
            if (
                snakeBlock.style.top == this.snakeFirstBlock.style.top &&
                snakeBlock.style.left == this.snakeFirstBlock.style.left
            ) {
                isDead = true;
            }
        });
        return isDead;
    }
}