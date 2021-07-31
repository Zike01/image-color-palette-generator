function copyColor(index_inner, index_outer) {
    // Get the div element and it's background color
    const div = document.getElementById("color" + index_inner);
    let bgColor = window.getComputedStyle(div).backgroundColor;

    // Create a textarea element
    const text  = document.createElement('textarea');
    document.body.appendChild(text);

    // Set the textarea value to the div background color
    text.value = bgColor;

    // Select text
    text.select();
    text.setSelectionRange(0, 99999);
    
    document.execCommand('copy');
    document.body.removeChild(text);

    var copied = document.getElementById("copied" + index_outer)
    copied.innerHTML = "Copied " + bgColor + "!";
    copied.style.color = "green";

    window.setTimeout(function() {
        copied.innerHTML = "";
    }, 5000);
}
