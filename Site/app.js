Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });

    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;

        var url = "http://127.0.0.1:4999/Avengers_classification";
//        var url = "/api/Avengers_classification";

        $.post(url, {
            'image_data': file.dataURL
        },function(data, status) {
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();
                $("#error").show();
                dz.removeFile(file);
                return;
            }
            let players = ["Chris_Evans", "Christopher_Hemsworth", "Mark_Ruffalo", "Robert_Downey_Jr", "Scarlet_Johnson"];
            let total_scores = [0,0,0,0,0]

            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                match = data[i]
                for (let personName in match.class_labels){
                    let index = match.class_labels[personName] - 1
                    let score = match.prob[index]
                    total_scores[index]  = total_scores[index] + score
                    }
                }
            $("#error").hide();
            $("#resultHolder").show();
            $("#divClassTable").show();
            $("#resultHolder").html($(`[data-player="${match.class}"`).html());
            let classDictionary = match.class_labels;
            for(let personName in classDictionary) {
                let index = classDictionary[personName];
                let score = total_scores[index-1]
                let elementName = "#score_" + personName;
                $(elementName).html(score);
            }
             dz.removeFile(file);
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});