let urlValue = null;
// Валидация введенного
$('#submit_url').prop('disabled', true);
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (error) {
        return false;
    }
}
function validateForm() {
    urlValue = $('#url_yandex').val().trim();

    if (isValidUrl(urlValue)) {
        $('#url_yandex').removeClass('is-invalid');
        $('#submit_url').prop('disabled', false);
    } else {
        $('#url_yandex').addClass('is-invalid');
        $('#submit_url').prop('disabled', true);
    }
}
$('#url_yandex').on('input', validateForm);

$('#urlForm').on('submit', function (event) {
    if (!isValidUrl($('#url_yandex').val().trim())) {
        event.preventDefault();
        event.stopPropagation();
    }
});


// Отправка запроса на сервер
function SendData() {
    console.log("url_yandex: ", $('#url_yandex').val().trim())
    let data = new FormData();
    data.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').attr('value'));
    data.append('url_yandex', $('#url_yandex').val().trim());

    fetch('', {
        method: 'POST',
        body: data
    })
        .then(res => res.json())
        .then(res => {
            if (res.status === 'success') {
                const url = res.url;
                window.location.href = url;
            } else {
                console.log(2)
                Toastify({
                    text: res.error,
                    duration: 3000,
                    backgroundColor: "#ff6b6b"
                }).showToast();
            }

        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });

}


// При нажатии на кнопку тоже проверка
$(document).keypress((e) => {
    if (e.charCode === 13) {
        SendData()
    }
})

$('#submit_url').click(() => {
    SendData()
})


