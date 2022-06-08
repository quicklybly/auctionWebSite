function visits() {
    if (sessionStorage.getItem('session') == null || getCookie('visits') === undefined) {
        setVisits();
        sessionStorage.setItem('session', 'yes');
    }
}



function setVisits() {
    if (getCookie('visits') !== undefined) {
        setCookie('visits', parseInt(getCookie('visits')) + 1, 100);
    } else {
        setCookie('visits', 1, 100);
    }
}

function printVisits() {
    if (getCookie('visits') === '1') {
        document.write('Поздравляем вас с первым посещением нашего сайта');
    } else {
        document.write('Вы посещали наш сайт ' + getCookie('visits') + ' раз(a)');
    }

}

function setCookie(cname, cvalue, exdays) {
    let d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}