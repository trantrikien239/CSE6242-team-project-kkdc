var FORM_ID_INCR = 0; // Ever-increasing couter
var array_name = [];   

document.getElementById('add-form-btn').addEventListener('click', function(e) {
createAndAppendNewContactForm();
});


function createAndAppendNewContactForm() {
    
    if (FORM_ID_INCR < 11) {
        FORM_ID_INCR ++
        let viewModel = { formId : FORM_ID_INCR};
        let template = document.getElementById('form-template').innerHTML;
        template.display = 'block';
        let renderedHtml = Mustache.render(template, viewModel);
        let node = document.createRange().createContextualFragment(renderedHtml);
        document.getElementById('form-container').appendChild(node);

        
        sp = document.getElementById("submit");
        sp.setAttribute("class","button");
        sp.removeAttribute("hidden");
        
        
        // var btn = document.getElementById('submit'+subButon).addEventListener('click', func());
        
    } else {
        alert('We only accept 10 people ratings at the same time');
    }
}


function func() {
    // formId = "form-"+ FORM_ID_INCR
    // for (var i = 1; i <= FORM_ID_INCR; i++) {
    //     var elements = document.getElementById(formId).elements;
    //     for (var i = 0, element; element = elements[i++];) {
    //         console.log(element.value)
    //         if (element.type === "text" && element.value === "")
    //             console.log("it's an empty textfield")
    //     }
    // }

    var username = document.getElementById("name_input").value;
    var anime_names = [];
    var ratings = [];

    for (var i = 0; i <= 9; i++) {
        anime = document.getElementById("anime_input_" + i).value;
        rating = document.getElementById("rating_input_" + i).value;

        if (anime !=  "" && rating != "" && username != "") {
            anime_names.push(anime);
            ratings.push(rating);
        }
    }

    data = {
        "name": username,
        "animes": anime_names,
        "ratings": ratings
    }

    //console.log(data);

    $.post("/collect", {
        javascript_data: JSON.stringify(data)
    });

    
}