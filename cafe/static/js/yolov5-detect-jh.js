
const age_names = ['(0, 3)','(15, 24)','(25, 37)','(38, 47)','(4, 7)','(48, 59)','(60, 100)','(8, 14)']

class Camera {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('imageHolder');
        this.ctx = this.canvas.getContext('2d');
    }

    static async setupCamera() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Browser API navigator.mediaDevices.getUserMedia not available');
            throw new Error(
            'Browser API navigator.mediaDevices.getUserMedia not available');
        }

        const $size = { width: 720, height: 560 };
        const videoConfig = {
            'audio': false,
            'video': {
                facingMode: 'user',
                // Only setting the video to a specified size for large screen, on
                // mobile devices accept the default size.
                width: $size.width,
                height: $size.height,
            }
        };
        const stream = await navigator.mediaDevices.getUserMedia(videoConfig);

        const camera = new Camera();
        camera.video.srcObject = stream;

        await new Promise((resolve) => {
            camera.video.onloadedmetadata = () => {
            resolve(video);
            };
        });

        camera.video.play();
            return camera;
    }

    drawCtx() {
        this.ctx.drawImage(
            this.video, 0, 0, this.video.videoWidth, this.video.videoHeight);
    }

    clearCtx() {
        this.ctx.clearRect(0, 0, this.video.videoWidth, this.video.videoHeight);
    }


    drawResult(res) {
        const font = "20px sans-serif";
        this.ctx.font = font;
        this.ctx.textBaseline = "top";

        const [boxes, scores, classes, valid_detections] = res;
        const boxes_data = boxes.dataSync();
        const scores_data = scores.dataSync();
        const classes_data = classes.dataSync();
        const valid_detections_data = valid_detections.dataSync()[0];

        tf.dispose(res);

        var i;
        for (i = 0; i < valid_detections_data; ++i) {
            let [x1, y1, x2, y2] = boxes_data.slice(i * 4, (i + 1) * 4);
            x1 *= this.canvas.width;
            x2 *= this.canvas.width;
            y1 *= this.canvas.height;
            y2 *= this.canvas.height;
            const width = x2 - x1;
            const height = y2 - y1;

            const age_group = age_names[classes_data[i]];
            const score = scores_data[i].toFixed(2);

            // Draw the bounding box.
            this.ctx.strokeStyle = "#E51937";
            this.ctx.lineWidth = 4;
            this.ctx.strokeRect(x1, y1, width, height);

            // Draw the label background.
            this.ctx.fillStyle = "#E51937";
            const textWidth = this.ctx.measureText(age_group + ":" + score).width;
            const textHeight = parseInt(font, 10); // base 10
            this.ctx.fillRect(x1, y1, textWidth + 4, textHeight + 4);

        }
        for (i = 0; i < valid_detections_data; ++i) {
            let [x1, y1, ,] = boxes_data.slice(i * 4, (i + 1) * 4);
            x1 *= this.canvas.width;
            y1 *= this.canvas.height;

            const age_group = age_names[classes_data[i]];
            const score = scores_data[i].toFixed(2);

            // Draw the text last to ensure it's on top.
            this.ctx.fillStyle = "#F2F2F2";
            this.ctx.fillText(age_group + ":" + score, x1, y1);

            document.getElementById("estimation_result").innerHTML = classes_data[i] < 4 ? "young_order" : "old_order";
        }
    }
}

let detector, camera, stats;
let startInferenceTime, numInferences = 0;
let inferenceTimeSum = 0, lastPanelUpdate = 0;
let rafId;

// const yolov5n_weight = "/static/js/yolo_model_jh/model.json"
const yolov5n_weight = "/static/js/yolo04/model.json"

async function createDetector() {
    return tf.loadGraphModel(yolov5n_weight);
}

async function renderResult() {
    if (camera.video.readyState < 2) {
    await new Promise((resolve) => {
        camera.video.onloadeddata = () => {
        resolve(video);
        };
    });
    }

    let detect_res = null;
    //const webcam = await tf.data.webcam(camera.video, { resizeWidth: 640, resizeHeight: 640 });
    //const img = await webcam.capture();
    
    let [modelWidth, modelHeight] = detector.inputs[0].shape.slice(1, 3);
    console.log(modelWidth, modelHeight);
    console.log(detector.inputs[0])
    const input = tf.tidy(() => {
        return tf.image.resizeBilinear(tf.browser.fromPixels(camera.video), [modelWidth, modelHeight])
            .div(255.0).expandDims(0);
    });

    // Detector can be null if initialization failed (for example when loading
    // from a URL that does not exist).
    if (detector != null) {
    // Detectors can throw errors, for example when using custom URLs that
    // contain a model that doesn't provide the expected output.
    try {
        detect_res = await detector.executeAsync(
            input,
        );
    } catch (error) {
        detector.dispose();
        detector = null;
        alert(error);
    }

    }
    camera.drawCtx();
    camera.drawResult(detect_res);
    tf.dispose(input);
}

async function renderPrediction() {
    await renderResult();
        rafId = requestAnimationFrame(renderPrediction);
};

async function app() {
    camera = await Camera.setupCamera();
    detector = await createDetector();

    renderPrediction();
};

app();