window.addEventListener("load",()=>{
    const user_input = document.getElementById("upload");
    const filewrapper = document.getElementById("filewrapper");
    
    user_input.addEventListener("change",(e)=>{
        let fileName = e.target.files[0].name;
        let fileType = e.target.value.split(".").pop();
        file_show(fileName, fileType);

    })

    const file_show=(fileName, fileType) => {
        const showfileboxElem = document.createElement("div");
        showfileboxElem.classList.add("showfilebox");
        const leftElem = document.createElement("div");
        leftElem.classList.add("left");
        // show file type
        const fileTypeElem = document.createElement("span");
        fileTypeElem.classList.add("filetype");
        fileTypeElem.innerHTML = fileType;
        leftElem.append(fileTypeElem);
        // show file name
        const fileNameElem = document.createElement("h3");
        fileNameElem.innerHTML = fileName;
        leftElem.append(fileNameElem);
        showfileboxElem.append(leftElem);
        // show right element
        const rightElem = document.createElement("div");
        rightElem.classList.add("right");
        showfileboxElem.append(rightElem);
        const crossElem = document.createElement("span");
        crossElem.innerHTML = "&#215"
        rightElem.append(crossElem);
        filewrapper.append(showfileboxElem);
        // add event listener to cross element
        crossElem.addEventListener("click",()=>{
            filewrapper.removeChild(showfileboxElem);
            document.getElementById("upload").value = null;
        })
    }
})