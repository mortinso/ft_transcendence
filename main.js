let pageState = 'overview'

window.onpopstate = function (event) {
    if (event.state)
    {
        pageState = event.state;
        changeContent(pageState);
    }
}

function initialize()
{
    window.history.replaceState(pageState, null, "");
}

function changeContent(page)
{
    var contentDiv = document.getElementById('content');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', `${page}.html`, true);
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4)
            return;
        if (this.status !== 200)
        {
            contentDiv.innerHTML = `<h2>Content not found!</h2>`
            return;
        }
        contentDiv.innerHTML = this.responseText;
        pageState = page;
        window.history.pushState(pageState, null, "");
    }
    xhr.send();
}