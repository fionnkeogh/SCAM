function initCanvas() {
    const canvas = document.getElementById("view");
    console.log(canvas);
    setCanvasSize(canvas);
    return canvas;
}

function getWindowSize() {
    let w = window.innerHeight < window.innerWidth ? window.innerHeight : window.innerWidth;
    let h = window.innerHeight < window.innerWidth ? window.innerHeight : window.innerWidth;
    console.log({w, h})
    return {width: w*0.75, height: h*0.75};
}

function setCanvasSize(canvas) {
    const size = getWindowSize();
    console.log(size)
    canvas.width = size.width;
    canvas.height = size.height;
}

const canvasObjects = [];
let canvasObjectsMacrophages = [];
let canvasObjectsCandida = [];
let canvasObjectsCytokines = [];
let lastCalledTime;
let fps;

function addCanvasObject(obj) {
    canvasObjects.push(obj);
}

function addCanvasCytokines(obj) {
    canvasObjectsCytokines.push(obj);
}

function addCanvasCandida(obj) {
    canvasObjectsCandida.push(obj);
}

function addCanvasMacrophages(obj) {
    canvasObjectsMacrophages.push(obj);
}

function getCanvasCytokines() {
    return canvasObjectsCytokines;
}

function getCanvasCandida() {
    return canvasObjectsCandida;
}

function getCanvasMacrophages() {
    return canvasObjectsMacrophages;
}

function removeCanvasObject(obj) {
    let index = canvasObjects.indexOf(obj);
    if (index > -1) {
        canvasObjects.splice(index, 1);
    }
}

function removeCanvasCandida(obj) {
    let index = canvasObjectsCandida.indexOf(obj);
    if (index > -1) {
        canvasObjectsCandida.splice(index, 1);
    }
}

function clearCanvasMacrophage() {
    canvasObjectsMacrophages = [];
    return canvasObjectsMacrophages;
}

function clearCanvasCytokines(obj) {
    canvasObjectsCytokines = [];
    return canvasObjectsCytokines;
}

function loop(context, canvas) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    canvasObjectsCytokines.forEach(object => {
        object.draw(context);
    });
    canvasObjectsCandida.forEach(candida => {
        candida.draw(context);
    });
    canvasObjectsMacrophages.forEach(macrophage => {
        macrophage.draw(context);
    });
    canvasObjects.forEach(object => {
        object.draw(context);
    });

    // canvasObjectsCytokines.forEach(object => {
    //     object.update();
    // });

    requestAnimationFrame(() => {
        if(!lastCalledTime) {
            lastCalledTime = performance.now();
            fps = 0;
        }
        delta = (performance.now() - lastCalledTime)/1000;
        lastCalledTime = performance.now();
        fps = 1/delta;
        
        setTimeout(() => {
            //console.log((fps*2)-fps);
            const event = new Event("contextrestored");
            canvas.dispatchEvent(event);
            loop(context, canvas)
        }, (fps*2)-fps > 0 ? (fps*2)-fps : 0);
    });
}