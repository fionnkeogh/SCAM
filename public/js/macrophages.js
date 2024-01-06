class Macrophage extends CanvasObject{
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
        this.size = 2
        this.img = new Image();
        this.img.src = "macrophage.svg";
        //console.log(this);
    }

    draw(context) {
        context.save();

        const pos_x = this.x*this.rectWidth;
        const pos_y = this.y*this.rectHeight;

        context.fillStyle = `rgba(100, 100, 242, 180)`
        context.fillRect(pos_x, pos_y, this.rectWidth*this.size, this.rectHeight*this.size);

        //context.drawImage(this.img, pos_x, pos_y, rW*2, rH*2);

        context.restore();
    }

    update(x,y) {
        this.x = x;
        this.y = y;
    }

    updateCanvasSize(width, height) {
        this.canvasWidth = width;
        this.canvasHeight = height;
    }
}