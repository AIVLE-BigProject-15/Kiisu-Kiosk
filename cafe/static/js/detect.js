const age_names = ['10-19', '20-29', '30-39', '40-49', '50-59', '60+']

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

        const $size = { width: 720, height: 720 };
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
    drawResult(box, box_score, res) {
        if (res == null){
            return
        }
        const font = "20px sans-serif";
        this.ctx.font = font;
        this.ctx.textBaseline = "top";

        const estimate_cls = res.argMax().dataSync()
        const estimate_score = res.max().dataSync()

        let [x, y, w, h] = box;
        const age_group = age_names[estimate_cls];

        // Draw the bounding box.
        this.ctx.strokeStyle = "#E51937";
        this.ctx.lineWidth = 4;
        this.ctx.strokeRect(x, y, w, h);

        // Draw the label background.
        this.ctx.fillStyle = "#E51937";
        const textWidth = this.ctx.measureText(age_group + ": " + (estimate_score[0]).toFixed(2)).width;
        const textHeight = parseInt(font, 10); // base 10
        this.ctx.fillRect(x, y, textWidth + 4, textHeight + 4);

        // Draw the text last to ensure it's on top.
        this.ctx.fillStyle = "#F2F2F2";
        this.ctx.fillText(age_group + ": " + (estimate_score[0]).toFixed(2), x, y);
        
        document.getElementById("estimation_result").innerHTML += " " + age_names[estimate_cls].slice(0, 2);
        document.getElementById("estimation_confidence").innerHTML += " " + (estimate_score[0]).toFixed(2);
    }
}

let estimator, camera, stats;
let startInferenceTime, numInferences = 0;
let inferenceTimeSum = 0, lastPanelUpdate = 0;
let rafId;

const cnn_weight = "/static/js/cnn_model/model.json"

async function createEstimator() {
    return tf.loadLayersModel(cnn_weight);
}

async function renderResult() {
    if (camera.video.readyState < 2) {
        await new Promise((resolve) => {
            camera.video.onloadeddata = () => {
            resolve(video);
            };
        });
    }
    

    let estimate_res= null;
    let detections = null;
    let resizedDetections = null;

    let cnn_input = null;
    let modelWidth = 128, modelHeight = 128;
    let score = 0, box = null;
    
    const displaySize = { width: video.width, height: video.height }
    
    if (estimator != null) {
        try {
            detections = await faceapi
                .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
            resizedDetections = faceapi.resizeResults(detections, displaySize);

            if (resizedDetections.length > 0){
                score = resizedDetections[0]['_score']
                var x = parseInt(resizedDetections[0]['box']['_x'])
                var y = parseInt(resizedDetections[0]['box']['_y'])
                var w = parseInt(resizedDetections[0]['box']['_width'])
                var h = parseInt(resizedDetections[0]['box']['_height'])
                
                box = [x, y, w, h]

                var img_tensor = tf.browser.fromPixels(camera.video)
                    .mean(2)
                    .toFloat()
                    .expandDims(0)
                    .expandDims(-1)
                
                cnn_input = tf.tidy(() => {
                    return img_tensor.slice([0, y, x, 0], [1, w, h, 1]).resizeBilinear([modelWidth, modelHeight])
                        .div(255.0);
                });
                
                // Cropped Image Check
                // tf.browser.toPixels(cnn_input.squeeze(axis=0), document.getElementById("imageHolder2"))
                
                estimate_res = await estimator.predict(
                    cnn_input,
                ).squeeze()
            }

        } catch (error) {
            console.error(error);
        }
    }
    camera.drawCtx();
    camera.drawResult(box, score, estimate_res);
    tf.dispose(cnn_input);
}

async function renderPrediction() {
    await renderResult();
    rafId = requestAnimationFrame(renderPrediction);
};

async function app() {
    camera = await Camera.setupCamera();
    estimator = await createEstimator();

    renderPrediction();
};

Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('/static/js/models'),
  ]).then(app)