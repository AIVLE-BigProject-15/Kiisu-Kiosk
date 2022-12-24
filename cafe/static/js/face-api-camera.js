
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

function isCanvasBlank(canvas) {
  return !canvas.getContext('2d')
    .getImageData(0, 0, canvas.width, canvas.height).data
    .some(channel => channel !== 0);
}


setInterval(async () => {
  const canvas = document.getElementById("imageHolder")

  if (isCanvasBlank(canvas)){
    return
  }
  var blobBin = atob(canvas.toDataURL("image/png").split(',')[1]);
  var array = [];
  for (var i = 0; i < blobBin.length; i++) {
    array.push(blobBin.charCodeAt(i));
  }
  var file = new Blob([new Uint8Array(array)], {type: 'image/png'});
            
  // FormData -> Bounding Box와 Image
  var formdata = new FormData(document.getElementById("face_submission"));
  var usage_type = $.getUrlVar('usage_type');      

  formdata.append("face_image", file);
  formdata.append("usage_type", usage_type);	
  formdata.append("box", document.getElementById("box").value);

  // 동기 방식으로 서버에 FormData 전송
  // 전송에 성공할 경우, 페이지 이동
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "camera", false);
  xhr.onload = () => {
    if (xhr.status == 200) {
      let result = xhr.response;
      document.getElementById("estimation_result").innerHTML = result;
    } else {
      alert("ERROR LOADING FILE!" + this.status);
    }
  };
  xhr.send(formdata);
   
}, 2000)

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