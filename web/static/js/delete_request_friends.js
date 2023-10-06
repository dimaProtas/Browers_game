$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    var hostPort = $('meta[name="host-port"]').attr('content');

    // Обработчик для кнопки "Добавить в друзья" и "Отменить запрос"
    $(document).on("click", ".request, .cancel", function() {
        var userId = $(this).data("user-id");
        var isRequest = $(this).hasClass("request"); // Проверяем класс кнопки
        const URL_VAR = "http://localhost:8888/request_friends/"

        // Отправляем Ajax-запрос на сервер
        $.ajax({
            url: isRequest ? hostPort + "request_friends/" + userId + "/" : hostPort + "delete_request_friends/" + userId + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },

            success: function(data) {
                if (data.result === 'Success') {
                    // Находим элемент кнопки с помощью data-user-id
                    var buttonElement = $('.clik_button[data-user-id="' + userId + '"]');

                    // Обновляем текст кнопки и классы
                    if (isRequest) {
                        buttonElement.text('Отменить заявку').addClass('cancel').removeClass('request');
                        buttonElement.removeClass("request").addClass("cancel");
                    } else {
                        buttonElement.text('Добавить в друзья').addClass('request').removeClass('cancel');
                        buttonElement.removeClass("cancel").addClass("request");
                    }
                }
            },
            error: function() {
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
    });
});