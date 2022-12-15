
const video = document.getElementById('video')

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/static/js/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/static/js/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/static/js/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('/static/js/models')
]).then(startVideo)

function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video)
  const holder = document.getElementById("cameraHolder");
  holder.prepend(canvas)

  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)
  
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)

    faceapi.draw.drawDetections(canvas, resizedDetections)

    if (resizedDetections.length > 0){
        console.log("submit")
        var box_info = resizedDetections[0]['detection']['_box']
        
        var mediaStream = video.srcObject
        var imageCapture = new ImageCapture(mediaStream.getVideoTracks()[0])
        imageCapture.takePhoto().then((blob) => {
            console.log('Took photo:', blob);
            
            const formData = new FormData(document.getElementById("face_submission"));
            formData.append("face_image", blob);
            formData.append("bounding_box", box_info);

            const request = new XMLHttpRequest();
            request.open("POST", "camera");
            request.send(formData);

            // document.getElementById("face_image").value = blob
            // document.getElementById("bounding_box").value = box_info
            // document.getElementById("face_submission").submit()


          }).catch((error) => {
            console.error('takePhoto() error: ', error);
          });

    } 
  }, 100)
})