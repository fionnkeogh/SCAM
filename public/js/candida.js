class Candida extends CanvasObject{
    x;
    y;
    rectWidth;
    rectHeight;
    img;

    constructor(id, x, y, rectWidth, rectHeight) {
        super(id);
        
        this.x = x;
        this.y = y;
        this.rectWidth = rectWidth;
        this.rectHeight = rectHeight;
        this.img = new Image();
        this.img.src = "candida.svg";
        //console.log(this);
    }

    draw(context) {
        context.save();

        const pos_x = this.x*this.rectWidth;
        const pos_y = this.y*this.rectHeight;
        const rW = this.rectWidth;
        const rH = this.rectHeight;
        //console.log([pos_x, pos_y, rW, rH]);

        context.fillStyle = `rgba(242, 192, 100, 180)`
        context.fillRect(pos_x, pos_y, this.rectWidth, this.rectHeight);

        //context.drawImage(this.img, pos_x, pos_y, rW, rH);

        context.restore();
    }

    update() {
    }

    updateCanvasSize(width, height) {
        this.canvasWidth = width;
        this.canvasHeight = height;
    }
}