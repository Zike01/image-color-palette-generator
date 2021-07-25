function copyColor() {
    const div = document.getElementById('color');

    let bgColor = window.getComputedStyle(div).backgroundColor;
    let text = document.createElement('textarea');
    text.style.display = 'none';
    document.body.appendChild(text);

    text.value = bgColor;

    text.select();

    document.execCommand('copy');

    document.body.removeChild(text);
}