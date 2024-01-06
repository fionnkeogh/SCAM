class CanvasObject {
    id;
    constructor(id) {
        if (new.target === CanvasObject) {
            throw new TypeError("Cannot construct Abstract instances directly");
        }
        this.id = id;
    }

    draw(){};
}