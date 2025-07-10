export default class Apple {
    apple: HTMLDivElement
    constructor() {
        this.apple = document.createElement<'div'>('div');
        this.apple.setAttribute('id', 'apple');
        this.apple.setAttribute(
            'style',
            `
                position: absolute;
                top: ${Math.floor(Math.random() * 580 / 20) * 20}px;
                left: ${Math.floor(Math.random() * 780 / 20) * 20}px;
            `);
        (document.querySelector<HTMLDivElement>('#game-board') as HTMLDivElement)
            .appendChild(this.apple)
    }
}