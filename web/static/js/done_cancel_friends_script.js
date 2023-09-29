$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    // Обработчик для кнопки "Принять" и "Отменить"
    $(document).on("click", ".done, .cancel", function() {
        var userId = $(this).data("user-id");
        var status = $(this).data("friend-status");
        //var isRequest = $(this).hasClass("request"); // Проверяем класс кнопки
        var friendElement = $(`[data-toggle="friend-${userId}"]`);
        var requestCountElement = $(`[class="count_request"]`);
        var requestCount = parseInt(requestCountElement.data('request-count'), 10);
        var friendsCountElement = $(`[class="count_friends"]`);
        var friendsCount = parseInt(friendsCountElement.data('friends-count'), 10);

        // Отправляем Ajax-запрос на сервер
        $.ajax({
            url: "http://127.0.0.1:8888/done_cancel_friend/" + userId + "/" + status + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                if (data.result === 'done') {
                    friendElement.prependTo($(".add_friends_container"));
                    //friendElement.hide();

                    // Находим кнопки "Принять" и "Отклонить" внутри friendElement
                    var acceptButton = friendElement.find('.done');
                    var rejectButton = friendElement.find('.cancel');

                    // Обновляем текст кнопок
                    acceptButton.text('Сообщение').addClass('message');
                    rejectButton.text('Удалить из друзей').addClass('delete');

                    requestCountElement.data('request-count', requestCount - 1); // Обновляем атрибут
                    requestCountElement.text(requestCount - 1); // Обновляем текст элемента

                    friendsCountElement.data('request-count', friendsCount + 1); // Обновляем атрибут
                    friendsCountElement.text(friendsCount + 1); // Обновляем текст элемента

                } else if (data.result === 'delete') {
                    friendElement.hide();

                    requestCountElement.data('request-count', requestCount - 1); // Обновляем атрибут data-commen-count
                    requestCountElement.text(requestCount - 1); // Обновляем текст элемента
                }
            },
            error: function() {
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
    });
});