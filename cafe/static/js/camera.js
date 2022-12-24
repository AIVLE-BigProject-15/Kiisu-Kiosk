
const video = document.getElementById('video')

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/static/js/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/static/js/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/static/js/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('/static/js/models'),
  faceapi.nets.ageGenderNet.loadFromUri('/static/js/models')
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

    const detections = await faceapi
    .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withAgeAndGender();

    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)


    faceapi.draw.drawDetections(canvas, resizedDetections)

    if (resizedDetections.length > 0){
        var box_info = resizedDetections[0]['detection']['_box']
        
        document.getElementById("imageHolder").getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
        document.getElementById("box").value = JSON.stringify(box_info)
    } 
  }, 100)
})