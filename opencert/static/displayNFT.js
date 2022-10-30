try{
    var _img = document.getElementById('imageNFT');
    var newImg = new Image;
    newImg.onload = function() {
        _img.src = this.src;
    }
    newImg.src = localStorage.getItem("pic2");
}catch(error){
    window.location.href = '/displayfail';
}


try{
    var attribute = localStorage.getItem("attribute");

    var a = JSON.parse(attribute);
    b = a.attributes;
    certNum = b[0].value;
    breed = b[1].value;
    gen = b[2].value;
    farm = b[3].value;
    c = b[4].value;
    d = b[5].value;
    document.getElementById("cert").innerHTML = certNum;
    document.getElementById("breed").innerHTML = breed;
    document.getElementById("gen").innerHTML = gen;
    document.getElementById("farm").innerHTML = farm;
    document.getElementById("cites").innerHTML = c;
    document.getElementById("doi").innerHTML = d;
}catch(er){
    window.location.href = '/displayfail';
}






