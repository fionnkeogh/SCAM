class Grid extends CanvasObject{
    x;
    y;
    canvasHeight;
    canvasWidth;

    constructor(x, y, width, height) {
        super();
        this.x = x;
        this.y = y;
        this.canvasWidth = width;
        this.canvasHeight = height;
    }

    draw(context) {
        context.save();
        if(this.x <= 20 && this.y <= 20) {
            for(let i = 0; i <= this.x; i++) {
                context.beginPath(); 
                // Staring point (10,45)
                context.moveTo(0,this.canvasHeight/this.y*i);
                // End point (180,47)
                context.lineTo(this.canvasWidth,this.canvasHeight/this.y*i);
                // Make the line visible
                context.stroke();
            }
            for(let i = 0; i <= this.y; i++) {
                context.beginPath(); 
                // Staring point (10,45)
                context.moveTo(this.canvasWidth/this.x*i, 0);
                // End point (180,47)
                context.lineTo(this.canvasWidth/this.x*i,this.canvasHeight);
                // Make the line visible
                context.stroke();
            }
        }
        
        
        context.restore();
    }

    updateCanvasSize(width, height) {
        this.canvasWidth = width;
        this.canvasHeight = height;
    }
}