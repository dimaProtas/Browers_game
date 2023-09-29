$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    // Обработчик для кнопки "Принять" и "Отменить"
    $(document).on("click", ".delete", function() {
        var userId = $(this).data("user-id");
        var friendElement = $(`[data-toggle="friend-${userId}"]`);
        var friendsCountElement = $(`[class="count_friends"]`);
        var friendsCount = parseInt(friendsCountElement.data('friends-count'), 10);

        // Отправляем Ajax-запрос на сервер
        $.ajax({
            url: "http://127.0.0.1:8888/done_cancel_friend/" + userId + "/" + "cancel" + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                if (data.result === 'delete') {
                    friendElement.hide();

                    friendsCountElement.data('request-count', friendsCount - 1); // Обновляем атрибут
                    friendsCountElement.text(friendsCount - 1); // Обновляем текст элемента

                }
            },
            error: function() {
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
    });
});