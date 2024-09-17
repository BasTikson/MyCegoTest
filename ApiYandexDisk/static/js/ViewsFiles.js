// Список выбранных файлов
var selected_files = [];

$(document).ready(function () {
    function Update() {
        let data = new FormData();
        data.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').attr('value'));
        data.append('action', 'update');
        var Url = window.location.href;

        fetch(Url, {
            method: 'POST',
            body: data
        })
            .then(res => res.json())
            .then(res => {
                if (res.status === 'success') {
                    console.log("Обновление страницы, запуск скрипта на отрисовку штуки с файлами");
                    const files = res.files;
                    files.forEach(function (file) {
                        insertFileItem(file.name, file.path);
                    });
                    StartAction();
                } else {
                    console.log("Произошла ошибка при попытке получить ответ на запрос к серверу");
                }
            })
            .catch(error => {
                console.error('Ошибка при обновлении страницы "/viewsFiles" :', error);
            });
    }

    function insertFileItem(fileName, filePath) {
        var fileItemHtml = `
        <div class="file-item universal_template_file">
            <div class="file-item-select-bg bg-primary"></div>
            <label class="file-item-checkbox custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input"/>
                <span class="custom-control-label"></span>
            </label>
            <div class="file-item-icon far fa-file text-secondary"></div>
            <div class="filePath" hidden>${filePath}</div>
            <a class="file-item-name">${fileName}</a>
        </div>
    `;

        // Вставляем HTML-блок и скрытый div в нужный контейнер
        var container = $('.file-manager-container'); // Замените на селектор вашего контейнера
        container.append(fileItemHtml);
    }

    // Составление списка файлов для скачивания
    function handleCheckboxChange() {
        $('.custom-control-input').change(function () {
            var checkbox = $(this);
            var filePathDiv = checkbox.closest('.universal_template_file').find('.filePath');
            var filePath = filePathDiv.text();

            if (checkbox.is(':checked')) {
                // Если чекбокс выбран, добавляем путь в список selected_files
                if (!selected_files.includes(filePath)) {
                    selected_files.push(filePath);
                }
            } else {
                // Если чекбокс снят, удаляем путь из списка selected_files
                var index = selected_files.indexOf(filePath);
                if (index !== -1) {
                    selected_files.splice(index, 1);
                }
            }

            // Выводим текущий список выбранных файлов (для отладки)
            console.log('Selected Files:', selected_files);
        });
    }

    // Скачивание файлов
    function DownloadFiles() {
        // Блокируем кнопку и показываем кружочек с загрузкой
        const downloadButton = document.getElementById('downloadFilesButton');
        const backButton = document.getElementById('backButton');
        const spinner = document.getElementById('downloadFilesSpinner');
        downloadButton.disabled = true;
        backButton.disabled = true;
        spinner.style.display = 'inline-block';

        let data = new FormData();
        data.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').attr('value'));
        data.append('action', 'downloadFiles');
        data.append('listFiles', JSON.stringify(selected_files)); // Преобразуем массив в строку JSON

        var Url = window.location.href;

        fetch(Url, {
            method: 'POST',
            body: data
        })
            .then(res => {
                // Проверяем, что ответ успешный
                if (res.ok) {
                    // Возвращаем Blob объект
                    return res.blob();
                } else {
                    // Если ответ не успешный, выбрасываем ошибку
                    throw new Error('Ошибка при загрузке файла');
                }
            })
            .then(blob => {
                // Создаем ссылку для скачивания файла
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'downloaded_file.zip'; // Укажите имя файла по умолчанию
                document.body.appendChild(a);
                a.click();
                a.remove(); // Удаляем ссылку после скачивания
                window.URL.revokeObjectURL(url); // Освобождаем URL объект
            })
            .catch(error => {
                console.error('Ошибка при загрузке файла:', error);
            })
            .finally(() => {
                // Разблокируем кнопку и скрываем кружочек с загрузкой
                downloadButton.disabled = false;
                backButton.disabled = false;
                spinner.style.display = 'none';

                // Очистка массива выбранных файлов
                $('.custom-control-input').prop('checked', false);
                selected_files = [];

            });
    }

    function StartAction() {
        handleCheckboxChange();
        // Вешаем действие на кнопку
        $('#downloadFilesButton').click(DownloadFiles);
    }

    // Функция фильтр файлов

    Update();
});