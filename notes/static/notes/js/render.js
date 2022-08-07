//vars to track ACE code editors
let codeEditors = [];
let codeContents = {};

function scanDoc(text) {
    //reset output
    output = document.getElementById("output");
    output.innerHTML = "";

    let lines = text.split("\n");
    let codeEditorQueue = [];
    let stars_by_line = [];

    //first, we have to cycle through lines to find keywords
    for(let i = 0; i < lines.length; i++) {
        //check images and code editors
        let rawLine = lines[i];
        let additions = []; // this is the special items to add
        //search for keywords in line
        for(let c = 0; c < rawLine.length - 3; c++) {
            let word = rawLine.slice(c, c + 4); //keyword
            if(word == "img:") { //img case
                let url = rawLine.slice(c + 4).split(" ")[0];
                additions.push([c, c + 4 + url.length, url, "img"]); //push start, end, url, and img keyword
            } else if(word == "cod:") { //code editor case
                let lang = rawLine.slice(c + 4).split(",")[0];
                if(lang == "c") { //special case for c language
                    lang = "c_cpp";
                }
                let id = rawLine.slice(c + 4).split(",")[1].split(" ")[0];
                additions.push([c, c + 5 + lang.length + id.length, lang, "cod", id]); //push start, end, language, cod keyword, and id
            }
        }//end for char in line

        //next reformat line if needed with additions
        let line = "";
        if(additions.length == 0){
            line = rawLine; //if no addition
        } else {
            let added = 0;
            line = rawLine;
            for(let a = 0; a < additions.length; a++) { //for each addition
                let addition = additions[a];
                if(addition[3] == "img"){ //if img
                    //extract data
                    let s = addition[0]; //start char
                    let e = addition[1]; //end char
                    let url = addition[2];
                    //build html and add
                    line = line.slice(0, s + added) + '<img src="' + url + '" style="width:300px;height:auto;">' + line.slice(e + added);
                    added = added + 41;
                } else if(addition[3] == "cod") { //if cod
                    //extract data
                    let s = addition[0]; //start char
                    let e = addition[1]; //end char
                    let lang = addition[2];
                    let id = addition[4];
                    //build html and add
                    line = line.slice(0, s + added) + '<div id="' + id + '" class="code"></div>' + line.slice(e + added);
                    added = added + 30 + id.length;
                    codeEditorQueue.push([id, lang]);
                }
            } //end for addition
        } //end if additions exist

        //count bullet * for line
        let count = 0;
        //search for *
        for(let c = 0; c < line.length; c ++) { //add until * not found
            let character = line.slice(c, c + 1);
            if(character == "*") {
                count += 1;
            } else {
                break;
            }
        } //end for char
        //add to list
        stars_by_line.push(count);

        //update output
        output.innerHTML = output.innerHTML + line + "<br>";

    }//end for line

    //now render bullet points
    let prev_count = 0;
    let bullet_active = false;
    let oldHTML = output.innerHTML;
    let html = ""
    lines = oldHTML.split("<br>"); //get updated lines
    for(let i = 0; i < stars_by_line.length; i++) { //for each line
        let line = lines[i];
        let count = stars_by_line[i];
        //the bellow logic decides if a given bullet is nested, also checks for end of list
        if(count == 0 && bullet_active) { //end list
            bullet_active = false;
            for(let e = 0; e < prev_count; e++) {
                html = html + "</ul>";
            }
            html = html + line.slice(count);
        } else if(count == 0 && !bullet_active) { //no list
            html = html + line.slice(count) + "<br>";
        } else if(count > prev_count) { //create new list
            bullet_active = true;
            html = html + "<ul><li>" + line.slice(count) + "</li>";
        } else if(count == prev_count && count != 0) { //add list element
            html = html + "<li>" + line.slice(count) + "</li>";
        } else if(count < prev_count) { //add nested list
            html = html + "</ul><li>" + line.slice(count) + "</li>";
        }
        prev_count = count;
    }

    //set output
    output.innerHTML = html;

    //render code editors via Ace
    codeEditors = [];
    //go throuhg all the code editors in queue
    for(let e = 0; e < codeEditorQueue.length; e++) {
        let editor = codeEditorQueue[e];
        let lang = editor[1];
        let id = editor[0];
        var aceEdit = ace.edit(id);
        //setupd with ACE
        aceEdit.setTheme("ace/theme/monokai");
        aceEdit.session.setMode("ace/mode/" + lang);
        if(!(id in codeContents)) {
            codeContents[id] = "";
        }
        aceEdit.setValue(codeContents[id]);
        codeEditors.push([aceEdit, id]);
        aceEdit.setOptions({
            maxLines: 500,
            autoScrollEditorIntoView: true
        });
    }
}//end scanDoc

//this function puts the code editor contents into list
function saveCode() {
    for(let e = 0; e < codeEditors.length; e++) {
        let data = codeEditors[e];
        let editor = data[0];
        let id = data[1];
        codeContents[id] = editor.getValue();
    }
}//end saveCode

//this is tha main render  function that renders page
function render(text) {
    saveCode();
    scanDoc(text);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}//end render