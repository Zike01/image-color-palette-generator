function copyColor(color) {
    const div = document.getElementById(color);

    let bgColor = window.getComputedStyle(div).backgroundColor;
    const text  = document.createElement('textarea');
    document.body.appendChild(text);

    text.value = bgColor;
    text.select();
    text.setSelectionRange(0, 99999);
    

    document.execCommand('copy');
    document.body.removeChild(text);
}