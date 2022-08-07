let codeEditors = [];
let codeContents = {};

function scanDoc(text) {
    output = document.getElementById("output");
    output.innerHTML = "";

    let lines = text.split("\n");
    let codeEditorQueue = [];
    let stars_by_line = [];

    for(let i = 0; i < lines.length; i++) {

        //check images and code editors
        let rawLine = lines[i];
        let additions = [];
        for(let c = 0; c < rawLine.length - 3; c++) {
            let word = rawLine.slice(c, c + 4);
            if(word == "img:") {
                let url = rawLine.slice(c + 4).split(" ")[0];
                additions.push([c, c + 4 + url.length, url, "img"]);
            } else if(word == "cod:") {
                let lang = rawLine.slice(c + 4).split(",")[0];
                let id = rawLine.slice(c + 4).split(",")[1].split(" ")[0];
                additions.push([c, c + 5 + lang.length + id.length, lang, "cod", id]);
            }
        }//end for char in line

        let line = "";
        if(additions.length == 0){
            line = rawLine;
        } else {
            let added = 0;
            line = rawLine;
            for(let a = 0; a < additions.length; a++) {
                let addition = additions[a];
                if(addition[3] == "img"){
                    let s = addition[0];
                    let e = addition[1];
                    let url = addition[2];
                    line = line.slice(0, s + added) + '<img src="' + url + '" style="width:300px;height:auto;">' + line.slice(e + added);
                    added = added + 41;
                } else if(addition[3] == "cod") {
                    let s = addition[0];
                    let e = addition[1];
                    let lang = addition[2];
                    let id = addition[4];
                    line = line.slice(0, s + added) + '<div id="' + id + '" class="code"></div>' + line.slice(e + added);
                    added = added + 30 + id.length;
                    codeEditorQueue.push([id, lang]);
                }
            }  
        }

        //bullets
        let count = 0;
        //search for *
        for(let c = 0; c < line.length; c ++) {
            let character = line.slice(c, c + 1);
            if(character == "*") {
                count += 1;
            } else {
                break;
            }
        }
        //add to list
        stars_by_line.push(count);
        //update output
        output.innerHTML = output.innerHTML + line + "<br>";

    }//end for line

    //render code editors
    codeEditors = [];
    for(let e = 0; e < codeEditorQueue.length; e++) {
        let editor = codeEditorQueue[e];
        let lang = editor[1];
        let id = editor[0];
        var aceEdit = ace.edit(id);
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

    let prev_count = 0;
    let bullet_active = false;
    let oldHTML = output.innerHTML;
    let html = ""
    let line = oldHTML.split("\n");
    for(let i = 0; i < stars_by_line.length; i++) {
        let line = lines[i];
        let count = stars_by_line[i];
        if(count == 0 && bullet_active) {
            bullet_active = false;
            for(let e = 0; e < prev_count; e++) {
                html = html + "</ul>";
            }
            html = html + line.slice(count);
        } else if(count == 0 && !bullet_active) {
            html = html + line.slice(count) + "<br>";
        } else if(count > prev_count) {
            bullet_active = true;
            html = html + "<ul><li>" + line.slice(count) + "</li>";
        } else if(count == prev_count && count != 0) {
            html = html + "<li>" + line.slice(count) + "</li>";
        } else if(count < prev_count) {
            html = html + "</ul><li>" + line.slice(count) + "</li>";
        }
        prev_count = count;
    }
    output.innerHTML = html;
}//end scanDoc

function saveCode() {
    for(let e = 0; e < codeEditors.length; e++) {
        let data = codeEditors[e];
        let editor = data[0];
        let id = data[1];
        codeContents[id] = editor.getValue();
    }
}//end saveCode 


function render(text) {
    saveCode();
    scanDoc(text);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}//end render