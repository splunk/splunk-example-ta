export abstract class CustomTabBase {
  public tab: object;
  public el: HTMLElement;

  constructor(tab: object, el: HTMLElement) {
    this.tab = tab;
    this.el = el;
  }

  abstract render(): void;
}
