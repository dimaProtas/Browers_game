$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    // Обработчик для кнопки "Добавить в друзья" и "Отменить запрос"
    $(document).on("click", ".request, .cancel", function() {
        var userId = $(this).data("user-id");
        var isRequest = $(this).hasClass("request"); // Проверяем класс кнопки

        // Отправляем Ajax-запрос на сервер
        $.ajax({
            url: isRequest ? "http://127.0.0.1:8888/request_friends/" + userId + "/" : "http://127.0.0.1:8888/delete_request_friends/" + userId + "/",
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