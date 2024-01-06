class Cytokine extends CanvasObject{
    x;
    y;
    rectWidth;
    rectHeight;
    strength;

    constructor(id, x, y, rectWidth, rectHeight, strength) {
        super(id);
        this.x = x;
        this.y = y;
        this.rectWidth = rectWidth;
        this.rectHeight = rectHeight;
        this.strength = strength;
        //console.log(this);
    }

    draw(context) {
        context.save();

        const pos_x = this.x*this.rectWidth;
        const pos_y = this.y*this.rectHeight;
        const rW = this.rectWidth;
        const rH = this.rectHeight;

        context.fillStyle = `rgba(118, 175, 255, ${this.strength})`
        context.fillRect(pos_x, pos_y, this.rectWidth, this.rectHeight);

        //context.drawImage(this.img, pos_x, pos_y, rW, rH);

        context.restore();

        // for(let y = 0; y < this.neighborhood.length; y++) {
        //     for(let x = 0; x < this.neighborhood[y].length; x++) {
        //         context.fillStyle = `rgba(118, 175, 255, ${this.neighborhood[y][x]})`
        //         const pos_x = ((this.x-Math.round(this.neighborhood[y].length/2))+x)*this.rectWidth;
        //         const pos_y = ((this.y-Math.round(this.neighborhood.length/2))+y)*this.rectHeight;
        //         context.fillRect(pos_x, pos_y, this.rectWidth, this.rectHeight);
        //     }
        // }

        // context.restore();
    }

    // update(neighborhood) {
    //     this.neighborhood = neighborhood;
    // }

    updateCanvasSize(width, height) {
        this.canvasWidth = width;
        this.canvasHeight = height;
    }
}