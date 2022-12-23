const form = document.querySelector(".file-input-form"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");

var file_str = "";
form.addEventListener("click", () =>{
  fileInput.click();
});

fileInput.onchange = ({target})=>{
  let file = target.files[0];
  if(file){
    let fileName = file.name;
    console.log(fileInput.value);
    if(fileName.length >= 12){
      let splitName = fileName.split('.');
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    file_str += uploadFile(fileName);
  }

  document.getElementById("uploaded-area").innerHTML = file_str;

  addHover();
}

function uploadFile(name){
  var name_str = name.replace('.txt', '');
      let uploadedHTML = `<li class="row upload-doc" style:"width:100%; padding:auto; margin:auto" onclick="deleteUpload()">
                            <div class="content upload">
                              <i style="padding-right:0.5rem;margin-top:1rem"class="fas fa-file-alt"></i>
                              <div class="details">
                                <span class="name">${name} • Uploaded</span>
                                <i style="margin-left:15rem; margin-top:1rem"; class="fas fa-check"></i>
                              </div>
                            </div>
                          </li>`;
      return uploadedHTML;
}


function switchPage(){


  window.location.assign("dashboard.html");
}

function deleteUpload(){
  console.log("deleting upload");
  document.getElementById("uploaded-area").innerHTML = "";
  file_str="";
  fileInput.value = "";
}
