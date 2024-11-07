let pageState = 'overview'

window.onpopstate = function (event) {
    if (event.state !== null)
    {
        pageState = event.state;
        changeContent(pageState, false);
    }
}

function initialize()
{
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.setAttribute('data-bs-theme', 'dark');
    }
    else {
        document.body.setAttribute('data-bs-theme', 'light');
    }
    
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (e.matches) {
            document.body.setAttribute('data-bs-theme', 'dark');
        }
        else {
            document.body.setAttribute('data-bs-theme', 'light');
        }
    });

    history.replaceState(pageState, null, "");
    changeContent(pageState, false);
}

function changeContent(page, pushState = true)
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
        if (pushState && history.state !== pageState) {
            history.pushState(pageState, null, "");
        }
    }
    xhr.send();
}

initialize();