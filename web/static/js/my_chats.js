$(document).ready(function() {

     var csrfToken = $('meta[name="csrf-token"]').attr('content');

        // Обработчик для кнопки "Добавить в друзья" и "Отменить запрос"
    $(document).on("click", "#chat_button", function() {
        var userId = $(this).data("user-id");
        var isRequest = $(this).hasClass("request"); // Проверяем класс кнопки
        const chatURL = "http://127.0.0.1:8888/mess/chat/create_chat/"
        // Отправляем Ajax-запрос на сервер
        $.ajax({
            url: chatURL,
            type: "POST",
            cache: false,
            data: {
                csrfmiddlewaretoken: csrfToken,
                companion: userId,
            },



            success: function(data) {
                if (data.result === 'Success') {
                    // Находим элемент кнопки с помощью data-user-id
                    var buttonElement = $('.clik_button[data-user-id="' + userId + '"]');

                    // Обновляем текст кнопки и классы
                    if (isRequest) {
                        buttonElement.text('Чат создан').addClass('cancel').removeClass('request');
                        buttonElement.removeClass("request").addClass("cancel");
                    } else {
                        console.log('чат уже создан, проверки нет');
                    }
                }
            },
            error: function() {
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}